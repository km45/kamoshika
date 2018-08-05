# -*- coding: utf-8 -*-
"""Provide functions for pre_query, query and post_query"""

import logging
import os
import subprocess
import typing
import xml.dom.minidom

import requests

import kamoshika.postquery


def format_xml(input_file_path: str, input_file_encoding: str, logger: logging.Logger) -> str:
    """Format xml

    Args:
        input_file_path: input xml file path to format
        input_file_encoding: encoding of input xml file
        logger: logger instance

    Returns:
        formatted xml
    """
    with open(input_file_path, encoding=input_file_encoding) as input_file:
        read_file = input_file.read()
        logger.debug('read file ({}):\n{}\n'.format(
            input_file_path, read_file))
        return xml.dom.minidom.parseString(read_file).toprettyxml()


def fetch_responce(
        server: str, request_parameter: str,
        request_headers: dict, logger: logging.Logger) -> requests.Response:
    """Send a request and receive a responce

    Args:
        server: server path
        request_parameter: request parameter
        request_headers: dictionary of request headers
        logger: logger instance

    Returns
        received responce
    """
    with requests.Session() as session:
        prepared = requests.Request(
            'GET',
            server,
            params=request_parameter,
            headers=request_headers).prepare()
        logger.info('prepared request:\n'
                    'parameter:\n'
                    '{}\n'
                    'headers:\n'
                    '{}\n'.format(prepared.url, prepared.headers))
        responce = session.send(prepared)
        logger.info('received responce:\n'
                    'status code:\n'
                    '{}\n'
                    'headers:\n'
                    '{}\n'.format(responce.status_code, responce.headers))
        return responce


def guess_encoding(file_path: str, logger: logging.Logger) -> str:
    """Guess file encoding

    Args:
        file_path: file path to guess encoding
        logger: logger instance

    Returns:
        guessed encoding
    """
    command = ['nkf', '--guess=1', file_path]
    logger.debug('execute following command:\n{}'.format(command))
    external_process = subprocess.run(command, stdout=subprocess.PIPE)
    file_encoding = external_process.stdout.decode().rstrip('\n')
    logger.debug('guessed encoding of file {}: {}'.format(
        file_path, file_encoding))
    return file_encoding


def invoke_diff_viewer(post_processed_paths: typing.List[str], logger: logging.Logger) -> None:
    """Invoke diff viewer

    Args:
        post_processed_paths: post processed paths, files or directories
        logger: logger instance
    """
    command = ['meld'] + post_processed_paths
    logger.debug('execute following command:\n{}'.format(command))
    subprocess.run(command)


ContentType = typing.TypeVar(  # pylint: disable=invalid-name
    'ContentType', str, bytes)


def save_content_as_file(
        output_file_path: str, explanation: str,
        content: ContentType, logger: logging.Logger) -> None:
    """Save content as file

    Args:
        output_file_path: output file path
        explanation: explanation for output file, used for only logging
        content: binary or text to save as file
        logger: logger instance
    """
    if isinstance(content, bytes):
        file_mode = 'wb'
    if isinstance(content, str):
        file_mode = 'wt'
    with open(output_file_path, file_mode) as out:
        logger.info('save {} as {}'.format(explanation, output_file_path))
        out.write(content)
        logger.info('success to save {}'.format(output_file_path))


class XmlStrategy:
    """Strategy for xml"""

    def __init__(
            self,
            output_directory: str,
            server_config: typing.List[str],
            request: dict,
            logger: logging.Logger) -> None:
        """
        Args:
            output_directory: directory where save files
            server_config: server field of config
            request: request to post
            logger: logger instance
        """
        self._output_directory = output_directory
        self._server_config = server_config
        self._request = request
        self._logger = logger
        self._responces = []  # type: typing.List[requests.Response]
        self._saved_file_paths = []  # type: typing.List[str]
        self._post_processed_paths = []  # type: typing.List[str]
        self._post_query_stream: kamoshika.postquery.PostQueryStream = []

    def query(self) -> None:
        """Send a request and receive a responce for each server"""
        for index, server in enumerate(self._server_config):
            number = index + 1
            self._logger.info(
                'start query {}/{}'.format(number, len(self._server_config)))
            self._responces.append(fetch_responce(
                server, self._request['parameter'], self._request.get('header'), self._logger))
            self._logger.info(
                'end query {}/{}'.format(number, len(self._server_config)))

    def post_query(self) -> None:
        """Save responce, format xml, and invoke diff viewer"""
        self.__save_responces()
        self.__post_process()
        invoke_diff_viewer(self._post_processed_paths, self._logger)

    def __save_responces(self) -> None:
        """Save responces as files"""
        self._logger.info(
            'create output directory: {}'.format(self._output_directory))
        os.makedirs(self._output_directory)

        for index, responce in enumerate(self._responces):
            number = index + 1
            file_name = '{}.xml'.format(number)
            file_path = os.path.join(self._output_directory, file_name)
            save_content_as_file(
                file_path,
                'responce body for query {}'.format(number),
                responce.content,
                self._logger)
            self._saved_file_paths.append(file_path)

    def __post_process_to_single_file(
            self, saved_file_path: str, number: int)-> str:
        """Do post process to single file

        Args:
            saved_file_path: saved file path to process
            number: target file number

        Returns:
            processed file path
        """
        saved_file_encoding = guess_encoding(saved_file_path, self._logger)
        formatted_xml = format_xml(
            saved_file_path, saved_file_encoding, self._logger)

        # save file
        processed_file_name = '{}f.xml'.format(number)
        processed_file_path = os.path.join(
            self._output_directory, processed_file_name)
        save_content_as_file(
            processed_file_path, 'formated xml', formatted_xml, self._logger)
        self._post_query_stream.append(
            {'responce.xml': formatted_xml.encode('utf8')})
        return processed_file_path

    def __post_process(self) -> None:
        """Do post process for each files"""
        for index, path in enumerate(self._saved_file_paths):
            number = index + 1
            self._logger.info(
                'start post process {}/{}'.format(number, len(self._saved_file_paths)))
            self._post_processed_paths.append(
                self.__post_process_to_single_file(path, number))
            self._logger.info(
                'end post process {}/{}'.format(number, len(self._saved_file_paths)))

    def get_post_query_stream(self) -> kamoshika.postquery.PostQueryStream:
        return self._post_query_stream

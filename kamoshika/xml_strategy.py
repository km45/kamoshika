# -*- coding: utf-8 -*-
"""Provide functions for pre_query, query and post_query"""

import logging
import os
import subprocess
import typing
import xml.dom.minidom

import requests

import kamoshika.postquery.stream


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
        self._post_query_stream: kamoshika.postquery.stream.PostQueryStream = []

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

    def __post_process_to_single_file(self, saved_file_path: str) -> None:
        """Do post process to single file

        Args:
            saved_file_path: saved file path to process
        """
        with open(saved_file_path, 'br') as file:
            content = file.read()

        self._post_query_stream.append({'responce.xml': content})

    def __post_process(self) -> None:
        """Do post process for each files"""
        for index, path in enumerate(self._saved_file_paths):
            number = index + 1
            self._logger.info(
                'start post process {}/{}'.format(number, len(self._saved_file_paths)))
            self.__post_process_to_single_file(path)
            self._logger.info(
                'end post process {}/{}'.format(number, len(self._saved_file_paths)))

    def get_post_query_stream(self) -> kamoshika.postquery.stream.PostQueryStream:
        return self._post_query_stream

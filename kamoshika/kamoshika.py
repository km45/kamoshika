#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Usage:
  kamoshika.py [-c <FILE>] [-o <DIRECTORY>] [--log-level <LEVEL>] <KEY>
  kamoshika.py -h | --help

Options:
  -h --help             show this
  -c --config <FILE>    specify config file [default: kamoshika.yml]
  -o --out <DIRECTORY>  specify output directory [default: out]
  --log-level <LEVEL>   specify log level [default: info]
                        valid values:
                          - fatal
                          - error
                          - warn
                          - info
                          - debug
"""

import logging
import os
import typing

import docopt
import requests

import config
import log
import strategy


def parse_options() -> dict:
    """Parse command line options

    Returns:
        result dictionary
    """
    parameters = docopt.docopt(__doc__)
    return parameters


def query(server_config: typing.List[str],
          request: dict,
          logger: logging.Logger) -> typing.List[requests.Response]:
    """Send a request and receive a responce for each server

    Args:
        server_config: server field of config
        request: request to post
        logger: logger instance

    Returns:
        list of received reponces
    """

    responces = []  # type: typing.List[requests.Response]
    for index, server in enumerate(server_config):
        number = index + 1
        logger.info('start query {}/{}'.format(number, len(server_config)))
        responces.append(strategy.fetch_responce(
            server, request['parameter'], request.get('header'), logger))
        logger.info('end query {}/{}'.format(number, len(server_config)))
    return responces


def save_responces(responces: typing.List[requests.Response],
                   responce_conf: dict,
                   out_directory: str,
                   logger: logging.Logger) -> typing.List[str]:
    """Save responces as files

    Args:
        responces: list of responce instance
        responce_conf: responce field of config
        out_directory: directory where save files
        logger: logger instance

    Returns:
        saved file paths
    """
    logger.info('create output directory: {}'.format(out_directory))
    os.makedirs(out_directory)

    file_name_prefix = responce_conf['file_name_prefix']
    file_name_postfix = responce_conf['file_name_postfix']

    saved_files = []  # type: typing.List[str]
    for index, responce in enumerate(responces):
        number = index + 1
        file_name = '{}{}{}'.format(
            file_name_prefix, number, file_name_postfix)
        file_path = os.path.join(out_directory, file_name)
        strategy.save_content_as_file(
            file_path, 'responce body for query {}'.format(number), responce.content, logger)
        saved_files.append(file_path)
    return saved_files


def post_process_to_single_file(saved_file_path: str,
                                responce_conf: dict,
                                out_directory: str,
                                number: int,
                                logger: logging.Logger)-> str:
    """Do post process to single file

    Args:
        saved_file_path: saved file path to process
        responce_conf: responce field of config
        out_directory: directory where save files
        number: target file number
        logger: logger instance

    Returns:
        processed file path
    """
    # TODO: Implement post processes like followings:
    #   - uncompress archive
    #   - format text such as html and json
    #   - convert binary to text
    mode = responce_conf['post_process']
    logger.debug('post process mode: {}'.format(mode))

    file_name_prefix = responce_conf['file_name_prefix']
    file_name_postfix = responce_conf['file_name_postfix']

    if mode == 'disabled':
        # nothing to do
        return saved_file_path
    elif mode == 'xml':
        saved_file_encoding = strategy.guess_encoding(saved_file_path, logger)
        formatted_xml = strategy.format_xml(
            saved_file_path, saved_file_encoding, logger)

        # save file
        processed_file_name = '{}{}f{}'.format(
            file_name_prefix, number, file_name_postfix)
        processed_file_path = os.path.join(out_directory, processed_file_name)
        strategy.save_content_as_file(
            processed_file_path, 'formated xml', formatted_xml, logger)
        return processed_file_path
    else:
        # nothing to do
        return saved_file_path


def post_process(saved_file_paths: typing.List[str],
                 responce_conf: dict,
                 out_directory: str,
                 logger: logging.Logger) -> typing.List[str]:
    """Do post process for each files

    Args:
        saved_file_paths: saved file paths to process
        responce_conf: responce field of config
        out_directory: directory where save files
        logger: logger instance

    Returns:
        processed file paths
    """
    post_processed_paths = []  # type: typing.List[str]
    for index, path in enumerate(saved_file_paths):
        number = index + 1
        logger.info(
            'start post process {}/{}'.format(number, len(saved_file_paths)))
        post_processed_paths.append(
            post_process_to_single_file(path, responce_conf, out_directory, number, logger))
        logger.info(
            'end post process {}/{}'.format(number, len(saved_file_paths)))
    return post_processed_paths


def main():
    """main function
    """
    parameters = parse_options()

    logger = log.create_logger(parameters['--log-level'])

    logger.debug('parsed options:\n{}'.format(parameters))

    conf = config.Config(parameters['--config'], logger)

    request = conf.get_request(parameters['<KEY>'], logger)

    responces = query(conf.get_server_list(), request, logger)

    strategy.clear_output_directory(parameters['--out'], logger)

    saved_file_paths = save_responces(
        responces, conf.get_responce(), parameters['--out'], logger)

    post_processed_paths = post_process(
        saved_file_paths, conf.get_responce(), parameters['--out'], logger)

    strategy.invoke_diff_viewer(post_processed_paths, logger)


if __name__ == '__main__':
    main()

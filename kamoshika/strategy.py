# -*- coding: utf-8 -*-
"""Provide functions for pre_query, query and post_query
"""

import logging
import os
import shutil
import subprocess
import typing
import xml.dom.minidom


def clear_output_directory(directory: str, logger: logging.Logger) -> None:
    """Clear output directory

    Args:
        directory: directory to remove recursively
        logger: logger instance
    """
    logger.debug(
        'remove directory "{}" recursively if exists'.format(directory))

    if os.path.exists(directory):
        logger.debug('directory "{}" exists'.format(directory))
        logger.warn('remove directory "{}" recursively'.format(directory))
        shutil.rmtree(directory)


def format_xml(input_file_path: str, input_file_encoding: str, logger: logging.Logger) -> str:
    """format xml

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


def guess_encoding(file_path: str, logger: logging.Logger) -> str:
    """guess file encoding

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
    """invoke diff viewer

    Args:
        post_processed_paths: post processed paths, files or directories
        logger: logger instance
    """
    command = ['meld'] + post_processed_paths
    logger.debug('execute following command:\n{}'.format(command))
    subprocess.run(command)

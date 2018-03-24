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


ContentType = typing.TypeVar(  # pylint: disable=invalid-name
    'ContentType', str, bytes)


def save_content_as_file(
        output_file_path: str, explanation: str,
        content: ContentType, logger: logging.Logger) -> None:
    """save content as file

    Args:
        output_file_path: output file path
        explanation: explanation for output file, used for only logging
        content: binary or text to save as file
        logger: logger instance
    """
    if isinstance(content, bytes):
        file_mode = 'b'
    if isinstance(content, str):
        file_mode = 't'
    with open(output_file_path, 'w{}'.format(file_mode)) as out:
        logger.info('save {} as {}'.format(explanation, output_file_path))
        out.write(content)
        logger.info('success to save {}'.format(output_file_path))


def save_binary_as_file(
        output_file_path: str, explanation: str,
        content: bytes, logger: logging.Logger) -> None:
    """save binary as file

    Args:
        output_file_path: output file path
        explanation: explanation for output file, used for only logging
        content: binary to save as file
        logger: logger instance
    """
    save_content_as_file(output_file_path, explanation, content, logger)


def save_text_as_file(
        output_file_path: str, explanation: str,
        content: str, logger: logging.Logger) -> None:
    """save text as file

    Args:
        output_file_path: output file path
        explanation: explanation for output file, used for only logging
        content: string to save as file
        logger: logger instance
    """
    save_content_as_file(output_file_path, explanation, content, logger)

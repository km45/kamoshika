# -*- coding: utf-8 -*-
"""Provide functions for pre_query, query and post_query
"""

import logging
import os
import shutil
import subprocess
import typing


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


def guess_encoding(file_path: str, logger: logging.Logger) -> str:
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

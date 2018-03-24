# -*- coding: utf-8 -*-

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


def invoke_diff_viewer(post_processed_paths: typing.List[str], logger: logging.Logger) -> None:
    """invoke diff viewer

    Args:
        post_processed_paths: post processed paths, files or directories
        logger: logger instance
    """
    command = ['meld'] + post_processed_paths
    logger.debug('execute following command:\n{}'.format(command))
    subprocess.run(command)

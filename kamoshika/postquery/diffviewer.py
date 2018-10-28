# -*- coding: utf-8 -*-
import logging
import os
import subprocess
import typing

import kamoshika.postquery.stream


def invoke_meld(
        paths: typing.List[str],
        logger: logging.Logger) -> None:
    """Invoke meld as diff viewer

    Args:
        paths: files or directories
        logger: logger instance
    """
    command = ['meld'] + paths
    logger.debug('execute following command:\n{}'.format(command))
    subprocess.run(command)


def invoke_vscode(
        paths: typing.List[str],
        logger: logging.Logger) -> None:
    """Invoke vscode as diff viewer

    Args:
        paths: files or directories
        logger: logger instance
    """
    command = ['code', '--diff'] + paths
    logger.debug('execute following command:\n{}'.format(command))
    subprocess.run(command)


def execute(output_directory: str,
            stream: kamoshika.postquery.stream.PostQueryStream,
            config: dict,
            logger: logging.Logger) -> None:
    logger.debug('config: {}'.format(config))

    targets = [
        os.path.join(
            output_directory,
            config['dumped-dir'],
            '{}'.format(index),
            config['target-path']
        ) for index in range(len(stream))
    ]

    if config['viewer'] == 'vscode':
        invoke_vscode(targets, logger)
    else:
        invoke_meld(targets, logger)

# -*- coding: utf-8 -*-
import logging
import os
import subprocess
import typing

import kamoshika.postquery.stream


def invoke_diff_viewer(
        paths: typing.List[str],
        logger: logging.Logger) -> None:
    """Invoke diff viewer

    Args:
        paths: files or directories
        logger: logger instance
    """
    command = ['meld'] + paths
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

    invoke_diff_viewer(targets, logger)

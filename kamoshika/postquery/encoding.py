# -*- coding: utf-8 -*-
import logging
import subprocess

import kamoshika.postquery.stream


def change_encoding(
        input_bytes: bytes,
        input_encoding: str,
        output_encoding: str) -> bytes:
    return input_bytes.decode(input_encoding).encode(output_encoding)


def guess_encoding(target: bytes, logger: logging.Logger) -> str:
    """Guess encoding

    Args:
        target: bytes to guess encoding
        logger: logger instance

    Returns:
        guessed encoding
    """
    command = ['nkf', '--guess=1']
    logger.debug('execute following command:\n{}'.format(command))
    external_process = subprocess.run(
        command, input=target, stdout=subprocess.PIPE)
    result = external_process.stdout.decode().rstrip('\n')
    logger.debug('guessed encoding: {}'.format(result))

    return result


def execute(_: str,
            stream: kamoshika.postquery.stream.PostQueryStream,
            config: dict,
            logger: logging.Logger) -> None:
    logger.debug('config: {}'.format(config))

    guess_from: bool = config['guess-from']
    path: str = config['target-path']
    to_encoding: str = config['to']

    for single_host in stream:
        from_encoding: str = guess_encoding(
            single_host[path], logger) if guess_from else config['from']
        logger.debug(
            'change encoding: {} -> {}'.format(from_encoding, to_encoding))

        result = change_encoding(single_host[path], from_encoding, to_encoding)
        single_host[path] = result

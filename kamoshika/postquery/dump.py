# -*- coding: utf-8 -*-
import logging
import os.path
import typing

import kamoshika.postquery.stream


def dump_files(src: typing.Dict[str, bytes], dst: str) -> None:
    for src_key, from_bytes in src.items():
        to_filename = os.path.join(dst, src_key)
        to_dirname = os.path.dirname(to_filename)
        if not os.path.exists(to_dirname):
            os.makedirs(to_dirname)
        with open(to_filename, 'wb') as to_file:
            to_file.write(from_bytes)


def execute(output_directory: str,
            stream: kamoshika.postquery.stream.PostQueryStream,
            config: dict,
            logger: logging.Logger) -> None:
    logger.debug('config: {}'.format(config))
    for index, single_host in enumerate(stream):
        dump_files(
            single_host,
            os.path.join(output_directory, config['dst'], '{}'.format(index)))

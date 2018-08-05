# -*- coding: utf-8 -*-
import os.path
import typing


def dump_files(src: typing.Dict[str, bytes], dst: str) -> None:
    for src_key, from_bytes in src.items():
        to_filename = os.path.join(dst, src_key)
        to_dirname = os.path.dirname(to_filename)
        if not os.path.exists(to_dirname):
            os.makedirs(to_dirname)
        with open(to_filename, 'wb') as to_file:
            to_file.write(from_bytes)

# -*- coding: utf-8 -*-
import os.path


def dump_files(src: dict, dst: str)->None:
    for key, value in src.items():
        filename = os.path.join(dst, key)
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(filename, "wb") as out:
            out.write(value)

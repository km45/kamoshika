# -*- coding: utf-8 -*-

import logging

from kamoshika.postquery.encoding import change_encoding, guess_encoding

test_data: str = '''<?xml version="1.0" encoding="UTF-8"?>
<items>
    <item no="1">kamoshika</item>
    <item no="2">かもしか</item>
    <item no="3">カモシカ</item>
    <item no="4">氈鹿</item>
</items>'''


def null_logger() -> logging.Logger:
    handler = logging.NullHandler
    logger = logging.getLogger(__name__)
    logger.addHandler(handler)
    return logger


def test_change_encoding():
    eucjp: bytes = test_data.encode('eucjp')
    sjis: bytes = test_data.encode('sjis')
    utf8: bytes = test_data.encode('utf8')

    assert change_encoding(eucjp, 'eucjp', 'eucjp') == eucjp
    assert change_encoding(eucjp, 'eucjp', 'sjis') == sjis
    assert change_encoding(eucjp, 'eucjp', 'utf8') == utf8
    assert change_encoding(sjis, 'sjis', 'eucjp') == eucjp
    assert change_encoding(sjis, 'sjis', 'sjis') == sjis
    assert change_encoding(sjis, 'sjis', 'utf8') == utf8
    assert change_encoding(utf8, 'utf8', 'eucjp') == eucjp
    assert change_encoding(utf8, 'utf8', 'sjis') == sjis
    assert change_encoding(utf8, 'utf8', 'utf8') == utf8


def test_guess_encoding():
    eucjp: bytes = test_data.encode('eucjp')
    sjis: bytes = test_data.encode('sjis')
    utf8: bytes = test_data.encode('utf8')

    assert guess_encoding(eucjp, null_logger()) == 'EUC-JP'
    assert guess_encoding(sjis, null_logger()) == 'Shift_JIS'
    assert guess_encoding(utf8, null_logger()) == 'UTF-8'

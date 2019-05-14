# -*- coding: utf-8 -*-

import filecmp
import logging
import os.path

import kamoshika.postquery.dump


def null_logger() -> logging.Logger:
    handler = logging.NullHandler
    logger = logging.getLogger(__name__)
    logger.addHandler(handler)  # type: ignore
    return logger


def report(expected_dir: str, actual_dir: str) -> str:
    comparer = filecmp.dircmp(expected_dir, actual_dir)
    comparer.report_full_closure()
    return 'Something different. Report details to stdout.'


def compare(expected_dir: str, actual_dir: str) -> bool:
    comparer = filecmp.dircmp(expected_dir, actual_dir)

    if comparer.left_only != []:
        return False
    if comparer.right_only != []:
        return False
    if comparer.diff_files != []:
        return False

    for directory in comparer.common_dirs:
        if not compare(
                os.path.join(expected_dir, directory),
                os.path.join(actual_dir, directory)):
            return False

    return True


def test_dump_single_content(tmpdir):
    src = {
        'a.txt': 'aaa'.encode()
    }

    actual = tmpdir.mkdir('actual')
    kamoshika.postquery.dump.dump_files(src, actual, null_logger())

    expected = tmpdir.mkdir('expected')
    expected.join('a.txt').write('aaa'.encode())

    assert compare(expected, actual), report(expected, actual)


def test_dump_multiple_flat_contents(tmpdir):
    src = {
        'a.txt': 'aaa'.encode(),
        'b.txt': 'bbb'.encode(),
        'c.txt': 'ccc'.encode()
    }

    actual = tmpdir.mkdir('actual')
    kamoshika.postquery.dump.dump_files(src, actual, null_logger())

    expected = tmpdir.mkdir('expected')
    expected.join('a.txt').write('aaa'.encode())
    expected.join('b.txt').write('bbb'.encode())
    expected.join('c.txt').write('ccc'.encode())

    assert compare(expected, actual), report(expected, actual)


def test_dump_multiple_nested_contents(tmpdir):
    src = {

        'a.txt': 'aaa'.encode(),
        os.path.join('b', '1.txt'): 'b1'.encode(),
        os.path.join('b', '2.txt'): 'b2'.encode(),
        os.path.join('b', '3.txt'): 'b3'.encode(),
        os.path.join('c', '4.txt'): 'c4'.encode(),
        os.path.join('c', '5.txt'): 'c5'.encode(),
    }

    actual = tmpdir.mkdir('actual')
    kamoshika.postquery.dump.dump_files(src, actual, null_logger())

    expected = tmpdir.mkdir('expected')
    expected.join('a.txt').write('aaa'.encode())
    dir_b = expected.mkdir('b')
    dir_b.join('1.txt').write('b1'.encode())
    dir_b.join('2.txt').write('b2'.encode())
    dir_b.join('3.txt').write('b3'.encode())
    dir_c = expected.mkdir('c')
    dir_c.join('4.txt').write('c4'.encode())
    dir_c.join('5.txt').write('c5'.encode())

    assert compare(expected, actual), report(expected, actual)

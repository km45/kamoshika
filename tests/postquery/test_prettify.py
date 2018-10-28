import logging
import os.path

from kamoshika.postquery.prettify import format_json, format_xml


def null_logger() -> logging.Logger:
    handler = logging.NullHandler
    logger = logging.getLogger(__name__)
    logger.addHandler(handler)  # type: ignore
    return logger


def test_data_path() -> str:
    base_path = os.path.abspath(__file__)
    name, _ = os.path.splitext(__file__)
    return os.path.join(base_path, name)


def test_format_json():
    input_path = os.path.join(test_data_path(), 'input.json')
    output_path = os.path.join(test_data_path(), 'output.json')
    with open(input_path) as input, open(output_path) as output:
        actual = format_json(input.read(), null_logger())
        expected = output.read()
        assert actual == expected


def test_format_xml():
    input_path = os.path.join(test_data_path(), 'input.xml')
    output_path = os.path.join(test_data_path(), 'output.xml')
    with open(input_path) as input, open(output_path) as output:
        actual = format_xml(input.read(), null_logger())
        expected = output.read()
        assert actual == expected

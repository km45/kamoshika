# -*- coding: utf-8 -*-
import logging
import xml.dom.minidom

import kamoshika.postquery.stream


def format_xml(input_string: str, logger: logging.Logger) -> str:
    """Format xml

    Args:
        input_string: xml to format
        logger: logger instance

    Returns:
        formatted xml
    """
    logger.debug('before:\n{}'.format(input_string))

    output = xml.dom.minidom.parseString(input_string).toprettyxml()
    logger.debug('after:\n{}'.format(output))

    return output


def execute(_: str,
            stream: kamoshika.postquery.stream.PostQueryStream,
            config: dict,
            logger: logging.Logger) -> None:
    logger.debug('config: {}'.format(config))

    mode: str = config['format']
    path: str = config['target-path']

    if mode == 'xml':
        for single_host in stream:
            result = format_xml(single_host[path].decode(), logger)
            single_host[path] = result.encode()
    else:
        logger.warning('Invalid format is specified: {}'.format(format))

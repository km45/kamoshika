# -*- coding: utf-8 -*-
import logging
import xml.dom.minidom

import kamoshika.postquery.stream


def format_xml(input: str, logger: logging.Logger) -> str:
    """Format xml

    Args:
        input: xml to format
        logger: logger instance

    Returns:
        formatted xml
    """
    logger.debug('before:\n{}'.format(input))

    output = xml.dom.minidom.parseString(input).toprettyxml()
    logger.debug('after:\n{}'.format(output))

    return output


def execute(output_directory: str,
            stream: kamoshika.postquery.stream.PostQueryStream,
            config: dict,
            logger: logging.Logger) -> None:
    logger.debug('config: {}'.format(config))

    format: str = config['format']
    path: str = config['target-path']

    if format == 'xml':
        for single_host in stream:
            result = format_xml(single_host[path].decode(), logger)
            single_host[path] = result.encode()
    else:
        logger.warning('Invalid format is specified: {}'.format(format))

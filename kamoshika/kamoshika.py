#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Usage:
  kamoshika.py [-c <FILE>] [-o <DIRECTORY>] [--log-level <LEVEL>] <KEY>
  kamoshika.py -h | --help
  kamoshika.py --version

Options:
  -h --help             show this
  -c --config <FILE>    specify config file [default: kamoshika.yml]
  -o --out <DIRECTORY>  specify output directory [default: out]
  --log-level <LEVEL>   specify log level [default: info]
                        valid values:
                          - fatal
                          - error
                          - warn
                          - info
                          - debug
  --version             show version
"""

import docopt

import kamoshika.config
import kamoshika.log
import kamoshika.postquery.diffviewer
import kamoshika.postquery.dump
import kamoshika.postquery.encoding
import kamoshika.postquery.prettify
import kamoshika.postquery.stream
import kamoshika.utility
import kamoshika.version
import kamoshika.xml_strategy


def parse_options() -> dict:
    """Parse command line options

    Returns:
        result dictionary
    """
    parameters = docopt.docopt(__doc__, version=kamoshika.version.__version__)
    return parameters


def main():
    """main function"""
    parameters = parse_options()

    logger = kamoshika.log.create_logger(parameters['--log-level'])

    logger.debug('parsed options:\n{}'.format(parameters))

    conf = kamoshika.config.Config(parameters['--config'], logger)

    request = conf.get_request(parameters['<KEY>'], logger)

    # TODO: Support other strategies
    strategy_instance = kamoshika.xml_strategy.XmlStrategy(
        parameters['--out'], conf.get_server_list(), request, logger)

    kamoshika.utility.clear_output_directory(parameters['--out'], logger)
    strategy_instance.query()
    strategy_instance.post_query()

    pqstream: kamoshika.postquery.stream.PostQueryStream = strategy_instance.get_post_query_stream()
    # TODO: Use filter name specified in config file to select filter
    filters = [
        kamoshika.postquery.encoding,
        kamoshika.postquery.prettify,
        kamoshika.postquery.dump,
        kamoshika.postquery.diffviewer
    ]
    for index, filter in enumerate(filters):
        filter.execute(
            parameters['--out'],
            pqstream,
            conf.get_post_query_filters()[index]['config'], logger
        )


if __name__ == '__main__':
    main()

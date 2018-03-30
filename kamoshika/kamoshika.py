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

import config
import log
import version
import xml_strategy


def parse_options() -> dict:
    """Parse command line options

    Returns:
        result dictionary
    """
    parameters = docopt.docopt(__doc__, version=version.__version__)
    return parameters


def main():
    """main function"""
    parameters = parse_options()

    logger = log.create_logger(parameters['--log-level'])

    logger.debug('parsed options:\n{}'.format(parameters))

    conf = config.Config(parameters['--config'], logger)

    request = conf.get_request(parameters['<KEY>'], logger)

    # TODO: Support other strategies
    strategy_instance = xml_strategy.XmlStrategy(
        parameters['--out'], conf.get_server_list(), request, logger)

    strategy_instance.pre_query()
    strategy_instance.query()
    strategy_instance.post_query()


if __name__ == '__main__':
    main()

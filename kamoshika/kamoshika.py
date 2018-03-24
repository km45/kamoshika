#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Usage:
  kamoshika.py [-c <FILE>] [-o <DIRECTORY>] [--log-level <LEVEL>] <KEY>
  kamoshika.py -h | --help

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
"""

import logging
import os
import typing

import docopt
import requests

import config
import log
import strategy


def parse_options() -> dict:
    """Parse command line options

    Returns:
        result dictionary
    """
    parameters = docopt.docopt(__doc__)
    return parameters


def query(server_config: typing.List[str],
          request: dict,
          logger: logging.Logger) -> typing.List[requests.Response]:
    """Send a request and receive a responce for each server

    Args:
        server_config: server field of config
        request: request to post
        logger: logger instance

    Returns:
        list of received reponces
    """

    responces = []  # type: typing.List[requests.Response]
    for index, server in enumerate(server_config):
        number = index + 1
        logger.info('start query {}/{}'.format(number, len(server_config)))
        responces.append(strategy.fetch_responce(
            server, request['parameter'], request.get('header'), logger))
        logger.info('end query {}/{}'.format(number, len(server_config)))
    return responces


def main():
    """main function"""
    parameters = parse_options()

    logger = log.create_logger(parameters['--log-level'])

    logger.debug('parsed options:\n{}'.format(parameters))

    conf = config.Config(parameters['--config'], logger)

    request = conf.get_request(parameters['<KEY>'], logger)

    # TODO: Support other strategies
    strategy_instance = strategy.XmlStrategy(
        parameters['--out'], conf.get_server_list(), request, logger)

    strategy_instance.pre_query()
    strategy_instance.query()
    strategy_instance.post_query()


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
"""
Usage:
  diff_checker.py [-c <FILE>] [-o <DIRECTORY>] [-v | -vv | -vvv] <KEY>
  diff_checker.py -h | --help

Options:
  -h --help             show this
  -c --config <FILE>    specify config file [default: diff_checker.yml]
  -o --out <DIRECTORY>  specify output directory [default: out]
  -v                    show verbose message
"""

import logging
import os
import shutil
import subprocess
import typing

import docopt
import requests
import yaml


def create_logger(log_level: int) -> logging.Logger:
    """Create logger instance

    Args:
        log_level: log level integer value [0, 100]

    Returns:
        logger instance
    """
    log_format = (
        '[%(asctime)s] [%(levelname)s] (%(filename)s:%(lineno)d) %(message)s')

    handler = logging.StreamHandler()
    handler.setLevel(log_level)
    handler.setFormatter(logging.Formatter(log_format))

    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    logger.addHandler(handler)

    return logger


def parse_options() -> dict:
    """Parse command line options

    Returns:
        result dictionary
    """
    parameters = docopt.docopt(__doc__)
    return parameters


def load_config(file_path: str, logger: logging.Logger) -> dict:
    """Load config file

    Args:
        file_path: config file path
        logger: logger instance

    Returns:
        content dictionary
    """
    with open(file_path) as yaml_file:
        content = yaml.load(yaml_file)
        logger.debug('loaded config ({}):\n{}'.format(
            file_path,
            yaml.dump(content, default_flow_style=False)))
    return content


def get_request(request_config: typing.List[dict], case_id: str, logger: logging.Logger) -> dict:
    """Search request for target case id

    Args:
        requests: request field of config
        case_id: target case id
        logger: logger instance

    Returns:
        target request if found, otherwise None
    """
    for request in request_config:
        if request['case-id'] == case_id:
            logger.debug(
                'success to find request\n{}'.format(
                    yaml.dump(request, default_flow_style=False)))
            return request
    logger.error('failed to find request (case-id = {})'.format(case_id))
    return None


def query(server_config: typing.List[str], request: dict, logger: logging.Logger) -> typing.List[requests.Response]:
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
        with requests.Session() as session:
            prepared = requests.Request(
                'GET',
                server,
                params=request['parameter'],
                headers=request.get('header')).prepare()
            logger.info('prepared request:\n'
                        'parameter:\n'
                        '{}\n'
                        'headers:\n'
                        '{}\n'.format(prepared.url, prepared.headers))
            responce = session.send(prepared)
            logger.info('received responce:\n'
                        'status code:\n'
                        '{}\n'
                        'headers:\n'
                        '{}\n'.format(responce.status_code, responce.headers))
            responces.append(responce)
        logger.info('end query {}/{}'.format(number, len(server_config)))
    return responces


def clear_output_directory(directory: str, logger: logging.Logger) -> None:
    """Clear output directory

    Args:
        directory: directory to remove recursively
        logger: logger instance
    """
    logger.debug(
        'remove directory "{}" recursively if exists'.format(directory))

    if os.path.exists(directory):
        logger.debug('directory "{}" exists'.format(directory))
        logger.warn('remove directory "{}" recursively'.format(directory))
        shutil.rmtree(directory)


def save_responces(responces: typing.List[requests.Response], responce_conf: dict, out_directory: str, logger: logging.Logger) -> typing.List[str]:
    """Save responces as files

    Args:
        responces: list of responce instance
        responce_conf: responce field of config
        out_directory: directory where save files
        logger: logger instance

    Returns:
        saved file paths
    """
    logger.info('create output directory: {}'.format(out_directory))
    os.makedirs(out_directory)

    file_name_prefix = responce_conf['file_name_prefix']
    file_name_postfix = responce_conf['file_name_postfix']

    saved_files = []  # type: typing.List[str]
    for index, responce in enumerate(responces):
        number = index + 1
        file_name = '{}{}{}'.format(
            file_name_prefix, number, file_name_postfix)
        file_path = os.path.join(out_directory, file_name)
        with open(file_path, 'wb') as out:
            logger.info(
                'save responce body for query {} as {}'.format(number, file_path))
            out.write(responce.content)
            logger.info('success to save {}'.format(file_path))
            saved_files.append(file_path)
    return saved_files


def invoke_diff_viewer(post_processed_paths: typing.List[str], logger: logging.Logger) -> None:
    """invoke diff viewer

    Args:
        post_processed_paths: post processed paths, files or directories
        logger: logger instance
    """
    command = ['meld'] + post_processed_paths
    logger.debug('execute following command:\n{}'.format(command))
    subprocess.call(command)


def main():
    """main function
    """
    parameters = parse_options()

    log_level_map = {
        0: logging.ERROR,
        1: logging.WARN,
        2: logging.INFO,
        3: logging.DEBUG
    }
    logger = create_logger(log_level_map[parameters['-v']])

    logger.debug('parsed options:\n{}'.format(parameters))

    config = load_config(parameters['--config'], logger)

    request = get_request(config['request'], parameters['<KEY>'], logger)

    responces = query(config['server'], request, logger)

    clear_output_directory(parameters['--out'], logger)

    saved_file_paths = save_responces(
        responces, config['responce'], parameters['--out'], logger)

    # TODO: Implement post processes like followings:
    #   - uncompress archive
    #   - format text such as html/xml and json
    #   - convert binary to text
    post_processed_paths = saved_file_paths

    invoke_diff_viewer(post_processed_paths, logger)


if __name__ == '__main__':
    main()

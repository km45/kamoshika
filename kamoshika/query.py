# -*- coding: utf-8 -*-
"""Send requests and receive responces"""

import logging
import typing

import requests

from kamoshika.postquery.stream import PostQueryStream


def fetch_responce(
        server: str,
        request_parameter: str,
        request_headers: typing.Optional[dict],
        logger: logging.Logger) -> requests.Response:
    """Send a request and receive a responce

    Args:
        server: server path
        request_parameter: request parameter
        request_headers: dictionary of request headers
        logger: logger instance

    Returns
        received responce
    """
    with requests.Session() as session:
        prepared = requests.Request(
            'GET',
            server,
            params=request_parameter,
            headers=request_headers).prepare()
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
        return responce


def query(
        query_config: dict,
        server_config: typing.List[str],
        request: dict,
        logger: logging.Logger) -> PostQueryStream:
    """
    Send a request and receive a responce for each server

    Args:
        query_config: query config filed of config
        server_config: server field of config
        request: request to post
        logger: logger instance
    """
    responces = []  # type: typing.List[requests.Response]
    for index, server in enumerate(server_config):
        number = index + 1
        logger.info(
            'start query {}/{}'.format(number, len(server_config)))
        responces.append(fetch_responce(
            server,
            request['parameter'],
            request.get('header'),
            logger))
        logger.info(
            'end query {}/{}'.format(number, len(server_config)))

    post_query_stream: PostQueryStream = []
    path = query_config['dst']
    for responce in responces:
        post_query_stream.append({path: responce.content})
    return post_query_stream

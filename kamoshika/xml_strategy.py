# -*- coding: utf-8 -*-
"""Provide functions for pre_query, query and post_query"""

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


class XmlStrategy:
    """Strategy for xml"""

    def __init__(
            self,
            server_config: typing.List[str],
            request: dict,
            logger: logging.Logger) -> None:
        """
        Args:
            server_config: server field of config
            request: request to post
            logger: logger instance
        """
        self._server_config = server_config
        self._request = request
        self._logger = logger
        self._responces = []  # type: typing.List[requests.Response]
        self._post_query_stream: PostQueryStream = []

    def query(self) -> PostQueryStream:
        """Send a request and receive a responce for each server"""
        for index, server in enumerate(self._server_config):
            number = index + 1
            self._logger.info(
                'start query {}/{}'.format(number, len(self._server_config)))
            self._responces.append(fetch_responce(
                server,
                self._request['parameter'],
                self._request.get('header'),
                self._logger))
            self._logger.info(
                'end query {}/{}'.format(number, len(self._server_config)))

        for responce in self._responces:
            self._post_query_stream.append({'responce.xml': responce.content})
        return self._post_query_stream

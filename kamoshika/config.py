# -*- coding: utf-8 -*-
"""
Load config file and access loaded data
"""

import logging
import typing

import yaml


class Config:
    """
    Load config file and provide data accessor
    """

    def __init__(self, file_path: str, logger: logging.Logger) -> None:
        self.__load(file_path, logger)

    def __load(self, file_path: str, logger: logging.Logger) -> None:
        """Load config file and set its dictionary as self._content

        Args:
            file_path: config file path
            logger: logger instance
        """
        with open(file_path) as yaml_file:
            self._content = yaml.load(yaml_file)
            logger.debug('loaded config ({}):\n{}'.format(
                file_path,
                yaml.dump(self._content, default_flow_style=False)))

    def get_request(self, case_id: str, logger: logging.Logger) -> dict:
        """Search request for target case id

        Args:
            requests: request field of config
            case_id: target case id
            logger: logger instance

        Returns:
            target request if found, otherwise None
        """
        for request in self._content['request']:
            if request['case-id'] == case_id:
                logger.debug(
                    'success to find request\n{}'.format(
                        yaml.dump(request, default_flow_style=False)))
                return request
        logger.error('failed to find request (case-id = {})'.format(case_id))
        return None

    def get_server_list(self) -> typing.List[str]:
        """Return server config

        Returns:
            list of servers
        """
        return self._content['server']

    def get_responce(self) -> dict:
        """Return responce config

        Returns:
            dictionary of responce config
        """
        return self._content['responce']

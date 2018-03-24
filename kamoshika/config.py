import logging
import typing

import yaml


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

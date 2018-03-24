import logging

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

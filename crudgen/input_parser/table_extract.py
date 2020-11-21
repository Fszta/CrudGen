import json
from utils.logging import logger


def extract_tables_name(input_dict: dict):
    """Extract tables names from input dictionnary"""
    return list(input_dict.keys())


def parse_json(file_path: str):
    """
    Parse json file containing table details
    :param file_path: json file path
    :return: dict containing json data
    """
    try:
        with open(file_path) as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        logger.error("Cannot find input json file that describe table content")
        exit(1)

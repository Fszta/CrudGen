import os
from crudgen.utils.config import config, CONFIG_ENV

PACKAGES = ["controller", "model", "schema", "router", "database"]
BASE = config[CONFIG_ENV].GENERATED_API_PATH


def create_api_structure(output_path: str):
    """
    Create api package structure
    Generate all defined packages inside Base
    """
    create_package(output_path, True, output_path)
    [create_package(package, False, output_path) for package in PACKAGES]


def create_package(package_name: str, is_base: bool, output_path: str):
    """
    Create python package if not exists

    :param package_name: name of the package dir
    :param is_base: bool - true is package is base (higher level)
    """
    if not is_base:
        directory_path = output_path + "/" + package_name
    else:
        directory_path = package_name

    if not os.path.exists(directory_path):
        os.mkdir(directory_path)
        with open(directory_path+"/__init__.py", "w"):
            pass

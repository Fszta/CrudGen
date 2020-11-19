import os

PACKAGES = ["controller", "model", "schema", "router"]
BASE = "generated_api"


def create_api_structure():
    """
    Create api package structure
    Generate all defined packages inside Base
    """
    create_package(BASE, True)
    [create_package(package, False) for package in PACKAGES]


def create_package(package_name: str, is_base: bool):
    """
    Create python package if not exists

    :param package_name: name of the package dir
    :param is_base: bool - true is package is base (higher level)
    """
    if not is_base:
        directory_path = BASE + "/" + package_name
    else:
        directory_path = package_name

    if not os.path.exists(directory_path):
        os.mkdir(directory_path)
        with open(directory_path+"/__init__.py", "w"):
            pass

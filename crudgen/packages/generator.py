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


def create_package(directory_name: str, is_base_dir: bool):
    """ Create python package if not exists """

    if not is_base_dir:
        directory_path = BASE + "/" + directory_name
    else:
        directory_path = directory_name

    if not os.path.exists(directory_path):
        os.mkdir(directory_path)
        os.mknod(os.path.join(directory_path, "__init__.py"))


import os


def create_package(directory_name: str):
    if not os.path.exists(directory_name):
        os.mkdir(directory_name)

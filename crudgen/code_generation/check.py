import os
from crudgen.utils.logging import logger


def is_generated(package_name: str):
    def decorator(generation_function):
        def wrapper(*args):
            file = generation_function(*args)
            if file in os.listdir(os.getenv("OUTPUT_PATH") + "/" + package_name):
                logger.info(f"Successfully create {file} in {package_name} package")
                return True
            else:
                logger.error(f"Fail to create {file} in {package_name} package")
                return False
        return wrapper
    return decorator


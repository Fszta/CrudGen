import os
import argparse
from dataclasses import dataclass
from crudgen.utils.config import config, CONFIG_ENV
from crudgen.utils.logging import logger


@dataclass
class UserArgs:
    file: str
    output_dir: str
    name: str


def set_parameters():
    """ Parse command line arguments """
    args = parse_arguments()
    user_arguments = UserArgs(
        args["file"],
        args["output_dir"],
        args["name"]
    )
    if user_arguments.name is None:
        logger.warn(f"--name parameter is unset, set default to {config[CONFIG_ENV].GENERATED_API_PATH}")
        user_arguments.name = config[CONFIG_ENV].GENERATED_API_PATH

    os.environ["OUTPUT_PATH"] = user_arguments.output_dir + user_arguments.name

    return user_arguments


def parse_arguments():
    """
    Parse command line arguments with argparse
    :return: list contaning arguments
    """

    ap = argparse.ArgumentParser()

    ap.add_argument("-f", "--file", required=True, help="input json file with table description")
    ap.add_argument("-o", "--output-dir", required=True, help="path of the output directory")
    ap.add_argument("-n", "--name", required=False, help="name of the generated directory", nargs="?",
                    const=config[CONFIG_ENV].GENERATED_API_PATH)

    args = vars(ap.parse_args())

    return args

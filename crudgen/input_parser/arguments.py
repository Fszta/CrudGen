import os
import argparse
from dataclasses import dataclass
from crudgen.utils.config import config, CONFIG_ENV
from crudgen.utils.logging import logger


@dataclass
class UserArgs:
    file: str
    output_dir: str
    start: bool
    name: str
    cors_activation: bool


def set_parameters():
    """ Parse command line arguments """
    args = parse_arguments()
    user_arguments = UserArgs(
        args["file"],
        process_output_dir_path(args["output_dir"]),
        args["start"],
        args["name"],
        args["cors_activation"]
    )
    if user_arguments.name is None:
        logger.warn(f"--name parameter is unset, set default to {config[CONFIG_ENV].GENERATED_API_PATH}")
        user_arguments.name = config[CONFIG_ENV].GENERATED_API_PATH

    os.environ["OUTPUT_PATH"] = user_arguments.output_dir + user_arguments.name

    if args["db_url"] is not None:
        logger.info(f"Set default database to {args['db_url']}")
        os.environ["DB_URL"] = args["db_url"]
    else:
        logger.warn("No db url pass as argument, will check if DB_URL environment variable exists, "
                    "otherwise will use SQL Lite as default db")
    return user_arguments


def parse_arguments():
    """
    Parse command line arguments with argparse
    :return: list contaning arguments
    """

    ap = argparse.ArgumentParser()

    ap.add_argument("-f", "--file", required=True, help="input json file with table description")
    ap.add_argument("-o", "--output-dir", required=True, help="path of the output directory")
    ap.add_argument("-s", "--start", required=True, help="boolean - true to run api - false to only generate files")
    ap.add_argument("-n", "--name", required=False, help="name of the generated directory", nargs="?",
                    const=config[CONFIG_ENV].GENERATED_API_PATH)
    ap.add_argument("-d", "--db_url", required=False, help="db url as driver://user:password@host:port/dbName")
    ap.add_argument("-c", "--cors_activation", required=False, help="boolean - true to activate cors", nargs="?",
                    const=False)
    args = vars(ap.parse_args())

    return args


def process_output_dir_path(output_dir):
    """
    Add a / to the end of path is user don't
    :param output_dir: path of the output_dir
    :return: output_dir path processed
    """
    if output_dir[-1] != "/":
        return output_dir + "/"
    else:
        return output_dir

from crudgen.utils.logging import logger
from crudgen.utils.config import config, CONFIG_ENV
from crudgen.input_parser.table_extract import extract_table_structure
from crudgen.code_generation.packages.generator import create_api_structure
from crudgen.code_generation.schema import schema_generator
from crudgen.code_generation.model import model_generator
from crudgen.code_generation.database.db_init_generator import generate_db_init_file
from crudgen.code_generation.router import router_generator
from crudgen.code_generation.controller import controller_generator
from crudgen.input_parser.arguments import set_parameters
from crudgen.utils.exceptions import *


def start():
    user_arguments = set_parameters()
    logger.info("Start CrudGen {} ...".format(config[CONFIG_ENV].VERSION))
    full_output_path = user_arguments.output_dir + "/" + user_arguments.name

    # Create generated api layout
    create_api_structure(full_output_path)

    # Create db initialization file
    generate_db_init_file(full_output_path)

    # Extract input file content
    tables_content = extract_table_structure(user_arguments.file)

    # Generate crud foreach table describe in input file
    [generate(table, fields, full_output_path) for table, fields in tables_content.items()]

    logger.info(f"Generation finished, folder has been created at location {user_arguments.output_dir}")


def generate(table_name: str, description: dict, output_path: str):
    """
    Run files generation for a single table
    :param table_name: name of the table
    :param description: fields of the table with value, type and db params
    """
    fields = description["fields"]
    key_identifier = description["key_identifier"]["name"]
    key_type = description["key_identifier"]["type"].pydantic_type_name

    if schema_generator.run(table_name, fields, output_path) is False:
        raise SchemaGenerationException(f"Fail to generate schema for {table_name} table")

    if model_generator.run(table_name, fields, output_path) is False:
        raise ModelGenerationException(f"Fail to generate model for {table_name} table")

    if router_generator.run(table_name, output_path, key_identifier, key_type) is False:
        raise RouterGenerationException(f"Fail to generate router for {table_name} table")

    if controller_generator.run(table_name, key_identifier, key_type, fields, output_path) is False:
        raise ControllerGenerationException(f"Fail to generate controller for {table_name} table")


if __name__ == '__main__':
    start()

import os
from crudgen.utils.logging import logger
from crudgen.utils.config import config, CONFIG_ENV
from crudgen.input_parser.table_extract import extract_table_structure
from crudgen.code_generation.packages.generator import create_api_structure
from crudgen.code_generation.schema import schema_generator
from crudgen.code_generation.model import model_generator
from crudgen.code_generation.database.db_init_generator import generate_db_init_file
from crudgen.code_generation.router import router_generator
from crudgen.code_generation.controller import controller_generator
from crudgen.code_generation.launcher import launcher_generator
from crudgen.input_parser.arguments import set_parameters
from crudgen.utils.exceptions import *
from crudgen.input_parser.arguments import UserArgs


class Crudgen:
    def __init__(self, user_args: UserArgs):
        self.user_args = user_args
        self.output_path = user_args.output_dir + user_args.name + "/"

    def create_common_files(self, tables_content, cors_activation: bool):
        """
        Generate needed common files and directory whatever
        the number of tables. Following files / dir are created :
        - package structure : schema / model / controller / router / database
        - db_init.py under database package
        - app.py under the root directory
        """

        create_api_structure(self.output_path)
        generate_db_init_file(self.output_path)
        launcher_generator.run(list(tables_content.keys()), "0.0.0.0", 8080, self.output_path, cors_activation)

    def create_table_files(self, table_name: str, description: dict):
        """
        Run files generation for a single table
        :param table_name: name of the table
        :param description: fields of the table with value, type and db params
        """
        fields = description["fields"]
        key_identifier = description["key_identifier"]["name"]
        key_type = description["key_identifier"]["type"].pydantic_type_name

        if schema_generator.run(table_name, fields, self.output_path) is False:
            raise SchemaGenerationException(f"Fail to generate schema for {table_name} table")

        if model_generator.run(table_name, fields, self.output_path) is False:
            raise ModelGenerationException(f"Fail to generate model for {table_name} table")

        if router_generator.run(table_name, self.output_path, key_identifier, key_type) is False:
            raise RouterGenerationException(f"Fail to generate router for {table_name} table")

        if controller_generator.run(table_name, key_identifier, key_type, fields, self.output_path) is False:
            raise ControllerGenerationException(f"Fail to generate controller for {table_name} table")

    @staticmethod
    def start_api(output_path: str):
        print(output_path)
        try:
            logger.info("Running api... swagger documentation is available at http://0.0.0.0:8080/docs")
            os.system(f"python {output_path}/app.py")
        except OSError:
            logger.error("Fail to start generated api, verify that output path is absolute path")
            pass

    def run(self):
        user_args = self.user_args

        tables_content = extract_table_structure(user_args.file)

        # Generate api structure and base files
        self.create_common_files(tables_content, user_args.cors_activation)

        # Generate crud foreach table describe in input file
        [self.create_table_files(table, fields) for table, fields in tables_content.items()]

        logger.info(f"Generation finished, folder has been created at location {user_args.output_dir}")

        # Start api
        if user_args.start.lower() == "true":
            self.start_api(self.output_path)
        else:
            logger.warning(f"Parameter start is set to False, api will not start automatically after files generation")


if __name__ == '__main__':
    logger.info("Start CrudGen {} ...".format(config[CONFIG_ENV].VERSION))
    user_args = set_parameters()
    crudgen = Crudgen(user_args)
    crudgen.run()

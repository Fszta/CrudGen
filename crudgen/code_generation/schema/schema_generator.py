from crudgen.code_generation.indentation import Indentator
from crudgen.utils.config import config, CONFIG_ENV
from crudgen.utils.logging import logger
from crudgen.code_generation.check import is_generated
from crudgen.code_generation.imports import pydantic_import, format_imports
from crudgen.code_generation.code_formatting import class_declare


@is_generated(package_name="schema")
def run(table_name: str, table_fields: dict, output_path: str):
    """
    Run schema file generation
    Generate schema_name.py file inside schema package
    """
    logger.info(f"Start {table_name} schema generation")

    filename = f"{table_name}_schema.py"
    file_schema = open(output_path + config[CONFIG_ENV].SCHEMA_PACKAGE_PATH + filename, "a")

    imports = format_imports(pydantic_import())
    class_declaration = declare_schema_class(table_name)
    content = imports + class_declaration + schema_fields(table_fields)

    file_schema.write(content)
    file_schema.close()

    return filename


@class_declare
def declare_schema_class(table_name: str):
    """
    Schema class declaration
    :param table_name: name of the table
    :return: class declaration string
    """
    class_name = table_name.capitalize()
    return f"class {class_name}(BaseModel):"


def schema_fields(fields: dict):
    """
    Generate schema fields
    :param fields: table fields dict
    :return: string containing formated fields
    """
    schema_fields = [Indentator.IND_LEVEL_1 + field["field_name"] + ": " + field["field_type"].pydantic_type_name +
                     "\n" for field in fields]
    return "".join(schema_fields)



from crudgen.utils.code_formatting import *
from crudgen.utils.indentation import Indentator
from crudgen.utils.config import config, CONFIG_ENV
from crudgen.generator.tools import check_is_generated


@generic_import_declaration
def typing_import():
    return "from typing import List"


@generic_import_declaration
def sql_alchemy_import():
    """ Generate sqlAlchemy session import"""
    return "from sqlalchemy.orm import Session"


@custom_import_declaration
def schema_import(table_name):
    """ Generate pydantic schema import based on table_name"""
    return "from schema import {}_schema".format(table_name)


@custom_import_declaration
def controller_import(table_name):
    """ Generate controller import based on table_name"""
    return "from controller import {}_controller".format(table_name)


@custom_import_declaration
def model_import(table_name):
    """ Generate controller import based on table_name"""
    return "from model import {}_model".format(table_name)


@imports_declaration
def format_imports(*args):
    """
    Generate & format controller imports.
    :return: formated imports
    """
    imports = "".join(args)
    return imports


@function_declaration
def generate_get_function(table_name: str, key: str, key_type: str):
    """
    Generate get one function
    :param table_name: name of the table
    :param key: key use to identify sample ie: id
    :param key_type: type of the key
    :return: string containing get one function
    """

    model_class = table_name.capitalize()

    # Build function declaration
    function_definition = f"def get_{table_name}(db: Session, {key}: {key_type}):"

    # Build get query
    return_statement = Indentator.IND_LEVEL_1 + f"return db.query({table_name}_model.{model_class}).filter(" \
                                                f"{table_name}_model.{model_class}.{key} == {key}).first()"

    return function_definition + "\n" + return_statement


@function_declaration
def generate_get_all_function(table_name: str):
    """
    Generate get all function
    :param table_name: name of the table
    :return: string containing get all function
    """
    model_class = table_name.capitalize()

    function_definition = f"def get_all_{table_name}(db: Session):"
    return_statement = Indentator.IND_LEVEL_1 + f"return db.query({table_name}_model.{model_class}).all()"

    return function_definition + "\n" + return_statement


@function_declaration
def generate_delete_function(table_name: str, key: str):
    """
    Generate delete function
    :param table_name: name of the table
    :param key: key to identify sample
    :return: string containing delete function
    """
    model_class = table_name.capitalize()
    function_definition = f"def delete_{table_name}(db: Session, {key}):"
    content = Indentator.IND_LEVEL_1 + f"to_delete = db.query({table_name}_model.{model_class}).filter(" \
                                       f"{table_name}_model.{model_class}.{key} == {key})" + "\n" + \
              Indentator.IND_LEVEL_1 + "deleted = to_delete.delete()" + "\n" + \
              Indentator.IND_LEVEL_1 + "if deleted == 0:" + "\n" + \
              Indentator.IND_LEVEL_2 + "return None" + "\n" + \
              Indentator.IND_LEVEL_1 + "else:" + "\n" + \
              Indentator.IND_LEVEL_2 + "db.commit()" + "\n" + \
              Indentator.IND_LEVEL_2 + "return True"

    return function_definition + "\n" + content


@function_declaration
def generate_create_function(table_name: str, fields: dict):
    """
    Generate create function
    :param table_name: name of the table
    :param fields: table attributs description
    :return: string containing create function
    """
    model_class = table_name.capitalize()
    function_definition = f"def create_{table_name}(db: Session, {table_name}: {table_name}_schema.{model_class}):\n"
    content = Indentator.IND_LEVEL_1 + f"db_{table_name} = {table_name}_model.{model_class}(\n" + \
              "".join([Indentator.IND_LEVEL_2 + f"{field['field_name']}={table_name}.{field['field_name']}," +
                       "\n" for field in fields]) +\
              Indentator.IND_LEVEL_1 + ")\n" + \
              Indentator.IND_LEVEL_1 + f"db.add(db_{table_name})" + "\n" + \
              Indentator.IND_LEVEL_1 + "db.commit()" + "\n" + \
              Indentator.IND_LEVEL_1 + f"db.refresh(db_{table_name})" + "\n" + \
              Indentator.IND_LEVEL_1 + f"return db_{table_name}"

    return function_definition + content


@function_declaration
def generate_update_function(table_name: str, identifier: str):
    """
    Generate update function.
    :param table_name: name of the table
    :param identifier: key use to identify sample
    :return: string containing update func
    """
    model_class = table_name + "_model." + table_name.capitalize()

    function_definition = f"def update_{table_name}(db: Session, {identifier}, new_value):\n"
    content = Indentator.IND_LEVEL_1 + f"db_{table_name} = db.query({model_class}).filter({model_class}." \
                                       f"{identifier} == {identifier}).first()" + "\n" + \
              Indentator.IND_LEVEL_1 + f"db_{table_name} = new_value" + "\n" + \
              Indentator.IND_LEVEL_1 + f"db.commit()" + "\n" + \
              Indentator.IND_LEVEL_1 + f"db.refresh(db_{table_name})" + "\n" + \
              Indentator.IND_LEVEL_1 + f"return db_{table_name}"

    return function_definition + content


def generate_crud_functions(table_name: str, key: str, key_type: str, fields: dict):
    """
    Generate crud function
    :param table_name: name of the table
    :param key: key use to identify sample ie: id
    :param key_type: type of the key
    :param fields: dict containing table attributs description
    """
    return generate_get_function(table_name, key, key_type) + \
           generate_get_all_function(table_name) + \
           generate_delete_function(table_name, key) + \
           generate_create_function(table_name, fields) + \
           generate_update_function(table_name, key)


@check_is_generated(package_name="controller")
def run(table_name: str, key: str, key_type: str, fields: dict, output_path: str):
    """
    Run controller generator. Create a table_name_controller file
    under controller packages. It contains following crud functions:
    * get one /get all / delete one / create one /update one
    :param output_path: path of the directory containing generated api
    :param table_name: name of the table
    :param key: key use to identify sample ie: id
    :param key_type: type of the key
    :param fields: dict containing table attributs description
    """
    filename = f"{table_name}_controller.py"
    file_controller = open(output_path + config[CONFIG_ENV].CONTROLLER_PACKAGE_PATH + filename, "a")

    imports = format_imports(
        sql_alchemy_import(),
        schema_import(table_name),
        model_import(table_name)
    )

    crud_functions = generate_crud_functions(table_name, key, key_type, fields)
    file_controller.write(imports+crud_functions)
    file_controller.close()

    return filename

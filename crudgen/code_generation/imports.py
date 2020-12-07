from crudgen.code_generation.code_formatting import generic_import_declaration, custom_import_declaration, \
    imports_declaration


@imports_declaration
def format_imports(*args):
    """
    Generate & format controller imports.
    :return: formated imports
    """
    imports = "".join(args)
    return imports


@generic_import_declaration
def typing_import():
    return "from typing import List"


@generic_import_declaration
def sql_alchemy_session_import():
    """ Generate sqlAlchemy session import"""
    return "from sqlalchemy.orm import Session"


def build_sql_alchemy_type_import(types: list):
    """
    Build sql alchemy types import statement
    :param types: set of sql alchemy types
    :return: import statement string
    """
    import_statement = "from sqlalchemy import Column"
    for sql_alchemy_type in types:
        import_statement += ", " + sql_alchemy_type

    return import_statement


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


@generic_import_declaration
def db_init_import():
    """ Generate init database import statement"""
    return "from database import get_db"


@generic_import_declaration
def db_base_import():
    return "from database.db_init import Base"


@generic_import_declaration
def fastapi_import():
    """ Generate fastApi import"""
    return "from fastapi import APIRouter, HTTPException, Depends"

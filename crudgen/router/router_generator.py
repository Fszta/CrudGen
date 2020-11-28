from crudgen.utils.config import config, CONFIG_ENV
from crudgen.utils.code_formatting import generic_import_declaration, custom_import_declaration, imports_declaration


class RouterGenerator:
    """
    Crud router generator, it creates a router_name.py file inside router package
    Following endpoints are implemented:
    - add one : add one element in database.
    - get one : get one element from database, based on a field.
    - get all : get all elements from database.
    - update one : update one element from database, based on a field
    - deleted_one : delete one element from database, based on a field
    """

    def __init__(self, table_name: str, key_field: str):
        self.table_name = table_name
        self.key_field = key_field
        self.filename = "router_{}.py".format(table_name)
        self.file_open = open(config[CONFIG_ENV].ROUTER_PACKAGE_PATH + self.filename, "a")

    @staticmethod
    @generic_import_declaration
    def generate_fastapi_import():
        """ Generate fastApi import"""
        return "from fastapi import APIRouter, HTTPException, Depends"

    @staticmethod
    @generic_import_declaration
    def generate_sql_alchemy_import():
        """ Generate sqlAlchemy session import"""
        return "from sqlalchemy.orm import Session"

    @staticmethod
    @custom_import_declaration
    def generate_schema_import(table_name):
        """ Generate pydantic schema import based on table_name"""
        return "from schema import schema_{}".format(table_name)

    @staticmethod
    @custom_import_declaration
    def generate_controller_import(table_name):
        """ Generate controller import based on table_name"""
        return "from controller import controller_{}".format(table_name)

    @staticmethod
    @generic_import_declaration
    def generate_database_import():
        """ Generate init database import statement"""
        return "from database import get_db"

    @staticmethod
    @imports_declaration
    def format_imports(fastapi, sql_alchemy, schema, controller, database):
        """ Generate all import statement of router"""
        global_import = fastapi + sql_alchemy + schema + controller + database
        return global_import

    def generate_add_one(self):
        pass

    def generate_get_one(self):
        pass

    def generate_get_all(self):
        pass

    def generate_update_one(self):
        pass

    def generate_delete_one(self):
        pass

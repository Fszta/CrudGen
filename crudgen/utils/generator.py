from abc import ABC, abstractmethod
from crudgen.utils.code_formatting import generic_import_declaration, custom_import_declaration


class Generator(ABC):

    @staticmethod
    @generic_import_declaration
    def typing_import():
        return "from typing import List"

    @staticmethod
    @generic_import_declaration
    def generate_sql_alchemy_import():
        """ Generate sqlAlchemy session import"""
        return "from sqlalchemy.orm import Session"

    @staticmethod
    @custom_import_declaration
    def generate_schema_import(table_name):
        """ Generate pydantic schema import based on table_name"""
        return "from schema import {}_schema".format(table_name)

    @staticmethod
    @custom_import_declaration
    def generate_controller_import(table_name):
        """ Generate controller import based on table_name"""
        return "from controller import {}_controller".format(table_name)

    @abstractmethod
    def format_imports(self):
        pass

    @abstractmethod
    def run(self):
        pass

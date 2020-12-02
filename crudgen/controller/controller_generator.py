import os
from crudgen.utils.code_formatting import *
from crudgen.utils.generator import Generator


class ControllerGenerator(Generator):
    def __init__(self, table_name, key_identifier: str, table_fields: dict):
        self.table_name = table_name
        self.key_identifier = key_identifier
        self.table_fields = table_fields

    @imports_declaration
    def format_imports(self):
        pass

    def generate_get_method(self):
        pass

    def generate_get_all_method(self):
        pass

    def generate_delete_method(self):
        pass

    def generate_update_one_method(self):
        pass

    def generate_create_method(self):
        pass

    def run(self):
        pass

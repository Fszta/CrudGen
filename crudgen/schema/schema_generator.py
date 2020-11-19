from utils.indentation import Indentator
from utils.config import config, CONFIG_ENV


class SchemaGenerator:
    def __init__(self, name: str, schema_fields: dict):
        self.name = name
        self.schema_fields = schema_fields
        self.filename = "schema_{}.py".format(name)
        self.file_open = open(config[CONFIG_ENV].SCHEMA_PACKAGE_PATH+self.filename, "a")
        
    def run(self):
        """
        Run schema file generation
        Generate schema_name.py file inside schema package
        """
        # Add import package
        self.add_imports()
        self.jump_lines(3)

        # Write class name
        class_name = "test".capitalize()
        class_declaration = "class " + class_name + "(BaseModel):"
        self.file_open.write(class_declaration)
        self.jump_lines(1)

        # Write all fields defined in schema dict
        self.add_fields()
        self.file_open.close()

    def add_fields(self):
        """
        Add fields to schema class
        """
        for field in self.schema_fields["schema_field"]:
            self.file_open.write(Indentator.IND_LEVEL_1)
            self.file_open.write(field["field_name"] + ": " + field["field_type"])
            self.jump_lines(1)

    def add_imports(self):
        """
        Add import statements
        """
        self.file_open.write("from pydantic import BaseModel")

    def jump_lines(self, number_of_jump):
        """
        Jump lines in file
        :param number_of_jump: number of line to jump, 0 = return to line
        """
        for i in range(0, number_of_jump):
            self.file_open.write("\n")

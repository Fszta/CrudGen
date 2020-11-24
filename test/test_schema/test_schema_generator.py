import unittest
import os

from test import setup
from crudgen.schema.schema_generator import SchemaGenerator
from crudgen.input_parser.type_mapper import TypeMapper
from crudgen.utils.config import config


class TestSchemaGenerator(unittest.TestCase):
    def test_init(self):
        """
        Test SchemaGenerator initialization
        schema_name.py should be created in schema
        package
        """
        schema_generator = SchemaGenerator("test", "test", {})
        files_in_dir = os.listdir(config["test"].SCHEMA_PACKAGE_PATH)
        schema_generator.file_open.close()

        self.assertTrue("schema_test.py" in files_in_dir)

        # Remove test file
        os.remove(config["test"].SCHEMA_PACKAGE_PATH + "schema_test.py")

    def test_run(self):
        """
        Test SchemaGenerator pipeline :
        It should create a schema_test.py file
        with pydantic schema format inside, according to the input dict
        contents which discribe tables
        """

        test_fields = [
            {
                "field_name": "id",
                "field_type": TypeMapper(pydantic_type_name='int', sql_alchemy_type_name='Integer'),
                "unique": True,
                "primary_key": True
            },
            {
                "field_name": "name",
                "field_type": TypeMapper(pydantic_type_name='str', sql_alchemy_type_name='String'),
                "unique": False,
                "primary_key": False
            },
            {
                "field_name": "age",
                "field_type": TypeMapper(pydantic_type_name='int', sql_alchemy_type_name='Integer'),
                "unique": False,
                "primary_key": False
            },
        ]

        test_schema_generator = SchemaGenerator("test", "test", test_fields)
        test_schema_generator.run()

        # Read generated test_schema
        generated_file_path = config["test"].SCHEMA_PACKAGE_PATH + "schema_test.py"
        generated_file = open(generated_file_path, "r")

        # Read expected test_schema
        expected_file = open(config["test"].SCHEMA_PACKAGE_PATH + "expected_schema.py", "r")

        self.assertEqual(generated_file.read(), expected_file.read())

        generated_file.close()
        expected_file.close()

        # Remove deleted file
        os.remove(generated_file_path)

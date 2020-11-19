import unittest
import os
from crudgen.schema.schema_generator import SchemaGenerator


class TestSchemaGenerator(unittest.TestCase):
    def test_init(self):
        schema_generator = SchemaGenerator("test", {})
        files_in_dir = os.listdir()
        schema_generator.file_open.close()
        self.assertTrue("schema_test.py" in files_in_dir)

    def test_run(self):
        test_fields = {
            "schema_field": [
                {
                    "field_name": "name",
                    "field_type": "str"
                },
                {
                    "field_name": "age",
                    "field_type": "int"
                },
                {
                    "field_name": "img_url",
                    "field_type": "str"
                },
                {
                    "field_name": "description",
                    "field_type": "str"
                }
            ]
        }
        test_schema_generator = SchemaGenerator("test", test_fields)
        test_schema_generator.run()

        # Read generated schema
        generated_filename = "schema_test.py"
        generated_file = open(generated_filename, "r")

        # Read expected schema
        expected_file = open("expected_schema.py", "r")

        self.assertEqual(generated_file.read(), expected_file.read())

        generated_file.close()
        expected_file.close()


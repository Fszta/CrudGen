import os
from unittest import TestCase
from test import setup
from crudgen.model.model_generator import ModelGenerator
from crudgen.utils.config import config
from test.resources.data_test import DataTest


class TestModelGenerator(TestCase):

    def test_init(self):
        test_generator = ModelGenerator("test", DataTest.TEST_FIELDS)
        files_in_dir = os.listdir(config["test"].MODEL_PACKAGE_PATH)

        self.assertTrue("model_test.py" in files_in_dir)

    def test_get_types(self):
        test_generator = ModelGenerator("test", DataTest.TEST_FIELDS)
        types = test_generator.get_types()
        expected_types = {"Integer", "String"}

        self.assertEqual(types, expected_types)

    def test_build_sql_alchemy_import(self):
        expected_import = "from sqlalchemy import Column, Boolean, Integer, String"
        test_types = {"Boolean, Integer, String"}
        test_generator = ModelGenerator("test", DataTest.TEST_FIELDS)
        generated_import = test_generator.build_sql_alchemy_import(test_types)

        self.assertEqual(expected_import, generated_import)

    def test_declare_class(self):
        test_generator = ModelGenerator("test", DataTest.TEST_FIELDS)
        expected_class_declaration = "class Test(Base):"
        test_class_declaration = test_generator.declare_class()

        self.assertEqual(expected_class_declaration, test_class_declaration)

    def test_set_table_name(self):
        test_generator = ModelGenerator("test", DataTest.TEST_FIELDS)
        expected_table_name_field = '__tablename__ = "test"'
        generated_field = test_generator.set_table_name()

        self.assertEqual(expected_table_name_field, generated_field)

    def test_build_attribute(self):
        test_generator = ModelGenerator("test", DataTest.TEST_FIELDS)
        expected_attribute = "id = Column(Integer, primary_key=True, index=True)"
        generated_attribute = test_generator.build_attribute(DataTest.TEST_FIELDS[0])

        self.assertEqual(expected_attribute, generated_attribute)

        # Remove test file
        os.remove(config["test"].MODEL_PACKAGE_PATH + "model_test.py")

    def test_run(self):
        test_generator = ModelGenerator("test", DataTest.TEST_FIELDS)
        test_generator.run()

        # Read generated test_schema
        generated_model_path = config["test"].MODEL_PACKAGE_PATH + "model_test.py"
        generated_model = open(generated_model_path, "r")

        # Read expected test_schema
        expected_file = open(config["test"].MODEL_PACKAGE_PATH + "expected_model.py", "r")

        self.assertEqual(generated_model.read(), expected_file.read())

        generated_model.close()
        expected_file.close()

        # Remove deleted file
        os.remove(generated_model_path)

    def test_generate_imports(self):
        pass

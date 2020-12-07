from unittest import TestCase
from test import setup
from crudgen.utils.config import config
from crudgen.code_generation.model import model_generator
from test.resources.data_test import DataTest
from test.utils.files import check_files_are_identical


class TestModelGenerator(TestCase):

    def test_get_types(self):
        """ Test get set of unique sql alchemy type """
        types = model_generator.get_types(DataTest.TEST_FIELDS)
        expected_types = ["Integer", "String"]

        self.assertEqual(types, expected_types)

    def test_build_sql_alchemy_import(self):
        """ Test sql alchemy type import generation """
        expected_import = "from sqlalchemy import Column, Boolean, Integer, String\n"
        test_types = ["Boolean, Integer, String"]
        generated_import = model_generator.build_sql_alchemy_import(test_types)

        self.assertEqual(expected_import, generated_import)

    def test_declare_class(self):
        """ Test write class desclaration in model.py file """
        expected_class_declaration = "\nclass Generated(Base):\n"
        test_class_declaration = model_generator.declare_class("generated")

        self.assertEqual(expected_class_declaration, test_class_declaration)

    def test_set_table_name(self):
        """ Test set table name """
        expected_table_name_field = '    __tablename__ = "generated"\n'
        generated_field = model_generator.set_table_name("generated")

        self.assertEqual(expected_table_name_field, generated_field)

    def test_build_attribute(self):
        """Test build model attribute for sql alchemy table description"""
        expected_attribute = "id = Column(Integer, primary_key=True, index=True)\n"
        generated_attribute = model_generator.build_attribute(DataTest.TEST_FIELDS[0])

        self.assertEqual(expected_attribute, generated_attribute)

    def test_run(self):
        """
        Test full model generation pipeline.
        model_test.py file should be generated in model package.
        """
        # Run model generation
        model_generator.run("generated", DataTest.TEST_FIELDS, "")

        # Files path to compare
        generated_model_path = config["test"].MODEL_PACKAGE_PATH + "generated_model.py"
        expected_file_path = config["test"].MODEL_PACKAGE_PATH + "expected_model.py"

        # Check files content
        is_identical = check_files_are_identical(generated_model_path, expected_file_path)
        self.assertTrue(is_identical)

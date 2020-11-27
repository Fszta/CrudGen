from unittest import TestCase
from test import setup
from crudgen.utils.config import config
from crudgen.database.db_init_generator import generate_db_init_file
from test.utils.files import check_files_are_identical


class TestDbInitGenerator(TestCase):
    def test_generate_db_init_file(self):
        """
        Test db init generation.
        db_init.py file should be created inside database package
        nb : content is generic
        """

        # Generate file & read it
        generate_db_init_file()
        generated_db_init_path = config["test"].DATABASE_PACKAGE_PATH + "db_init.py"

        # Read expected test_schema
        expected_file_path = config["test"].DATABASE_PACKAGE_PATH + "db_init.py"

        # Compare files content
        is_identical = check_files_are_identical(generated_db_init_path, expected_file_path)
        self.assertTrue(is_identical)

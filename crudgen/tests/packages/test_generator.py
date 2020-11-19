import unittest
import os
from crudgen.packages import generator


class TestPackageGenerator(unittest.TestCase):
    def test_create_package(self):
        test_package = "test"
        generator.create_package(test_package, True)

        # Check test_package has been created
        elem_in_dir = os.listdir()
        self.assertTrue(test_package in elem_in_dir)

        # Check test_package contains __init__.py
        files_in_test_package = os.listdir(test_package)
        self.assertTrue("__init__.py" in files_in_test_package)

    def test_create_api_structure(self):
        generator.create_api_structure()
        files_in_generated = os.listdir("generated_api")
        [self.assertTrue(package in files_in_generated) for package in generator.PACKAGES]

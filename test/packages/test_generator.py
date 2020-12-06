import unittest
import os
import shutil
from crudgen.code_generation.packages import generator


class TestPackageGenerator(unittest.TestCase):
    def test_create_package(self):
        """
        Test single package generation
        Should create a directory & __init__.py file
        inside
        """
        test_package = "test_package"
        generator.create_package(test_package, True, "")

        # Check test_package has been created
        elem_in_dir = os.listdir()
        self.assertTrue(test_package in elem_in_dir)

        # Check test_package contains __init__.py
        files_in_test_package = os.listdir(test_package)
        self.assertTrue("__init__.py" in files_in_test_package)
        shutil.rmtree("test_package")

    def test_create_api_structure(self):
        """
        Test full api structure generation
        Generated structure should contains all packages
        defined inside code_generation.PACKAGES
        """
        generator.create_api_structure("generated_api")
        files_in_generated = os.listdir("generated_api")
        [self.assertTrue(package in files_in_generated) for package in generator.PACKAGES]
        shutil.rmtree("generated_api")

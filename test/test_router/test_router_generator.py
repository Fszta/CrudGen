import os
from unittest import TestCase
from crudgen.utils.config import config
from test.test_router.router_generator_test import router_generator


class TestRouterGenerator(TestCase):
    def test_init(self):
        """ Test router generation init create router_table.py file inside router package """
        files_in_dir = os.listdir(config["test"].ROUTER_PACKAGE_PATH)
        self.assertTrue("router_generated.py" in files_in_dir)

    def test_generate_fastapi_import(self):
        """ Test fastapi import generation"""
        expected_import = "from fastapi import APIRouter, HTTPException, Depends" + "\n"
        generated_import = router_generator.generate_fastapi_import()
        self.assertEqual(expected_import, generated_import)

    def test_generate_sql_alchemy_import(self):
        """ Test sql_alchemy import generation"""
        expected_import = "from sqlalchemy.orm import Session" + "\n"
        generated_import = router_generator.generate_sql_alchemy_import()
        self.assertEqual(expected_import, generated_import)

    def test_generate_schema_import(self):
        """ Test generate pydantic schema import """
        expected_import = "from schema import schema_generated" + "\n"
        generated_import = router_generator.generate_schema_import("generated")
        self.assertEqual(expected_import, generated_import)

    def test_generate_controller_import(self):
        """ Test generate controler import """
        expected_import = "from controller import controller_generated" + "\n"
        generated_import = router_generator.generate_controller_import("generated")
        self.assertEqual(expected_import, generated_import)

    def test_database_import(self):
        """ Test database import generation """
        expected_import = "from database import get_db" + "\n"
        generated_import = router_generator.generate_database_import()
        self.assertEqual(expected_import, generated_import)

    def test_format_imports(self):
        """ Test global imports generation """
        expected_imports = "from fastapi import APIRouter, HTTPException, Depends" +\
                          "\n" + "from sqlalchemy.orm import Session" +\
                          "\n" + "from schema import schema_generated" +\
                          "\n" + "from controller import controller_generated" +\
                          "\n" + "from database import get_db" + "\n" + "\n" + "\n"

        generated_imports = router_generator.format_imports(
            "from fastapi import APIRouter, HTTPException, Depends" + "\n",
            "from sqlalchemy.orm import Session" + "\n",
            "from schema import schema_generated" + "\n",
            "from controller import controller_generated" + "\n",
            "from database import get_db" + "\n"
        )
        self.assertEqual(expected_imports, generated_imports)

    def test_generate_add_one(self):
        pass

    def test_generate_get_one(self):
        pass

    def test_generate_get_all(self):
        pass

    def test_generate_update_one(self):
        pass

    def test_generate_delete_one(self):
        pass

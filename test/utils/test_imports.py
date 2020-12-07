from unittest import TestCase
from crudgen.code_generation.imports import *


class TestImports(TestCase):
    def test_generate_fastapi_import(self):
        """ Test fastapi import generation"""
        expected_import = "from fastapi import APIRouter, HTTPException, Depends" + "\n"
        generated_import = fastapi_import()
        self.assertEqual(expected_import, generated_import)

    def test_generate_sql_alchemy_import(self):
        """ Test sql_alchemy import generation"""
        expected_import = "from sqlalchemy.orm import Session" + "\n"
        generated_import = sql_alchemy_session_import()
        self.assertEqual(expected_import, generated_import)

    def test_generate_schema_import(self):
        """ Test generate pydantic schema import """
        expected_import = "from schema import generated_schema" + "\n"
        generated_import = schema_import("generated")
        self.assertEqual(expected_import, generated_import)

    def test_generate_controller_import(self):
        """ Test generate controler import """
        expected_import = "from controller import generated_controller" + "\n"
        generated_import = controller_import("generated")
        self.assertEqual(expected_import, generated_import)

    def test_database_import(self):
        """ Test database import generation """
        expected_import = "from database import get_db" + "\n"
        generated_import = db_init_import()
        self.assertEqual(expected_import, generated_import)

    def test_format_imports(self):
        """ Test global imports generation """
        expected_imports = "from fastapi import APIRouter, HTTPException, Depends" + \
                           "\n" + "from typing import List" \
                                  "\n" + "from sqlalchemy.orm import Session" + \
                           "\n" + "from schema import generated_schema" + \
                           "\n" + "from controller import generated_controller" + \
                           "\n" + "from database import get_db" + "\n" + "\n"

        generated_imports = format_imports(
            "from fastapi import APIRouter, HTTPException, Depends" + "\n",
            "from typing import List" + "\n",
            "from sqlalchemy.orm import Session" + "\n",
            "from schema import generated_schema" + "\n",
            "from controller import generated_controller" + "\n",
            "from database import get_db" + "\n"
        )
        self.assertEqual(expected_imports, generated_imports)
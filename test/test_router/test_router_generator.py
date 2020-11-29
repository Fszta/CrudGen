import os
import test.setup
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
        expected_imports = "from fastapi import APIRouter, HTTPException, Depends" + \
                           "\n" + "from typing import List" \
                           "\n" + "from sqlalchemy.orm import Session" + \
                           "\n" + "from schema import schema_generated" + \
                           "\n" + "from controller import controller_generated" + \
                           "\n" + "from database import get_db" + "\n" + "\n" + "\n"

        generated_imports = router_generator.format_imports(
            "from fastapi import APIRouter, HTTPException, Depends" + "\n",
            "from typing import List" + "\n",
            "from sqlalchemy.orm import Session" + "\n",
            "from schema import schema_generated" + "\n",
            "from controller import controller_generated" + "\n",
            "from database import get_db" + "\n"
        )
        self.assertEqual(expected_imports, generated_imports)

    def test_router_declaration(self):
        expected = "router = APIRouter()" + "\n"
        self.assertEqual(expected, router_generator.router_declaration())

    def test_generate_router_decorator(self):
        expected_decorator = '@router.get("/generated/{id}", response_model=schema_generated.Generated,' \
                             ' tags=["generated"])'
        generated_decorator = router_generator.generate_router_decorator("get", "id", True)
        self.assertEqual(expected_decorator, generated_decorator)

        expected_decorator = '@router.get("/generated", response_model=List[schema_generated.Generated],' \
                             ' tags=["generated"])'
        generated_decorator = router_generator.generate_router_decorator("get", None, False)
        self.assertEqual(expected_decorator, generated_decorator)

    def test_generate_add_one(self):
        expected = "\n\n" + '@router.post("/generated", response_model=schema_generated.Generated, tags=["generated"])' + "\n" + \
                   "async def create_generated(generated: schema_generated.Generated, db: Session = Depends(get_db)):" + "\n" + \
                   "    return controller_generated.create_generated(db, generated)" + "\n"

        generated_add_one_method = router_generator.generate_add_one()
        self.assertEqual(expected, generated_add_one_method)

    def test_generate_get_one(self):
        expected = "\n\n" + '@router.get("/generated/{id}", response_model=schema_generated.Generated, tags=["generated"])' + "\n" + \
                   "async def get_generated(id: int, db: Session = Depends(get_db)):" + "\n" + \
                   "    db_generated = controller_generated.get_generated(db, id)" + "\n" + \
                   "    if db_generated is None:" + "\n" + \
                   '        raise HTTPException(status_code=404, detail="generated not found")' + "\n" + \
                   "    return db_generated" + "\n"
        generated_get_one = router_generator.generate_get_one("id", "int")
        self.assertEqual(expected, generated_get_one)

    def test_generate_get_all(self):
        expected = "\n\n" + '@router.get("/generated", response_model=List[schema_generated.Generated], tags=["generated"])' + "\n" + \
                   "async def get_all_generated(db: Session = Depends(get_db)):" + "\n" + \
                   "    all_db_generated = controller_generated.get_all_generated(db)" + "\n" + \
                   "    if all_db_generated is None:" + "\n" + \
                   '        raise HTTPException(status_code=404, detail="0 generated found, empty table")' + "\n" + \
                   "    return all_db_generated" + "\n"
        generated = router_generator.generate_get_all()

        self.assertEqual(expected, generated)

    def test_generate_update_one(self):
        expected = "\n\n" + '@router.put("/generated/{id}", tags=["generated"])' + "\n" + \
                   "async def update_generated(id: int, field_name: str, field_value: str, db: Session = " \
                   "Depends(get_db)):" + "\n" + \
                   "    try:" + "\n" + \
                   "        db_generated = controller_generated.update_generated(db, id, field_name, field_value)" + "\n" + \
                   "        if db_generated is None:" + "\n" + \
                   '            raise HTTPException(status_code=404, detail="generated not found")' + "\n" + \
                   "        return db_generated" + "\n" + \
                   "    except ValueError as error:" + "\n" + \
                   "        raise HTTPException(status_code=400, detail=str(error))" + "\n"

        generated = router_generator.generate_update_one("id", "int")
        self.maxDiff = None
        self.assertEqual(expected, generated)

    def test_generate_delete_one(self):
        expected = "\n\n" + '@router.delete("/generated/{id}", tags=["generated"])' + "\n" + \
                   "async def delete_generated(id: int, db: Session = Depends(get_db)):" + "\n" + \
                   "    controller_generated.delete_generated(db, id)" + "\n"

        generated = router_generator.generate_delete_one("id", "int")
        self.assertEqual(expected, generated)

    def test_run(self):
        router_generator.run()

import os
import test.setup
from unittest import TestCase
from crudgen.utils.config import config
from crudgen.code_generation.router.router_generator import *
from test.utils.files import check_files_are_identical
from crudgen.utils.logging import logger


class TestRouterGenerator(TestCase):
    def test_router_declaration(self):
        expected = "\nrouter = APIRouter()\n"
        self.assertEqual(expected, router_declaration())

    def test_generate_router_decorator(self):
        expected_decorator = '@router.get("/generated/{id}", response_model=generated_schema.Generated,' \
                             ' tags=["generated"])'
        generated_decorator = generate_router_decorator("generated", "get", "id", True)
        self.assertEqual(expected_decorator, generated_decorator)

        expected_decorator = '@router.get("/generated", response_model=List[generated_schema.Generated],' \
                             ' tags=["generated"])'
        generated_decorator = generate_router_decorator("generated", "get", None, False)
        self.assertEqual(expected_decorator, generated_decorator)

    def test_generate_add_one(self):
        expected = "\n\n" + '@router.post("/generated", response_model=generated_schema.Generated, tags=["generated"])' + "\n" + \
                   "async def create_generated(generated: generated_schema.Generated, db: Session = Depends(get_db)):" + "\n" + \
                   "    return generated_controller.create_generated(db, generated)" + "\n"

        generated_add_one_method = generate_add_one("generated")
        self.assertEqual(expected, generated_add_one_method)

    def test_generate_get_one(self):
        expected = "\n\n" + '@router.get("/generated/{id}", response_model=generated_schema.Generated, tags=["generated"])' + "\n" + \
                   "async def get_generated(id: int, db: Session = Depends(get_db)):" + "\n" + \
                   "    db_generated = generated_controller.get_generated(db, id)" + "\n" + \
                   "    if db_generated is None:" + "\n" + \
                   '        raise HTTPException(status_code=404, detail="generated not found")' + "\n" + \
                   "    return db_generated" + "\n"
        generated_get_one = generate_get_one("generated", "id", "int")
        self.assertEqual(expected, generated_get_one)

    def test_generate_get_all(self):
        expected = "\n\n" + '@router.get("/generated", response_model=List[generated_schema.Generated], tags=["generated"])' + "\n" + \
                   "async def get_all_generated(db: Session = Depends(get_db)):" + "\n" + \
                   "    all_db_generated = generated_controller.get_all_generated(db)" + "\n" + \
                   "    if all_db_generated is None:" + "\n" + \
                   '        raise HTTPException(status_code=404, detail="0 generated found, empty table")' + "\n" + \
                   "    return all_db_generated" + "\n"
        generated = generate_get_all("generated")

        self.assertEqual(expected, generated)

    def test_generate_update_one(self):
        expected = "\n\n" + '@router.put("/generated/{id}", tags=["generated"])' + "\n" + \
                   "async def update_generated(id: int, field_name: str, field_value: str, db: Session = " \
                   "Depends(get_db)):" + "\n" + \
                   "    try:" + "\n" + \
                   "        db_generated = generated_controller.update_generated(db, id, field_name, field_value)" + "\n" + \
                   "        if db_generated is None:" + "\n" + \
                   '            raise HTTPException(status_code=404, detail="generated not found")' + "\n" + \
                   "        return db_generated" + "\n" + \
                   "    except ValueError as error:" + "\n" + \
                   "        raise HTTPException(status_code=400, detail=str(error))" + "\n"

        generated = generate_update_one("generated", "id", "int")
        self.maxDiff = None
        self.assertEqual(expected, generated)

    def test_generate_delete_one(self):
        expected = "\n\n" + '@router.delete("/generated/{id}", tags=["generated"])' + "\n" + \
                   "async def delete_generated(id: int, db: Session = Depends(get_db)):" + "\n" + \
                   "    generated_controller.delete_generated(db, id)" + "\n"

        generated = generate_delete_one("generated", "id", "int")
        self.assertEqual(expected, generated)

    def test_run(self):
        """Test complete router file generation"""
        run("generated", "", "id", "int")

        # Files path to compare
        logger.info(os.getcwd())
        generated_router_path = config["test"].ROUTER_PACKAGE_PATH + "generated_router.py"
        expected_file_path = config["test"].ROUTER_PACKAGE_PATH + "expected_router.py"

        # Check files content
        is_identical = check_files_are_identical(generated_router_path, expected_file_path)
        self.assertTrue(is_identical)

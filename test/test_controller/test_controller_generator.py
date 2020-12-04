from unittest import TestCase
from test import setup
from crudgen.controller import controller_generator
from crudgen.utils.config import config
from test.resources.data_test import DataTest
from test.utils.files import check_files_are_identical


class TestControllerGenerator(TestCase):

    def test_generate_get_function(self):
        expected = "\n\ndef get_generated(db: Session, id: int):" + "\n" + \
                   "    return db.query(generated_model.Generated).filter(generated_model.Generated.id == id).first()"\
                   + "\n"
        generated = controller_generator.generate_get_function("generated", "id", "int")
        self.assertEqual(expected, generated)

    def test_generate_get_all_function(self):
        expected = "\n\ndef get_all_generated(db: Session):" + "\n" + \
                   "    return db.query(generated_model.Generated).all()" + "\n"
        generated = controller_generator.generate_get_all_function("generated")
        self.assertEqual(expected, generated)

    def test_generate_delete_function(self):
        expected = "\n\ndef delete_generated(db: Session, id):" + "\n" + \
                   "    to_delete = db.query(generated_model.Generated).filter(generated_model.Generated.id == id)" \
                   + "\n" + "    deleted = to_delete.delete()" + "\n" + \
                   "    if deleted == 0:" + "\n" + \
                   "        return None" + "\n" + \
                   "    else:" + "\n" + \
                   "        db.commit()" + "\n" + \
                   "        return True" + "\n"
        generated = controller_generator.generate_delete_function("generated", "id")

        self.assertEqual(expected, generated)

    def test_generate_create_function(self):
        expected = "\n\ndef create_generated(db: Session, generated: generated_schema.Generated):" + "\n" + \
                   "    db_generated = generated_model.Generated(" + "\n" + \
                   "        id=generated.id," + "\n" + \
                   "        name=generated.name," + "\n" + \
                   "        age=generated.age," + "\n" + \
                   "    )" + "\n" + \
                   "    db.add(db_generated)" + "\n" + \
                   "    db.commit()" + "\n" + \
                   "    db.refresh(db_generated)" + "\n" + \
                   "    return db_generated\n"
        generated = controller_generator.generate_create_function("generated", DataTest.TEST_FIELDS)

        self.assertEqual(expected, generated)

    def test_generate_update_function(self):
        expected = "\n\ndef update_generated(db: Session, id, new_value):" + "\n" + \
                   "    db_generated = db.query(generated_model.Generated).filter(generated_model.Generated.id == id)" \
                   ".first()" + "\n" + \
                   "    db_generated = new_value" + "\n" + \
                   "    db.commit()" + "\n" + \
                   "    db.refresh(db_generated)" + "\n" + \
                   "    return db_generated\n"

        generated = controller_generator.generate_update_function("generated", "id")
        self.maxDiff = None
        self.assertEqual(expected, generated)

    def test_run(self):
        """Test complete router file generation"""
        controller_generator.run("generated", "id", "int", DataTest.TEST_FIELDS)

        # Files path to compare
        generated_router_path = config["test"].CONTROLLER_PACKAGE_PATH + "generated_controller.py"
        expected_file_path = config["test"].CONTROLLER_PACKAGE_PATH + "expected_controller.py"

        # Check files content
        is_identical = check_files_are_identical(generated_router_path, expected_file_path)
        self.assertTrue(is_identical)


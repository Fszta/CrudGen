from unittest import TestCase
from crudgen.model.model_generator import *


test_fields_dict = {
        "table_1": [
            {
                "field_name": "name",
                "field_type": "string",
                "unique": False,
                "primary_key": False,
            },
            {
                "field_name": "age",
                "field_type": "integer",
                "unique": False,
                "primary_key": False,
            },
            {
                "field_name": "img_url",
                "field_type": "string",
                "unique": False,
                "primary_key": False,
            },
            {
                "field_name": "description",
                "field_type": "string",
                "unique": False,
                "primary_key": False,
            }
        ]
    }


class TestModelGenerator(TestCase):

    def test_init(self):
        test_generator = ModelGenerator("test", test_fields_dict)
        pass

    def test_run(self):
        pass

    def test_extract_unique_types(self):
        pass

    def test_generate_imports(self):
        pass

    def test_generate_key(self):
        pass


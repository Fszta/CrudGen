from unittest import TestCase
from input_parser.table_extract import *


class TestTableExtract(TestCase):
    def test_parse_file(self):
        test_file = "input_test.json"
        test_data = parse_json(test_file)

        expected_dict = {
            "table_1": [
                {
                    "field_name": "id",
                    "field_type": "integer",
                    "unique": True,
                    "primary_key": True
                },
                {
                    "field_name": "name",
                    "field_type": "string",
                    "unique": False,
                    "primary_key": False
                },
                {
                    "field_name": "age",
                    "field_type": "integer",
                    "unique": False,
                    "primary_key": False
                },
            ],
            "table_2": [
                {
                    "field_name": "id",
                    "field_type": "integer",
                    "unique": True,
                    "primary_key": True
                },
                {
                    "field_name": "contract_type",
                    "field_type": "string",
                    "unique": False,
                    "primary_key": False
                }
            ]
        }

        self.assertEqual(test_data, expected_dict)

    def test_extract_tables_name(self):
        test_file = "input_test.json"
        test_data = parse_json(test_file)
        tables_name = extract_tables_name(test_data)
        expected_tables = ["table_1", "table_2"]

        self.assertEqual(tables_name, expected_tables)
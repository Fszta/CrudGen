from unittest import TestCase
from crudgen.input_parser.table_extract import parse_json, map_dict_type, extract_tables_name
from crudgen.input_parser.type_mapper import TypeMapper
import os


class TestTableExtract(TestCase):
    def test_parse_file(self):
        test_file = os.getcwd() + "/test/test_input_parser/valid_input_test.json"
        test_data = parse_json(test_file)

        expected_dict = {
            "table_1": {
                "key_identifier": {
                    "name": "name",
                    "type": "string"
                },
                "fields": [
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
                ]},
            "table_2": {
                "key_identifier": {
                    "name": "id",
                    "type": "integer"
                },
                "fields": [
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
                ]}
        }

        self.assertEqual(test_data, expected_dict)

    def test_extract_tables_name(self):
        test_file = os.getcwd() + "/test/test_input_parser/valid_input_test.json"
        test_data = parse_json(test_file)
        tables_name = extract_tables_name(test_data)
        expected_tables = ["table_1", "table_2"]

        self.assertEqual(tables_name, expected_tables)

    def test_map_dict_type_valid_input(self):
        test_file = os.getcwd() + "/test/test_input_parser/valid_input_test.json"
        test_data = parse_json(test_file)

        mapped_data_type = map_dict_type(test_data)
        expected_mapped_data = {
            "table_1": {
                "key_identifier": {
                    "name": "name",
                    "type": TypeMapper(pydantic_type_name='str', sql_alchemy_type_name='String')
                },
                "fields": [
                    {
                        "field_name": "id",
                        "field_type": TypeMapper(pydantic_type_name='int', sql_alchemy_type_name='Integer'),
                        "unique": True,
                        "primary_key": True
                    },
                    {
                        "field_name": "name",
                        "field_type": TypeMapper(pydantic_type_name='str', sql_alchemy_type_name='String'),
                        "unique": False,
                        "primary_key": False
                    },
                    {
                        "field_name": "age",
                        "field_type": TypeMapper(pydantic_type_name='int', sql_alchemy_type_name='Integer'),
                        "unique": False,
                        "primary_key": False
                    },
                ]},

            "table_2": {
                "key_identifier": {
                    "name": "id",
                    "type": TypeMapper(pydantic_type_name='int', sql_alchemy_type_name='Integer')
                },
                "fields": [
                    {
                        "field_name": "id",
                        "field_type": TypeMapper(pydantic_type_name='int', sql_alchemy_type_name='Integer'),
                        "unique": True,
                        "primary_key": True
                    },
                    {
                        "field_name": "contract_type",
                        "field_type": TypeMapper(pydantic_type_name='str', sql_alchemy_type_name='String'),
                        "unique": False,
                        "primary_key": False
                    }
                ]}
        }
        self.maxDiff = None
        self.assertEqual(expected_mapped_data, mapped_data_type)

    def test_map_dict_not_valid_input(self):
        test_file = os.getcwd() + "/test/test_input_parser/not_valid_input_test.json"
        test_data = parse_json(test_file)

        with self.assertRaises(SystemExit):
            mapped_data_type = map_dict_type(test_data)

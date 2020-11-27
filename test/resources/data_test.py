from crudgen.input_parser.type_mapper import TypeMapper


class DataTest:
    TEST_FIELDS = [
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
        ]
from schema.schema_generator import SchemaGenerator

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    test_fields = {
        "schema_field": [
            {
                "field_name": "name",
                "field_type": "str"
            },
            {
                "field_name": "age",
                "field_type": "int"
            },
            {
                "field_name": "img_url",
                "field_type": "str"
            },
            {
                "field_name": "description",
                "field_type": "str"
            }
        ]
    }
    from packages import generator
    generator.create_api_structure()
    test = SchemaGenerator("tests", test_fields)
    test.run()

from dataclasses import dataclass


@dataclass
class TypeMapper:
    pydantic_type_name: str
    sql_alchemy_type_name: str


TYPE_MAPPING = {
    "string": TypeMapper("str", "String"),
    "integer": TypeMapper("int", "Integer"),
    "boolean": TypeMapper("bool", "Boolean")
}


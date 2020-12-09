from crudgen.utils.config import config, CONFIG_ENV
from crudgen.code_generation.indentation import Indentator
from crudgen.code_generation.check import is_generated
from crudgen.code_generation.code_formatting import custom_import_declaration, class_declare
from crudgen.code_generation.imports import format_imports, db_base_import


@is_generated(package_name="model")
def run(table_name: str, fields: dict, output_path: str):
    """
    Run model generation base on input field which
    corresponds to a table description.
    The output is a model_name.py file inside
    model package
    """

    filename = f"{table_name}_model.py"
    file_model = open(output_path + config[CONFIG_ENV].MODEL_PACKAGE_PATH + filename, "a")

    sql_alchemy_types = get_types(fields)
    imports = format_imports(build_sql_alchemy_import(sql_alchemy_types), db_base_import(False))
    model_attributes = build_all_attributes(fields)
    content = imports + declare_class(table_name) + set_table_name(table_name) + model_attributes

    file_model.write(content)
    file_model.close()

    return filename


def get_types(fields: dict):
    """
    Get set of unique type needed to be imported
    :return: set of sql alchemy type
    """
    types = [field["field_type"].sql_alchemy_type_name for field in fields]
    unique_types = list(set(types))
    unique_types.sort()

    return unique_types


@custom_import_declaration
def build_sql_alchemy_import(types: list):
    """
    Build sql alchemy types import statement
    :param types: set of sql alchemy types
    :return: import statement string
    """
    import_statement = "from sqlalchemy import Column"
    for sql_alchemy_type in types:
        import_statement += ", " + sql_alchemy_type

    return import_statement


@class_declare
def declare_class(table_name: str):
    """
    Generate class declaration line
    :return: class declaration
    """
    class_name = table_name.capitalize()
    class_declaration = f"class {class_name}(Base):"

    return class_declaration


@custom_import_declaration
def set_table_name(table_name: str):
    """
    Set table name field,
    will be used as table name by sqlalchemy
    :return: tablename field
    """
    set_table = f'__tablename__ = "{table_name}"'

    return Indentator.IND_LEVEL_1 + set_table


@custom_import_declaration
def build_attribute(table_field):
    """
    Build model attributes, generates :
    - field name
    - if field is primary key
    - sql alchemy type
    - if field is unique
    :param table_field: table field description
    """
    field_name = table_field["field_name"]
    field_type = table_field["field_type"].sql_alchemy_type_name

    if table_field["primary_key"] is True:
        return f"{field_name} = Column({field_type}, primary_key=True, index=True)"
    else:
        return f"{field_name} = Column({field_type}, unique={table_field['unique']})"


def build_all_attributes(fields: dict):
    return "".join([Indentator.IND_LEVEL_1 + build_attribute(field) for field in fields])

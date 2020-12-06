from crudgen.utils.config import config, CONFIG_ENV
from crudgen.code_generation.code_formatting import function_declaration
from crudgen.code_generation.check import is_generated
from crudgen.code_generation.indentation import Indentator
from crudgen.code_generation.imports import *


@is_generated(package_name="router")
def run(table_name: str, output_path: str, key_name: str, key_type: str):
    """
    Crud router code_generation, it creates a router_name.py file inside router package
    Following endpoints are implemented:
    - add one : add one element in database.
    - get one : get one element from database, based on a field.
    - get all : get all elements from database.
    - update one : update one element from database, based on a field
    - deleted_one : delete one element from database, based on a field
    :param table_name: name of the table
    :param output_path: path of the output directory
    :param key_name: name of the key use to identify sample
    :param key_type: type of the key
    :return: boolean, generated filename
    """

    filename = f"{table_name}_router.py"
    file_router = open(output_path + config[CONFIG_ENV].ROUTER_PACKAGE_PATH + filename, "a")

    imports = format_imports(
        fastapi_import(),
        typing_import(),
        sql_alchemy_import(),
        schema_import(table_name),
        controller_import(table_name),
        database_import()
    )

    create_method = generate_add_one(table_name)
    get_one_method = generate_get_one(table_name,key_name, key_type)
    get_all_method = generate_get_all(table_name)
    update_method = generate_update_one(table_name, key_name, key_type)
    delete_method = generate_delete_one(table_name, key_name, key_type)

    router_file_content = imports + router_declaration() + create_method + \
                          get_one_method + get_all_method + update_method + delete_method

    file_router.write(router_file_content)
    file_router.close()

    return filename


def router_declaration():
    """Init router declaration"""
    return "\nrouter = APIRouter()" + "\n"


def generate_router_decorator(table_name: str, http_method: str, key: str, single_return: bool):
    """
    Generate routing function decorator which defines route, parameters and return model.
    :param table_name: name of the table
    :param http_method: get / post / create / update
    :param key: key to of the element in table, could be None for get_all method
    :param single_return: True if route return single element, otherwise False
    :return: string containing route_decorator
    """
    if key is None:
        route = "/" + table_name
    else:
        route = "/" + table_name + "/{" + key + "}"
    if single_return is True:
        response_model = table_name + "_schema" + "." + table_name.capitalize()
    elif single_return is False:
        response_model = "List[" + table_name + "_schema" + "." + table_name.capitalize() + "]"
    tag = f'["{table_name}"]'

    if single_return is None:
        router_decorator = f'@router.{http_method}("{route}", tags={tag})'
    else:
        router_decorator = f'@router.{http_method}("{route}", response_model={response_model}, tags={tag})'

    return router_decorator


@function_declaration
def generate_add_one(table_name: str):
    """ Generate create route """
    decorator = generate_router_decorator(table_name, "post", None, True) + "\n"
    function_definition = "async def create_" + table_name + "(" + table_name + ": " + \
                          table_name + "_schema" + "." + table_name.capitalize() + ", db: Session = " \
                                                                                   "Depends(get_db)):" + "\n"

    content = Indentator.IND_LEVEL_1 + "return " + table_name + "_controller" + \
              ".create_" + table_name + f"(db, {table_name})"

    add_one_method = decorator + function_definition + content

    return add_one_method


@function_declaration
def generate_get_one(table_name: str, key: str, key_type: str):
    decorator = generate_router_decorator(table_name, "get", key, True) + "\n"
    function_definition = "async def get_{}({}: {}, db: Session = Depends(get_db)):".format(
        table_name,
        key,
        key_type
    )
    content = Indentator.IND_LEVEL_1 + f"db_{table_name} = {table_name}_controller.get_{table_name}(db, {key})\n" +  \
              Indentator.IND_LEVEL_1 + f"if db_{table_name} is None:" + "\n" + \
              Indentator.IND_LEVEL_2 + f'raise HTTPException(status_code=404, detail="{table_name} not found")\n' + \
              Indentator.IND_LEVEL_1 + "return db_{}".format(table_name)

    get_one_method = decorator + function_definition + "\n" + content
    return get_one_method


@function_declaration
def generate_get_all(table_name: str):
    decorator = generate_router_decorator(table_name, "get", None, False) + "\n"

    function_definition = f"async def get_all_{table_name}(db: Session = Depends(get_db)):"

    content = Indentator.IND_LEVEL_1 + f"all_db_{table_name} = {table_name}_controller.get_all_{table_name}(db)\n"  + \
              Indentator.IND_LEVEL_1 + f"if all_db_{table_name} is None:" + "\n" + \
              Indentator.IND_LEVEL_2 + f'raise HTTPException(status_code=404,' \
                                       f' detail="0 {table_name} found, empty table")\n' + \
              Indentator.IND_LEVEL_1 + f"return all_db_{table_name}"

    get_all_method = decorator + function_definition + "\n" + content
    return get_all_method


@function_declaration
def generate_update_one(table_name: str, key: str, key_type: str):
    decorator = generate_router_decorator(table_name, "put", key, None) + "\n"
    function_definition = f"async def update_{table_name}({key}: {key_type}, field_name: str, field_value: str," \
                          " db: Session = Depends(get_db)):"
    content = Indentator.IND_LEVEL_1 + "try:" + "\n" + \
              Indentator.IND_LEVEL_2 + f"db_{table_name} = {table_name}_controller.update_{table_name}(db, {key}," \
                                       " field_name, field_value)" + "\n" + \
              Indentator.IND_LEVEL_2 + f"if db_{table_name} is None:" + "\n" + \
              Indentator.IND_LEVEL_3 + f'raise HTTPException(status_code=404, detail="{table_name} not found")\n' + \
              Indentator.IND_LEVEL_2 + f"return db_{table_name}" + "\n" + \
              Indentator.IND_LEVEL_1 + "except ValueError as error:" + "\n" + \
              Indentator.IND_LEVEL_2 + "raise HTTPException(status_code=400, detail=str(error))"

    update_method = decorator + function_definition + "\n" + content

    return update_method


@function_declaration
def generate_delete_one(table_name: str, key: str, key_type: str):
    decorator = generate_router_decorator(table_name, "delete", key, None) + "\n"
    function_definition = f"async def delete_{table_name}({key}: {key_type}, db: Session = Depends(get_db)):"
    content = Indentator.IND_LEVEL_1 + f"{table_name}_controller.delete_{table_name}(db, {key})"

    delete_one_method = decorator + function_definition + "\n" + content

    return delete_one_method

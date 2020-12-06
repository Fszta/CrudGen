from crudgen.utils.config import config, CONFIG_ENV
from crudgen.code_generation.code_formatting import generic_import_declaration, imports_declaration, function_declaration
from crudgen.code_generation.check import is_generated
from crudgen.code_generation.indentation import Indentator
from crudgen.utils.generator import Generator


class RouterGenerator(Generator):
    """
    Crud router code_generation, it creates a router_name.py file inside router package
    Following endpoints are implemented:
    - add one : add one element in database.
    - get one : get one element from database, based on a field.
    - get all : get all elements from database.
    - update one : update one element from database, based on a field
    - deleted_one : delete one element from database, based on a field
    """

    def __init__(self, table_name: str, key_name: str, key_type: str, output_path: str):
        self.table_name = table_name
        self.key_name = key_name
        self.key_type = key_type
        self.filename = "{}_router.py".format(table_name)
        self.file_open = open(output_path + config[CONFIG_ENV].ROUTER_PACKAGE_PATH + self.filename, "a")

    @staticmethod
    @generic_import_declaration
    def generate_fastapi_import():
        """ Generate fastApi import"""
        return "from fastapi import APIRouter, HTTPException, Depends"

    @staticmethod
    @generic_import_declaration
    def typing_import():
        return "from typing import List"

    @staticmethod
    @generic_import_declaration
    def generate_database_import():
        """ Generate init database import statement"""
        return "from database import get_db"

    @staticmethod
    @imports_declaration
    def format_imports(fastapi, typing, sql_alchemy, schema, controller, database):
        """ Generate all import statement of router"""
        global_import = fastapi + typing + sql_alchemy + schema + controller + database
        return global_import

    @staticmethod
    def router_declaration():
        """Init router declaration"""
        return "\nrouter = APIRouter()" + "\n"

    def generate_router_decorator(self, http_method: str, key: str, single_return: bool):
        """
        Generate routing function decorator which defines route, parameters and return model.
        :param http_method: get / post / create / update
        :param key: key to of the element in table, could be None for get_all method
        :param single_return: True if route return single element, otherwise False
        :return: string containing route_decorator
        """
        if key is None:
            route = "/" + self.table_name
        else:
            route = "/" + self.table_name + "/{" + key + "}"

        if single_return is True:
            response_model = self.table_name + "_schema" + "." + self.table_name.capitalize()
        elif single_return is False:
            response_model = "List[" + self.table_name + "_schema" + "." + self.table_name.capitalize() + "]"
        tag = '["{}"]'.format(self.table_name)

        if single_return is None:
            router_decorator = '@router.{}("{}", tags={})'.format(http_method, route, tag)
        else:
            router_decorator = '@router.{}("{}", response_model={}, tags={})'.format(http_method,
                                                                                     route,
                                                                                     response_model,
                                                                                     tag)

        return router_decorator

    @function_declaration
    def generate_add_one(self):
        """ Generate create route """
        decorator = self.generate_router_decorator("post", None, True) + "\n"
        function_definition = "async def create_" + self.table_name + "(" + self.table_name + ": " + \
                              self.table_name+"_schema"+"."+self.table_name.capitalize() + ", db: Session = " \
                                                                                           "Depends(get_db)):" + "\n"

        content = Indentator.IND_LEVEL_1 + "return " + self.table_name + "_controller" +\
                  ".create_" + self.table_name + "(db, {})".format(self.table_name)

        add_one_method = decorator + function_definition + content

        return add_one_method

    @function_declaration
    def generate_get_one(self, key: str, key_type: str):
        decorator = self.generate_router_decorator("get", key, True) + "\n"
        function_definition = "async def get_{}({}: {}, db: Session = Depends(get_db)):".format(
            self.table_name,
            key,
            key_type
        )
        content = Indentator.IND_LEVEL_1 + "db_{} = {}_controller.get_{}(db, {})".format(self.table_name,
                                                                                         self.table_name,
                                                                                         self.table_name, key) + "\n" +\
                  Indentator.IND_LEVEL_1 + "if db_{} is None:".format(self.table_name) + "\n" + \
                  Indentator.IND_LEVEL_2 + 'raise HTTPException(status_code=404, detail="{} not found")'.format(self.table_name) + "\n" + \
                  Indentator.IND_LEVEL_1 + "return db_{}".format(self.table_name)

        get_one_method = decorator + function_definition + "\n" + content
        return get_one_method

    @function_declaration
    def generate_get_all(self):
        decorator = self.generate_router_decorator("get", None, False) + "\n"

        function_definition = "async def get_all_{}(db: Session = Depends(get_db)):".format(self.table_name)

        content = Indentator.IND_LEVEL_1 + "all_db_{} = {}_controller.get_all_{}(db)"\
            .format(self.table_name, self.table_name, self.table_name) + "\n" +\
                  Indentator.IND_LEVEL_1 + "if all_db_{} is None:".format(self.table_name) + "\n" + \
                  Indentator.IND_LEVEL_2 + 'raise HTTPException(status_code=404, detail="0 {} found, empty table")'\
                      .format(self.table_name) + "\n" + \
                  Indentator.IND_LEVEL_1 + "return all_db_{}".format(self.table_name)

        get_all_method = decorator + function_definition + "\n" + content
        return get_all_method

    @function_declaration
    def generate_update_one(self, key, key_type):
        decorator = self.generate_router_decorator("put", key, None) + "\n"
        function_definition = "async def update_{}({}: {}, field_name: str, field_value: str," \
                              " db: Session = Depends(get_db)):".format(self.table_name, key, key_type)
        content = Indentator.IND_LEVEL_1 + "try:" + "\n" + \
                  Indentator.IND_LEVEL_2 + "db_{} = {}_controller.update_{}(db, {}," \
                                           " field_name, field_value)".format(self.table_name,
                                                                      self.table_name, self.table_name, key) + "\n" + \
                  Indentator.IND_LEVEL_2 + "if db_{} is None:".format(self.table_name) + "\n" + \
                  Indentator.IND_LEVEL_3 + 'raise HTTPException(status_code=404, detail="{} not found")'\
                      .format(self.table_name) + "\n" + \
                  Indentator.IND_LEVEL_2 + "return db_{}".format(self.table_name).format(self.table_name) + "\n" + \
                  Indentator.IND_LEVEL_1 + "except ValueError as error:" + "\n" + \
                  Indentator.IND_LEVEL_2 + "raise HTTPException(status_code=400, detail=str(error))"

        update_method = decorator + function_definition + "\n" + content

        return update_method

    @function_declaration
    def generate_delete_one(self, key: str, key_type: str):
        decorator = self.generate_router_decorator("delete", key, None) + "\n"
        function_definition = "async def delete_{}({}: {}, db: Session = Depends(get_db)):".format(
            self.table_name,
            key,
            key_type
        )
        content = Indentator.IND_LEVEL_1 + "{}_controller.delete_{}(db, {})".format(self.table_name, self.table_name, key)

        delete_one_method = decorator + function_definition + "\n" + content

        return delete_one_method

    @is_generated(package_name="router")
    def run(self):
        fastapi_import = self.generate_fastapi_import()
        typing_import = self.typing_import()
        schema_import = self.generate_schema_import(self.table_name)
        sql_alchemy_import = self.generate_sql_alchemy_import()
        database_import = self.generate_database_import()
        controller_import = self.generate_controller_import(self.table_name)
        all_imports = self.format_imports(fastapi_import,
                                          typing_import,
                                          sql_alchemy_import,
                                          schema_import,
                                          controller_import,
                                          database_import
                                          )

        create_method = self.generate_add_one()
        get_one_method = self.generate_get_one(self.key_name, self.key_type)
        get_all_method = self.generate_get_all()
        update_method = self.generate_update_one(self.key_name, self.key_type)
        delete_method = self.generate_delete_one(self.key_name, self.key_type)
        router_file_content = all_imports + self.router_declaration() + create_method +\
                              get_one_method + get_all_method + update_method + delete_method
        self.file_open.write(router_file_content)
        self.file_open.close()

        return self.filename

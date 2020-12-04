from crudgen.utils.code_formatting import function_declaration, imports_declaration
from crudgen.utils.generator import Generator
from crudgen.utils.indentation import Indentator
from crudgen.utils.config import config, CONFIG_ENV


class ControllerGenerator(Generator):
    def __init__(self, table_name, key_identifier: str, key_type, table_fields: dict):
        self.table_name = table_name
        self.key = key_identifier
        self.key_type = key_type
        self.table_fields = table_fields
        self.model_class = self.table_name.capitalize()
        self.filename = "controller_{}.py".format(table_name)
        self.file_open = open(config[CONFIG_ENV].CONTROLLER_PACKAGE_PATH + self.filename, "a")

    @imports_declaration
    def format_imports(self):
        """
        Generate & format controller imports.
        :return: formated imports
        """
        imports = self.generate_sql_alchemy_import() + self.generate_schema_import(self.table_name) +\
                  self.generate_controller_import(self.table_name)

        return imports

    @function_declaration
    def generate_get_method(self):
        """
        Generate get one method
        :return:
        """

        # Build function declaration
        function_definition = f"def get_{self.table_name}(db: Session, {self.key}: {self.key_type}):"

        # Build get query
        return_statement = Indentator.IND_LEVEL_1 + f"db.query({self.table_name}_model.{self.model_class}).filter(" \
                           f"{self.table_name}_model.{self.model_class}.{self.key} == {self.key}).first()"

        return function_definition + "\n" + return_statement

    @function_declaration
    def generate_get_all_method(self):
        """
        Generate get all method
        :return:
        """
        function_definition = f"def get_all_{self.table_name}(db: Session):"
        return_statement = Indentator.IND_LEVEL_1 + f"return db.query({self.table_name}_model.{self.model_class}).all()"

        return function_definition + "\n" + return_statement

    @function_declaration
    def generate_delete_method(self):
        function_definition = f"def delete_{self.table_name}(db: Session, {self.key}):"
        content = Indentator.IND_LEVEL_1 + f"to_delete = db.query({self.table_name}_model.{self.model_class}).filter(" \
                                           f"{self.table_name}_model.{self.model_class}.{self.key} == {self.key})" + \
                  "\n" + Indentator.IND_LEVEL_1 + "deleted = to_delete.delete()" + "\n" + \
                  Indentator.IND_LEVEL_1 + "if deleted == 0:" + "\n" + \
                  Indentator.IND_LEVEL_2 + "return None" + "\n" + \
                  Indentator.IND_LEVEL_1 + "else:" + "\n" + \
                  Indentator.IND_LEVEL_2 + "db.commit()" + "\n" + \
                  Indentator.IND_LEVEL_2 + "return True"

        return function_definition + "\n" + content

    def generate_update_one_method(self):
        pass

    def generate_create_method(self):
        function_definition = f"def create_{self.table_name}(db: Session, {self.table_name}.{self.model_class}):"
        content = Indentator.IND_LEVEL_1 + f"{self.table_name}_model.{self.model_class}" + "\n"

        for field in self.fields:
            field["field_type"].sql_alchemy_type_name
            field["field_name"]


            """Create a new user in database"""
            db_user = user_model.User(
                name=user.name,
                age=user.age,
                job=user.job,
                description=user.description,
                img_url=user.img_url,
                score=user.score,
                user_firebase_id=user.user_firebase_id
            )

            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user

        pass

    def run(self):
        imports = self.format_imports()
        get_method = self.generate_get_method()
        get_all_method = self.generate_get_all_method()
        delete_method = self.generate_delete_method()

        file_content = imports + get_method + get_all_method + delete_method

        self.file_open.write(file_content)
        self.file_open.close()


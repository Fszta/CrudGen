from crudgen.utils.config import config, CONFIG_ENV
from crudgen.utils.indentation import Indentator


class ModelGenerator:
    """
    SQL Alchemy test_model generator
    name will be used to create test_model file as :
    model_name.py & also to name the corresponding
    table in database
    """

    def __init__(self, name, fields: dict):
        self.name = name
        self.fields = fields
        self.filename = "model_{}.py".format(name)
        self.file_open = open(config[CONFIG_ENV].MODEL_PACKAGE_PATH + self.filename, "a")

    def get_types(self):
        """
        Get set of unique type needed to be imported
        :return: set of sql alchemy type
        """
        types = [field["field_type"].sql_alchemy_type_name for field in self.fields]
        unique_types = set(types)

        return unique_types

    @staticmethod
    def build_sql_alchemy_import(types: set):
        """
        Build sql alchemy types import statement
        :param types: set of sql alchemy types
        :return: import statement string
        """
        import_statement = "from sqlalchemy import Column"
        for sql_alchemy_type in types:
            import_statement += ", " + sql_alchemy_type

        return import_statement

    def declare_class(self):
        """
        Generate class declaration line
        :return: class declaration
        """
        class_name = self.name.capitalize()
        class_declaration = "class " + class_name + "(Base):"

        return class_declaration

    def set_table_name(self):
        """
        Set table name field,
        will be used as table name by sqlalchemy
        :return: tablename field
        """
        set_table = '__tablename__ = "{}"'.format(self.name)

        return set_table

    @staticmethod
    def build_attribute(table_field):
        if table_field["primary_key"] is True:
            return "{} = Column({}, primary_key=True, index=True)"\
                .format(table_field["field_name"], table_field["field_type"].sql_alchemy_type_name)
        else:
            return "{} = Column({}, unique={})".format(table_field["field_name"],
                                                       table_field["field_type"].sql_alchemy_type_name,
                                                       table_field["unique"])

    def jump_lines(self, number_of_jump):
        """
        Jump lines in file
        :param number_of_jump: number of line to jump, 0 = return to line
        """
        for i in range(0, number_of_jump):
            self.file_open.write("\n")

    def run(self):
        sql_alchemy_types = self.get_types()
        self.file_open.write(self.build_sql_alchemy_import(sql_alchemy_types))
        self.jump_lines(3)

        self.file_open.write(self.declare_class())
        self.jump_lines(1)

        for field in self.fields:
            self.file_open.write(Indentator.IND_LEVEL_1 + self.build_attribute(field))
            self.jump_lines(1)

    def generate_imports(self):
        pass

from crudgen.utils.config import config, CONFIG_ENV
from crudgen.code_generation.indentation import Indentator
from crudgen.code_generation.check import is_generated


class ModelGenerator:
    """
    SQL Alchemy model code_generation.
    Name will be used to create model file as :
    model_name.py & also to name the corresponding
    table in database
    """

    def __init__(self, name, fields: dict, output_path: str):
        self.name = name
        self.fields = fields
        self.filename = "{}_model.py".format(name)
        self.file_open = open(output_path + config[CONFIG_ENV].MODEL_PACKAGE_PATH + self.filename, "a")

    def get_types(self):
        """
        Get set of unique type needed to be imported
        :return: set of sql alchemy type
        """
        types = [field["field_type"].sql_alchemy_type_name for field in self.fields]
        unique_types = list(set(types))
        unique_types.sort()

        return unique_types

    @staticmethod
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

    @staticmethod
    def write_import_statements(sql_alchemy_import: str):
        """ Write model class imports """
        imports = sql_alchemy_import + "\n" + "from database.db_init import Base"
        return imports

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

        return Indentator.IND_LEVEL_1 + set_table

    @staticmethod
    def build_attribute(table_field):
        """
        Build model attributes, generates :
        - field name
        - if field is primary key
        - sql alchemy type
        - if field is unique
        :param table_field: table field description
        """
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

    @is_generated(package_name="model")
    def run(self):
        """
        Run model generation base on input field which
        corresponds to a table description.
        The output is a model_name.py file inside
        model package
        """

        # Extract unique sql alchemy types
        sql_alchemy_types = self.get_types()

        # Write import statement
        self.file_open.write(self.write_import_statements(self.build_sql_alchemy_import(sql_alchemy_types)))
        self.jump_lines(3)

        # Write class declaration
        self.file_open.write(self.declare_class())
        self.jump_lines(1)

        # Set table name
        self.file_open.write(self.set_table_name())
        self.jump_lines(1)

        # Write class content
        for field in self.fields:
            self.file_open.write(Indentator.IND_LEVEL_1 + self.build_attribute(field))
            self.jump_lines(1)

        # Close generated file
        self.file_open.close()

        return self.filename

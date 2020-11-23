
class ModelGenerator:
    """
    SQL Alchemy test_model generator
    name will be used to create test_model file as :
    model_name.py & also to name the corresponding
    table in database
    """
    def __init__(self, name, fields_dict: dict):
        self.name = name
        self.fields_dict = fields_dict

    def run(self):
        pass

    def generate_import(self):
        pass

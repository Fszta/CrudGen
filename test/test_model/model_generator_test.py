from test import setup
from crudgen.model.model_generator import ModelGenerator
from test.resources.data_test import DataTest


test_generator = ModelGenerator("generated", DataTest.TEST_FIELDS)

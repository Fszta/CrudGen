import os

CONFIG_ENV = os.getenv("CONFIG")

if CONFIG_ENV is None:
    CONFIG_ENV = "dev"


class Config:
    VERSION = "v0.1-alpha"
    GENERATED_API_PATH = "generated_api"
    SCHEMA_PACKAGE_PATH = GENERATED_API_PATH + "/schema/"
    MODEL_PACKAGE_PATH = GENERATED_API_PATH + "/model/"


class DevConfig(Config):
    TYPE = ""


class TestConfig(Config):
    CONFIG_ENV = "test"
    GENERATED_API_PATH = "generated_api"
    SCHEMA_PACKAGE_PATH = "test/test_schema/"
    MODEL_PACKAGE_PATH = "test/test_model/"
    DATA_TEST_PATH = "test/resources/"


config = dict(
    dev=DevConfig,
    test=TestConfig
)

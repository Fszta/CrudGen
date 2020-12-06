import os

CONFIG_ENV = os.getenv("CONFIG")

if CONFIG_ENV is None:
    CONFIG_ENV = "dev"


class Config:
    VERSION = "v0.1-alpha"


class DevConfig(Config):
    GENERATED_API_PATH = "generated_api"
    SCHEMA_PACKAGE_PATH = "/schema/"
    MODEL_PACKAGE_PATH = "/model/"
    DATABASE_PACKAGE_PATH = "/database/"
    ROUTER_PACKAGE_PATH = "/router/"
    CONTROLLER_PACKAGE_PATH = "/controller/"


class TestConfig(Config):
    CONFIG_ENV = "test"
    GENERATED_API_PATH = "generated_api"
    SCHEMA_PACKAGE_PATH = "test/schema/"
    MODEL_PACKAGE_PATH = "test/model/"
    DATABASE_PACKAGE_PATH = "test/database/"
    ROUTER_PACKAGE_PATH = "test/router/"
    CONTROLLER_PACKAGE_PATH = "test/controller/"
    DATA_TEST_PATH = "test/resources/"


config = dict(
    dev=DevConfig,
    test=TestConfig
)

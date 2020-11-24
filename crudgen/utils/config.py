import os

CONFIG_ENV = os.getenv("CONFIG")

if CONFIG_ENV is None:
    CONFIG_ENV = "dev"


class Config:
    GENERATED_API_PATH = "generated_api"
    SCHEMA_PACKAGE_PATH = GENERATED_API_PATH + "/schema/"
    VERSION = "v0.1-alpha"


class DevConfig(Config):
    TYPE = ""


class TestConfig(Config):
    CONFIG_ENV = "test"
    GENERATED_API_PATH = "generated_api"
    SCHEMA_PACKAGE_PATH = "test/test_schema/"


config = dict(
    dev=DevConfig,
    test=TestConfig
)

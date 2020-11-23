import os

CONFIG_ENV = os.getenv("CONFIG")

if CONFIG_ENV is None:
    CONFIG_ENV = "test"


class Config:
    GENERATED_API_PATH = "generated_api"
    SCHEMA_PACKAGE_PATH = GENERATED_API_PATH + "/test_schema/"


class DevConfig(Config):
    TYPE = ""


class TestConfig(Config):
    CONFIG_ENV = "test"
    GENERATED_API_PATH = "generated_api"
    SCHEMA_PACKAGE_PATH = ""


config = dict(
    dev=DevConfig,
    test=TestConfig
)

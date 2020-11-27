import inspect
from crudgen.database import db_init
from crudgen.utils.config import config, CONFIG_ENV


def generate_db_init_file():
    """
    Generate db_init file inside database package
    Its content is generic except DB_URL which needs to be set as environment variable.
    In case env variable is unset, default value is sqllite database url
    """
    # Get db_init file content as string
    db_init_content = inspect.getsource(db_init)

    # Write content to db_init file
    file_open = open(config[CONFIG_ENV].DATABASE_PACKAGE_PATH + "db_init.py", "a")
    file_open.write(db_init_content)

from crudgen.utils.logging import logger
from crudgen.code_generation.indentation import Indentator
from crudgen.code_generation.code_formatting import function_declaration
from crudgen.code_generation.check import is_generated
from crudgen.code_generation.imports import uvicorn_import, fastapi_core_import, db_base_import, routers_import, \
    format_imports, cors_import


@is_generated(package_name="")
def run(tables_name: list, host: str, port: int, output_path: str, activate_cors: bool):
    """
    Create app.py file, the entrypoint of the api under root directory
    :param tables_name: name of the table
    :param host: host of the generated api
    :param port: port of the generated api
    :param output_path: path of the output directory
    :param activate_cors: boolean, true to activate cors
    :return: generated filename
    """
    logger.info(f"Start app entrypoint generation under {output_path}")
    filename = "app.py"
    file_app = open(output_path + filename, "a")

    if activate_cors is True:
        imports = format_imports(
            uvicorn_import(),
            fastapi_core_import(),
            db_base_import(True),
            routers_import(tables_name),
            cors_import()
        )
    else:
        imports = format_imports(
            uvicorn_import(),
            fastapi_core_import(),
            db_base_import(True),
            routers_import(tables_name)
        )

    content = imports + fast_setup_content(activate_cors) + include_routers(tables_name) + exec_app(host, port)

    file_app.write(content)
    file_app.close()

    return filename


def fast_setup_content(activate_cors: bool):
    """
    Generate fastapi setup content
    :param activate_cors: boolean, to to activate cors
    :return: string containing fastapi setup
    """
    fast_setup = "Base.metadata.create_all(bind=engine)\n" + \
                 "app = FastAPI()\n"

    if activate_cors is True:
        logger.info("CORS activated...")

        fast_setup_with_cors = fast_setup + "\napp.add_middleware(" + "\n" + \
                               Indentator.IND_LEVEL_1 + "CORSMiddleware," + "\n" + \
                               Indentator.IND_LEVEL_1 + "allow_origins=['*']," + "\n" + \
                               Indentator.IND_LEVEL_1 + "allow_credentials=True," + "\n" + \
                               Indentator.IND_LEVEL_1 + "allow_methods=['*']," + "\n" + \
                               Indentator.IND_LEVEL_1 + "allow_headers=['*']" + "\n" + ")\n"
        return fast_setup_with_cors

    else:
        logger.warn("CORS not activated - You can activate cors support using --cors_activation boolean argument")
        return fast_setup


def include_routers(tables_name: list):
    """
    Generate routers include statement
    :param tables_name: list containing all table names
    :return: string with all includes statement
    """
    return "".join([f"app.include_router({name}_router.router)\n" for name in tables_name])


@function_declaration
def exec_app(host: str, port: int):
    """
    Generate app execution main
    :param host: hostname or ip of the api
    :param port: port of the api
    :return: main statement
    """
    if port is None:
        port = 8080
    if host is None:
        host = "0.0.0.0"

    main = 'if __name__ == "__main__":\n' + Indentator.IND_LEVEL_1 + f'uvicorn.run(app, host="{host}",port={port})'
    return main

import json
from crudgen.utils.logging import logger
from crudgen.input_parser.type_mapper import TYPE_MAPPING


def extract_tables_name(input_dict: dict):
    """Extract tables names from input dictionnary"""
    return list(input_dict.keys())


def parse_json(file_path: str):
    """
    Parse json file containing table details
    :param file_path: json file path
    :return: dict containing json data
    """
    try:
        with open(file_path) as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        logger.error("Cannot find input json file that describe table content")
        exit(1)


def map_dict_type(tables_dict: dict):
    """
    Map tables_dict field_type with corresponding TypeMapper
    class containing pydantic and sql alchemy correspondancy
    :param tables_dict: dictionnary containing tables description
    :return: tables_dict with TypeMapper field_type
    """
    tables_name = extract_tables_name(tables_dict)
    authorized_input_type = list(TYPE_MAPPING.keys())

    for table in tables_name:

        tables_dict[table]["key_identifier"]["type"] = TYPE_MAPPING[tables_dict[table]["key_identifier"]["type"]]
        for field in tables_dict[table]["fields"]:
            try:
                field["field_type"] = TYPE_MAPPING[field["field_type"]]
            except KeyError:
                logger.error("Invalid type {} in table {}, field_type should be one of {}"
                             .format(field["field_type"], table, authorized_input_type))
                exit(1)

    return tables_dict


def extract_table_structure(json_path: str):
    """
    Extract table structure
    :param json_path: path of the json describing tables
    :return: dict mapping table type
    """
    table_description = parse_json(json_path)
    tables = extract_tables_name(table_description)
    number_of_tables = len(tables)
    logger.info("Find {} tables in file {} : {}".format(number_of_tables, json_path, tables))
    table_mapped_type = map_dict_type(table_description)

    return table_mapped_type

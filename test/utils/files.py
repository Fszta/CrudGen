import os


def check_files_are_identical(generated_file_path: str, expected_file_path: str):
    """
    Check whether generated file and expected file content are identical
    Use for testing purpose
    :param generated_file_path: path of the generated file
    :param expected_file_path: path of the expected file
    :return: True if files are identical, otherwise False
    """

    # Read generated file
    generated_file = open(generated_file_path, "r")

    # Read expected file
    expected_file = open(expected_file_path, "r")

    try:
        assert generated_file.read() == expected_file.read()
        return True

    except AssertionError:
        return False

    finally:
        generated_file.close()
        expected_file.close()
        os.remove(generated_file_path)

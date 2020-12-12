from crudgen.input_parser.arguments import process_output_dir_path
from unittest import TestCase


class TestArgument(TestCase):
    def test_process_output_dir_path(self):
        test_path = "my/test/path"
        expected = "my/test/path/"
        processed_input = process_output_dir_path(test_path)
        self.assertEqual(expected, processed_input)

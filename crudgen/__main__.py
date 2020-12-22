from crudgen.input_parser.arguments import set_parameters
from crudgen.app import Crudgen


def main():
    Crudgen(set_parameters()).run()


if __name__ == '__main__':
    main()

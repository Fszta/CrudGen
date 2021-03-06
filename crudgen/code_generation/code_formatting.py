
def function_declaration(declaration):
    def inner(*args):
        if len(args) > 0:
            return "\n\n" + declaration(*args) + "\n"
        else:
            return "\n\n" + declaration() + "\n"

    return inner


def generic_import_declaration(single_import):
    def inner():
        return single_import() + "\n"

    return inner


def custom_import_declaration(custom_import):
    def inner(name):
        return custom_import(name) + "\n"

    return inner


def imports_declaration(generate_imports):
    def inner(*arg):
        return generate_imports(*arg) + "\n"

    return inner


def class_declare(declare):
    def inner(*args):
        return "\n" + declare(*args) + "\n"

    return inner

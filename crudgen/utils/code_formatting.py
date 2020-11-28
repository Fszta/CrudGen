def class_declaration(declaration):
    def inner():
        return declaration()
    return inner


def function_declaration(declaration):
    def inner():
        return declaration() + "\n"
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
        return generate_imports(*arg) + "\n" + "\n"
    return inner


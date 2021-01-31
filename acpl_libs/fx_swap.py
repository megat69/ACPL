"""
ACPL Swap lib.
Swaps two variables' contents.
"""
from recurrent_classes import *

def libs_to_import():
    return tuple(), tuple()

def requirements(file):
    if file == "main":
        return ("line_numbers",)
    elif file == "compiler":
        return "line_numbers", "variables"
    else:
        return tuple()

def main(line, variables_container, other_args):
    line_numbers = other_args[0]

    if line.startswith("swap"):
        line = line.replace("swap ", "", 1)
        line = remove_suffix(line, line.endswith("\n"))
        line = line.split(" ")  # [var1, var2]

        if len(line) != 2:
            error(line_numbers, "ArgumentError", texts.errors["FunctionArgumentError"].format(args_required=3, args_nbr=len(line)))

        if line[0] not in variables_container.keys():
            error(line_numbers, "VarNotFoundError", texts.errors["VarNotFoundError"].format(variable=line[0]))
        elif line[1] not in variables_container.keys():
            error(line_numbers, "VarNotFoundError", texts.errors["VarNotFoundError"].format(variable=line[1]))

        variables_container[line[0]], variables_container[line[1]] = variables_container[line[1]], variables_container[line[0]]

    return line, variables_container

def pytranslation(line, other_args):
    line_numbers = other_args[0]
    variables = other_args[1]

    if line.startswith("swap"):
        line = line.replace("swap ", "", 1)
        line = remove_suffix(line, line.endswith("\n"))
        line = line.split(" ")  # [var1, var2]

        if len(line) != 2:
            error(line_numbers, "ArgumentError", texts.errors["FunctionArgumentError"].format(args_required=3, args_nbr=len(line)))

        if line[0] not in variables.keys():
            error(line_numbers, "VarNotFoundError", texts.errors["VarNotFoundError"].format(variable=line[0]))
        elif line[1] not in variables.keys():
            error(line_numbers, "VarNotFoundError", texts.errors["VarNotFoundError"].format(variable=line[1]))

        line = f"{line[0]}, {line[1]} = {line[1]}, {line[0]}"

    return (line,)

def var_methods(line, variables_container, other_args):
    return line, variables_container

def compiler_var_methods(line, other_args):
    return (line,)

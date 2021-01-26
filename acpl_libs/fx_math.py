from recurrent_classes import *
import math

def libs_to_import():
    # Returning all the basic imports (import <lib>) and the from imports (from <lib> import <element>)
    # as tuple of strings
    return (("math",), tuple())

def requirements(file):
    return ("line_numbers",)

def main(line, variables_container, *args):
    """
    Allows for math functions through ACPL.
    """
    line_numbers = args[0][0]

    if line.startswith('math'):
        line = line.replace("math ", "", 1)
        line = remove_suffix(line, line.endswith("\n"))
        if line.startswith("sqrt"):  # Syntax : math sqrt var_name value
            line = line.replace("sqrt ", "", 1)
            line = line.split(" ")
            if len(line) != 2:
                # Arguments missing !
                error(line_numbers, "ArgumentError", texts.errors["ArgumentMissing"])
            if float(line[1]) < 0:
                error(line_numbers, "NegativeNumberError", "Cannot do the square root of a negative number.")
                sys.exit()
            try:
                variables_container[line[0]] = math.sqrt(int(line[1]))
            except ValueError:
                try:
                    variables_container[line[0]] = math.sqrt(float(line[1]))
                except ValueError:
                    error(line_numbers, "ArgumentError", "Argument 'value' has to be 'int' or 'float' !\nCurrent type : "+type(line[1]))
        elif line.startswith("fabs"):  # math fabs variable value
            line = line.replace("fabs ", "", 1)
            line = line.split(" ")
            try:
                line[1] = int(line[1])
            except ValueError:
                try:
                    line[1] = float(line[1])
                except ValueError:
                    error(line_numbers, "ArgumentError", "Argument 'value' has to be 'int' or 'float' !\nCurrent type : " + str(type(line[1])))
            variables_container[line[0]] = math.fabs(line[1])
        elif line.startswith("factorial"): # math factorial variable value
            line = line.replace("factorial ", "", 1)
            line = line.split(" ")
            try:
                line[1] = int(line[1])
            except ValueError:
                try:
                    line[1] = float(line[1])
                except ValueError:
                    error(line_numbers, "ArgumentError", "Argument 'value' has to be 'int' or 'float' !\nCurrent type : " + str(type(line[1])))
                    sys.exit()
            if line[1] < 0:
                error(line_numbers, "NegativeNumberError", "The value to factorial should not be negative.")
                sys.exit()
            elif line[1] == 0:
                variables_container[line[0]] = 0
            else:
                variables_container[line[0]] = math.factorial(line[1])
        elif line.startswith("floor"):  # math floor variable value
            line = line.replace("floor ", "", 1)
            line = line.split(" ")
            try:
                line[1] = float(line[1])
            except ValueError:
                error(line_numbers, "ArgumentError", "Argument 'value' has to be 'int' or 'float' !\nCurrent type : " + str(type(line[1])))
            variables_container[line[0]] = math.floor(line[1])

    return (line, variables_container)

def pytranslation(line, *args):
    """
    Allows for math functions through ACPL, transpiled in Python.
    """
    line_numbers = args[0][0]

    if line.startswith("math"):
        line = line.replace("math ", "", 1)
        line = remove_suffix(line, line.endswith("\n"))
        line = line.replace("{", "")
        line = line.replace("}", "")
        if line.startswith("sqrt"):
            line = line.replace("sqrt ", "", 1)
            line = line.split(" ")
            if len(line) != 2:
                error(line_numbers, "ArgumentError", "Arguments missing.")
                sys.exit()
            line = f"{line[0]} = sqrt({line[1]})"
        elif line.startswith("fabs"):
            line = line.replace("fabs ", "", 1)
            line = line.split(" ")
            line = f"{line[0]} = fabs({line[1]})"
        elif line.startswith("factorial"):
            line = line.replace("factorial ", "", 1)
            line = line.split(" ")
            line = f"{line[0]} = factorial({line[1]})"
        elif line.startswith("floor"):
            line = line.replace("floor ", "", 1)
            line = line.split(" ")
            line = f"{line[0]} = floor({line[1]})"
    return (line,)

def var_methods(line, variables_container, other_args):
    """
    Var methods for ACPL math library.
    """
    line_numbers = other_args[0]
    if line[2].startswith("math"):
        line[2] = line[2].replace("math ", "", 1)
        if line[2].startswith("sqrt"):  # Syntax : math sqrt value
            line[2] = line[2].replace("sqrt ", "", 1)
            if float(line[2]) < 0:
                error(line_numbers, "NegativeNumberError", "Cannot do the square root of a negative number.")
            try:
                line[2] = math.sqrt(int(line[2]))
            except ValueError:
                try:
                    line[2] = math.sqrt(float(line[2]))
                except ValueError:
                    error(line_numbers, "ArgumentError", "Argument 'value' has to be 'int' or 'float' !\nCurrent type : "+type(line[1]))

        elif line[2].startswith("fabs"):
            line[2] = line[2].replace("fabs ", "", 1)
            try:
                line[2] = math.fabs(int(line[2]))
            except ValueError:
                try:
                    line[2] = math.fabs(float(line[2]))
                except ValueError:
                    error(line_numbers, "ArgumentError", "Argument 'value' has to be 'int' or 'float' !\nCurrent type : " + str(type(line[2])))

        elif line[2].startswith("factorial"):
            line[2] = line[2].replace("factorial ", "", 1)
            try:
                line[2] = int(line[2])
            except ValueError:
                try:
                    line[2] = float(line[2])
                except ValueError:
                    error(line_numbers, "ArgumentError", "Argument 'value' has to be 'int' or 'float' !\nCurrent type : " + str(type(line[1])))

            if line[2] < 0:
                error(line_numbers, "NegativeNumberError", "The value to factorial should not be negative.")
            elif line[2] == 0:
                line[2] = 0
            else:
                line[2] = math.factorial(line[2])

        elif line[2].startswith("floor"):
            line[2] = line[2].replace("floor ", "", 1)
            try:
                line[2] = float(line[2])
            except ValueError:
                error(line_numbers, "ArgumentError", "Argument 'value' has to be 'int' or 'float' !\nCurrent type : " + str(type(line[1])))
            line[2] = math.floor(line[2])

    return line, variables_container

def compiler_var_methods(line, other_args):
    """
    Var methods for ACPL math library. Designed for compiler.
    """
    line_numbers = other_args[0]
    if line[2].startswith("math"):
        line[2] = line[2].replace("math ", "", 1)
        line[2] = line[2][:-2]
        line[2] = line[2].split(" ")
        try:
            line[2] = f"math.{line[2][0]}({line[2][1]})"
        except IndexError:
            error(line_numbers, "ArgumentError", texts.errors["FunctionArgumentError"].format(args_required=1, args_nbr=0))

    return line, ("no_string", True)
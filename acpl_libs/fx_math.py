from recurrent_classes import *
import math

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
                error(line_numbers, "ArgumentError", "Arguments missing.")
                sys.exit()
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
                    sys.exit()
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
                    sys.exit()
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
                sys.exit()
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
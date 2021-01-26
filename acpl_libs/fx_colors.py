from recurrent_classes import *

def libs_to_import():
    # Returning all the basic imports (import <lib>) and the from imports (from <lib> import <element>)
    # as tuple of strings
    return (tuple(), tuple())

def requirements(file):
    if "var_methods" in file:
        return ("line_numbers",)
    else:
        return tuple()

def main(line, variables_container, *args):
    """
    Allows to introduce colors to ACPL.
    """
    if line.startswith("colors"):
        line = line.replace("colors ", "", 1)
        if line.startswith("import"):
            variables_container["colors_BLUE"] = bcolors.OKBLUE
            variables_container["colors_PINK"] = bcolors.HEADER
            variables_container["colors_GREEN"] = bcolors.OKGREEN
            variables_container["colors_YELLOW"] = bcolors.WARNING
            variables_container["colors_RED"] = bcolors.FAIL
            variables_container["colors_UNDERLINE"] = bcolors.UNDERLINE
            variables_container["colors_BOLD"] = bcolors.BOLD
            variables_container["colors_ITALICS"] = bcolors.ITALICS
            variables_container["colors_END"] = bcolors.ENDC
    return line, variables_container

def pytranslation(line, *args):
    if line.startswith("colors"):
        line = line.replace("colors ", "", 1)
        if line.startswith("import"):
            line = f"colors_BLUE = '{bcolors.OKBLUE}'\ncolors_PINK = '{bcolors.HEADER}'\ncolors_GREEN = '{bcolors.OKGREEN}'\n"
            line += f"colors_YELLOW = '{bcolors.WARNING}'\ncolors_RED = '{bcolors.FAIL}'\ncolors_UNDERLINE = '{bcolors.UNDERLINE}'\n"
            line += f"colors_BOLD = '{bcolors.BOLD}'\ncolors_ITALICS = '{bcolors.ITALICS}'\ncolors_END = '{bcolors.ENDC}'"
    return (line,)

def var_methods(line:list, variables_container, other_args):
    """
    Var method transformation of the ACPL colors lib.
    """
    line_numbers = other_args[0]

    if line[2].startswith("colors"):
        line[2] = line[2].replace("colors ", "", 1)
        if line[2].lower().startswith("blue"):
            line[2] = bcolors.OKBLUE
        elif line[2].lower().startswith("pink"):
            line[2] = bcolors.HEADER
        elif line[2].lower().startswith("green"):
            line[2] = bcolors.OKGREEN
        elif line[2].lower().startswith("yellow"):
            line[2] = bcolors.WARNING
        elif line[2].lower().startswith("red"):
            line[2] = bcolors.FAIL
        elif line[2].lower().startswith("underline"):
            line[2] = bcolors.UNDERLINE
        elif line[2].lower().startswith("bold"):
            line[2] = bcolors.BOLD
        elif line[2].lower().startswith("italics"):
            line[2] = bcolors.ITALICS
        elif line[2].lower().startswith("end"):
            line[2] = bcolors.ENDC
        else:
            error(line_numbers, "UnknownColorError", f"Unknown color '{line[2]}'.")

    return line, variables_container

def compiler_var_methods(line, other_args):
    """
    Var method transformation of the ACPL colors lib for compiler.
    """
    line_numbers = other_args[0]

    if line[2].startswith("colors"):
        line[2] = line[2].replace("colors ", "", 1)
        if line[2].lower().startswith("blue"):
            line[2] = bcolors.OKBLUE
        elif line[2].lower().startswith("pink"):
            line[2] = bcolors.HEADER
        elif line[2].lower().startswith("green"):
            line[2] = bcolors.OKGREEN
        elif line[2].lower().startswith("yellow"):
            line[2] = bcolors.WARNING
        elif line[2].lower().startswith("red"):
            line[2] = bcolors.FAIL
        elif line[2].lower().startswith("underline"):
            line[2] = bcolors.UNDERLINE
        elif line[2].lower().startswith("bold"):
            line[2] = bcolors.BOLD
        elif line[2].lower().startswith("italics"):
            line[2] = bcolors.ITALICS
        elif line[2].lower().startswith("end"):
            line[2] = bcolors.ENDC
        else:
            error(line_numbers, "UnknownColorError", f"Unknown color '{line[2]}'.")

    return (line,)

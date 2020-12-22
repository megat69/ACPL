from recurrent_classes import *

def libs_to_import():
    # Returning all the basic imports (import <lib>) and the from imports (from <lib> import <element>)
    # as tuple of strings
    return (tuple(), tuple())

def requirements(file):
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

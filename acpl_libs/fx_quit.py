from recurrent_classes import *

def requirements(file):
    if file == "main":
        return ("code_lines", "line_numbers")
    else:
        return tuple()

def main(line, variables_container, other_args):
    """
    Allows to leave an ACPL program.
    """
    code_lines = other_args[0]
    line_numbers = other_args[1]
    if line.startswith("quit"):
        code_lines.append("")
        line_numbers = len(code_lines)-1
    return line, variables_container, ("code_lines", code_lines, "line_numbers", line_numbers)

def pytranslation(line, *args):
    """
    Allows to quit an ACPL program.
    """
    if line.startswith("quit"):
        line = "import sys\nsys.exit()"
    return (line,)
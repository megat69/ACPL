from recurrent_classes import *

def libs_to_import():
    # Returning all the basic imports (import <lib>) and the from imports (from <lib> import <element>)
    # as tuple of strings
    return (tuple(), tuple())

def requirements(file):
    return tuple()

def main(line, variables_container, other_args):
    """
    Allows the user to wait.
    """
    if line.startswith("wait_until_user_input"):
        line = line.replace("wait_until_user_input ", "", 1)
        line = remove_suffix(line, line.endswith("\n"))
        if line != "":
            if line.lower() == "true":
                input("Press enter to continue...")
            elif line.lower() == "false":
                input("")
            else:
                input(line)
        else:
            input("")
    return line, variables_container, other_args

def pytranslation(line, *args):
    if line.startswith("wait_until_user_input"):
        line = line.replace("wait_until_user_input ", "", 1)
        line = remove_suffix(line, line.endswith("\n"))
        if line != "":
            if line.lower() == "true":
                line = "input(\"Press enter to continue...\")"
            elif line.lower() == "false":
                line = "input(\"\")"
            else:
                line = f"input(\"{line}\")"
        else:
            line = "input(\"\")"
    return (line,)

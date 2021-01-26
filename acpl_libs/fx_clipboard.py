from recurrent_classes import *
import pyperclip

def libs_to_import():
    return ("pyperclip",), tuple()

def requirements(file):
    if file == "compiler_var_methods":
        return ("line_numbers", "is_lib")
    else:
        return ("line_numbers",)

def main(line, variables_container, other_args):
    """
    Main function for clipboard ACPL lib.
    """
    line_numbers = other_args[0]

    if line.startswith("clipboard"):
        line = line.replace("clipboard ", "", 1)
        if line.startswith("copy"):
            # lib clipboard copy <text>
            line = line.replace("copy ", "", 1)
            line = remove_suffix(line, line.endswith("\n"))
            pyperclip.copy(line)

        elif line.startswith("get"):
            # lib clipboard get <return_variable>
            line = line.replace("get ", "", 1)
            line = remove_suffix(line, line.endswith("\n"))
            variables_container[line] = pyperclip.paste()

        else:
            error(line_numbers, "ArgumentError", f"Function '{line.split(' ')[0]}' does not exist in clipboard lib !")

    return line, variables_container

def pytranslation(line, other_args):
    line_numbers = other_args[0]

    if line.startswith("clipboard"):
        line = line.replace("clipboard ", "", 1)
        if line.startswith("copy"):
            # lib clipboard copy <text>
            line = line.replace("copy ", "", 1)
            line = remove_suffix(line, line.endswith("\n"))
            line = line.replace("\"", "\\\"")
            line = f"pyperclip.copy(f\"{line}\")"

        elif line.startswith("get"):
            # lib clipboard get <return_variable>
            line = line.replace("get ", "", 1)
            line = remove_suffix(line, line.endswith("\n"))
            line = f"{line} = pyperclip.paste()"

        else:
            error(line_numbers, "ArgumentError", f"Function '{line.split(' ')[0]}' does not exist in clipboard lib !")

    return (line,)

def var_methods(line, variables_container, other_args):
    line_numbers = other_args[0]
    method = line[2]
    if method.startswith("clipboard "):
        method = method.replace("clipboard ", "", 1)
        if method.startswith("get"):
            method = method.replace("get", "", 1)
            method = pyperclip.paste()
        else:
            error(line_numbers, "ArgumentError", f"Function '{line.split(' ')[0]}' does not exist in clipboard lib !")

    line[2] = method

    return line, variables_container

def compiler_var_methods(line, other_args):
    line_numbers = other_args[0]
    is_lib = other_args[1]
    method = line[2]

    if method.startswith("clipboard "):
        method = method.replace("clipboard ", "", 1)
        if method.startswith("get"):
            method = method.replace("get", "", 1)
            line = f"{line[0]} {line[1]} pyperclip.paste()"
            is_lib = True
        else:
            error(line_numbers, "ArgumentError", f"Function '{line.split(' ')[0]}' does not exist in clipboard lib !")

    return line, ("is_lib", is_lib)
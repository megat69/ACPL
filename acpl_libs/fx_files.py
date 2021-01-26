from recurrent_classes import *

def libs_to_import():
    # Returning all the basic imports (import <lib>) and the from imports (from <lib> import <element>)
    # as tuple of strings
    return (tuple(), tuple())

def requirements(file):
    if file == "var_methods":
        return ("line_numbers", "var_type")
    elif file == "compiler_var_methods":
        return ("line_numbers", "var_type", "is_lib")
    else:
        return ("line_numbers",)

def main(line, variables_container, other_args):
    """
    This library adds file support to ACPL.
    """

    line_numbers = other_args[0]

    if str(line).startswith("files"):
        line = line.replace("files ", "", 1)
        line = remove_suffix(line, line.endswith("\n"))
        if line.startswith("read"):  # lib files read <file> <return_var>
            line = line.replace("read ", "", 1)
            line = line.split(" ")
            # READING FILE

            # Too few arguments ?
            if len(line) < 2:
                error(line_numbers, "ArgumentError", texts.errors['FunctionArgumentError'].format(args_required=2, args_nbr=len(line)))

            encoding = "--encoding:" in line
            if encoding is True:
                encoding = line.split("--encoding:")[1]
                try:
                    encoding = encoding.split(" ")[0]
                except IndexError:
                    pass
                line = line.replace(f" --encoding:{encoding}", "", 1)
            else:
                encoding = "utf-8"

            try:
                file = open(line[0], "r", encoding=encoding)
            except FileNotFoundError:
                error(line_numbers, "FileNotFoundError", f"The file '{line[0]}' doesn't exist.")
            file_contents = file.readlines()
            file.close()

            if "--remove_newlines" in line:
                for i in range(len(file_contents)):
                    file_contents[i] = remove_suffix(file_contents[i], file_contents[i].endswith("\n"))

            variables_container[line[1]] = file_contents

        elif line.startswith("write"):  # lib files write <file> <var_from>
            line = line.replace("write ", "", 1)
            line = line.split(" ")
            # WRITING FILE

            # Too few arguments ?
            if len(line) < 2:
                error(line_numbers, "ArgumentError", texts.errors['FunctionArgumentError'].format(args_required=2, args_nbr=len(line)))

            text_to_paste = variables_container[line[1]]
            # If it is just a string, then a single line, we convert it to a 1 element list.
            if isinstance(text_to_paste, str):
                text_to_paste = [text_to_paste]

            try:
                if "--write_mode:a" in line:
                    file_to_write = open(line[0], "a")
                else:
                    file_to_write = open(line[0], "w")
            except FileNotFoundError:
                error(line_numbers, "FileNotFoundError", f"The file '{line[0]}' doesn't exist.")

            file_to_write.writelines(text_to_paste)
            file_to_write.close()

    return line, variables_container, ("line_numbers", line_numbers)

def pytranslation(line, other_args):
    """
    Translation to Python of the files ACPL lib.
    """

    line_numbers = other_args[0]

    if line.startswith("files"):
        line = line.replace("files ", "", 1)
        line = remove_suffix(line, line.endswith("\n"))
        if line.startswith("read"):  # lib files read <file> <return_var>
            line = line.replace("read ", "", 1)
            line = line.split(" ")

            # Too few arguments ?
            if len(line) < 2:
                error(line_numbers, "ArgumentError", texts.errors['FunctionArgumentError'].format(args_required=2, args_nbr=len(line)))

            line[0] = f"'{line[0]}'"

            if "--remove_newlines" not in line:
                temp_line = f"temp_file = open({line[0]}, 'r')\n" \
                            f"{line[1]} = temp_file.readlines()\n" \
                            f"temp_file.close()"
            else:
                temp_line = f"temp_file = open({line[0]}, 'r')\n" \
                            f"{line[1]} = temp_file.readlines()\n" \
                            f"for i in range(len({line[1]})):\n" \
                            f"\tif {line[1]}[i].endswith(\\n):\n" \
                            f"\t\t{line[1]}[i] = {line[1]}[i][:-1]\n" \
                            f"temp_file.close()"

            line = temp_line

        elif line.startswith("write"):  # lib files write <file> <var_from>
            line = line.replace("write ", "", 1)
            line = line.split(" ")

            # Too few arguments ?
            if len(line) < 2:
                error(line_numbers, "ArgumentError", texts.errors['FunctionArgumentError'].format(args_required=2, args_nbr=len(line)))

            line[0] = f"'{line[0]}'"

            temp_line = f"if isinstance(text_to_paste, str):\n" \
                        f"\ttext_to_paste = [text_to_paste]\n"

            if "--write_mode:a" in line:
                temp_line += f"temp_file = open({line[0]}, 'a')\n" \
                            f"temp_file.writelines({line[1]})\n" \
                            f"temp_file.close()"
            else:
                temp_line += f"temp_file = open({line[0]}, 'w')\n" \
                             f"temp_file.writelines({line[1]})\n" \
                             f"temp_file.close()"

            line = temp_line

    return line, ("line_numbers", line_numbers)

def var_methods(line:list, variables_container, other_args):
    """
    File reading/writing as variable method.
    """
    line_numbers = other_args[0]
    var_type = other_args[1]
    method = line[2]

    if str(method).startswith("files"):
        method = method.replace("files ", "", 1)
        if method.startswith("read"):  # lib files read <file>
            method = method.replace("read ", "", 1)
            remove_newlines = "--remove_newlines" in method
            encoding = "--encoding:" in method
            if encoding is True:
                encoding = method.split("--encoding:")[1]
                try:
                    encoding = encoding.split(" ")[0]
                except IndexError:
                    pass
                method = method.replace(f" --encoding:{encoding}", "", 1)
            else:
                encoding = "utf-8"
            method = method.replace(" --remove_newlines", "", 1)
            method = remove_suffix(method, method.endswith('\n'))
            try:
                temp_file = open(method, "r", encoding=encoding)
            except FileNotFoundError:
                error(line_numbers, "FileNotFoundError", f"The file '{method}' doesn't exist.")
            method = temp_file.readlines()
            if remove_newlines is True:
                for i in range(len(method)):
                    method[i] = remove_suffix(method[i], method[i].endswith("\n"))
            temp_file.close()
            var_type = "list"

        line[2] = method

    return line, variables_container, ("line_numbers", line_numbers, "var_type", var_type)

def compiler_var_methods(line:list, other_args):
    """
    File reading/writing as variable method for ACPL compiler.
    """
    line_numbers = other_args[0]
    var_type = other_args[1]
    method = line[2]

    if method.startswith("files"):
        method = method.replace("files ", "", 1)
        if method.startswith("read"):  # lib files read <file>
            method = method.replace("read ", "", 1)
            remove_newlines = "--remove_newlines" in method
            method = method.replace(" --remove_newlines", "", 1)
            temp_method = f"temp_file = open('{method[:-2]}', 'r')\n" \
                     f"{line[0]} = temp_file.readlines()\n" \
                     f"temp_file.close()"
            if remove_newlines is True:
                temp_method += f"\nfor i in range(len({line[0]})):\n" \
                               f"\tif {line[0]}[i].endswith('\\n'):\n" \
                               f"\t\t{line[0]}[i] = {line[0]}[i][:-1]"
            method = temp_method
            del temp_method
            line = method
        else:
            line[2] = method

    return line, ("line_numbers", line_numbers, "is_lib", True)
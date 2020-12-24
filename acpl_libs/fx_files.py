from recurrent_classes import *

def libs_to_import():
    # Returning all the basic imports (import <lib>) and the from imports (from <lib> import <element>)
    # as tuple of strings
    return (tuple(), tuple())

def requirements(file):
    return ("line_numbers",)

def main(line, variables_container, other_args):
    """
    This library adds file support to ACPL.
    """

    line_numbers = other_args[0]

    if line.startswith("files"):
        line = line.replace("files ", "", 1)
        line = remove_suffix(line, line.endswith("\n"))
        if line.startswith("read"):  # lib files read <file> <return_var>
            line = line.replace("read ", "", 1)
            line = line.split(" ")
            # READING FILE

            # Too few arguments ?
            if len(line) < 2:
                error(line_numbers, "ArgumentError", texts.errors['FunctionArgumentError'].format(args_required=2, args_nbr=len(line)))

            try:
                file = open(line[0], "r")
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

            if "--write_mode:a" in line:
                file_to_write = open(line[0], "a")
            else:
                file_to_write = open(line[0], "w")

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

    return line, other_args
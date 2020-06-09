version = "1.0"
lib_type = "functions+variables"

import json
from recurrent_classes import *
from time import sleep

line = var_line
variables_container = VARIABLES_CONTAINER
line = line.replace("files ", "", 1)

if line.startswith("open"):
    # Syntax : lib open <filename> [opening_mode = "r"]
    line = line.replace("open ", "", 1)
    file = line.split(" ")
    if len(file) == 1:
        file.append("r")
    opened_file = open(file[0], file[1])
    variables_container[file[0]] = opened_file
elif line.startswith("read"):
    # Syntax : lib read <file> <method> <line_number> <return_variable>
    line = line.replace("read ", "", 1)
    line = line.split(" ")
    if "{" in line[0] and "}" in line[0]:
        variable = line[0][line[0].find("{") + 1:line[0].find("}")]
        line[0] = variable

    file = open(line[0], line[1], encoding="utf-8")

    if "{" in line[2] and "}" in line[2]:
        variable = line[2][line[2].find("{") + 1:line[2].find("}")]
        line[2] = variable

    line[3] = line[3].replace("{", "", 1)
    line[3] = line[3].replace("}", "")

    file_lines = file.readlines()
    searched_line = file_lines[int(line[2])].replace("\n", "")
    variables_container[line[3]] = searched_line
    #print("DEBUG : ", file_lines[int(line[2])].replace("\n", ""))
    file.close()
elif line.startswith("write"):
    # Syntax : write <file> <content> [line_number, if unspecified, at the end of the file.]
    line = line.replace("write ", "", 1)
    file = line.split(" ")
    filename = file[0]
    line = line.replace(f"{filename} ", "", 1)
    if "line_number" in line:
        line_number = line.split("line_number")
        line_number = line_number[1].replace("=", "")
        line_number = line_number.replace(" ", "")
        line = line.split(line_number)
        line = line[0]
    else:
        line_number = None

    if line_number is not None:
        file = open(filename, "w")
        replace_line(str(filename), int(line_number), str(line))
    else:
        file = open(filename, "a")
        file.write(line)

elif line.startswith("close"):
    # Syntax : close <file>
    line = line.replace("close ", "", 1)
    if "{" in line and "}" in line:
        variable = line[line.find("{") + 1:line.find("}")]
        line = variable
    else:
        error(line_numbers, "LibError", f"Variable required at this position, got \"{line[0]}\" instead.")

    variables_container.remove(line)
    line.close()



with open("var_transfer.json", "w") as transfer_file:
    transfer_file.write(json.dumps(variables_container))
    transfer_file.close()
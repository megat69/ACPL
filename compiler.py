import inspect
import string
import re
from time import sleep
from random import randrange
import sys
import json
from recurrent_classes import *
import os
import msvcrt

# Files opening
try:
    filename_file = open("startup.acpl-ini", "r+", encoding="utf-8")
except FileNotFoundError:
    print(texts.critic_errors["ImpossibleLoad_StartupIni"])
    sys.exit()
filename = filename_file.readlines()
for lines in filename:
    if lines.startswith("filename: "):
        lines = lines.replace("filename: ", "")
        if lines.endswith("\n"):
            lines = lines.replace("\n", "")
        if not lines.endswith(".acpl"):
            lines += ".acpl"
        final_filename = lines

    if lines.startswith("debug-state: "):
        lines = lines.replace("debug-state: ", "")
        if lines.lower() == "true" or lines == "1":
            debug_const = True
        else:
            debug_const = False

    if lines.startswith("debug-state: "):
        lines = lines.replace("debug-state: ", "")
        if lines.lower() == "true" or lines == "1":
            debug_const = True
        else:
            debug_const = False

    if lines.startswith("lang: "):
        lines = lines.replace("lang: ", "")
        lines = lines.replace("\n", "")
        language = lines

        try:
            with open("trad_" + language + ".json", "r", encoding="utf-8") as json_file:
                texts = json.load(json_file)
                json_file.close()
                texts = Text(texts)
        except NameError:
            raise CriticError(texts.critic_errors["NameError_LanguageFile"])


debug_file = open("debug.log", "w", encoding="utf-8")
code_file = open(final_filename, "r", encoding="utf-8")

# Code lines getting
code_lines = code_file.readlines()
debug("other", lineno(), code_lines)

# Blank lines removing
debug("in", lineno(), "Entrée dans la boucle pour retirer les commentaires et lignes vides des instructions.")
for i in range(0, len(code_lines)):
    result = code_lines[i].split("#")
    code_lines[i] = result[0]
    result = code_lines[i].split("//")
    code_lines[i] = result[0]
    result = code_lines[i].split(";")
    code_lines[i] = result[0]
debug("other", lineno(), "code_lines = ", code_lines)

code_lines[len(code_lines)-1] += "\n"

line_numbers = 0
variables_container = {}
is_in_comment = False

final_filename = str(final_filename).replace(".acpl", "")
with open(f"compiled_{final_filename}.py", "w", encoding="utf-8") as compiled_file:

    compiled_file.write("from time import sleep\nfrom random import randrange\nimport libs\nimport os\n\n")

    for line in code_lines:
        line_numbers += 1
        indentation_level = 0
        if "/*" in line:
            is_in_comment = True
        if "*/" in line:
            is_in_comment = False
            continue
        if not is_in_comment:
            line = split(line)
            for i in range(len(line)-1):
                if line[i] == "\t":
                    line.pop(0)
                    indentation_level += 1
                else:
                    break
            temp_line = ""
            for chr in line:
                temp_line += chr
            line = temp_line
            if line.startswith("if"):
                line = line.replace("&&", "and")
                line = line.replace("||", "or")
            if line.startswith("print"):
                line = line.replace("\"", "\\\"") # Replacement of "
                line = line.replace("print(", "print(f\"") # Replacement of print
                line = line.replace(")\n", "\")\n") # Add of the quote
                line = line.replace(") \n", "\")\n") # Add of the quote
            elif line.startswith("var"):
                line = line.replace("var ", "", 1)
                while "{" in line and "}" in line:
                    variable = line[line.find("{") + 1:line.find("}")]
                    line = line.replace("{"+variable+"}", variable)
                if "input(" in line:
                    line = line.replace("input(", "input(\"", 1)
                    line = line.replace(")\n", "\")\n")
                if "--round" in line:
                    line = line.replace(" --round", "", 1)
                    line = line.replace("--round", "", 1)
                    actual_state = "name"
                    name = ""
                    for char in split(line):
                        if char != " " and char != "=" and actual_state == "name":
                            name += char
                        elif char == " " or char == "=" and actual_state == "name":
                            line = line.replace(name, "", 1)
                            break
                    actual_state = "var"
                    temp_line = line.replace("=", "", 1)
                    while temp_line.startswith(" "):
                        temp_line = split(temp_line)
                        temp_line.pop(0)
                        temp_temp_line = ""
                        for char in temp_line:
                            temp_temp_line += char
                        temp_line = temp_temp_line
                    var_content = ""
                    for char in split(temp_line):
                        var_content += char
                    line = name + " = " + str(round(float(var_content))) + "\n"
                if "random(" in line:
                    line = line.replace("random(", "randrange(", 1)
                    while "{" in line and "}" in line:
                        variable = line[line.find("{") + 1:line.find("}")]
                        line = line.replace("{" + variable + "}", variable)
            elif line.startswith("pause"):
                line = line.replace("pause(", "sleep(float(", 1)
                if "{" in line and "}" in line:
                    variable = line[line.find("{") + 1:line.find("}")]
                    line = line.replace("{"+variable+"}", variable)
                line = line.replace("\n", ")\n")
            elif line.startswith("$use: "):
                line = line.replace("$use:", "")
                line = line.replace(" ", "")
                line = line.replace("\n", "")
                if os.path.exists(f"{os.getcwd()}/libs/lib_{line}.py") is True:
                    line = f"from libs import lib_{line}\n\n"
                else:
                    error(line_numbers, "UnexistingLibError", "Lib is not existing or has not been installed.")
                    break
            elif line.startswith("lib"):
                line = line.replace("lib ", "", 1)
                line = line.split(" ")
                line = line[0]
                line = f"""with open(f"libs/lib_{line}.py", "r") as lib_content:
    lib_content = lib_content.readlines()
    with open("temp.py", "w") as executable:
        for i in range(len(lib_content)):
            if "var_line" in lib_content[i]:
                line = line.replace("\\n", "")
            lib_content[i] = lib_content[i].replace("var_line", f'"{line}"')
        executable.writelines(lib_content)
    os.system("python temp.py")"""
            line = ("\t" * indentation_level) + line
            compiled_file.write(line)
    compiled_file.close()

print(bcolors.OKBLUE+texts.console["compiling-successfull"]+bcolors.ENDC)

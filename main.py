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
import timeit

time_launch = timeit.default_timer()

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

    if lines.startswith("process-time-round-numbers: "):
        lines = lines.replace("process-time-round-numbers: ", "")
        process_time_round_numbers = int(lines)


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

# Var container
variables_container = {}
#constants_container = {}
used_libs = []

# Use variables
is_in_comment = False
line_numbers = 0
execute_until_endif = False

while line_numbers < len(code_lines):
    line = code_lines[line_numbers]
    if msvcrt.kbhit() and msvcrt.getch() == chr(27).encode():
        sys.exit()
    if "/*" in line:
        is_in_comment = True
    if "*/" in line:
        is_in_comment = False
        continue
    if not is_in_comment:
        line = line.replace("\t", "")

        while "{" in line and "}" in line:
            variable = line[line.find("{") + 1:line.find("}")]
            debug("other", lineno(), f"Variable {variable} found in print.")
            try:
                line = line.replace("{" + variable + "}", str(variables_container[variable]))
            except KeyError:
                error(line_numbers, "ArgumentError",
                      f"The variable \"{variable}\" is not existing or has been declared later in the code.")

        while "<" in line and ">" in line:
            equation = line[line.find("<") + 1:line.find(">")]
            debug("other", lineno(), f"Equation {equation} found in print.")
            try:
                line = line.replace(f"<{str(equation)}>", str(eval(str(equation))))
            except KeyError:
                error(line_numbers, "ArgumentError",
                      f"The equation \"{equation}\" is not existing or has been declared later in the code.")


        if line.startswith("if "):
            line = line.replace("if ", "", 1)
            if eval(line) is True:
                execute_until_endif = False
            else:
                execute_until_endif = True
            last_condition = line
            line_numbers += 1
            continue
        elif line.startswith("else"):
            if eval(last_condition) is False:
                execute_until_endif = False
            else:
                execute_until_endif = True
                line_numbers += 1
                continue

        if line.startswith("endif") or line.startswith("end if"):
            execute_until_endif = False
            line_numbers += 1
            continue

        if line.startswith("for"):  # for <name> <min> <max>
            line = line.replace("for ", "", 1)
            line = line.split(" ")
            try:
                variables_container[line[0]] = int(line[1])
            except ValueError:
                error(line_numbers, "ArgumentNotInt", "Argument should be integer !")
            for_var = line[0]
            try:
                for_max = int(line[2])
            except ValueError:
                error(line_numbers, "ArgumentNotInt", "Argument should be integer !")
            for_line_number = line_numbers + 1
            line_numbers += 1
            continue

        if line.startswith("endfor") or line.startswith("end for"):
            variables_container[for_var] += 1
            if variables_container[for_var] < for_max:
                line_numbers = for_line_number
                continue
            else:
                variables_container.pop(for_var)


        if execute_until_endif is False:
            if line.startswith("print"):
                line = line.replace("print ", "", 1)
                if line.endswith("\n"):
                    line = line[:-1]  # Removing the \n
                print(line)
            elif line.startswith("var"):
                line = line.replace("var ", "", 1)
                if line.endswith("\n"):
                    line = split(line)
                    line.pop()
                    temp_line = ""
                    for char in line:
                        temp_line += char
                    line = temp_line
                line = line.replace("\\n", "\n")

                line = line.split(" ") # Result : [name, "=", content]

                if str(line[2]).lower() == "true":
                    line[2] = True
                elif str(line[2]).lower() == "false":
                    line[2] = False

                if line[2].startswith("input"):
                    line[2] = line[2].replace("input", "", 1)
                    for i in range(3, len(line)):
                        line[2] = line[2] + " " + line[i]
                    line[2] += " "
                    line[2] = input(line[2])

                if line[2].startswith("random"):
                    line[2] = line[2].replace("random", "", 1)
                    for i in range(3, len(line) - 1):
                        line[2] = line[2] + " " + line[i]

                    if len(line) == 4:
                        rand_min = 0
                        rand_max = line[3].replace(",", "")
                    else:
                        rand_min = line[3].replace(",", "")
                        rand_max = line[4]
                    line[2] = randrange(int(rand_min), int(rand_max))

                try:
                    line[2] = eval(line[2])
                except SyntaxError:
                    pass
                except TypeError:
                    pass

                try:
                    line[2] = int(line[2])
                except ValueError:
                    try:
                        line[2] = float(line[2])
                    except ValueError:
                        line[2] = str(line[2])

                variables_container[line[0]] = line[2]

            elif line.startswith("pause"):
                line = line.replace("pause ", "", 1)
                sleep(float(line))

            elif line.startswith("deletevar"):
                line = line.replace("deletevar ", "", 1)
                variables_container.pop(line)

            elif line.startswith("$use: "):
                line = line.replace("$use:", "")
                line = line.replace(" ", "")
                line = line.replace("\n", "")
                if os.path.exists(f"{os.getcwd()}/libs/lib_{line}.py") is True:
                    used_libs.append(line)
                else:
                    error(line_numbers, "UnexistingLibError", "Lib is not existing or has not been installed.")
                    break
            elif line.startswith("lib "):
                line = line.replace("lib ", "", 1)
                for lib in used_libs:
                    if lib in line:
                        with open(f"libs/lib_{lib}.py", "r") as lib_content:
                            lib_content = lib_content.readlines()
                            with open("temp.py", "w+") as executable:
                                for i in range(len(lib_content)):
                                    if "var_line" in lib_content[i]:
                                        line = line.replace("\n", "")
                                        lib_content[i] = lib_content[i].replace("var_line", f'"{line}"')
                                    lib_content[i] = lib_content[i].replace("VARIABLES_CONTAINER", str(variables_container))
                                    lib_content[i] = lib_content[i].replace("line_numbers", f"int({line_numbers})")
                                    if "variables" in lib_content[1]:
                                        with open("var_transfer.json", "r+", encoding="utf-8") as transfer_file:
                                            variables_container = json.load(transfer_file)
                                            transfer_file.close()
                                            # print(variables_container)
                                executable.writelines(lib_content)
                                # print(variables_container)
                                executable.close()
                        os.system("python temp.py")
            elif line != "" and line != " " and line != "\n" and line != "if" and line != "else" and line != "endif" and line != "end if" and line != "for" and line != "endfor" and line != "end for":
                if debug_const is True:
                    error(line_numbers, "Error", "Unknown function or method !")

    if debug_state:
        debug("other", line_numbers, f"Variables : {variables_container}")

    line_numbers += 1

print(f"{bcolors.OKBLUE}Process time : {round((timeit.default_timer()-time_launch), process_time_round_numbers)}s{bcolors.ENDC}")

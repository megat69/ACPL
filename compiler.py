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
import platform
import shlex

print(f"{bcolors.OKBLUE}Starting compilation.{bcolors.ENDC}")

try:
    config_file = open("startup.acpl-ini", "r")
except FileNotFoundError:
    print(texts.critic_errors["ImpossibleLoad_StartupIni"])
    sys.exit()

for config_line in config_file.readlines():
    if config_line.startswith("filename: "):  # File to compile
        config_line = config_line.replace("filename: ", "", 1)
        if not config_line.endswith(".acpl"):
            config_line += ".acpl"
        if ":" not in config_line:
            config_line = os.getcwd()+"/"+config_line

        file_to_compile = config_line

    elif config_line.startswith("compiled-file-filename: "):  # Compiled file filename
        config_line = config_line.replace("compiled-file-filename: ", "", 1).replace("\n", "")
        if not config_line.endswith(".py"):
            config_line += ".py"
        if ":" not in config_line:
            config_line = os.getcwd()+"/"+config_line

        compiled_file_filename = config_line
        if os.path.exists(compiled_file_filename):
            confirm = input(f"{bcolors.FAIL}This file, located at \"{compiled_file_filename}\" already exists.\nDo you want to replace it ? (Yes/No) {bcolors.ENDC}")
            while confirm.lower() != "yes" and confirm.lower() != "no":
                print("Wrong answer.")
                confirm = input(f"{bcolors.FAIL}This file, located at \"{compiled_file_filename}\" already exists.\nDo you want to replace it ? (Yes/No) {bcolors.ENDC}")
            if confirm.lower() == "no":
                sys.exit()

    elif config_line.startswith("open-compiled-file: "):
        config_line = config_line.replace("open-compiled-file: ", "", 1).replace("\n", "")
        open_compiled_file = config_line

    elif config_line.startswith("leave-comments-at-compiling: "):
        config_line = config_line.replace("leave-comments-at-compiling: ", "", 1).replace("\n", "")
        leave_comments_at_compiling = config_line

    elif config_line.startswith("compiling-style: "):
        config_line = config_line.replace("compiling-style: ", "", 1).replace("\n", "")
        compiling_style = config_line

    """elif lines.startswith("process-time-round-numbers: "):
        lines = lines.replace("process-time-round-numbers: ", "")
        process_time_round_numbers = int(lines)"""
process_time_round_numbers = 6

time_launch = timeit.default_timer()

file_to_compile = file_to_compile.replace(".acpl\n", "").replace("\n", "")

code_file = open(file_to_compile, "r", encoding="utf-8")

# Code lines getting
code_lines = code_file.readlines()
debug("other", lineno(), code_lines)

# Blank lines removing
debug("in", lineno(), "Entrée dans la boucle pour retirer les commentaires et lignes vides des instructions.")
for i in range(0, len(code_lines)):
    result = code_lines[i].split(";")
    code_lines[i] = result[0]
debug("other", lineno(), "code_lines = ", code_lines)

# Var container
variables_container = {}
used_libs = []

# Use variables
is_in_comment = False
line_numbers = 0
execute_until_endif = False
indentation_required = 0

compiled_file = open(compiled_file_filename, "w", encoding="utf-8")
compiled_file.write("# Compiled from ACPL programming language\n# Download from github : https://www.github.com/megat69/ACPL\n\nfrom time import sleep\nfrom random import randrange\n\n")

while line_numbers < len(code_lines):
    line = code_lines[line_numbers]
    if "/*" in line:
        is_in_comment = True
    if "*/" in line:
        is_in_comment = False
        line_numbers += 1
        continue

    if line.startswith("#") or "//" in line:
        if leave_comments_at_compiling == "True":
            line = re.sub("( )*#", "", line, 1)
            line = re.sub("( )*//", "", line, 1)
            line = "# "+line
            if code_lines[line_numbers-1].endswith("\n"):
                return_to_line = ""
            else:
                return_to_line = "\n"
            compiled_file.write(return_to_line+("\t"*indentation_required)+line[:-1])
        else:
            line = re.sub("( )*//.*", "", line)
            line = re.sub("( )*#.*", "", line)
            if line == "" or line == "\n":
                line_numbers += 1
                continue

        for i in range(0, indentation_required):
            line = "\t"+line

    if not is_in_comment:
        line = line.replace("\t", "")

        line = re.sub('\"', '\'', line)

        while "<" in line and ">" in line:
            equation = line[line.find("<") + 1:line.find(">")]
            while "{" in line and "}" in equation:
                variable = equation[equation.find("{") + 1:equation.find("}")]
                debug("other", lineno(), f"Variable {variable} found in print.")
                try:
                    line = line.replace("{" + variable + "}", variable)
                except KeyError:
                    error(line_numbers, "ArgumentError",
                          f"The variable \"{variable}\" is not existing or has been declared later in the code.")
            debug("other", lineno(), f"Equation {equation} found.")
            try:
                line = line.replace(f"<{str(equation)}>", "{"+equation+"}")
            except KeyError:
                error(line_numbers, "ArgumentError",
                      f"The equation \"{equation}\" is not existing or has been declared later in the code.")

        if line.startswith("for"):
            indentation_required += 1
            line = line.split(" ")
            line = f"for {line[1]} in range({line[2]}, {line[3][:-1]}):"
            compiled_file.write(line + "\n")
            line_numbers += 1
            continue
        elif line.startswith("endfor") or line.startswith("end for"):
            indentation_required -= 1
            line = ""

        if line.startswith("if"):
            while "<" in line and ">" in line:
                equation = line[line.find("<") + 1:line.find(">")]
                while "{" in line and "}" in equation:
                    variable = equation[equation.find("{") + 1:equation.find("}")]
                    debug("other", lineno(), f"Variable {variable} found in print.")
                    try:
                        line = line.replace("{" + variable + "}", variable)
                    except KeyError:
                        error(line_numbers, "ArgumentError",
                              f"The variable \"{variable}\" is not existing or has been declared later in the code.")
                debug("other", lineno(), f"Equation {equation} found.")
                try:
                    line = line.replace(f"<{str(equation)}>", "{" + equation + "}")
                except KeyError:
                    error(line_numbers, "ArgumentError",
                          f"The equation \"{equation}\" is not existing or has been declared later in the code.")

            while "{" in line and "}" in line:
                variable = line[line.find("{") + 1:line.find("}")]
                debug("other", lineno(), f"Variable {variable} found in print.")
                try:
                    line = line.replace("{" + variable + "}", variable)
                except KeyError:
                    error(line_numbers, "ArgumentError", f"The variable \"{variable}\" is not existing")

            line = line[:-1] + ":"
            indentation_required += 1
            line_numbers += 1
            compiled_file.write(("\t"*(indentation_required-1)) + line + "\n")
            continue
        elif line.startswith("else"):
            line = ("\t"*indentation_required) + "else:"
            indentation_required += 1
            compiled_file.write(line + "\n")
            line_numbers += 1
            continue
        elif line.startswith("endif") or line.startswith("end if"):
            indentation_required -= 1
            line = ""

        if line.startswith("print "):
            line = line.replace("print ", "", 1)
            if line.endswith("\n"):
                line = line[:-1]
            line = "print(f\""+line+"\")"

        elif line.startswith("var "):
            line = line.replace("var ", "", 1)

            do_regroup = True

            line = line.split(" ")  # Result : [name, "=", content]

            if str(line[2]).startswith("input"):
                line[2] = line[2].replace("input", "", 1)
                for i in range(3, len(line)):
                    line[2] = line[2] + " " + line[i]
                if line[2].endswith("\n"):
                    line[2] = line[2][:-1]
                line[2] = "input(f\""+line[2].replace(" ", "", 1)+"\")"
                do_regroup = False

            if str(line[2]).startswith("random"):
                line[2] = line[2].replace("random", "", 1)
                for i in range(3, len(line) - 1):
                    line[2] = line[2] + " " + line[i]

                if len(line) == 4:
                    rand_min = "0"
                    rand_max = line[3].replace(",", "")
                else:
                    rand_min = line[3].replace(",", "")
                    rand_max = line[4]

                line[2] = "randrange("+rand_min+", "+rand_max[:-1]+")"

                while "{" in line[2] and "}" in line[2]:
                    variable = line[2][line[2].find("{") + 1:line[2].find("}")]
                    debug("other", lineno(), f"Variable {variable} found in print.")
                    try:
                        line[2] = line[2].replace("{" + variable + "}", variable)
                    except KeyError:
                        error(line_numbers, "ArgumentError",
                              f"The variable \"{variable}\" is not existing or has been declared later in the code.")
                do_regroup = False

            if do_regroup:
                for i in range(3, len(line)):
                    line[2] += " "+line[i]

            if not isinstance(line[2], bool):
                try:
                    line[2] = int(line[2])
                except ValueError:
                    try:
                        line[2] = float(line[2])
                    except ValueError:
                        pass

            if isinstance(line[2], str) and not line[2].startswith("input") and not line[2].startswith("randrange"):
                if line[2].endswith("\n"):
                    line[2] = line[2][:-1]
                line[2] = "f\""+line[2]+"\""

            if str(line[2]).lower() == "f\"true\"":
                line[2] = True
            elif str(line[2]).lower() == "f\"false\"":
                line[2] = False

            line = line[0] + " = " + str(line[2])

        elif line.startswith("pause"):
            line = line.replace("pause ", "", 1)
            while "{" in line and "}" in line:
                variable = line[line.find("{") + 1:line.find("}")]
                debug("other", lineno(), f"Variable {variable} found in print.")
                try:
                    line = line.replace("{" + variable + "}", str(variable))
                except KeyError:
                    error(line_numbers, "ArgumentError",
                          f"The variable \"{variable}\" is not existing or has been declared later in the code.")
            line = "sleep("+line.replace("\n", "")+")"

        elif line.startswith("deletevar "):
            line = line.replace("deletevar ", "", 1)
            line = line[:-1] + " = None"

        elif line.startswith("break"):
            line = "break"

        else:
            line = ""

        for i in range(0, indentation_required):
            line = "\t"+line

        if compiling_style.lower() == "compacted" or compiling_style.lower() == "collapsed":
            if line.replace("\t", "") != "":
                compiled_file.write(line + "\n")
        else:
            compiled_file.write(line + "\n")

    line_numbers += 1

print(f"{bcolors.OKBLUE}Compiling time : {round((timeit.default_timer()-time_launch), process_time_round_numbers)}s{bcolors.ENDC}")
print(f"{bcolors.OKBLUE}File compiled using style \"{compiling_style}\".{bcolors.ENDC}")

# Disabled part, removes \n when too much
"""compiled_lines = compiled_file.readlines()
last_break = False
lines_to_pop = list()
for i in range(0, len(compiled_lines)-1):
    compiled_lines[i] = compiled_lines[i].replace("\t", "")
    if i > 0 and compiled_lines[i-1] == "\n" and compiled_lines[i] == "\n":
        lines_to_pop.append(i)

compiled_lines = compiled_file.readlines()
for i in range(0, len(lines_to_pop)-1):
    compiled_lines.pop(lines_to_pop[i])

compiled_file.writelines(compiled_lines)"""

compiled_file.close()
config_file.close()

if open_compiled_file == "True":
    print(f"{bcolors.OKGREEN}File is being opened.{bcolors.ENDC}")
    if platform.system() == "Windows":
        os.system("start "+compiled_file_filename)
    else:
        os.system("open "+shlex.quote(compiled_file_filename))
    print(f"{bcolors.OKGREEN}File opened successfully.{bcolors.ENDC}")
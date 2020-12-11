import inspect
import string
import re
from time import sleep
from random import randint
import sys
import json
from recurrent_classes import *
import os
import timeit
import platform
import shlex
import importlib

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

    elif config_line.startswith("open-compiled-file: "):
        config_line = config_line.replace("open-compiled-file: ", "", 1).replace("\n", "")
        open_compiled_file = config_line

    elif config_line.startswith("leave-comments-at-compiling: "):
        config_line = config_line.replace("leave-comments-at-compiling: ", "", 1).replace("\n", "")
        leave_comments_at_compiling = config_line

    elif config_line.startswith("compiling-style: "):
        config_line = config_line.replace("compiling-style: ", "", 1).replace("\n", "")
        compiling_style = config_line

    elif config_line.startswith("compile-ask-for-replace"):
        config_line = config_line.replace("compile-ask-for-replace: ", "", 1).replace("\n", "")
        compile_ask_for_replace = config_line

    """elif lines.startswith("process-time-round-numbers: "):
        lines = lines.replace("process-time-round-numbers: ", "")
        process_time_round_numbers = int(lines)"""
process_time_round_numbers = 6

if os.path.exists(compiled_file_filename) and compile_ask_for_replace == "True":
    confirm = input(f"{bcolors.FAIL}This file, located at \"{compiled_file_filename}\" already exists.\nDo you want to replace it ? (Yes/No) {bcolors.ENDC}")
    while confirm.lower() != "yes" and confirm.lower() != "no":
        print("Wrong answer.")
        confirm = input(
            f"{bcolors.FAIL}This file, located at \"{compiled_file_filename}\" already exists.\nDo you want to replace it ? (Yes/No) {bcolors.ENDC}")
    if confirm.lower() == "no":
        sys.exit()

time_launch = timeit.default_timer()

file_to_compile = file_to_compile.replace(".acpl\n", "").replace("\n", "")

code_file = open(file_to_compile, "r", encoding="utf-8")

# Code lines getting
code_lines = code_file.readlines()
debug("other", lineno(), 1, code_lines)

# Blank lines removing
debug("in", lineno(), 1, "Entrée dans la boucle pour retirer les commentaires et lignes vides des instructions.")
for i in range(0, len(code_lines)):
    result = code_lines[i].split(";")
    code_lines[i] = result[0]
debug("other", lineno(), 1, "code_lines = ", code_lines)

# Var container
variables_container = {}
used_libs = []

# Use variables
is_in_comment = False
line_numbers = 0
execute_until_endif = False
indentation_required = 0

compiled_file = open(compiled_file_filename, "w", encoding="utf-8")
compiled_file.write("# Compiled from ACPL programming language\n# Download from github : https://www.github.com/megat69/ACPL\n\nfrom time import sleep\nfrom random import randint\nfrom math import *\n\n")

while line_numbers < len(code_lines):
    line = code_lines[line_numbers]
    if "/*" in line:
        is_in_comment = True
    if "*/" in line:
        is_in_comment = False
        line_numbers += 1
        continue

    debug("other", line_numbers, 3, "Current line : ", line)

    if line.startswith("#") or "//" in line:
        if leave_comments_at_compiling == "True":
            line = re.sub("( )*#", "", line, 1)
            line = re.sub("( )*//", "", line, 1)
            line = "# "+line
            if code_lines[line_numbers-1].endswith("\n"):
                return_to_line = ""
            else:
                return_to_line = "\n"
            compiled_file.write(return_to_line+("\t"*indentation_required)+remove_suffix(line))
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
            """new_equation = line[line.find("<") + 1:line.find(">")]
            while "{" in new_equation and "}" in new_equation:
                variable = new_equation[new_equation.find("{") + 1:new_equation.find("}")]
                new_equation = new_equation.replace("{"+variable+"}", variable)
            line = line.replace("<"+equation+">", "{"+new_equation+"}")"""
            new_equation = equation.replace("{", "")
            new_equation = new_equation.replace("}", "")
            line = line.replace("<"+equation+">", "{"+new_equation+"}")

        while len(re.findall("\{[a-zA-Z]*\[len\]\}", line)) > 0 and re.findall("\{[a-zA-Z]*\[len\]\}", line)[0] in line:
            variable = line[line.find("{") + 1:line.find("[")]
            full_var = re.findall("\{[a-zA-Z]*\[len\]\}", line)[0]
            line = line.replace(str(full_var), "{len("+variable+")}")
        while "[{" in line and "}]" in line:
            variable = line[line.find("[") + 1:line.find("]")]
            full_var = line[line.find("{") + 1:line.find("[")]
            variable = variable.replace("{", "", 1)
            variable = variable.replace("}", "", 1)
            if variable == "len":
                line = line.replace("{"+full_var+"[{"+variable+"}]}", "{len("+full_var+")}")
            else:
                line = line.replace("[{"+variable+"}]", "["+variable+"]", 1)

        if line.startswith("$use: "):
            line = line.replace("$use: ", "", 1)
            line = remove_suffix(line, line.endswith("\n"))
            while line.endswith(" "):
                line = remove_suffix(line)
            used_libs.append("fx_"+line+".py")

        if line.startswith("function"):
            for i in range(0, indentation_required):
                line = "\t" + line
            indentation_required += 1
            line = remove_suffix(line, line.endswith("\n"))
            line = line.split(" ")
            line[0] = "def"
            temp_line = line[0] + " " + line[1] + "("
            if len(line) > 2:
                temp_line += line[2]
                if len(line) > 3:
                    for i in range(3, len(line)):
                        temp_line += ", " + line[i]
            temp_line += "):"
            line = temp_line
            del temp_line
            compiled_file.write(line + "\n")
            line_numbers += 1
            continue
        elif line.startswith("end func") or line.startswith("endfunc"):
            indentation_required -= 1
            line = ""

        if line.startswith("for"):
            indentation_required += 1
            line = remove_from_string(line, ["{", "}"])
            line = line.split(" ")
            line = f"for {line[1]} in range({line[2]}, {remove_suffix(line[3])}):"
            for i in range(0, indentation_required-1):
                line = "\t" + line
            compiled_file.write(line + "\n")
            line_numbers += 1
            continue
        elif line.startswith("endfor") or line.startswith("end for"):
            indentation_required -= 1
            line = ""

        if line.startswith("while"):
            for i in range(0, indentation_required):
                line = "\t" + line
            indentation_required += 1
            line = remove_suffix(line, condition=line.endswith("\n"))
            line += ":"
            while "{" in line and "}" in line:
                variable = line[line.find("{") + 1:line.find("}")]
                debug("other", lineno(), 2, f"Variable {variable} found in print.")
                try:
                    line = line.replace("{" + variable + "}", variable)
                except KeyError:
                    error(line_numbers, "ArgumentError", f"The variable \"{variable}\" is not existing or has been declared later in the code.")
            compiled_file.write(line + "\n")
            line_numbers += 1
            continue
        elif line.startswith("endwhile") or line.startswith("end while"):
            indentation_required -= 1
            line = ""

        if line.startswith("if"):
            for i in range(0, indentation_required):
                line = "\t" + line
            while "<" in line and ">" in line:
                equation = line[line.find("<") + 1:line.find(">")]
                while "{" in line and "}" in equation:
                    variable = equation[equation.find("{") + 1:equation.find("}")]
                    debug("other", lineno(), 2, f"Variable {variable} found in print.")
                    try:
                        line = line.replace("{" + variable + "}", variable)
                    except KeyError:
                        error(line_numbers, "ArgumentError",
                              f"The variable \"{variable}\" is not existing or has been declared later in the code.")
                debug("other", lineno(), 2, f"Equation {equation} found.")
                try:
                    line = line.replace(f"<{str(equation)}>", "{" + equation + "}")
                except KeyError:
                    error(line_numbers, "ArgumentError",
                          f"The equation \"{equation}\" is not existing or has been declared later in the code.")

            while "{" in line and "}" in line:
                variable = line[line.find("{") + 1:line.find("}")]
                debug("in", lineno(), 2, f"Variable {variable} found in print.")
                try:
                    line = line.replace("{" + variable + "}", variable)
                except KeyError:
                    error(line_numbers, "ArgumentError", f"The variable \"{variable}\" is not existing")

            line = remove_suffix(line) + ":"
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
            line = remove_suffix(line, condition=line.endswith("\n"))
            line = "print(f\""+line+"\")"

        elif line.startswith("var"):
            line = line.replace("var", "", 1)
            var_type = None
            var_action = None
            var_parameters = None

            do_regroup = True

            if line.startswith(":"):
                if line.startswith(":int"):
                    var_type = 'int'
                elif line.startswith(":float"):
                    var_type = 'float'
                elif line.startswith(":list"):
                    var_type = 'list'
                else:
                    var_type = 'str'
                line = line.replace(":"+var_type, "", 1)
            if line.startswith(" "):
                line = line.replace(" ", "", 1)

            if line.startswith("--"):
                if line.startswith("--lowercase"):
                    var_action = "lowercase"
                elif line.startswith("--uppercase"):
                    var_action = "uppercase"
                elif line.startswith("--round:"):
                    var_action = "round"
                    var_parameters = [re.search('--round:\d*', line).group(0)]
                elif line.startswith("--ceil"):
                    var_action = "ceil"
                elif line.startswith("--replace:"):
                    var_action = "replace"
                    var_parameters = re.findall('\'([^\']*)\'', line[:-1].replace("--replace:", "", 1))
                elif line.startswith("--split:"):
                    var_action = "split"
                    var_parameters = re.findall('--split:\'.*\'', line[:-1])
                    var_parameters[0] = var_parameters[0].replace("--split:", "", 1)


                if var_parameters is None:
                    line = line.replace("--"+var_action, "", 1)
                elif var_action == "replace":
                    var_parameters_to_str = ""
                    for param in var_parameters:
                        var_parameters_to_str += "\"" + param + "\""
                    line = line.replace("--" + var_action + ":" + var_parameters_to_str, "", 1)
                else:
                    var_parameters_to_str = ""
                    for param in var_parameters:
                        var_parameters_to_str += param
                    line = line.replace("--" + var_action + ":" + var_parameters_to_str, "", 1)
                if line.startswith(" "):
                    line = line.replace(" ", "", 1)

            line = line.split(" ")  # Result : [name, var_operator, content]

            if var_parameters is not None:
                if var_action != "split":
                    line.pop(0)
                line[2] = remove_suffix(line[2], line[2].endswith("\n"))

            if str(line[2]).startswith("input"):
                line[2] = line[2].replace("input", "", 1)
                for i in range(3, len(line)):
                    line[2] = line[2] + " " + line[i]
                line[2] = remove_suffix(line[2], line[2].endswith("\n"))
                line[2] = "input(f\""+line[2].replace(" ", "", 1)+"\")"
                do_regroup = False

            elif str(line[2]).startswith("random"):
                line[2] = line[2].replace("random", "", 1)
                for i in range(3, len(line) - 1):
                    line[2] = line[2] + " " + line[i]

                if len(line) == 4:
                    rand_min = "0"
                    rand_max = line[3].replace(",", "")
                else:
                    rand_min = line[3].replace(",", "")
                    rand_max = line[4]

                line[2] = "randint(int("+rand_min+"), int("+remove_suffix(rand_max)+"))"

                while "{" in line[2] and "}" in line[2]:
                    variable = line[2][line[2].find("{") + 1:line[2].find("}")]
                    debug("other", lineno(), 2, f"Variable {variable} found in print.")
                    try:
                        line[2] = line[2].replace("{" + variable + "}", variable)
                    except KeyError:
                        error(line_numbers, "ArgumentError",
                              f"The variable \"{variable}\" is not existing or has been declared later in the code.")
                do_regroup = False

            elif var_type == "list":
                # Recombination of line vars in a single line
                for i in range(3, len(line)):
                    line[2] = line[2] + " " + line[i]

                # Initializing list elements
                list_elements = []
                if "list." not in line[2]:
                    while "[" in line[2] and "]" in line[2]:
                        errors_count = 0
                        variable = line[2][line[2].find("[") + 1:line[2].find("]")]
                        debug("other", lineno(), 2, f"List element {variable} found.")
                        try:
                            line[2] = line[2].replace("[" + variable + "]", "")
                        except KeyError:
                            error(line_numbers, "ArgumentError",
                                  f"An error occured while trying to parse the list \"{line[0]}\".")
                            errors_count += 1
                        if errors_count >= 10:
                            print(
                                f"\n\n{bcolors.FAIL}Debug has chosen to stop this program due to too many errors. Sorry for the inconvenicence.{bcolors.ENDC}")
                            line_numbers = len(code_lines)
                            break
                        list_elements.append(variable)
                    # Dememorizing 'variable'
                    del variable

                    line[2] = list_elements
                    var_type = "list"
                    do_regroup = False
                elif line[2].startswith("list.add"):
                    line[2] = line[2].replace("list.add ", "", 1)
                    line[2] = remove_suffix(line[2], line[2].endswith("\n"))
                    line = line[0]+".append(f\""+line[2]+"\")"
                    do_regroup = False
                elif line[2].startswith("list.insert"):
                    line[2] = line[2].replace("list.insert ", "", 1)
                    index = re.findall("\d*", str(line[2]))[0]
                    line[2] = line[2].replace(index+" ", "", 1)
                    line[2] = remove_suffix(line[2], line[2].endswith("\n"))
                    line = line[0]+".insert("+index+", f\""+line[2]+"\")"
                    do_regroup = False
                elif line[2].startswith("list.remove"):
                    line[2] = line[2].replace("list.remove ", "", 1)
                    index = re.findall("\d*", str(line[2]))[0]
                    line = line[0]+".pop("+index+")"
                    do_regroup = False

            else:
                try:
                    if "." not in str(line[2]):
                        line[2] = int(line[2])
                    elif re.search("\d*", str(line[2]).replace(".", "")).group(0) == str(line[2]):
                        line[2] = float(line[2])
                except ValueError:
                    try:
                        line[2] = float(line[2])
                    except ValueError:
                        line[2] = str(line[2])


            if do_regroup:
                for i in range(3, len(line)):
                    line[2] += " "+line[i]


            if not isinstance(line[2], bool) and not isinstance(line[2], list):
                try:
                    line[2] = int(line[2])
                except ValueError:
                    try:
                        line[2] = float(line[2])
                    except ValueError:
                        pass


            if isinstance(line[2], str) and not line[2].startswith("input") and not line[2].startswith("randint") and not isinstance(line, str):
                line[2] = remove_suffix(line[2], line[2].endswith("\n"))
                line[2] = "f\""+line[2]+"\""

            if str(line[2]).lower() == "f\"true\"":
                line[2] = True
            elif str(line[2]).lower() == "f\"false\"":
                line[2] = False

            if var_action == "lowercase":
                line[2] = str(line[2]) + ".lower()"
            elif var_action == "uppercase":
                line[2] = str(line[2]) + ".upper()"
            elif var_action == "round":
                line[2] = f"round(float({line[2]}), {int(var_parameters[0].replace('--round:', ''))})"
            elif var_action == "ceil":
                line[2] = f"ceil({line[2]})"
            elif var_action == "replace":
                if len(var_parameters) == 1:
                    var_parameters.append("")
                if len(var_parameters) == 3:
                    var_parameters[2] = int(var_parameters[2])
                    # Replaces from line : <search> <replace with> <count>
                    line[2] = f"{line[2]})\n{line[0]} = {line[0]}.replace(\"{var_parameters[0]}\", \"{var_parameters[1]}\", {var_parameters[2]}"
                else:
                    line[2] = f"{line[2]})\n{line[0]} = {line[0]}.replace(\"{var_parameters[0]}\", \"{var_parameters[1]}\""
            elif var_action == "split":
                line[2] = f"{line[0]}.split(f{var_parameters[0]})"

            if ("append" in line or "insert" in line or "pop" in line) and var_type == "list":
                line = line
            elif var_type == "list":
                line = line[0] + " " + line[1] + " " + str(line[2])
            elif var_type is not None:
                line = line[0] + " " + line[1] + " " + var_type + "(" + str(line[2]) + ")"
            else:
                line = line[0] + " " + line[1] + " " + str(line[2])

        elif line.startswith("pause"):
            line = line.replace("pause ", "", 1)
            while "{" in line and "}" in line:
                variable = line[line.find("{") + 1:line.find("}")]
                debug("in", lineno(), 2, f"Variable {variable} found in print.")
                try:
                    line = line.replace("{" + variable + "}", str(variable))
                except KeyError:
                    error(line_numbers, "ArgumentError",
                          f"The variable \"{variable}\" is not existing or has been declared later in the code.")
            line = "sleep("+line.replace("\n", "")+")"

        elif line.startswith("deletevar "):
            line = line.replace("deletevar ", "", 1)
            line = "del " + remove_suffix(line)

        elif line.startswith("break"):
            line = "break"

        elif line.startswith("continue"):
            line = "continue"

        elif line.startswith("use_function"):
            line = line.replace("use_function ", "", 1)
            line = remove_suffix(line, line.endswith("\n"))
            line = remove_from_string(line, ["{", "}"])
            line = line.split(" ")
            temp_line = line[0] + "("
            if len(line) > 1:
                temp_line += line[1]
                if len(line) > 2:
                    for i in range(2, len(line)):
                        temp_line += ", " + line[i]
            temp_line += ")"
            line = temp_line
            del temp_line

        elif line.startswith("lib"):
            line = line.replace("lib ", "", 1)
            files = os.listdir('acpl_libs')
            import acpl_libs

            for file in files:
                if ".py" in file and file in used_libs:
                    file = file.replace(".py", "")
                    importlib.import_module("acpl_libs." + file)
            result = (None, None)
            for i in dir(acpl_libs):
                item = getattr(acpl_libs, i)
                if i.startswith("fx_"):
                    requirements = item.requirements("compiler")
                    requirements_list = list()
                    for element in requirements:
                        requirements_list.append(globals()[element])
                    del requirements
                    requirements_list = tuple(requirements_list)
                    result = item.pytranslation(line, requirements_list)
                    line = result[0]
                    if len(result) > 1:
                        for i in range(0, len(result[1]), 2):
                            globals()[result[1][i]] = result[1][i + 1]

        else:
            line = ""

        for i in range(0, indentation_required):
            line = "\t"+line

    compiling_style = "FORCED ATM. DUH"
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

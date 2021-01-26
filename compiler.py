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
import acpl_libs
import sys


print(bcolors.OKBLUE + texts.compiler["StartingCompilation"] + bcolors.ENDC)

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

    elif config_line.startswith("optimize-transpiled-file"):
        config_line = config_line.replace("optimize-transpiled-file: ", "", 1).replace("\n", "")
        optimize_transpiled_file = config_line.lower() != "false"

    """elif lines.startswith("process-time-round-numbers: "):
        lines = lines.replace("process-time-round-numbers: ", "")
        process_time_round_numbers = int(lines)"""
process_time_round_numbers = 6
config_file.close()

# If opened with command line arguments (python compiler.py <file_to_compile> [compiled_file_filename])
if len(sys.argv) > 1:
    file_to_compile = sys.argv[1]
    if not file_to_compile.endswith(".acpl"):
        file_to_compile += ".acpl"
    if ":" not in file_to_compile:
        file_to_compile = os.getcwd()+"/"+file_to_compile

    if len(sys.argv) > 2:
        compiled_file_filename = sys.argv[2]
    else:
        compiled_file_filename = sys.argv[1]

    if not compiled_file_filename.endswith(".py"):
        compiled_file_filename += ".py"
    if ":" not in compiled_file_filename:
        compiled_file_filename = os.getcwd()+"/"+compiled_file_filename

if os.path.exists(compiled_file_filename) and compile_ask_for_replace == "True":
    # This file, located at \"{compiled_file_filename}\" already exists.\nDo you want to replace it ?
    confirm = input(f"{bcolors.FAIL}{texts.compiler['CompilingConfirmation'].format(compiled_file_filename=compiled_file_filename)} (Yes/No) {bcolors.ENDC}")
    while confirm.lower() != "yes" and confirm.lower() != "no":
        print(texts.compiler["WrongAnswer"])
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
variables = {
    "length": {},
    "true": True,
    "false": False
}
used_libs = []

# Use variables
is_in_comment = False
line_numbers = 0
execute_until_endif = False
indentation_required = 0
aliases = {
    "print": [],
    "var": [],
    "pause": [],
    "deletevar": [],
    "$use": [],
    "function": [],
    "use_function": [],
    "if": [],
    "while": [],
    "for": [],
    "break": [],
    "continue": []
}
variables = {}

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

        # Built-in var "length"
        while "{length[" in line:
            temp = line[line.find("{length[") + 1:line.find("]}")].replace("length[", "", 1)
            line = line.replace("{length[" + temp + "]}", "{''.join(str(len("+temp+")) if isinstance("+temp+", list) else str(len(str("+temp+"))))}")

        while "<" in line and ">" in line and not line.startswith("if") and not line.startswith("while"):
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

        if line.startswith("$alias "):
            line = line.replace("$alias ", "", 1)
            line = line.split(" ")
            # line[0] : Function to which alias is given ; line[1] : alias
            if len(line) != 2:
                error(line_numbers, "ArgumentError",
                      texts.errors["FunctionArgumentError"].format(args_required=2, args_nbr=len(line)))

            line[1] = remove_suffix(line[1], line[1].endswith("\n"))

            # Setting alias
            try:
                aliases[line[0]].append(line[1])
            except KeyError:
                error(line_numbers, "ArgumentError", f"Unknown function '{line[0]}'.")

            line_numbers += 1
            continue

        if line.startswith("$use: ") or line.split(" ")[0] in aliases["$use"]:
            if line.split(" ")[0] in aliases["$use"]:
                line = line.replace(aliases["$use"][aliases["$use"].index(line.split(" ")[0])]+": ", "")
            else:
                line = line.replace("$use: ", "", 1)
            line = remove_suffix(line, line.endswith("\n"))
            while line.endswith(" "):
                line = remove_suffix(line)
            used_libs.append("fx_"+line+".py")
            importlib.import_module("acpl_libs.fx_"+line)
            item = getattr(acpl_libs, "fx_"+line)
            requirements = item.libs_to_import()
            line = ""
            for element in requirements[0]:
                line += "import " + element + "\n"
            for element in requirements[1]:
                line += "from " + element[0] + " import " + element[1] + "\n"
            compiling_style = "standard"
            if compiling_style.lower() == "compacted" or compiling_style.lower() == "collapsed":
                if line.replace("\t", "") != "":
                    compiled_file.write(line + "\n")
            else:
                compiled_file.write(line + "\n")
            line_numbers += 1
            continue

        if line.startswith("function") or line.split(" ")[0] in aliases["function"]:
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

        if line.startswith("for") or line.split(" ")[0] in aliases["for"]:
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

        if line.startswith("while") or line.split(" ")[0] in aliases["while"]:
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
                    # The variable "{variable}" is not existing or has been declared later in the code.
                    error(line_numbers, "VariableNotFound", texts.errors["VariableNotFound"].format(variable=variable))
            compiled_file.write(line + "\n")
            line_numbers += 1
            continue
        elif line.startswith("endwhile") or line.startswith("end while"):
            indentation_required -= 1
            line = ""

        if line.startswith("if") or line.split(" ")[0] in aliases["if"]:
            for i in range(0, indentation_required-1):
                line = "\t" + line
            while "<" in line and ">" in line:
                equation = line[line.find("<") + 1:line.find(">")]
                while "{" in line and "}" in equation:
                    variable = equation[equation.find("{") + 1:equation.find("}")]
                    debug("other", lineno(), 2, f"Variable {variable} found in print.")
                    try:
                        line = line.replace("{" + variable + "}", variable)
                    except KeyError:
                        # The variable "{variable}" is not existing or has been declared later in the code.
                        error(line_numbers, "VariableNotFound", texts.errors["VariableNotFound"].format(variable=variable))
                debug("other", lineno(), 2, f"Equation {equation} found.")
                try:
                    line = line.replace(f"<{str(equation)}>", "{" + equation + "}")
                except KeyError:
                    # The variable "{variable}" is not existing or has been declared later in the code.
                    error(line_numbers, "VariableNotFound", texts.errors["VariableNotFound"].format(variable=variable))

            while "{" in line and "}" in line:
                variable = line[line.find("{") + 1:line.find("}")]
                debug("in", lineno(), 2, f"Variable {variable} found in print.")
                try:
                    line = line.replace("{" + variable + "}", variable)
                except KeyError:
                    # The variable "{variable}" is not existing or has been declared later in the code.
                    error(line_numbers, "VariableNotFound", texts.errors["VariableNotFound"].format(variable=variable))

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

        if line.startswith("print ") or line.split(" ")[0] in aliases["print"]:
            if line.split(" ")[0] in aliases["print"]:
                line = line.replace(aliases["print"][aliases["print"].index(line.split(" ")[0])]+" ", "")
            else:
                line = line.replace("print ", "", 1)
            line = remove_suffix(line, condition=line.endswith("\n"))
            line = "print(f\""+line+"\")"

        elif line.startswith("var") or line.split(" ")[0] in aliases["var"]\
                or line.split(" ")[0] in variables.keys() or line.split(":")[0] in variables.keys():
            if line.split(" ")[0] in aliases["var"]:
                line = line.replace(aliases["var"][aliases["var"].index(line.split(" ")[0])], "")
                var_type = None
            elif line.split(":")[0] in aliases["var"]:
                line = line.replace(aliases["var"][aliases["var"].index(line.split(":")[0])], "")
                var_type = None
            elif line.split(" ")[0] in variables.keys():
                temp_name = line.split(" ")[0]
                var_type = variables[temp_name]
                del temp_name
            else:
                line = line.replace("var", "", 1)
                var_type = None

            var_action = None
            var_parameters = None
            no_string = False

            do_regroup = True

            if line.startswith(":"):
                if line.startswith(":int"):
                    var_type = 'int'
                elif line.startswith(":float"):
                    var_type = 'float'
                elif line.startswith(":list"):
                    var_type = 'list'
                elif line.startswith(":bool"):
                    var_type = "bool"
                elif line.startswith(":str"):
                    var_type = "str"
                else:
                    error(line_numbers, "VarTypeError", f"Var type '{line.split(' ')[0].replace(':', '')}' does not exist.")
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

            # For var redefining, see if the user wants to change the types
            if ":" in line[0]:
                temp_name = line[0].split(":")[0]
                if line[0].startswith(f"{temp_name}:int"):
                    var_type = "int"
                elif line[0].startswith(f"{temp_name}:float"):
                    var_type = "float"
                elif line[0].startswith(f"{temp_name}:list"):
                    var_type = "list"
                elif line[0].startswith(f"{temp_name}:bool"):
                    var_type = "bool"
                elif line[0].startswith(f"{temp_name}:str"):
                    var_type = "str"
                else:
                    error(line_numbers, "VarTypeError",
                          f"Var type '{line[0].split(':')[1].split(' ')[0]}' does not exist.")
                line[0] = line[0].replace(":" + var_type, "", 1)
                line[0] = remove_prefix(line[0], line[0].startswith(" "))
                del temp_name

            if var_parameters is not None:
                if var_action != "split":
                    line.pop(0)
                line[2] = remove_suffix(line[2], line[2].endswith("\n"))

            is_lib = False

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
                        # The variable "{variable}" is not existing or has been declared later in the code.
                        error(line_numbers, "VariableNotFound", texts.errors["VariableNotFound"].format(variable=variable))
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
                            # An error occurred while trying to parse the list \"{line[0]}\".
                            error(line_numbers, "ListParsingError", texts.errors["ListParsingError"].format(line[0]))
                            errors_count += 1
                        if errors_count >= 10:
                            print("\n\n" + bcolors.FAIL + texts.compiler["Stop_TooManyErrors"] + bcolors.ENDC)
                            line_numbers = len(code_lines)
                            break
                        list_elements.append(variable)
                    # Dememorizing 'variable'
                    del variable

                    for i in range(len(list_elements)):
                        if list_elements[i].startswith("int:"):
                            list_elements[i] = list_elements[i].replace("int:", "", 1)
                            list_elements[i] = int(list_elements[i])
                        elif list_elements[i].startswith("float:"):
                            list_elements[i] = list_elements[i].replace("float:", "", 1)
                            list_elements[i] = float(list_elements[i])
                        elif list_elements[i].startswith("bool:"):
                            list_elements[i] = list_elements[i].replace("bool:", "", 1)
                            list_elements[i] = list_elements[i].lower() == "true"
                        elif list_elements[i].startswith("str:") or list_elements[i].startswith("string:"):
                            list_elements[i] = list_elements[i].replace("string:", "", 1)
                            list_elements[i] = list_elements[i].replace("str:", "", 1)

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

            elif str(line[2]).startswith("lib"):
                line[2] = recreate_string(line[2:len(line)], " ")
                line[2] = remove_suffix(line[2], line[2].endswith("\n"))
                do_regroup = False
                line[2] = line[2].replace("lib ", "", 1)
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
                        requirements = item.requirements("compiler_var_methods")
                        requirements_list = list()
                        for element in requirements:
                            requirements_list.append(locals()[element])
                        del requirements
                        requirements_list = tuple(requirements_list)
                        result = item.compiler_var_methods(line, requirements_list)
                        line = result[0]
                        if len(result) > 1:
                            for k in range(0, len(result[1]), 2):
                                locals()[result[1][k]] = result[1][k + 1]

            elif recreate_string(line[2:len(line)], " ").startswith("var_action"):
                line[2] = recreate_string(line[2:len(line)], " ").replace("var_action ", "", 1)
                do_regroup = False
                if line[2].startswith("lowercase"):
                    var_action = "lowercase"
                    line[2] = line[2].replace("lowercase ", "", 1)
                elif line[2].startswith("uppercase"):
                    var_action = "uppercase"
                    line[2] = line[2].replace("uppercase ", "", 1)
                elif line[2].startswith("round"):
                    var_action = "round"
                    line[2] = line[2].replace("round ", "", 1)
                    try:
                        var_parameters = [int(line[2].split(" ")[0])]
                    except ValueError:
                        error(line_numbers, "ArgumentError", texts.errors["ArgumentNotInt"])
                    line[2] = line[2].replace(f"{var_parameters[0]} ", "", 1)
                elif line[2].startswith("ceil"):
                    var_action = "ceil"
                    line[2] = line[2].replace("ceil ", "", 1)
                elif line[2].startswith("replace"):
                    # Syntax :
                    # var_action replace <str_to_search> with <str_to_use> for [times=INFINITE] in <str>
                    var_action = "replace2"
                    line[2] = line[2].replace("replace ", "", 1)
                    temp_params = line[2].split(" in ")[0]
                    temp_params = temp_params.strip()
                    if not "for" in temp_params:
                        var_parameters = [
                            remove_suffix(temp_params.split("with")[0], temp_params.split("with")[0].endswith(" ")),
                            temp_params.split("with")[1].strip()
                        ]
                    else:
                        try:
                            var_parameters = [
                                remove_suffix(temp_params.split("with")[0], temp_params.split("with")[0].endswith(" ")),
                                temp_params.split("with")[1].split("for")[0].strip(),
                                int(temp_params.split("for")[1].strip())
                            ]
                        except ValueError:
                            error(line_numbers, "ArgumentError", texts.errors["ArgumentNotInt"])
                        line[2] = line[2].replace("for ", "", 1)

                    line[2] = line[2].replace("with ", "", 1)

                    # Error :
                    if len(var_parameters) < 2:
                        error(line_numbers, "ArgumentError",
                              texts.console["FunctionArgumentError"].format(args_required="2/3",
                                                                            args_nbr=len(var_parameters)))

                    for element in var_parameters:
                        line[2] = line[2].replace(str(element), "", 1)
                    line[2] = line[2].replace("in", "", 1)
                    line[2] = line[2].strip()
                elif line[2].startswith("split"):
                    var_action = "split"
                    line[2] = line[2].replace("split ", "", 1)
                    var_parameters = [remove_suffix(line[2].split("in")[0], line[2].split("in")[0].endswith(" "))]
                    line[2] = line[2].replace(var_parameters[0], "", 1)
                    line[2] = line[2].replace("in", "", 1)
                    line[2] = line[2].strip()
                else:
                    error(line_numbers, "ArgumentError", f"Var action '{line[2].split(' ')[0]}' does not exist !")

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

            if var_type == "bool":
                if str(line[2]).lower() == "true":
                    line[2] = "True"
                elif str(line[2]).lower() == "false":
                    line[2] = "False"
                do_regroup = False

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


            if isinstance(line[2], str) and not line[2].startswith("input") and not line[2].startswith("randint")\
                    and not isinstance(line, str) and is_lib is False and no_string is False:
                line[2] = remove_suffix(line[2], line[2].endswith("\n"))
                line[2] = "f\""+line[2]+"\""

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
            elif var_action == "replace2":
                if len(var_parameters) == 1:
                    var_parameters.append("")
                if len(var_parameters) == 3:
                    var_parameters[2] = int(var_parameters[2])
                    # Replaces from line : <search> <replace with> <count>
                    line[2] = f"{line[2]}\n{line[0]} = {line[0]}.replace(\"{var_parameters[0]}\", \"{var_parameters[1]}\", {var_parameters[2]})"
                else:
                    line[2] = f"{line[2]}\n{line[0]} = {line[0]}.replace(\"{var_parameters[0]}\", \"{var_parameters[1]}\")"
            elif var_action == "split":
                line[2] = f"{line[0]}.split(f{var_parameters[0]})"

            # Adding var name for redefintions
            if is_lib is False:
                variables[line[0]] = var_type if var_type is not None else "str"

            if (("append" in line or "insert" in line or "pop" in line) and var_type == "list") or is_lib is True:
                pass
            elif var_type == "list":
                line = line[0] + " " + line[1] + " " + str(line[2])
            elif var_type is not None:
                line = line[0] + " " + line[1] + " " + var_type + "(" + str(line[2]) + ")"
            else:
                line = line[0] + " " + line[1] + " " + str(line[2])

        elif line.startswith("pause") or line.split(" ")[0] in aliases["pause"]:
            if line.split(" ")[0] in aliases["pause"]:
                line = line.replace(aliases["pause"][aliases["pause"].index(line.split(" ")[0])]+" ", "")
            else:
                line = line.replace("pause ", "", 1)
            while "{" in line and "}" in line:
                variable = line[line.find("{") + 1:line.find("}")]
                debug("in", lineno(), 2, f"Variable {variable} found in print.")
                try:
                    line = line.replace("{" + variable + "}", str(variable))
                except KeyError:
                    # The variable "{variable}" is not existing or has been declared later in the code.
                    error(line_numbers, "VariableNotFound", texts.errors["VariableNotFound"].format(variable=variable))
            line = "sleep("+line.replace("\n", "")+")"

        elif line.startswith("deletevar ") or line.split(" ")[0] in aliases["deletevar"]:
            if line.split(" ")[0] in aliases["deletevar"]:
                line = line.replace(aliases["deletevar"][aliases["deletevar"].index(line.split(" ")[0])]+" ", "")
            else:
                line = line.replace("deletevar ", "", 1)

            # If the user want to delete a single var (if) or multiple variables (else)
            if not "," in line:
                line = "del " + remove_suffix(line)
                print(line)
            else:
                # Removing all spaces (we don't need them)
                line = line.replace(" ", "")

                # Creating a list of all the vars to delete
                line = line.split(",")

                # Initializing line :
                temp_line = ""

                # Deleting all of them, one by one
                for i in range(len(line)):
                    line[i] = remove_suffix(line[i], line[i].endswith('\n'))
                    temp_line += f"del {line[i]}\n"
                line = temp_line
                del temp_line

        elif line.startswith("break"):
            line = "break"

        elif line.startswith("continue"):
            line = "continue"

        elif line.startswith("use_function") or line.split(" ")[0] in aliases["use_function"]:
            if line.split(" ")[0] in aliases["use_function"]:
                line = line.replace(aliases["use_function"][aliases["use_function"].index(line.split(" ")[0])]+" ", "")
            else:
                line = line.replace("$use: ", "", 1)
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
                        requirements_list.append(locals()[element])
                    del requirements
                    requirements_list = tuple(requirements_list)
                    result = item.pytranslation(line, requirements_list)
                    line = result[0]
                    if len(result) > 1:
                        for i in range(0, len(result[1]), 2):
                            locals()[result[1][i]] = result[1][i + 1]

        else:
            line = ""

        for i in range(0, indentation_required):
            line = "\t"+line

    compiling_style = "standard"
    if compiling_style.lower() == "compacted" or compiling_style.lower() == "collapsed":
        if line.replace("\t", "") != "":
            compiled_file.write(line + "\n")
    else:
        compiled_file.write(line + "\n")
    line_numbers += 1

print(f"{bcolors.OKBLUE}{texts.compiler['CompilingTime']} : {round((timeit.default_timer()-time_launch), process_time_round_numbers)}s{bcolors.ENDC}")
print(f"{bcolors.OKBLUE}{texts.compiler['FileCompiledWithStyle']} \"{compiling_style}\".{bcolors.ENDC}")

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

if optimize_transpiled_file is True:
    print(f"{bcolors.OKBLUE}Starting optimization...{bcolors.ENDC}")
    compiled_file = open(compiled_file_filename, "r", encoding="utf-8")
    code_lines = compiled_file.readlines()
    compiled_file.close()
    compiled_file = open(compiled_file_filename, "w", encoding="utf-8")
    #print(code_lines)
    # Fetching all code lines
    for i in range(len(code_lines)):
        line = code_lines[i]

        # Regex party
        for element in re.findall("int\([0-9]*\)", line):
            line = line.replace(element, remove_suffix(element.replace("int(", "")))

        for element in re.findall("float\([0-9.]*\)", line):
            line = line.replace(element, remove_suffix(element.replace("float(", "")))

        for element in re.findall("bool\(f\"(True|False)\"\)", line):
            line = line.replace(f"bool(f\"{element}\")", element)
        
        for element in re.findall("str\(f\".*\"\)", line):
            line = line.replace(element, remove_suffix(element.replace("str(", "")))

        code_lines[i] = line

    compiled_file.writelines(code_lines)
    compiled_file.close()
    print(f"{bcolors.OKGREEN}File successfully optimized.{bcolors.ENDC}")

if open_compiled_file == "True":
    print(bcolors.OKGREEN + texts.compiler['OpeningFile'] + bcolors.ENDC)
    if platform.system() == "Windows":
        os.system("start "+compiled_file_filename)
    else:
        os.system("open "+shlex.quote(compiled_file_filename))
    print(bcolors.OKGREEN + texts.compiler['FileOpened'] + bcolors.ENDC)

import importlib
import re
import timeit
from math import *
from random import randint
from time import sleep
from recurrent_classes import *
from copy import deepcopy
import psutil

time_launch = timeit.default_timer()
final_filename = ""

# Files opening
try:
    filename_file = open("startup.acpl-ini", "r+", encoding="utf-8")
except FileNotFoundError:
    print(texts.critic_errors["ImpossibleLoad_StartupIni"])
    sys.exit()

command_line_args = deepcopy(sys.argv)
try:
    command_line_args.pop(0)
except IndexError:
    command_line_args = []

filename = filename_file.readlines()
for lines in filename:
    if lines.startswith("filename: "):
        if len(command_line_args) == 0:  # If there is no command line argument
            lines = lines.replace("filename: ", "")
            if lines.endswith("\n"):
                lines = lines.replace("\n", "")
            if not lines.endswith(".acpl"):
                lines += ".acpl"
            final_filename = lines
        else:  # If there is an argument, it is the filename
            if not command_line_args[0].endswith(".acpl"):
                command_line_args[0] += ".acpl"
            command_line_args[0] = lines

    if lines.startswith("debug-state: "):
        lines = lines.replace("debug-state: ", "")
        debug_const = int(lines)

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

    if lines.startswith("debugger-enabled: "):
        lines = lines.replace("debugger-enabled: ", "")
        lines = remove_suffix(lines, lines.endswith("\n"))
        debug_acpl_program = lines.lower() == "true"
        replace_line("startup.acpl-ini", 14, "debugger-enabled: False\n")


code_file = open(final_filename, "r", encoding="utf-8")

# Code lines getting
code_lines = code_file.readlines()
debug("other", lineno(), 2, code_lines)

# Blank lines removing -> This loop is there since Alpha0.2 (nostalgia)
debug("in", lineno(), 3, "Entering loop to remove blank lines and comments.")
for i in range(0, len(code_lines)):
    result = code_lines[i].split("#")
    code_lines[i] = result[0]
    result = code_lines[i].split("//")
    code_lines[i] = result[0]
    result = code_lines[i].split(";")
    code_lines[i] = result[0]
debug("other", lineno(), 3, "code_lines = ", code_lines)

# Var container
variables_container = {
    "length": {},
    "true": True,
    "false": False
}
used_libs = []
functions = {}
aliases = {
    "print": [],
    "var": [],
    "pause": [],
    "deletevar": [],
    "$use": [],
    "function": [],
    "use_function": [],
    "while": [],
    "if": [],
    "for": [],
    "break": [],
    "continue": []
}

# Use variables
is_in_comment = False
line_numbers = 0
execute_until_endif = {-1: False, 0: False}
in_for = False
is_breaking = False
wait_next_loop = False
in_while = False
indent = 0
function_line_numbers = 0
if "process_time_round_numbers" not in globals() and "process_time_round_numbers" not in locals():
    process_time_round_numbers = 6
built_in_vars = deepcopy(variables_container)

# Undefined variables
last_condition = {0: None}
for_var = None
for_max = None
for_line_number = None
while_condition = None
while_line = None
skip_while = False
in_function = False
function_name = None

# TODO :
# DONE :
# Translations
# Files lib
# Lib access to variables (input-like methods)
# GUI Lib
# Deletevar : Delete multiple variables at once
# Var actions alias
# Built-in variable of type 'dict' containing every variable's length
# ls/dir command
# Aliases
# Full booleans implementation, with new type ':bool'
# Var modifications, without re-assignment (simple var name typing)
# Compiler + Transpiler

# Order :
# Video changelogs

# 3.12
# Re-do equations in 'if' and 'while'
# ifs and whiles variables -> add quotes if string.
# Better compiler
# Lambdas
# Clipboard lib -> pyperclip lib

# DELAYED :
# Line numbers in functions
# Full use of lists in functions
# GUI IDE

# MAYBE IN THE FUTURE
# 1) 'os.acpl-ini', with different vars, depending on the operating systems.
# 2) return

# SCRAPPED AT THE MOMENT
# Automatic quotes
# try/except
# EXE version

# KNOWN BUGS
# Ares variables O_o

while line_numbers < len(code_lines):
    line = code_lines[line_numbers]
    og_line = code_lines[line_numbers]
    debug("other", lineno(), 2, "Line number : ", line_numbers)
    if "/*" in line:
        is_in_comment = True
    if "*/" in line:
        is_in_comment = False
        line_numbers += 1
        continue
    if not is_in_comment:
        line = line.replace("\t", "")

        errors_count = 0

        while "{" in line and "}" in line and not in_function:
            variable = line[line.find("{") + 1:line.find("}")]
            debug("in", lineno(), 2, f"Variable {variable} found.")

            # Detect if the variable is a list or not
            if "[" in variable:  # Then it is a list
                # We get the list index
                list_index = variable[variable.find("["):]
                # If it starts with an unnecessary bracket, we remove it
                list_index = remove_prefix(list_index, list_index.startswith("["))

                # We define an unmodified variable so we can replace it,
                # and we define another var without the list index
                og_variable, variable = variable, variable.replace("["+list_index+"]", "", 1)
                # Same goes on for list_index
                og_list_index = list_index

                # If the list index is a variable, (because it starts with a '{'), we replace it with the variable
                if list_index.startswith("{"):
                    og_list_index += "}"
                    list_index = remove_prefix(list_index, list_index.startswith("{"))
                    try:  # We replace it with the variable
                        list_index = variables_container[list_index]
                    except KeyError:  # If the index doesn't exist
                        # The index '{}' seems not to exist
                        error(line_numbers, "UnexistingIndexError", texts.errors["UnexistingIndexError"].format(list_index))
                    variable = variable[0:variable.find("[")]

                # Remove the list_index from the variable
                variable = variable.replace("["+og_list_index, "", 1)

                # If the list index ends with an unnecessary ']', then we remove it
                try:
                    list_index = remove_suffix(list_index, list_index.endswith("]"))
                except AttributeError:  # If 'list_index' is already an integer
                    pass

                if not str(list_index).startswith("len"):
                    try:
                        line = line.replace("{"+og_variable+"}]}", str(variables_container[variable][int(list_index)]), 1)
                        line = line.replace("{"+og_variable+"}", str(variables_container[variable][int(list_index)]), 1)
                    except ValueError as e:
                        if variable in built_in_vars.keys():
                            line = line.replace("{" + og_variable + "}]}", str(variables_container[variable][list_index]), 1)
                            line = line.replace("{" + og_variable + "}", str(variables_container[variable][list_index]), 1)
                        else:
                            error(line_numbers, "VarNameError", "List index cannot be string.")
                else:
                    line = line.replace("{" + og_variable + "}]}", str(len(variables_container[variable])), 1)
                    line = line.replace("{" + og_variable + "}", str(len(variables_container[variable])), 1)

            else:  # If it is a standard variable
                try:
                    # We try to replace the variable asked with its content
                    line = line.replace("{"+variable+"}", str(variables_container[variable]), 1)
                except KeyError:
                    # The variable was not found, throwing an error.
                    # The variable "{variable}" seems not to exist.
                    error(line_numbers, "VarNotFoundError", texts.errors["VarNotFoundError"].format(variable=variable))

        while "<" in line and ">" in line and not in_function and not line.startswith("if") and not line.startswith("while"):
            equation = line[line.find("<") + 1:line.find(">")]
            debug("other", lineno(), 2, f"Equation {equation} found in print.")
            try:
                line = line.replace(f"<{str(equation)}>", str(eval(str(equation))))
            except KeyError:
                # The variable "{variable}" is not existing or has been declared later in the code.
                error(line_numbers, "VariableNotFound", texts.errors["VariableNotFound"].format(variable=variable))
                errors_count += 1
            if errors_count >= 100:
                # Debug has chosen to stop this program due to too many errors. Sorry for the inconvenience.
                print("\n\n" + bcolors.FAIL + texts.main["ProgramStopped_Errors"] + bcolors.ENDC)
                break

        debug("other", line_numbers, 3, f"line : {line}")

        if line.startswith("$alias "):
            line = line.replace("$alias ", "", 1)
            line = line.split(" ")
            # line[0] : Function to which alias is given ; line[1] : alias
            if len(line) != 2:
                error(line_numbers, "ArgumentError", texts.errors["FunctionArgumentError"].format(args_required=2, args_nbr=len(line)))

            line[1] = remove_suffix(line[1], line[1].endswith("\n"))

            # Setting alias
            try:
                aliases[line[0]].append(line[1])
            except KeyError:
                error(line_numbers, "ArgumentError", f"Unknown function '{line[0]}'.")

            if debug_acpl_program is True:
                print(f"{bcolors.WARNING}'{bcolors.OKGREEN}{line[1]}{bcolors.WARNING}' has been defined as '{bcolors.OKGREEN}{line[0]}{bcolors.WARNING}' alias.{bcolors.ENDC}")

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

        if line.startswith("function") or line.split(" ")[0] in aliases["function"]:
            if line.split(" ")[0] in aliases["function"]:
                line = line.replace(aliases["function"][aliases["function"].index(line.split(" ")[0])]+" ", "")
            else:
                line = line.replace("function ", "", 1)
            in_function = True
            function_header = line.replace("function ", "", 1).split(" ")
            function_header[-1] = remove_suffix(function_header[-1], condition=function_header[-1].endswith("\n"))

            function_name = function_header[0]
            function_name = remove_suffix(function_name, condition=function_name.endswith("\n"))
            functions[function_name] = {}
            functions[function_name]["lines"] = []

            # Parameters
            functions[function_name]["parameters"] = []
            for i in range(1, len(function_header)):
                functions[function_name]["parameters"].append(function_header[i])

            line_numbers += 1
            continue
        elif line.startswith("endfunc") or line.startswith("end func"):
            in_function = False
            del function_name
            line_numbers += 1
            continue

        if in_function:
            functions[function_name]["lines"].append(line)

        debug("in", lineno(), 1, "In function : ", in_function)

        if not in_function:
            if line.startswith("use_function ") or line.split(" ")[0] in aliases["use_function"]:
                if line.split(" ")[0] in aliases["use_function"]:
                    line = line.replace(aliases["use_function"][aliases["use_function"].index(line.split(" ")[0])]+" ", "")
                else:
                    line = line.replace("use_function ", "", 1)
                debug("in", line_numbers, 3, "Functions : ", functions)
                line = remove_suffix(line, condition=line.endswith("\n"))

                function_name = line.split(" ")[0]
                function_arguments = line.split(" ")
                function_arguments.pop(0)

                # Check for lists in arguments
                for i in range(len(function_arguments)):
                    if function_arguments[i].startswith("list:"):
                        function_arguments[i] = function_arguments[i].replace("list:", "", 1)
                        function_arguments[i] = variables_container[function_arguments[i]]

                if len(functions[function_name]["parameters"]) != len(function_arguments):
                    # {len(functions[function_name]['parameters'])} arguments required, got {len(function_arguments)}.
                    error(line_numbers, "FunctionArgumentError", texts.errors["FunctionArgumentError"].format(args_required=len(functions[function_name]['parameters']), args_nbr=len(function_arguments)))

                # Adding lines
                for i in range(len(functions[function_name]["lines"])):
                    for k in range(len(function_arguments)):  # Replacing the parameters of the function with the arguments
                        try:
                            functions[function_name]["lines"][i] = functions[function_name]["lines"][i].replace("{"+functions[function_name]["parameters"][k]+"}", str(function_arguments[k]))
                        except IndexError:
                            pass
                    try:
                        code_lines.insert(line_numbers+i+1, functions[function_name]["lines"][i])
                    except IndexError:
                        pass

                code_lines.pop(line_numbers)

                if debug_acpl_program is True:
                    # Created function '{bcolors.WARNING}{function_name}{bcolors.OKBLUE}' with arguments :
                    # {bcolors.OKGREEN}{recreate_string(function_arguments, ', ')}{bcolors.OKBLUE} on line {line_numbers}.
                    print(bcolors.OKBLUE +
                          texts.acpl_debugger["CreatedFunction"].format(WARNING=bcolors.WARNING,
                                                                                         function_name=function_name,
                                                                                         OKBLUE=bcolors.OKBLUE,
                                                                                         OKGREEN=bcolors.OKGREEN,
                                                                                         recreate_string=recreate_string(function_arguments, ', '),
                                                                                         line_numbers=line_numbers) + bcolors.ENDC)

                debug("other", lineno(), 2, "Code lines : ", code_lines)
                continue

            if line.startswith("if ") or line.split(" ")[0] in aliases["if"]:
                if line.split(" ")[0] in aliases["if"]:
                    line = line.replace(aliases["if"][aliases["if"].index(line.split(" ")[0])]+" ", "")
                else:
                    line = line.replace("if ", "", 1)
                if eval(line) is True and all(value == False for value in execute_until_endif.values()):
                    execute_until_endif[indent] = False
                    if debug_acpl_program is True:
                        # Condition '{bcolors.ENDC}{line}{bcolors.OKBLUE}' on line {line_numbers} marked as
                        # {bcolors.OKGREEN}True
                        print(bcolors.OKBLUE + texts.acpl_debugger["ConditionTrue"].format(ENDC=bcolors.ENDC, line=line,
                                                                                           OKBLUE=bcolors.OKBLUE,
                                                                                           OKGREEN=bcolors.OKGREEN,
                                                                                           line_numbers=line_numbers)
                              + bcolors.ENDC)
                else:
                    execute_until_endif[indent] = True
                    if debug_acpl_program is True:
                        # Condition '{bcolors.ENDC}{line}{bcolors.OKBLUE}' on line {line_numbers} marked as
                        # {bcolors.FAIL}False
                        print(bcolors.OKBLUE + texts.acpl_debugger["ConditionFalse"].format(ENDC=bcolors.ENDC, line=line,
                                                                                           OKBLUE=bcolors.OKBLUE,
                                                                                           FAIL=bcolors.FAIL,
                                                                                           line_numbers=line_numbers)
                              + bcolors.ENDC)
                last_condition[indent] = line
                line_numbers += 1
                indent += 1
                continue
            # 'else' statement has been scrapped in version 3.10
            # elif line.startswith("else"):
            """if eval(last_condition[indent]) is False and all(value == True for value in execute_until_endif.values()):
                    execute_until_endif[indent] = False
                else:
                    execute_until_endif[indent] = True
                line_numbers += 1
                continue"""

            if line.startswith("while") or line.split(" ")[0] in aliases["while"]:
                if line.split(" ")[0] in aliases["while"]:
                    line = line.replace(aliases["while"][aliases["while"].index(line.split(" ")[0])]+" ", "")
                else:
                    line = line.replace("while ", "", 1)

                line = remove_suffix(line, line.endswith("\n"))
                while_condition = line
                in_while = True
                while_line = line_numbers
                if eval(while_condition) and is_breaking is False:
                    skip_while = False
                    if debug_acpl_program is True:
                        # Condition for while loop '{bcolors.ENDC}{line}{bcolors.OKBLUE}' on line {line_numbers} marked as
                        # {bcolors.OKGREEN}True
                        print(bcolors.OKBLUE + texts.acpl_debugger["WhileTrue"].format(ENDC=bcolors.ENDC, line=line,
                                                                                           OKBLUE=bcolors.OKBLUE,
                                                                                           OKGREEN=bcolors.OKGREEN,
                                                                                           line_numbers=line_numbers)
                              + bcolors.ENDC)
                else:
                    if debug_acpl_program is True:
                        # Condition for while loop '{bcolors.ENDC}{line}{bcolors.OKBLUE}' on line {line_numbers} marked as
                        # {bcolors.FAIL}False{bcolors.OKBLUE}\nSkipping loop.
                        print(bcolors.OKBLUE + texts.acpl_debugger["WhileFalse"].format(ENDC=bcolors.ENDC, line=line,
                                                                                           OKBLUE=bcolors.OKBLUE,
                                                                                           OKGREEN=bcolors.OKGREEN,
                                                                                           line_numbers=line_numbers)
                              + bcolors.ENDC)
                    skip_while = True
            elif line.startswith("endwhile") or line.startswith("end while"):
                if eval(while_condition) and is_breaking is False:
                    line_numbers = while_line
                    wait_next_loop = False
                    continue
                else:
                    in_while = False
                    skip_while = False
                    line_numbers += 1
                    wait_next_loop = False
                    if is_breaking:
                        is_breaking = False
                    continue

            if line.startswith("endif") or line.startswith("end if"):
                execute_until_endif[indent-1] = False
                line_numbers += 1
                indent -= 1
                continue

            if line.startswith("for") or line.split(" ")[0] in aliases["for"]:  # for <name> <min> <max>
                if line.split(" ")[0] in aliases["for"]:
                    line = line.replace(aliases["for"][aliases["for"].index(line.split(" ")[0])]+" ", "")
                else:
                    line = line.replace("for ", "", 1)
                in_for = True
                line = line.split(" ")
                try:
                    variables_container[line[0]] = int(line[1])
                except ValueError:
                    # Argument should be integer !
                    error(line_numbers, "ArgumentNotInt", texts.errors["ArgumentNotInt"])
                for_var = line[0]
                try:
                    for_max = int(line[2])
                except ValueError:
                    # Argument should be integer !
                    error(line_numbers, "ArgumentNotInt", texts.errors["ArgumentNotInt"])
                for_line_number = line_numbers + 1
                if debug_acpl_program is True:
                    # Looping {int(line[2])-int(line[1])} times using variable {bcolors.OKGREEN}{line[0]}
                    print(bcolors.OKBLUE + texts.acpl_debugger["ForLoop"].format(times=int(line[2])-int(line[1]),
                                                                                 OKGREEN=bcolors.OKGREEN,
                                                                                 line=line[0]) + bcolors.ENDC)
                line_numbers += 1
                continue

            if line.startswith("endfor") or line.startswith("end for"):
                line = remove_suffix(line, line.endswith("\n"))
                in_for = False
                wait_next_loop = False
                if is_breaking is False:
                    variables_container[for_var] += 1
                    if variables_container[for_var] < for_max:
                        line_numbers = for_line_number
                        continue
                    else:
                        variables_container.pop(for_var)
                else:
                    variables_container.pop(for_var)
                    is_breaking = False

            if (line.startswith("break") or line.split(" ")[0] in aliases["break"]) and execute_until_endif is False:
                is_breaking = True
                if debug_acpl_program is True:
                    # Breaking loop.
                    print(bcolors.OKBLUE + texts.acpl_debugger["break"] + bcolors.ENDC)

            if (line.startswith("continue") or line.split(" ")[0] in aliases["continue"]) and execute_until_endif is False:
                wait_next_loop = True
                if debug_acpl_program is True:
                    # Going to next loop.
                    print(bcolors.OKBLUE + texts.acpl_debugger["continue"] + bcolors.ENDC)

            if execute_until_endif[indent-1] is False and is_breaking is False and wait_next_loop is False and skip_while is False:
                if line.startswith("print") or line.split(" ")[0] in aliases["print"]:
                    if line.split(" ")[0] in aliases["print"]:
                        line = line.replace(aliases["print"][aliases["print"].index(line.split(" ")[0])]+" ", "")
                    else:
                        line = line.replace("print ", "", 1)

                    line = remove_suffix(line, line.endswith("\n"))
                    if debug_acpl_program is False:
                        print(line)
                    else:
                        print(f"{bcolors.OKGREEN} >>> \t{bcolors.ENDC}{line}")
                elif line.startswith("var") or line.split(" ")[0] in aliases["var"] or line.split(":")[0] in aliases["var"]\
                        or line.split(" ")[0] in variables_container.keys() or line.split(":")[0] in variables_container.keys():
                    if line.split(" ")[0] in aliases["var"]:
                        line = line.replace(aliases["var"][aliases["var"].index(line.split(" ")[0])], "")
                        var_type = None
                    elif line.split(":")[0] in aliases["var"]:
                        line = line.replace(aliases["var"][aliases["var"].index(line.split(":")[0])], "")
                        var_type = None
                    elif line.split(" ")[0] in variables_container.keys():
                        temp_name = line.split(" ")[0]
                        if isinstance(variables_container[temp_name], int):
                            var_type = "int"
                        elif isinstance(variables_container[temp_name], float):
                            var_type = "float"
                        elif isinstance(variables_container[temp_name], list):
                            var_type = None
                        elif isinstance(variables_container[temp_name], bool):
                            var_type = "bool"
                        else:
                            var_type = "str"
                        del temp_name
                    else:
                        line = line.replace("var", "", 1)
                        var_type = None

                    var_action = None
                    var_parameters = None
                    do_not_the_operator = False

                    if line.startswith(":"):
                        if line.startswith(":int"):
                            var_type = "int"
                        elif line.startswith(":float"):
                            var_type = "float"
                        elif line.startswith(":list"):
                            var_type = "list"
                        elif line.startswith(":bool"):
                            var_type = "bool"
                        elif line.startswith(":str"):
                            var_type = "str"
                        else:
                            error(line_numbers, "VarTypeError",f"Var type '{line.split(' ')[0].replace(':', '')}' does not exist.")
                        line = line.replace(":"+var_type, "", 1)
                    line = remove_prefix(line, line.startswith(" "))

                    if line.startswith("--"):
                        if line.startswith("--lowercase"):
                            var_action = "lowercase"
                        elif line.startswith("--uppercase"):
                            var_action = "uppercase"
                        elif line.startswith("--round:"):
                            var_action = "round"
                            var_parameters = [re.search('--round:\d*', line).group(0).replace("--round:", "")]
                        elif line.startswith("--ceil"):
                            var_action = "ceil"
                        elif line.startswith("--replace:"):
                            var_action = "replace"
                            var_parameters_temp = re.search('--replace:\".*\"', line).group(0).replace("--replace:", "")
                            var_parameters = re.findall('"([^"]*)"', var_parameters_temp)
                            del var_parameters_temp
                        elif line.startswith("--split:"):
                            var_action = "split"
                            var_parameters = [re.search('--split:\".*\"', line).group(0).replace("--split:", "")]


                        if var_parameters is None:
                            line = line.replace("--" + var_action, "", 1)
                        elif var_action == "replace":
                            var_parameters_to_str = ""
                            for param in var_parameters:
                                var_parameters_to_str += "\""+param+"\""
                            line = line.replace("--" + var_action + ":" + var_parameters_to_str, "", 1)
                        else:
                            var_parameters_to_str = ""
                            for param in var_parameters:
                                var_parameters_to_str += param
                            line = line.replace("--" + var_action + ":" + var_parameters_to_str, "", 1)
                        if line.startswith(" "):
                            line = line.replace(" ", "", 1)

                    line = remove_suffix(line, line.endswith("\n"))
                    line = line.replace("\\n", "\n")

                    line = line.split(" ")  # Result : [name, operator, content]

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
                            error(line_numbers, "VarTypeError", f"Var type '{line[0].split(':')[1].split(' ')[0]}' does not exist.")
                        line[0] = line[0].replace(":" + var_type, "", 1)
                        line[0] = remove_prefix(line[0], line[0].startswith(" "))
                        del temp_name

                    if var_type == "bool":
                        if str(line[2]).lower() == "true":
                            line[2] = True
                        elif str(line[2]).lower() == "false":
                            line[2] = False
                        recombine = False
                    else:
                        recombine = True

                    if str(line[2]).startswith("input"):
                        line[2] = line[2].replace("input", "", 1)
                        line[2] = line[2].replace(" ", "", 1)
                        for i in range(3, len(line)):
                            line[2] = line[2] + " " + line[i]
                        while line[2].startswith(" "):
                            line[2] = line[2].replace(" ", "", 1)
                        line[2] = input(line[2])
                        try:
                            for i in range(3, len(line)):
                                line.pop(i)
                        except IndexError:
                            pass
                        recombine = False

                    elif str(line[2]).startswith("random"):
                        line[2] = line[2].replace("random", "", 1)
                        for i in range(3, len(line)):
                            line[2] = line[2] + " " + line[i]

                        if len(line) == 4:
                            rand_min = 0
                            rand_max = line[3].replace(",", "")
                        else:
                            rand_min = line[3].replace(",", "")
                            rand_max = line[4]
                        line[2] = randint(int(rand_min), int(rand_max))
                        recombine = False

                    elif str(line[2]).startswith("list"):
                        line[2] = line[2].replace("list", "", 1)

                        # Recombination of line vars in a single line
                        for i in range(3, len(line)):
                            line[2] = line[2] + " " + line[i]

                        # Initializing list elements
                        list_elements = []

                        if not line[2].startswith("."):  # If we just define a list
                            while "[" in line[2] and "]" in line[2]:
                                variable = line[2][line[2].find("[") + 1:line[2].find("]")]
                                debug("other", lineno(), 3, f"List element {variable} found.")
                                try:
                                    line[2] = line[2].replace("[" + variable + "]", "")
                                except KeyError:
                                    # An error occurred while trying to parse the list "{}".
                                    error(line_numbers, "ListParsingError", texts.errors["ListParsingError"].format(line[0]))
                                    errors_count += 1
                                if errors_count >= 100:
                                    print(f"\n\n{bcolors.FAIL}{texts.main['ProgramStopped_Errors']}{bcolors.ENDC}")
                                    line_numbers = len(code_lines)
                                    break
                                list_elements.append(variable)
                            # Dememorizing 'variable'
                            del variable

                            # Check the elements types
                            for i in range(len(list_elements)):
                                # If the user wants it as :
                                if list_elements[i].startswith("int:"):  # An integer
                                    list_elements[i] = list_elements[i].replace("int:", "", 1)
                                    try:
                                        list_elements[i] = int(list_elements[i])
                                    except ValueError:
                                        # The element no{i} cannot be casted as integer.
                                        error(line_numbers, "TypeError", texts.error["TypeErrorInt"].format(i=i, list_element=list_elements[i]))
                                elif list_elements[i].startswith("float:"): # A float
                                    list_elements[i] = list_elements[i].replace("float:", "", 1)
                                    try:
                                        list_elements[i] = float(list_elements[i])
                                    except ValueError:
                                        # The element no{i} cannot be casted as float.
                                        error(line_numbers, "TypeError",
                                              texts.error["TypeErrorFloat"].format(i=i, list_element=list_elements[i]))
                                elif list_elements[i].startswith("bool:"): # A boolean
                                    list_elements[i] = list_elements[i].replace("bool:", "", 1)
                                    if list_elements[i].lower() == "true":
                                        list_elements[i] = True
                                    elif list_elements[i].lower() == "false":
                                        list_elements[i] = False
                                    else:
                                        # The element no{i} cannot be casted as boolean.
                                        error(line_numbers, "TypeError",
                                              texts.error["TypeErrorBool"].format(i=i, list_element=list_elements[i]))
                                elif list_elements[i].startswith("str:"): # A string
                                    list_elements[i] = list_elements[i].replace("str:", "", 1)
                                elif list_elements[i].startswith("string:"): # A string
                                    list_elements[i] = list_elements[i].replace("string:", "", 1)

                            line[2] = list_elements
                            var_type = "list"
                        elif line[2].startswith(".add"):  # If it is list.add
                            line[2] = line[2].replace(".add ", "", 1)
                            # We should append the variable here to the list
                            variables_container[line[0]].append(line[2])
                            var_type = "list"
                            # Then just 'continue' to avoid variables code.
                            line_numbers += 1
                            continue
                        elif line[2].startswith(".insert"):  # If it is list.insert
                            line[2] = line[2].replace(".insert ", "", 1)
                            index = int(re.findall("\d*", line[2])[0])
                            line[2] = line[2].replace(str(index)+" ", "", 1)
                            # Inserting at the right index
                            try:
                                variables_container[line[0]].insert(index, line[2])
                            except IndexError:
                                # The index is not existing.
                                error(line_numbers, "IndexError", texts.errors["IndexError"])
                                sys.exit()
                            var_type = "list"
                            # Continue to avoid variables code
                            line_numbers += 1
                            continue
                        elif line[2].startswith(".remove"):  # If it is list.remove
                            line[2] = line[2].replace(".remove ", "", 1)
                            index = int(re.findall("\d*", line[2])[0])
                            # Removing correct index
                            try:
                                variables_container[line[0]].pop(index)
                            except IndexError:
                                # The index is not existing.
                                error(line_numbers, "IndexError", texts.errors["IndexError"])
                            line_numbers += 1
                            continue

                        recombine = False

                    elif str(line[2]).startswith("lib"):
                        line[2] = recreate_string(line[2:len(line)], " ")
                        recombine = False
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
                                requirements = item.requirements("var_methods")
                                requirements_list = list()
                                for element in requirements:
                                    requirements_list.append(locals()[element])
                                del requirements
                                requirements_list = tuple(requirements_list)
                                result = item.var_methods(line, variables_container, requirements_list)
                                line = result[0]
                                variables_container = result[1]
                                if len(result) > 2:
                                    for k in range(0, len(result[2]), 2):
                                        globals()[result[2][k]] = result[2][k + 1]

                    elif recreate_string(line[2:len(line)], " ").startswith("var_action"):
                        line[2] = recreate_string(line[2:len(line)], " ").replace("var_action ", "", 1)
                        recombine = False
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
                            var_action = "replace"
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
                                error(line_numbers, "ArgumentError", texts.console["FunctionArgumentError"].format(args_required="2/3", args_nbr=len(var_parameters)))

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

                    # Recombining if required
                    if recombine is True:
                        for i in range(3, len(line)):
                            line[2] += " "+line[i]

                    if line[1] != "=" and line[0] in variables_container.keys() and do_not_the_operator is False:
                        operator = line[1].split("=")[0]
                        line[2] = eval(str(variables_container[line[0]]) + operator + str(line[2]))

                    if var_type not in ("list", "bool"):
                        try:
                            line[2] = eval(line[2])
                        except SyntaxError:
                            pass
                        except TypeError:
                            pass
                        except NameError:
                            # line[2] = "\""+line[2]+"\""
                            pass

                    if not var_type == "bool":
                        try:
                            if "." not in str(line[2]):
                                line[2] = int(line[2])
                            elif re.search("\d*", str(line[2]).replace(".", "")).group(0) == str(line[2]):
                                line[2] = float(line[2])
                        except ValueError:
                            try:
                                line[2] = float(line[2])
                            except ValueError:
                                try:
                                    line[2] = str(line[2])
                                except TypeError:
                                    pass
                        except TypeError:
                            pass

                    if var_action == "lowercase":
                        line[2] = str(line[2]).lower()
                    elif var_action == "uppercase":
                        line[2] = str(line[2]).upper()
                    elif var_action == "round":
                        line[2] = round(float(str(line[2]).replace("= ", "", 1)), int(str(var_parameters[0]).replace("--round:", "", 1)))
                    elif var_action == "ceil":
                        line[2] = ceil(float(str(line[2]).replace("= ", "", 1)))
                    elif var_action == "replace":
                        if len(var_parameters) == 1:
                            var_parameters.append("")
                        if len(var_parameters) == 3:
                            var_parameters[2] = int(var_parameters[2])
                            # Replaces from line : <search> <replace with> <count>
                            line[2] = line[2].replace(var_parameters[0], var_parameters[1], var_parameters[2])
                        else:
                            line[2] = line[2].replace(var_parameters[0], var_parameters[1])
                    elif var_action == "split":
                        var_type = "list"
                        var_parameters[0] = var_parameters[0].replace("\"", "")
                        line[2] = line[2].split(var_parameters[0])

                    index = None
                    if "[" and "]" in line[0]:
                        index = int(line[0][line[0].find("[") + 1:line[0].find("]")])
                        line[0] = line[0].replace("["+str(index)+"]", "")

                    # If line[0] is in the built-in variables
                    if line[0] in built_in_vars.keys():
                        error(line_numbers, "VarNameError", f"Cannot assign value to built-in variable '{line[0]}' !")

                    if index is None:
                        if var_type is not None:
                            if var_type == "int":
                                try:
                                    variables_container[line[0]] = int(line[2])
                                    variables_container["length"][line[0]] = len(str(line[2]))
                                except ValueError:
                                    # Variable '{line[0]}' cannot be casted as integer.
                                    error(line_numbers, "TypeError", texts.errors["ImpossibleCast_Int"].format(var=line[0]))
                                    sys.exit(1)
                            elif var_type == "float":
                                try:
                                    variables_container[line[0]] = float(line[2])
                                    variables_container["length"][line[0]] = len(str(line[2]))
                                except ValueError:
                                    # Variable '{line[0]}' cannot be casted as float.
                                    error(line_numbers, "TypeError",
                                          texts.errors["ImpossibleCast_Float"].format(var=line[0]))
                            elif var_type == "list":
                                variables_container[line[0]] = line[2]
                                variables_container["length"][line[0]] = len(line[2])
                            elif var_type == "bool":
                                variables_container[line[0]] = line[2]
                                variables_container["length"][line[0]] = 0
                            else:
                                variables_container[line[0]] = str(line[2])
                                variables_container["length"][line[0]] = len(str(line[2]))
                        else:
                            variables_container[line[0]] = line[2]
                            if not isinstance(line[2], (int, float, bool)):
                                variables_container["length"][line[0]] = len(line[2])
                    else:
                        if var_type is not None:
                            if var_type == "int":
                                variables_container[line[0]][index] = int(line[2])
                                variables_container["length"][line[0]][index] = len(str(line[2]))
                            elif var_type == "float":
                                variables_container[line[0]][index] = float(line[2])
                                variables_container["length"][line[0]][index] = len(str(line[2]))
                            elif var_type == "list":
                                variables_container[line[0]][index] = line[2]
                                variables_container["length"][line[0]][index] = len(line[2])
                            elif var_type == "bool":
                                variables_container[line[0]][index] = line[2]
                                variables_container["length"][line[0]][index] = 0
                            else:
                                variables_container[line[0]][index] = str(line[2])
                                variables_container["length"][line[0]][index] = len(str(line[2]))
                        else:
                            variables_container[line[0]][index] = line[2]
                            if not isinstance(line[2], (int, float, bool)):
                                variables_container["length"][line[0]][index] = len(str(line[2]))

                    if debug_acpl_program is True:
                        # Created variable '{bcolors.OKGREEN}{line[0]}{bcolors.OKBLUE}' with content {bcolors.OKGREEN}{line[2]}{bcolors.OKBLUE} on line {line_numbers}
                        print(bcolors.OKBLUE + texts.acpl_debugger["variable"].format(OKGREEN=bcolors.OKGREEN,
                                                                                      line0=line[0],
                                                                                      OKBLUE=bcolors.OKBLUE,
                                                                                      line_numbers=line_numbers,
                                                                                      line2=line[2])
                              + bcolors.ENDC)

                elif line.startswith("pause") or line.split(" ")[0] in aliases["pause"]:
                    if line.split(" ")[0] in aliases["pause"]:
                        line = line.replace(aliases["pause"][aliases["pause"].index(line.split(" ")[0])]+" ", "")
                    else:
                        line = line.replace("pause ", "", 1)
                        
                    sleep(float(line))

                elif line.startswith("deletevar") or line.split(" ")[0] in aliases["deletevar"]:
                    if line.split(" ")[0] in aliases["deletevar"]:
                        line = line.replace(aliases["deletevar"][aliases["deletevar"].index(line.split(" ")[0])]+" ", "")
                    else:
                        line = line.replace("deletevar ", "", 1)

                    line = remove_suffix(line, line.endswith("\n"))

                    # If the user want to delete a single var (if) or multiple variables (else)
                    if not "," in line:
                        variables_container.pop(line)
                    else:
                        # Removing all spaces (we don't need them)
                        line = line.replace(" ", "")
                        
                        # Creating a list of all the vars to delete
                        line = line.split(",")
                        
                        # Deleting all of them, one by one
                        for i in range(len(line)):
                            variables_container.pop(line[i])
                        
                    if debug_acpl_program is True:
                        # Deleted variable '{bcolors.OKGREEN}{line}{bcolors.OKBLUE}' on line {line_numbers}.
                        if isinstance(line, list):
                            line = recreate_string(line, ", ")
                        print(bcolors.OKBLUE + texts.acpl_debugger["DeletedVariable"].format(OKGREEN=bcolors.OKGREEN,
                                                                                             var=line,
                                                                                             OKBLUE=bcolors.OKBLUE,
                                                                                             line_numbers=line_numbers)
                              + bcolors.ENDC)

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
                            requirements = item.requirements("main")
                            requirements_list = list()
                            for element in requirements:
                                requirements_list.append(locals()[element])
                            del requirements
                            requirements_list = tuple(requirements_list)
                            try:
                                result = item.main(line, variables_container, requirements_list)
                                line = result[0]
                                variables_container = result[1]
                                if len(result) > 2:
                                    for k in range(0, len(result[2]), 2):
                                        globals()[result[2][k]] = result[2][k + 1]
                            except AttributeError:
                                pass
                elif line != "" and line != " " and line != "\n" and og_line.split(" ")[0] not in\
                        ("if", "for", "while", "$use:", "endfor", "endwhile", "endif", "break", "continue", "function", "endfunction") and "$use:" not in og_line:
                    #error(line_numbers+1, "Error", "Unknown function or method !", quit=False)
                    debug("out", line_numbers, 2, "Function : ", line)

    debug("out", line_numbers, 2, f"Variables : {variables_container}")

    # Debugger
    if debug_acpl_program is True:
        # Variables for line {line_numbers} :
        print(bcolors.OKBLUE + texts.acpl_debugger["VariablesAtLineNO"].format(line_numbers=line_numbers))
        for element in variables_container:
            print(f"{bcolors.OKBLUE} - {bcolors.OKGREEN}{element}{bcolors.OKBLUE} = {var_type_as_str(variables_container[element])} : {variables_container[element]}{bcolors.ENDC}")
        user_input = input(f"{bcolors.WARNING}{texts.acpl_debugger['StopOrContinue']}{bcolors.ENDC}\n")
        if user_input.lower() in ("stop", "end", "quit"):
            print(bcolors.FAIL + texts.acpl_debugger["ExecutionStopped"] + bcolors.ENDC)
            running = False
            break
        else:
            del user_input

    line_numbers += 1

print(f"{bcolors.OKBLUE}{texts.main['ProcessTime']} : {round((timeit.default_timer()-time_launch), process_time_round_numbers)}s")
print(f"This script uses {round(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2, 2)}MB of memory.{bcolors.ENDC}")

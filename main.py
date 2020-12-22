import importlib
import re
import timeit
from math import *
from random import randint
from time import sleep
from recurrent_classes import *

time_launch = timeit.default_timer()
final_filename = ""

# Files opening
try:
    filename_file = open("startup.acpl-ini", "r+", encoding="utf-8")
except FileNotFoundError:
    print(texts.critic_errors["ImpossibleLoad_StartupIni"])
    sys.exit()

command_line_args = sys.argv
command_line_args.pop(0)

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
variables_container = {}
used_libs = []
functions = {}

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
if "process_time_round_numbers" not in globals():
    process_time_round_numbers = 6

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
# Automatic updates
# Fixed lists bug
# Integrated lists syntax for functions
# Types in lists
# Command line arguments for main.py
# Conditions and loops inside each other -> ELSE HAS BEEN REMOVED
# libs -> function to define which libs to import in the compiler
# ACPL debugger
# Redo Modify-ini into 'settings'

# Order :

# DELAYED :
# Line numbers in functions
# Full use of lists in functions

# 3.11
# Translations
# GUI Lib
# Files lib

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
                        error(line_numbers, "VarNotFoundError", f"The index '{list_index}' seems not to exist.")
                    variable = variable[0:variable.find("[")]

                # Remove the list_index from the variable
                variable = variable.replace("["+og_list_index, "", 1)

                # If the list index ends with an unnecessary ']', then we remove it
                try:
                    list_index = remove_suffix(list_index, list_index.endswith("]"))
                except AttributeError:  # If 'list_index' is already an integer
                    pass

                if not str(list_index).startswith("len"):
                    line = line.replace("{"+og_variable+"}]}", str(variables_container[variable][int(list_index)]), 1)
                    line = line.replace("{"+og_variable+"}", str(variables_container[variable][int(list_index)]), 1)
                else:
                    line = line.replace("{" + og_variable + "}]}", str(len(variables_container[variable])), 1)
                    line = line.replace("{" + og_variable + "}", str(len(variables_container[variable])), 1)

            else:  # If it is a standard variable
                try:
                    # We try to replace the variable asked with its content
                    line = line.replace("{"+variable+"}", str(variables_container[variable]), 1)
                except KeyError:
                    # The variable was not found, throwing an error.
                    error(line_numbers, "VarNotFoundError", f"The variable '{variable}' seems not to exist.")

        while "<" in line and ">" in line and not in_function:
            equation = line[line.find("<") + 1:line.find(">")]
            debug("other", lineno(), 2, f"Equation {equation} found in print.")
            try:
                line = line.replace(f"<{str(equation)}>", str(eval(str(equation))))
            except KeyError:
                error(line_numbers, "ArgumentError",
                      f"The equation \"{equation}\" is not existing or has been declared later in the code.")
                errors_count += 1
            if errors_count >= 100:
                print(f"\n\n{bcolors.FAIL}Debug has chosen to stop this program due to too many errors. Sorry for the inconvenience.{bcolors.ENDC}")
                break

        debug("other", line_numbers, 3, f"line : {line}")

        if line.startswith("$use: "):
            line = line.replace("$use: ", "", 1)
            line = remove_suffix(line, line.endswith("\n"))
            while line.endswith(" "):
                line = remove_suffix(line)
            used_libs.append("fx_"+line+".py")

        if line.startswith("function"):
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
            if line.startswith("use_function "):
                debug("in", line_numbers, 3, "Functions : ", functions)
                line = line.replace("use_function ", "", 1)
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
                    error(line_numbers, "ArgumentError: ", f"{len(functions[function_name]['parameters'])} arguments required, got {len(function_arguments)}.")
                    sys.exit()

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
                    print(f"{bcolors.OKBLUE}Created function '{bcolors.WARNING}{function_name}{bcolors.OKBLUE}' with arguments : {bcolors.OKGREEN}{recreate_string(function_arguments, ', ')}{bcolors.OKBLUE} on line {line_numbers}.{bcolors.ENDC}")

                debug("other", lineno(), 2, "Code lines : ", code_lines)
                continue

            if line.startswith("if "):
                line = line.replace("if ", "", 1)
                if eval(line) is True and all(value == False for value in execute_until_endif.values()):
                    execute_until_endif[indent] = False
                    if debug_acpl_program is True:
                        print(f"{bcolors.OKBLUE}Condition '{bcolors.ENDC}{line}{bcolors.OKBLUE}' on line {line_numbers} marked as {bcolors.OKGREEN}True{bcolors.ENDC}")
                else:
                    execute_until_endif[indent] = True
                    if debug_acpl_program is True:
                        print(f"{bcolors.OKBLUE}Condition '{bcolors.ENDC}{line[:-1]}{bcolors.OKBLUE}' on line {line_numbers} marked as {bcolors.FAIL}False{bcolors.ENDC}")
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

            if line.startswith("while"):
                line = line.replace("while ", "", 1)
                line = remove_suffix(line, line.endswith("\n"))
                while_condition = line
                in_while = True
                while_line = line_numbers
                if eval(while_condition) and is_breaking is False:
                    skip_while = False
                    if debug_acpl_program is True:
                        print(f"{bcolors.OKBLUE}Condition for while loop '{bcolors.ENDC}{line}{bcolors.OKBLUE}' on line {line_numbers} marked as {bcolors.OKGREEN}True{bcolors.OKBLUE}.\nEntering loop again.{bcolors.ENDC}")
                else:
                    if debug_acpl_program is True:
                        print(f"{bcolors.OKBLUE}Condition for while loop '{bcolors.ENDC}{line}{bcolors.OKBLUE}' on line {line_numbers} marked as {bcolors.FAIL}False{bcolors.OKBLUE}.\nSkipping loop.{bcolors.ENDC}")
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

            if line.startswith("for"):  # for <name> <min> <max>
                in_for = True
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
                if debug_acpl_program is True:
                    print(f"{bcolors.OKBLUE}Looping {int(line[2])-int(line[1])} times using variable {bcolors.OKGREEN}{line[0]}{bcolors.ENDC}")
                line_numbers += 1
                continue

            if line.startswith("endfor") or line.startswith("end for"):
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

            if line.startswith("break") and execute_until_endif is False:
                is_breaking = True
                if debug_acpl_program is True:
                    print(f"{bcolors.OKBLUE}Breaking loop.{bcolors.ENDC}")

            if line.startswith("continue") and execute_until_endif is False:
                wait_next_loop = True
                if debug_acpl_program is True:
                    print(f"{bcolors.OKBLUE}Going to next loop.{bcolors.ENDC}")

            if execute_until_endif[indent-1] is False and is_breaking is False and wait_next_loop is False and skip_while is False:
                if line.startswith("print"):
                    line = line.replace("print ", "", 1)
                    line = remove_suffix(line, line.endswith("\n"))
                    if debug_acpl_program is False:
                        print(line)
                    else:
                        print(f"{bcolors.OKGREEN} >>> \t{bcolors.ENDC}{line}")
                elif line.startswith("var"):
                    line = line.replace("var", "", 1)
                    var_type = None
                    var_action = None
                    var_parameters = None

                    if line.startswith(":"):
                        if line.startswith(":int"):
                            var_type = "int"
                        elif line.startswith(":float"):
                            var_type = "float"
                        elif line.startswith(":list"):
                            var_type = "list"
                        else:
                            var_type = "str"
                        line = line.replace(":"+var_type, "", 1)  # ERROR HERE !
                    if line.startswith(" "):
                        line = line.replace(" ", "", 1)

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

                    if str(line[2]).lower() == "true":
                        line[2] = True
                    elif str(line[2]).lower() == "false":
                        line[2] = False

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

                    if str(line[2]).startswith("random"):
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

                    if str(line[2]).startswith("list"):
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
                                    error(line_numbers, "ArgumentError", f"An error occurred while trying to parse the list \"{line[0]}\".")
                                    errors_count += 1
                                if errors_count >= 100:
                                    print(f"\n\n{bcolors.FAIL}Debug has chosen to stop this program due to too many errors. Sorry for the inconvenience.{bcolors.ENDC}")
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
                                        error(line_numbers, "TypeError", f"List element no{i} '{list_elements[i]}' cannot be casted as integer.")
                                elif list_elements[i].startswith("float:"): # A float
                                    list_elements[i] = list_elements[i].replace("float:", "", 1)
                                    try:
                                        list_elements[i] = float(list_elements[i])
                                    except ValueError:
                                        error(line_numbers, "TypeError", f"List element no{i} '{list_elements[i]}' cannot be casted as float.")
                                elif list_elements[i].startswith("bool:"): # A boolean
                                    list_elements[i] = list_elements[i].replace("bool:", "", 1)
                                    if list_elements[i].lower() == "true":
                                        list_elements[i] = True
                                    elif list_elements[i].lower() == "false":
                                        list_elements[i] = False
                                    else:
                                        error(line_numbers, "TypeError", f"List element no{i} '{list_elements[i]}' cannot be casted as boolean.")
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
                                error(line_numbers, "IndexError", "The index is not existing.")
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
                                error(line_numbers, "IndexError", "The index is not existing.")
                                sys.exit()
                            line_numbers += 1
                            continue

                        recombine = False

                    if recombine:
                        for i in range(3, len(line)):
                            line[2] += " "+line[i]

                    if line[1] != "=":
                        operator = line[1].split("=")[0]
                        line[2] = eval(str(variables_container[line[0]]) + operator + str(line[2]))

                    if var_type != "list":
                        try:
                            line[2] = eval(line[2])
                        except SyntaxError:
                            pass
                        except TypeError:
                            pass
                        except NameError:
                            # line[2] = "\""+line[2]+"\""
                            pass

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
                    except TypeError:
                        pass

                    if var_action == "lowercase":
                        line[2] = str(line[2]).lower()
                    elif var_action == "uppercase":
                        line[2] = str(line[2]).upper()
                    elif var_action == "round":
                        line[2] = round(float(str(line[2]).replace("= ", "", 1)), int(var_parameters[0].replace("--round:", "", 1)))
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

                    if index is None:
                        if var_type is not None:
                            if var_type == "int":
                                try:
                                    variables_container[line[0]] = int(line[2])
                                except ValueError:
                                    error(line_numbers, "TypeError", f"Variable '{line[0]}' cannot be casted as integer.")
                                    sys.exit(1)
                            elif var_type == "float":
                                try:
                                    variables_container[line[0]] = float(line[2])
                                except ValueError:
                                    error(line_numbers, "TypeError", f"Variable '{line[0]}' cannot be casted as float.")
                                    sys.exit(1)
                            elif var_type == "list":
                                variables_container[line[0]] = line[2]
                            else:
                                variables_container[line[0]] = str(line[2])
                        else:
                            variables_container[line[0]] = line[2]
                    else:
                        if var_type is not None:
                            if var_type == "int":
                                variables_container[line[0]][index] = int(line[2])
                            elif var_type == "float":
                                variables_container[line[0]][index] = float(line[2])
                            elif var_type == "list":
                                variables_container[line[0]][index] = line[2]
                            else:
                                variables_container[line[0]][index] = str(line[2])
                        else:
                            variables_container[line[0]][index] = line[2]

                    if debug_acpl_program is True:
                        print(f"{bcolors.OKBLUE}Created variable '{bcolors.OKGREEN}{line[0]}{bcolors.OKBLUE}' with content {bcolors.OKGREEN}{line[2]}{bcolors.OKBLUE} on line {line_numbers}{bcolors.ENDC}")

                elif line.startswith("pause"):
                    line = line.replace("pause ", "", 1)
                    sleep(float(line))

                elif line.startswith("deletevar"):
                    line = line.replace("deletevar ", "", 1)
                    line = remove_suffix(line, line.endswith("\n"))
                    variables_container.pop(line)
                    if debug_acpl_program is True:
                        print(f"{bcolors.OKBLUE}Deleted variable '{bcolors.OKGREEN}{line}{bcolors.OKBLUE}' on line {line_numbers}.{bcolors.ENDC}")

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
                                requirements_list.append(globals()[element])
                            del requirements
                            requirements_list = tuple(requirements_list)
                            result = item.main(line, variables_container, requirements_list)
                            line = result[0]
                            variables_container = result[1]
                            if len(result) > 2:
                                for k in range(0, len(result[2]), 2):
                                    globals()[result[2][k]] = result[2][k + 1]
                elif line != "" and line != " " and line != "\n" and line != "if" and line != "else" and line != "endif" and line != "end if" and line != "for" and line != "endfor" and line != "end for":
                    if debug_const > 0:
                        error(line_numbers, "Error", "Unknown function or method !")
                        debug("out", line_numbers, 2, "Function : ", line)

    debug("out", line_numbers, 2, f"Variables : {variables_container}")

    # Debugger
    if debug_acpl_program is True:
        print(f"{bcolors.OKBLUE}Variables for line {line_numbers} :")
        for element in variables_container:
            print(f"{bcolors.OKBLUE} - {bcolors.OKGREEN}{element}{bcolors.OKBLUE} = {var_type_as_str(variables_container[element])} : {variables_container[element]}{bcolors.ENDC}")
        user_input = input(f"{bcolors.WARNING}Press Enter to continue or type 'stop'/'end' to quit.{bcolors.ENDC}\n")
        if user_input.lower() in ("stop", "end", "quit"):
            print(f"{bcolors.FAIL}Execution stopped.{bcolors.ENDC}\n")
            running = False
            break
        else:
            del user_input

    line_numbers += 1

print(f"{bcolors.OKBLUE}Process time : {round((timeit.default_timer()-time_launch), process_time_round_numbers)}s{bcolors.ENDC}")

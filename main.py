import inspect
import string
import re
from time import sleep
from random import randrange
import sys
import json
from recurrent_classes import *
import os


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
        if lines == "fr":
            language = "fr"
        elif lines == "nl":
            language = "nl"
        else:
            language = "en"

        try:
            with open(language + ".json", "r", encoding="utf-8") as json_file:
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

# Multilines comments (WIP)
"""all_lines = ""
for line in code_lines:
    all_lines += line + "NEWLINE"
start = all_lines.find( '/*' )
end = all_lines.find( '*/' )
if start != -1 and end != -1:
    result = all_lines[start+1:end]
    all_lines.replace(result, "")
all_lines = all_lines.split("NEWLINE")
print("ALL_LINES", all_lines, end="    END\n\n\n")"""

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
constants_container = {}
used_libs = []

line_numbers = 0
is_in_comment = False
indentation_required = 0
condition = []
for i in range(20):
    condition.append(True)

# Instructions
for line in code_lines:
    was_if = False
    line_numbers += 1
    if "/*" in line:
        is_in_comment = True
    if "*/" in line:
        is_in_comment = False
        continue
    if not is_in_comment:
        line = split(line)
        indentation_level = 0
        try:
            while line[0] == "\t":
                indentation_level += 1
                line.pop(0)
        except IndexError:
            line = [""]
            pass
        temp_line = ""
        for char in line:
            temp_line += char
        line = temp_line

        if indentation_level == 0:
            indentation_required = 0
            #condition[indentation_level] = True
        if indentation_level > indentation_required:
            continue
        if line.startswith("if"):
            line = line.replace("if ", "")
            line = line.replace("\n", "")
            was_if = True
            if line.endswith(":"):
                line = split(line)
                line.pop()
                temp_line = ""
                for char in line:
                    temp_line += char
                line = temp_line
            else:
                error(line_numbers, "StatementError", "If has to finish with \":\" !")
            line = line.replace("&&", "and")
            line = line.replace("||", "or")
            while "{" in line and "}" in line:
                variable = line[line.find("{") + 1:line.find("}")]
                try:
                    line = line.replace("{"+variable+"}", str(variables_container[variable]))
                except KeyError:
                    error(line_numbers, "ArgumentError", f"The variable \"{variable}\" is not existing or has been declared later in the code.")
            condition[indentation_level] = eval(str(line))
            if condition[indentation_level]:
                indentation_required += 1
        elif line.startswith("else"):
            if condition[indentation_level] is False:
                indentation_required += 1
            else:
                indentation_required -= 1
            was_if = True

        if indentation_level < indentation_required and was_if is False:
            indentation_required -= 1
        elif indentation_level > indentation_required:
            continue


        if line.startswith("print"): # print instruction
            line = line.replace("print", "")
            if "(" in line and ")" in line:
                line = line.replace("(", "")
                line = line.replace(")", "")
                line = line.replace(";", "")
                while "{" in line and "}" in line:
                    variable = line[line.find("{") + 1:line.find("}")]
                    debug("other", lineno(), "Variable found in print.")
                    try:
                        line = line.replace("{"+variable+"}", str(variables_container[variable]))
                    except KeyError:
                        error(line_numbers, "ArgumentError", f"The variable \"{variable}\" is not existing or has been declared later in the code.")
                print(line)
            else:
                error(line_numbers, "StatementError", "Statement missing.")
                break
        elif line.startswith("var "):
            line = line.replace("var ", "")
            if line.endswith("\n"):
                line = split(line)
                line.pop()
                temp_line = ""
                for char in line:
                    temp_line += char
                line = temp_line
            line = line.replace("\\n", "\n")
            try:
                if float(line):
                    line = line.replace(",", ".")
            except ValueError:
                pass
            name = ""
            actual_state = "name"
            for char in split(line):
                if char != " " and char != "=" and actual_state == "name":
                    name += char
                elif char == " " or char == "=" and actual_state == "name":
                    line = line.replace(name, "", 1)
                    break
            actual_state = "var"
            line = line.replace("=", "")
            while line.startswith(" "):
                line = split(line)
                line.pop(0)
                temp_line = ""
                for char in line:
                    temp_line += char
                line = temp_line
            var_content = ""
            for char in split(line):
                var_content += char
            # Round
            round_bool = "--round" in var_content
            if round_bool:
                var_content = var_content.replace("--round", "")
            if var_content.endswith(" "):
                var_content = split(var_content)
                var_content.pop()
                temp_var_content = ""
                for temp_var_content_thing in var_content:
                    temp_var_content += temp_var_content_thing
                var_content = temp_var_content
            # Inputs
            if var_content.startswith("input("):
                var_content = var_content.replace("input(", "")
                var_content = split(var_content)
                var_content.pop()
                temp_var_content = ""
                for char in var_content:
                    temp_var_content += char
                var_content = temp_var_content
                var_content = input(bcolors.WARNING + var_content + bcolors.ENDC)
            # Random
            if "random(" in var_content:
                while "{" in var_content and "}" in var_content:
                    variable = line[line.find("{") + 1:line.find("}")]
                    debug("other", lineno(), "Variable found in print.")
                    var_content = var_content.replace("{"+variable+"}", str(variables_container[variable]))
                old_content = var_content[var_content.find("random(") + 1:line.find(")")]
                content = old_content
                content = content.replace(" ", "")
                if "," in content:
                    content = content.replace(")", "")
                    old_content = old_content.replace(")", "")
                    content = content.replace("andom(", "")
                    old_content = old_content.replace("andom(", "")
                    content = content.split(",")
                    content = randrange(int(content[0]), int(content[1]))
                else:
                    content = randrange(0, int(content))
                var_content = var_content.replace(f"random({old_content})", str(content))
            # Maths
            if ("*" in var_content or "+" in var_content or re.compile("-{0}-{1}\w{0}").match(var_content) or "/" in var_content or "//" in var_content or "%" in var_content or "^" in var_content or "**" in var_content) and string.ascii_letters not in var_content:
                var_content = var_content.replace("^", "**")
                while "{" in var_content and "}" in var_content:
                    variable = line[line.find("{") + 1:line.find("}")]
                    debug("other", lineno(), "Variable found in print.")
                    var_content = var_content.replace("{"+variable+"}", str(variables_container[variable]))
                var_content = eval(str(var_content))
            # Round
            if round_bool:
                var_content = round(float(var_content))
            # LIBS
            # STRING LIB
            if "string" in used_libs:
                import libs.lib_string
                var_content = libs.lib_string.lower(var_content)
                var_content = libs.lib_string.upper(var_content)
            variables_container[name] = var_content
            debug("other", lineno(), variables_container)
        elif line.startswith("pause"):
            line = line.replace("pause", "")
            if "(" in line and ")" in line:
                line = line.replace("(", "")
                line = line.replace(")", "")
                line = line.replace(";", "")
                line = line.replace("\n", "")
                if "{" in line and "}" in line:
                    variable = line[line.find("{") + 1:line.find("}")]
                    debug("other", lineno(), "Variable found in pause.")
                    line = variables_container[variable]
                try:
                    time = int(line)
                except ValueError:
                    try:
                        time = float(line)
                    except ValueError:
                        error(line_numbers, "StatementError")
                        break
                sleep(time)
            else:
                error(line_numbers, "StatementError", "Statements Missing !")
                break
        elif line.startswith("$use: "):
            line = line.replace("$use:", "")
            line = line.replace(" ", "")
            line = line.replace("\n", "")
            if os.path.exists(f"{os.getcwd()}/libs/lib_{line}.py") is True:
                used_libs.append(line)
            else:
                error(line_numbers, "UnexistingLibError", "Lib is not existing or has not been installed.")
                break
        elif line != "" and line != " " and line != "\n" and was_if == False:
            error(line_numbers, "Error", "Unknown function or method !")

debug("other", lineno(), variables_container)

print(f"\n{bcolors.OKBLUE}{texts.texts['program-ended']}{bcolors.ENDC}")

code_file.close()
debug_file.close()
filename_file.close()

import inspect
import string
import re
from time import sleep
from random import randrange
import sys
import json
from recurrent_classes import *


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


# Var containers
ints = {}
floats = {}
strings = {}
bools = {}

line_numbers = 0

# Instructions
for line in code_lines:
    line_numbers += 1
    if line.startswith("print"): # print instruction
        line = line.replace("print", "")
        if "(" in line and ")" in line:
            line = line.replace("(", "")
            line = line.replace(")", "")
            line = line.replace(";", "")
            while "{" in line and "}" in line:
                variables = line[line.find("{") + 1:line.find("}")]
                debug("other", lineno(), "Variable found in print.")
                variables = variables.split(" ")
                if variables[0] == "int":
                    variable = ints.get(variables[1])
                elif variables[0] == "float":
                    variable = floats.get(variables[1])
                elif variables[0] == "str" or variables[0] == "string":
                    variable = strings.get(variables[1])
                elif variables[0] == "bool" or variables[0] == "boolean":
                    variable = bools.get(variables[1])
                line = line.replace("{" + variables[0] + " " + variables[1] + "}", str(variable))
            print(line)
        else:
            error(line_numbers, "StatementError", "Statement missing.")
            break
    elif line.startswith("int"):
        if "input(" in line:
            instruction = line.split(" ")
            for i in range(4, len(instruction)):
                instruction[3] += " " + instruction[i]
            if "(" in line and ")" in instruction[3]:
                instruction[3] = instruction[3].replace("(", "")
                instruction[3] = instruction[3].replace(")", "")
                instruction[3] = instruction[3].replace("input", "")
                instruction[3] = instruction[3].replace("\\n", "\n")
                instruction[3] = instruction[3].replace("\\t", "\t")
                try:
                    instruction[3] = int(input(bcolors.WARNING+instruction[3]+bcolors.ENDC))
                except ValueError:
                    error(line_numbers, "ValueError", "What was inputted is not an integer !")
                    break
            else:
                error(line_numbers, "StatementError")
                break
            if "--round" in line:
                instruction[3] = instruction[3].replace("-round(", "")
                instruction[3] = round(float(instruction[3]))
        elif "math" in line:
            instruction = line.split(" ")
            if "{" in instruction[4] and "}" in instruction[4]:
                for i in range(4, len(instruction)):
                    instruction[4] += instruction[i]
                variables = line[line.find("{") + 1:line.find("}")]
                debug("other", lineno(), "Variable found in math.")
                variables = variables.split(" ")
                if variables[0] == "int":
                    variable = ints.get(variables[1])
                elif variables[0] == "float":
                    variable = floats.get(variables[1])
                else:
                    error(line_numbers, "StatementError")
                    break
                final_instruction = re.sub("({).*?(\})", "\g<1>\g<2>", instruction[4])
                final_instruction = final_instruction.replace("{}", str(variable))
                instruction[4] = final_instruction
                debug("other", lineno(), "final_instruction : ", final_instruction)
                instruction[4] = instruction[4].replace("^", "**")
            result = eval(str(instruction[4]))
            instruction[3] = result
            if "--round" in line:
                instruction[3] = instruction[3].replace("-round(", "")
                instruction[3] = round(float(instruction[3]))
        elif "random(" in line:
            instruction = line.split(" ")
            if len(instruction) > 4:
                instruction[3] += instruction[4]
            debug("other", lineno(), instruction[3])
            instruction[3] = instruction[3].replace("random(", "")
            instruction[3] = instruction[3].replace(")", "")
            instruction[3] = instruction[3].replace(" ", "")
            if "," in instruction[3]:
                randomness = instruction[3].split(",")
            else:
                randomness = [0, instruction[3]]
            debug("other", lineno(), randomness)
            instruction[3] = randrange(int(randomness[0]), int(randomness[1]))
        else:
            instruction = line.split(" ")
            if "--round" in line:
                instruction[3] = instruction[3].replace("--round(", "")
                instruction[3] = round(float(instruction[3]))
            try:
                instruction[3] = int(instruction[3])
            except ValueError:
                error(line_numbers, "StatementError:", "Variable not int !")
                break
        if isinstance(instruction[1], str) and isinstance(instruction[3], int) and instruction[2] == "=":
            ints[instruction[1]] = instruction[3]
        else:
            error(line_numbers, "StatementError")
            break
    elif line.startswith("float"):
        if "input(" in line:
            instruction = line.split(" ")
            for i in range(4, len(instruction)):
                instruction[3] += " " + instruction[i]
            if "(" in line and ")" in instruction[3]:
                instruction[3] = instruction[3].replace("(", "")
                instruction[3] = instruction[3].replace(")", "")
                instruction[3] = instruction[3].replace("input", "")
                instruction[3] = instruction[3].replace("\\n", "\n")
                instruction[3] = instruction[3].replace("\\t", "\t")
                try:
                    instruction[3] = float(input(bcolors.WARNING+instruction[3]+bcolors.ENDC))
                except ValueError:
                    error(line_numbers, "ValueError", "What was inputted is not an float number !")
                    break
            else:
                error(line_numbers, "StatementError")
                break
        elif "math" in line:
            instruction = line.split(" ")
            for i in range(4, len(instruction)):
                instruction[4] += instruction[i]
            if "{" in instruction[4] and "}" in instruction[4]:
                variables = line[line.find("{") + 1:line.find("}")]
                debug("other", lineno(), "Variable found in math.")
                variables = variables.split(" ")
                if variables[0] == "int":
                    variable = ints.get(variables[1])
                elif variables[0] == "float":
                    variable = floats.get(variables[1])
                else:
                    error(line_numbers, "StatementError")
                    break
                final_instruction = re.sub("({).*?(\})", "\g<1>\g<2>", instruction[4])
                final_instruction = final_instruction.replace("{}", str(variable))
                instruction[4] = final_instruction
                debug("other", lineno(), "final_instruction : ", final_instruction)
            result = eval(instruction[4])
            instruction[3] = result
        elif "random(" in line:
            instruction = line.split(" ")
            if len(instruction) > 4:
                instruction[3] += instruction[4]
            debug("other", lineno(), instruction[3])
            instruction[3] = instruction[3].replace("random(", "")
            instruction[3] = instruction[3].replace(")", "")
            instruction[3] = instruction[3].replace(" ", "")
            if "," in instruction[3]:
                randomness = instruction[3].split(",")
            else:
                randomness = [0, instruction[3]]
            debug("other", lineno(), randomness)
            instruction[3] = randrange(int(randomness[0]), int(randomness[1]))
        else:
            instruction = line.split(" ")
            if len(instruction) != 4:
                error(line_numbers, "StatementError", "Arguments missing !")
                break
            try:
                if "," in instruction[3]:
                    instruction[3] = instruction[3].replace(",", ".")
                instruction[3] = float(instruction[3])
            except ValueError:
                error(line_numbers, "StatementError", "Variable not float !")
                break
        if isinstance(instruction[1], str) and isinstance(instruction[3], float) and instruction[2] == "=":
            floats[instruction[1]] = instruction[3]
        else:
            error(line_numbers, "StatementError")
            break
    elif line.startswith("str") or line.startswith("string"):
        if "input(" in line:
            instruction = line.split(" ")
            for i in range(4, len(instruction)):
                instruction[3] += " " + instruction[i]
            if "(" in line and ")" in instruction[3]:
                instruction[3] = instruction[3].replace("(", "")
                instruction[3] = instruction[3].replace(")", "")
                instruction[3] = instruction[3].replace("input", "")
                instruction[3] = instruction[3].replace("\\n", "\n")
                instruction[3] = instruction[3].replace("\\t", "\t")
                instruction[3] = input(bcolors.WARNING+instruction[3]+bcolors.ENDC)
            else:
                error(line_numbers, "StatementError")
                break
        else:
            instruction = line.split(" ")
            if len(instruction) != 4:
                error(line_numbers, "StatementError", "Arguments missing !")
                break
            try:
                instruction[3] = str(instruction[3])
            except ValueError:
                error(line_numbers, "StatementError", "Variable not string !")
                break
        if isinstance(instruction[1], str) and isinstance(instruction[3], str) and instruction[2] == "=":
            strings[instruction[1]] = instruction[3].replace("\n", "")
        else:
            error(line_numbers, "StatementError")
            break
    elif line.startswith("bool") or line.startswith("boolean"):
        instruction = line.split(" ")
        if len(instruction) != 4:
            error(line_numbers, "StatementError", "Arguments Missing !")
            break
        try:
            if instruction[3].lower() == "false":
                instruction[3] = 0
            elif instruction[3].lower() == "true":
                instruction[3] = 1
            instruction[3] = bool(instruction[3])
        except ValueError:
            error(line_numbers, "StatementError", "Variable not bool !")
            break
        if isinstance(instruction[1], str) and isinstance(instruction[3], bool) and instruction[2] == "=":
            bools[instruction[1]] = bool(instruction[3])
        else:
            error(line_numbers, "StatementError")
            break
    elif line.startswith("pause"):
        line = line.replace("pause", "")
        if "(" in line and ")" in line:
            line = line.replace("(", "")
            line = line.replace(")", "")
            line = line.replace(";", "")
            if "{" in line and "}" in line:
                variables = line[line.find("{") + 1:line.find("}")]
                debug("other", lineno(), "Variable found in pause.")
                variables = variables.split(" ")
                if variables[0] == "int":
                    variable = ints.get(variables[1])
                elif variables[0] == "float":
                    variable = floats.get(variables[1])
                elif variables[0] == "str" or variables[0] == "string":
                    error(line_numbers, "StatementError", "Cannot get string for pause")
                    break
                elif variables[0] == "bool" or variables[0] == "boolean":
                    error(line_numbers, "StatementError", "Cannot get boolean for pause")
                    break
                line = variable
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

debug("other", lineno(), ints)
debug("other", lineno(), floats)
debug("other", lineno(), strings)
debug("other", lineno(), bools)

print(f"\n{bcolors.OKBLUE}Program successfully stopped.{bcolors.ENDC}")

code_file.close()
debug_file.close()
filename_file.close()

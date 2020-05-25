import inspect
import string
import re
from time import sleep

def lineno():
    return inspect.currentframe().f_back.f_lineno

def split(word):
    return [char for char in word]

def debug(entry_type, line, message, *args):
    if debug_const:
        if entry_type.lower() == "in":
            entry = "\n>>>"
        elif entry_type.lower() == "out":
            entry = "<<<"
        else:
            entry = "==="
        if args:
            for arg in args:
                message += str(arg)
        debug_msg = entry + "\t" + "(" + str(line) + ")\t" + str(message) + "\n"
        debug_file.write(debug_msg)
        print(debug_msg)
        if entry == "<<<":
            debug_file.write("\n")

class StatementError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return "StatementError : {0}".format(self.message)
        else:
            return "StatementError error has been raised."

# Debug mode enabled ?
debug_const = True

# Files opening
code_file = open("code.acpl", "r", encoding="utf-8")
debug_file = open("debug.log", "w", encoding="utf-8")

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
    result = code_lines[i].split("\n")
    code_lines[i] = result[0]
pop_positions = list()
for i in range(0, len(code_lines)):
    if code_lines[i] == "\n" or code_lines[i] == "" or code_lines[i] == " ":
        pop_positions.append(i)
pop_positions.reverse()
for i in (range(0, len(code_lines)-3)):
    try:
        code_lines.pop(pop_positions[i])
    except IndexError:
        pass
debug("other", lineno(), "code_lines = ", code_lines)


# Var containers
ints = {}
floats = {}
strings = {}
bools = {}

# Instructions
for line in code_lines:
    if line.startswith("print"): # print instruction
        line = line.replace("print", "")
        if "(" in line and ")" in line:
            line = line.replace("(", "")
            line = line.replace(")", "")
            line = line.replace(";", "")
            if "{" in line and "}" in line:
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
            raise StatementError("Statements missing.")
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
                instruction[3] = int(input(instruction[3]))
            else:
                raise StatementError
        else:
            instruction = line.split(" ")
            if len(instruction) != 4:
                raise StatementError("Arguments Missing")
            try:
                instruction[3] = int(instruction[3])
            except ValueError:
                raise StatementError("Variable not int !")
        if isinstance(instruction[1], str) and isinstance(instruction[3], int) and instruction[2] == "=":
            ints[instruction[1]] = instruction[3]
        else:
            raise StatementError
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
                instruction[3] = float(input(instruction[3]))
            else:
                raise StatementError
        else:
            instruction = line.split(" ")
            if len(instruction) != 4:
                raise StatementError("Arguments Missing")
            try:
                if "," in instruction[3]:
                    instruction[3] = instruction[3].replace(",", ".")
                instruction[3] = float(instruction[3])
            except ValueError:
                raise StatementError("Variable not float !")
        if isinstance(instruction[1], str) and isinstance(instruction[3], float) and instruction[2] == "=":
            floats[instruction[1]] = instruction[3]
        else:
            raise StatementError
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
                instruction[3] = input(instruction[3])
            else:
                raise StatementError
        else:
            instruction = line.split(" ")
            if len(instruction) != 4:
                raise StatementError("Arguments Missing")
            try:
                instruction[3] = str(instruction[3])
            except ValueError:
                raise StatementError("Variable not string !")
        if isinstance(instruction[1], str) and isinstance(instruction[3], str) and instruction[2] == "=":
            strings[instruction[1]] = instruction[3].replace("\n", "")
        else:
            raise StatementError
    elif line.startswith("bool") or line.startswith("boolean"):
        instruction = line.split(" ")
        if len(instruction) != 4:
            raise StatementError("Arguments Missing")
        try:
            if instruction[3].lower() == "false":
                instruction[3] = 0
            elif instruction[3].lower() == "true":
                instruction[3] = 1
            instruction[3] = bool(instruction[3])
        except ValueError:
            raise StatementError("Variable not bool !")
        if isinstance(instruction[1], str) and isinstance(instruction[3], bool) and instruction[2] == "=":
            bools[instruction[1]] = bool(instruction[3])
        else:
            raise StatementError
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
                    raise StatementError("Cannot get string for pause")
                elif variables[0] == "bool" or variables[0] == "boolean":
                    raise StatementError("Cannot get boolean for pause")
                line = variable
            try:
                time = int(line)
            except ValueError:
                try:
                    time = float(line)
                except ValueError:
                    raise StatementError
            sleep(time)
        else:
            raise StatementError("Statements missing.")

debug("other", lineno(), ints)
debug("other", lineno(), floats)
debug("other", lineno(), strings)
debug("other", lineno(), bools)

code_file.close()
debug_file.close()
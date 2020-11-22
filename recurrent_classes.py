import inspect
import sys
import json

class bcolors:
    with open("startup.acpl-ini", "r", encoding="utf-8") as startup_file:
        for line in startup_file.readlines():
            if line.startswith("use-colors: "):
                line = line.replace("use-colors: ", "")
                line = line.replace("\n", "")
                if line.lower() == "true":
                    HEADER = '\033[95m'
                    OKBLUE = '\033[94m'
                    OKGREEN = '\033[92m'
                    WARNING = '\033[93m'
                    FAIL = '\033[91m'
                    ENDC = '\033[0m'
                    BOLD = '\033[1m'
                    UNDERLINE = '\033[4m'
                    ITALICS = '\x1B[3m'
                else:
                    HEADER = ''
                    OKBLUE = ''
                    OKGREEN = ''
                    WARNING = ''
                    FAIL = ''
                    ENDC = ''
                    BOLD = ''
                    UNDERLINE = ''
                    ITALICS = ''
        startup_file.close()
        colors_used = HEADER != ''

class Text():
    def __init__(self, texts):
        self.texts = texts
        self.console = self.texts["console"]
        self.console_modify_ini = self.console["modify-ini"]
        self.console_help = self.console["help"]
        self.critic_errors = self.texts["critic-errors"]
        self.statement_errors = self.texts["statement-errors"]
        self.updates = self.texts["update-checker"]

    def get(self, key):
        return self.texts.get(key)

class CriticError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return "CriticError : {0}".format(self.message)
        else:
            return "CriticError error has been raised."

def error(line_number, error_type, message=None, *args):
    if args:
        for arg in args:
            message += arg
    if message != None:
        print(f"{bcolors.FAIL}{error_type} {texts.statement_errors['on-line']} {line_number} : {message}{bcolors.ENDC}")
    else:
        print(f"{bcolors.FAIL}{error_type} {texts.statement_errors['has-been-raised']} {line_number}{bcolors.ENDC}")

def lineno():
    """
    Returns the current line number where the function is called.
    """
    return inspect.currentframe().f_back.f_lineno

def split(word:str):
    """
    Splits a string into a list.
    Parameter 'word' (str) : The string to split.
    """
    return list(word)

def debug(entry_type, line, message, *args):
    """
    Debug function.
    Parameter 'entry_type' (str) : in, out, or other.
    Parameter 'line' (int) : The line where the debug is placed.
    Parameter 'message' (str) and '*args' : The message to display.
    """
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
        debug_msg = bcolors.ITALICS + bcolors.OKBLUE + entry + "\t" + "(" + str(line) + ")\t" + str(message) + bcolors.ENDC + "\n"
        with open("debug.log", "w", encoding="utf-8") as debug_file:
            debug_file.write(debug_msg)
            debug_file.close()
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

def replace_line(file_name:str, line_num:int, text:str):
    """
    Replaces a line of a file with a given string.
    Parameter 'file_name' (str) : The path to the file.
    Parameter 'line_num' (int) : The line to replace.
    Parameter 'text' (str) : The text that will replace the current line.
    """
    lines = open(file_name, 'r').readlines()
    try:
        lines[int(line_num)] = text
    except IndexError:
        lines = [text]
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()

def delete_line(file_name:str, line_number:int, condition:bool=True):
    """
    Deletes one line in a file.
    Parameter 'file_name' (str) : The path to the file.
    Parameter 'line_number' (int) : The line to delete.
    Parameter 'condition' (bool, Default : True) : Will only delete the file if the condition is True.
    """
    if condition is True:  # If the condition is verified
        file = open(file_name, "r", encoding="utf-8")  # Opens the file once
        lines = file.readlines()  # Reads its lines and stores them in a list
        file.close()  # Closes the file

        lines.pop(line_number)  # Removes the specified line from the list

        file = open(file_name, "w", encoding="utf-8")  # Re-opens the file, and erases its content
        file.writelines(lines)  # Rewrites the file with the new content (old + deleted line)
        file.close()  # Closes the file

def insert_line(path_to_file:str, index:int, value:str):
    """
    Inserts a line in a specified file, at a specific index.
    Parameter 'path_to_file' (str) : The path to the file.
    Parameter 'index' (int) : The line number where the text has to be inserted.
    Parameter 'value' (str) : The text to insert.
    """
    file = open(path_to_file, "r", encoding="utf-8")  # Opens the file
    contents = file.readlines()  # Stores the content in a list
    file.close()  # Closes the file

    contents.insert(index, value)  # Inserts the correct text at the index (creates a new line)

    file = open(path_to_file, "w", encoding="utf-8")  # Re-opens the file, and erases its content
    file.writelines(contents)  # Rewrites everything, with the modified line
    file.close()  # Closes the file again

def remove_suffix(variable:str, condition:bool=True, chars_amount:int=1):
    """
    Removes the suffix of a string.
    Parameter 'variable' (str) : The text where the suffix has to be removed.
    Parameter 'chars_amount' (int) : Default : 1. Number of chars to remove.
    Parameter 'condition' (bool) : Default : True. Will only remove if the condition is True.
    """
    if condition is True:  # If the condition is respected
        variable = variable[:-chars_amount]  # Suffix gets removed
    return variable

def add_suffix(variable:str, suffix:str, condition:bool=True):
    """
    Removes the suffix of a string.
    Parameter 'variable' (str) : The text where the suffix has to be added.
    Parameter 'suffix' (int) : Default : 1. The suffix to add.
    Parameter 'condition' (bool) : Default : True. Will only add if the condition is True.
    """
    if condition is True:
        variable += suffix
    return variable

def recreate_string(variable:list):
    """
    Recreates a string from a list.
    Parameter 'variable' (list) : The list to put together to a string.
    """
    temp_str = ""
    for element in variable:
        temp_str += str(element)
    return temp_str

#def increment_variable(variable:(int, float), count:(int, float)=1, condition:bool=True, condition_is_false:function=None)

def remove_from_string(variable:str, strs_to_remove:(list, tuple), condition:bool=True):
    """
    Removes all the specified strings from a string.
    Parameter 'variable' (str) : The string in which to replace.
    Parameter 'str_sto_remove' (list, tuple) : The strings that will be removed.
    Parameter 'condition' (bool, Default : True) : Will only execute the function if this parameter is set to True.
    """
    if condition is True:
        for element in strs_to_remove:
            variable = variable.replace(str(element), "")
    return variable

try:
    startup_file = open("startup.acpl-ini", "r+", encoding="utf-8")
except FileNotFoundError:
    print("Unable to load startup.acpl-ini !")
    sys.exit()
startup = startup_file.readlines()

for lines in startup:
    if lines.endswith("\n"):
        lines = lines.replace("\n", "")
    if lines.startswith("debug-state: "):
        lines = lines.replace("debug-state: ", "")
        debug_state = lines
        if debug_state.lower() == "false":
            debug_const = False
        else:
            debug_const = True

    if str(lines).startswith("lang: "):
        with open("startup.acpl-ini", "r", encoding="utf-8") as startup_file:
            lines = startup_file.readlines()
            lines = lines[1]
            lines = str(lines).replace("lang: ", "")
            lines = lines.replace("\n", "")
            language = lines
            try:
                with open("trad_" + language + ".json", "r", encoding="utf-8") as json_file:
                    texts = json.load(json_file)
                    json_file.close()
                    texts = Text(texts)
            except NameError:
                raise CriticError(texts.critic_errors["NameError_LanguageFile"])

ide_forbidden_files = ["main.py", "console.py", "ide.py", "compiler.py", "setup.py", "update_checker.py"]

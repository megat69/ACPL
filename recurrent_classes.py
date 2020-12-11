import inspect
import os
import sys
import json
import tkinter
from tkinter import filedialog
from datetime import datetime

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
    sys.exit()

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

def debug(entry_type, line, level, message, *args):
    """
    Debug function.
    Parameter 'entry_type' (str) : in, out, or other.
    Parameter 'line' (int) : The line where the debug is placed.
    Parameter 'message' (str) and '*args' : The message to display.
    Parameter 'level' (int) : corresponds to the level of importance of the debug message
    """
    global debug_const
    global date_format
    if debug_const >= level:
        if entry_type.lower() == "in":
            entry = "\n>>>"
        elif entry_type.lower() == "out":
            entry = "<<<"
        else:
            entry = "==="
        if args:
            for arg in args:
                message += str(arg)
        debug_msg_plain_text = entry + "\t" + "(" + str(line) + ")\t" + str(message) + "\n"
        debug_msg = bcolors.ITALICS + bcolors.OKBLUE + entry + "\t" + "(" + str(line) + ")\t" + str(message) + bcolors.ENDC + "\n"

        if not os.path.exists("/DEBUG/"):
            try:
                os.mkdir(os.getcwd()+"/DEBUG/")
            except FileExistsError:
                pass
        with open(f"DEBUG/debug_{date_format}.log", "a", encoding="utf-8") as debug_file:
            debug_file.write(debug_msg_plain_text)
            if entry == "<<<":
                debug_file.write("\n")
            debug_file.close()
        print(debug_msg)
        if len([name for name in os.listdir(os.getcwd()+"/DEBUG/")]) > 5:
            for file in os.listdir(os.getcwd()+"/DEBUG")[:5]:
                os.remove(os.getcwd()+'/DEBUG/'+file)


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

def remove_prefix(variable:str, condition:bool=True, chars_amount:int=1):
    """
        Removes the prefix of a string.
        Parameter 'variable' (str) : The text where the prefix has to be removed.
        Parameter 'chars_amount' (int) : Default : 1. Number of chars to remove.
        Parameter 'condition' (bool) : Default : True. Will only remove if the condition is True.
        """
    if condition is True:  # If the condition is respected
        variable = variable[chars_amount:len(variable)]  # Prefix gets removed
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

def recreate_string(variable:list, char_in_between:str=""):
    """
    Recreates a string from a list.
    Parameter 'variable' (list) : The list to put together to a string.
    Parameter 'char_in_between' (str) : The char to put between the elements to recompose. Nothing by default.
    """
    temp_str = ""
    for element in variable:
        temp_str += str(element) + char_in_between
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

def open_file_dialog(extensions:(list, tuple, str)=""):
    """
    Opens a "open file dialog".
    :extensions: If left empty, any extensions are accepted. If not, if the extension is not in the list,
    the function will return None.
    :return: The filename.
    """
    root = tkinter.Tk()
    root.geometry("1x1")
    root.title("Open")

    filename = filedialog.askopenfilename()

    root.withdraw()

    if extensions != "":
        if isinstance(extensions, str):
            if not filename.endswith("."+extensions):
                return None
        else:
            correct_extension = False
            for element in extensions:
                if filename.endswith("."+element):
                    correct_extension = True
                    break
            if correct_extension is False:
                return None
    return filename

def md_format(lines:(str, list)):
    """
    Formats markdown text or list.
    :param lines: The lines to format.
    :return: The formatted text, as string.
    """

    if isinstance(lines, list):
        lines = recreate_string(lines)

    while "**" in lines:
        lines = lines.replace("**", bcolors.BOLD, 1)
        lines = lines.replace("**", bcolors.ENDC, 1)

    while "*" in lines:
        lines = lines.replace("*", bcolors.ITALICS, 1)
        lines = lines.replace("*", bcolors.ENDC, 1)

    while "```" in lines:
        lines = lines.replace("```", bcolors.WARNING, 1)
        lines = lines.replace("```", bcolors.ENDC, 1)

    while "`" in lines:
        lines = lines.replace("`", bcolors.WARNING, 1)
        lines = lines.replace("`", bcolors.ENDC, 1)

    """"while "####" in lines:
        header = lines[lines.find("####") + 1:lines.find("\n")]
        print(header)
        lines = lines.replace(f"#{header}\n", f"{bcolors.HEADER}{bcolors.ITALICS}{header.replace('#', '')}{bcolors.ENDC}\n")

    while "###" in lines:
        header = lines[lines.find("###") + 1:lines.find("\n")]
        print(header)
        lines = lines.replace(f"#{header}\n", f"{bcolors.HEADER}{bcolors.BOLD}{header.replace('#', '')}{bcolors.ENDC}\n")

    while "##" in lines:
        header = lines[lines.find("##") + 1:lines.find("\n")]
        print(header)
        lines = lines.replace(f"#{header}\n", f"{bcolors.HEADER}{bcolors.BOLD}{bcolors.UNDERLINE}{header.replace('#', '')}{bcolors.ENDC}\n")
    """

    return lines


try:
    startup_file = open("startup.acpl-ini", "r+", encoding="utf-8")
except FileNotFoundError:
    print("Unable to load startup.acpl-ini !")
    sys.exit()
startup = startup_file.readlines()

date_format = datetime.now().strftime("%Y_%m_%d__%H_%M_%S")

for lines in startup:
    if lines.endswith("\n"):
        lines = lines.replace("\n", "")
    if lines.startswith("debug-state: "):
        lines = lines.replace("debug-state: ", "")
        debug_const = int(lines)

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

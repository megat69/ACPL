import inspect

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
                else:
                    HEADER = ''
                    OKBLUE = ''
                    OKGREEN = ''
                    WARNING = ''
                    FAIL = ''
                    ENDC = ''
                    BOLD = ''
                    UNDERLINE = ''
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
        print(f"{bcolors.FAIL}{error_type} {texts.statement_error['on-line']} {line_number} : {message}{bcolors.ENDC}")
    else:
        print(f"{bcolors.FAIL}{error_type} {texts.statement_errors['has-been-raised']} {line_number}{bcolors.ENDC}")

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

def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()

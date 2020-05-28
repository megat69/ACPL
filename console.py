import os
from time import sleep
import sys

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

running = True
ini_file = "startup.acpl-ini"

def replace_line(file_name, line_num, text):
    line_num -= 1
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()

try:
    startup_file = open(ini_file, "r+", encoding="utf-8")
except FileNotFoundError:
    print("Unable to load startup.acpl-ini !")
    sys.exit()
startup = startup_file.readlines()


for lines in startup:
    if lines.endswith("\n"):
        lines = lines.replace("\n", "")


    if lines.startswith("filename: "):
        lines = lines.replace("filename: ", "")
        if not lines.endswith(".acpl"):
            lines += ".acpl"
        final_filename = lines

    if lines.startswith("version: "):
        lines = lines.replace("version: ", "")
        final_version = lines

    if lines.startswith("current-version: "):
        lines = lines.replace("current-version: ", "")
        current_version = lines

    if lines.startswith("debug-state: "):
        lines = lines.replace("debug-state: ", "")
        debug_state = lines

    if lines.startswith("console-reloaded: True"):
        lines = lines.replace("console-reloaded: ", "")
        print("Console correctly reloaded.\n")
        replace_line(ini_file, 5, "console-reloaded: False")

print("ACPL Console - last stable release " + final_version + " - " + current_version + "- CC-BY-SA")

while running:
    output = None
    user_input = input("\n>>> ")

    if user_input.lower() == "end":
        print("Process ended.")
        break

    elif user_input.startswith("run"):
        user_input = user_input.replace("run ", "")
        replace_line('startup.acpl-ini', 1, 'filename: '+user_input+"\n")
        if not user_input.endswith(".acpl"):
            user_input += ".acpl"
        os.system("python main.py")

    elif user_input.startswith("version"):
        output = "Last stable release : " + final_version + "\nCurrent dev build : " + current_version

    elif user_input.startswith("eval"):
        output = "Feature not working at the moment."
        """user_input = user_input.replace("eval ", "")
        old_run_file = final_filename

        replace_line('startup.ini', 0, "filename: temp.acpl\n")

        temp_file = open("temp.acpl", "w+", encoding="utf-8")

        temp_file.write(user_input)

        os.system("python main.py")

        sleep(3)

        replace_line('startup.ini', 0, "filename: "+old_run_file+"\n")
        temp_file.close()
        #os.remove("temp.acpl")"""

    elif user_input.startswith("modify-ini "):
        user_input = user_input.replace("modify-ini ", "")
        user_input = user_input.split(" ")
        if user_input[0] == "debug-state":
            replace_line(ini_file, 4, "debug-state: "+user_input[1])
            output = "Option debug-state modified correctly in startup.ini with value " + user_input[1] + "."
        elif user_input[0] == "help":
            if user_input[1] == "debug-state":
                print("HELP : the \"debug-state\" statement asks if you want to enable or disable devlopper debug.\nType : boolean.\nDefault : False.\nActual : " + str(debug_state) + ".")
            else:
                print("Available values :\n\t- \"debug-state\"\n\nType \"modify-ini help <statement>\" for better help.")
        else:
            output = "Unable to modify this option."

    elif user_input.lower() == "help":
        print("Available commands :")
        print("\t- 'end' : Ends the console process.\n"
              "\t- 'run' : runs a specific file. Syntax : 'run <file>'.\n"
              "\t- 'about' : Gives a special message from the author concerning the language ;)\n"
              "\t- 'version' : Gives the last stable version and the actual dev build.\n"
              "\t- 'modify-ini' : Modifies a specific statement in the ini file. Better help with 'modify-ini help all'.")

    elif user_input.lower() == "about":
        about = open("about.txt", "r", encoding="utf-8")
        for line in about.readlines():
            print(line, end="")
        about.close()

    elif user_input.lower() == "restart" or user_input.lower() == "reload":
        print("Reloading console...")
        replace_line(ini_file, 5, "console-reloaded: True")
        sleep(2)
        os.system("python console.py")
        break

    else:
        output = "Command unknown."

    if output != None:
        print("OUTPUT :\n" + output)


startup_file.close()

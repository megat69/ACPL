import os
from time import sleep
import sys
import json
from recurrent_classes import *
import requests
import platform
import shlex

running = True
ini_file = "startup.acpl-ini"

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

    if lines.startswith("startup-check-update: "):
        lines = lines.replace("startup-check-update: ", "")
        check_update = lines

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

    if lines.startswith("console-reloaded: True"):
        lines = lines.replace("console-reloaded: ", "")
        print(f"{bcolors.OKGREEN}{texts.console['console-correctly-reloaded']}\n{bcolors.ENDC}")
        replace_line(ini_file, 5, "console-reloaded: False\n")

print(bcolors.BOLD + texts.console['bootup-message'].format(final_version, current_version) + bcolors.ENDC)
startup_file.close()
if check_update == "True":
    os.system("python update_checker.py")
startup_file = open(ini_file, "r", encoding="utf-8").readlines()

while running:
    output = None
    user_input = input("\n>>> ")

    debug("in", lineno(), user_input)

    if user_input.lower() == "end":
        print(f"{bcolors.OKBLUE}{texts.console['process-ended']}{bcolors.ENDC}")
        break

    elif user_input.startswith("run"):
        user_input = user_input.replace("run ", "")
        replace_line('startup.acpl-ini', 0, 'filename: ' + user_input + "\n")
        if not user_input.endswith(".acpl"):
            user_input += ".acpl"
        print(f"{bcolors.OKBLUE}{texts.console['launch-code-file'].format(user_input)}{bcolors.ENDC}")
        sleep(1.7)
        os.system("python main.py")

    elif user_input.startswith("version"):
        output = f"{texts.console['last-stable-release']} : {final_version}\n{texts.console['current-dev-build']} : " + current_version

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
            replace_line(ini_file, 4, "debug-state: " + user_input[1] + "\n")
            output = texts.console_modify_ini["debug-state-modified"].format(user_input[1])
        elif user_input[0] == "lang":
            replace_line(ini_file, 1, "lang: " + user_input[1] + "\n")
            output = texts.console_modify_ini["lang-modified"].format(user_input[1])
        elif user_input[0] == "use-colors":
            replace_line(ini_file, 6, "use-colors: " + user_input[1] + "\n")
            output = texts.console_modify_ini["use-colors-modified"].format(user_input[1])
        elif user_input[0] == "process-time-round-numbers":
            replace_line(ini_file, 7, "process-time-round-numbers: " + user_input[1] + "\n")
            output = "process-time-round-numbers modified with value {}.".format(user_input[1])
        elif user_input[0] == "open-compiled-file":
            replace_line(ini_file, 9, "open-compiled-file: " + str(user_input[1]) + "\n")
            output = "open-compiled-file modified with value {}.".format(user_input[1])
        elif user_input[0] == "leave-comments-at-compiling":
            replace_line(ini_file, 10, "leave-comments-at-compiling: " + str(user_input[1]) + "\n")
            output = "leave-comments-at-compiling modified with value {}.".format(user_input[1])
        elif user_input[0] == "startup-check-update":
            replace_line(ini_file, 11, "startup-check-update: " + str(user_input[1]) + "\n")
            output = "startup-check-update modified with value {}.".format(user_input[1])
        elif user_input[0] == "compiling-style":
            replace_line(ini_file, 12, "compiling-style: " + str(user_input[1]) + "\n")
            output = "compiling-style modified with value {}.".format(user_input[1])
        elif user_input[0] == "compile-ask-for-replace":
            replace_line(ini_file, 13, "compile-ask-for-replace: " + str(user_input[1]) + "\n")
            output = "compile-ask-for-replace modified with value {}.".format(user_input[1])
        elif user_input[0] == "help":
            if user_input[1] == "debug-state":
                print(texts.console_modify_ini['debug-state-help'].format(str(debug_state)))
            elif user_input[1] == "lang":
                print(texts.console_modify_ini['lang-help'].format(str(language)))
            elif user_input[1] == "use-colors":
                print(texts.console_modify_ini['use-colors-help'].format(str(bcolors.colors_used)))
            elif user_input[1] == "process-time-round-numbers":
                print(texts.console_modify_ini['process-time-round-numbers'].format(str(bcolors.colors_used)))
            elif user_input[1] == "open-compiled-file":
                print(texts.console_modify_ini['open-compiled-file'].format(str(bcolors.colors_used)))
            elif user_input[1] == "leave-comments-at-compiling":
                print(texts.console_modify_ini['leave-comments-at-compiling'].format(str(bcolors.colors_used)))
            elif user_input[1] == "startup-check-update":
                print(texts.console_modify_ini['startup-check-update'].format(str(bcolors.colors_used)))
            elif user_input[1] == "compiling-style":
                print("\"expanded\" or \"compacted\"")
            else:
                print(texts.console_modify_ini["else-help"])
        else:
            output = texts.console_modify_ini["unable-to-modify-option"]

    elif user_input.lower() == "help":
        print(texts.console_help["available-commands"] + " :")
        print(f"\t- 'end' : {texts.console_help['end']}\n"
              f"\t- 'run' : {texts.console_help['run']}\n"
              f"\t- 'about' : {texts.console_help['about']}\n"
              f"\t- 'version' : {texts.console_help['version']}\n"
              f"\t- 'modify-ini' : {texts.console_help['modify-ini']}\n"
              f"\t- 'update' : Launches the update program.\n"
              f"\t- 'pyrun' : Runs a specified python file\n"
              f"\t- 'compile' : Compiles an ACPL file to a Python file\n"
              f"\t- 'ini-content' : Displays the content of the ini file\n"
              f"\t- 'open' : Opens a specific file in its default program\n"
              f"\t- 'display' : Prints the content of a specified file.\n")

    elif user_input.lower() == "about":
        if language == "fr":
            language_for_about = "fr"
        else:
            language_for_about = "en"
        about = open(f"about_{language_for_about}.txt", "r", encoding="iso8859_15")
        for line in about.readlines():
            print(line, end="")
        about.close()

    elif user_input.lower() == "restart" or user_input.lower() == "reload":
        print(texts.console["reloading"])
        replace_line(ini_file, 5, "console-reloaded: True\n")
        sleep(2)
        os.system("python console.py")
        break

    elif user_input.lower() == "update":
        os.system("python update_checker.py")

    elif user_input.startswith("lib"):
        user_input = user_input.replace("lib ", "")
        if user_input.startswith("install"):
            user_input = user_input.replace("install ", "")
            url = "https://raw.githubusercontent.com/megat69/ACPL/master/libs/lib_" + user_input + ".py"
            r = requests.get(url)
            existing = r.status_code == 200
            if not existing:
                print("Error : Lib does not exist !")
                continue
            with open(f"libs/lib_{user_input}.py", "wb") as code:
                code.write(r.content)
            print(f"Library {user_input} installed !")
        elif user_input.startswith("update"):
            user_input = user_input.replace("update ", "")
            url = "https://raw.githubusercontent.com/megat69/ACPL/master/libs/lib_" + user_input + ".py"
            r = requests.get(url)
            existing = r.status_code == 200
            if not existing:
                print("Error : Lib does not exist !")
                continue
            with open(f"libs/lib_{user_input}.py", "wb") as code:
                code.write(r.content)
            print(f"Library {user_input} updated !")
        else:
            raise CriticError

    elif user_input.startswith("compile"):
        user_input = user_input.replace("compile ", "", 1)
        user_input = user_input.split(" ")
        if len(user_input) == 1:
            user_input.append(user_input[0]+".py")
        if not user_input[0].endswith(".acpl"):
            user_input[0] += ".acpl"
        replace_line('startup.acpl-ini', 0, 'filename: '+user_input[0]+"\n")
        replace_line("startup.acpl-ini", 8, "compiled-file-filename: "+user_input[1]+"\n")
        os.system("python compiler.py")

    elif user_input.startswith("pyrun"):
        user_input = user_input.replace("pyrun ", "", 1)
        if user_input.endswith("\n"):
            user_input = user_input[:-1]
        if not user_input.endswith(".py"):
            user_input += ".py"
        print(f"{bcolors.OKBLUE}Launching {user_input}.{bcolors.ENDC}")
        os.system(f"python {user_input}")

    elif user_input.startswith("open"):
        user_input = user_input.replace("open ", "", 1)
        if user_input.endswith("\n"):
            user_input = user_input[:-1]
        print(f"{bcolors.OKBLUE}Opening {user_input}.{bcolors.ENDC}")
        if platform.system() == "Windows":
            os.system("start " + user_input)
        else:
            os.system("open " + shlex.quote(user_input))
        print(f"{bcolors.OKGREEN}File opened successfully.{bcolors.ENDC}")

    elif user_input.startswith("ini-content"):
        startup_file = open("startup.acpl-ini", "r")
        for startup_lines in startup_file.readlines():
            print(startup_lines, end="")
        startup_file.close()

    elif user_input.startswith("display"):
        user_input = user_input.replace("display ", "", 1)
        if user_input.endswith("\n"):
            user_input = user_input[:-1]
        file = open(user_input, "r", encoding="utf-8")
        for file_line in file.readlines():
            print(file_line, end="")
        file.close()
        print(f"{bcolors.OKBLUE}File content ends here.{bcolors.ENDC}")

    elif user_input.startswith("creator"): # Easter egg ?
        ascii_art = open("ascii-art.txt", "r")
        for ascii_line in ascii_art.readlines():
            print(ascii_line, end="")
        ascii_art.close()
        print("\n\nMerci d'avoir jeté un coup d'oeil au code.")

    else:
        output = texts.console["unknown-command"]

    if output is not None:
        print(f"{bcolors.WARNING}{texts.console['output'].upper()} :{bcolors.ENDC}\n{output}")

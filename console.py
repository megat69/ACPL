import os
from time import sleep
import sys
import json
from recurrent_classes import *
import requests

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



print(bcolors.BOLD+texts.console['bootup-message'].format(final_version, current_version)+bcolors.ENDC)
startup_file.close()
os.system("python update_checker.py")
startup_file = open(ini_file, "r", encoding="utf-8").readlines()

while running:
    output = None
    user_input = input("\n>>> ")

    if user_input.lower() == "end":
        print(f"{bcolors.OKBLUE}{texts.console['process-ended']}{bcolors.ENDC}")
        break

    elif user_input.startswith("run"):
        user_input = user_input.replace("run ", "")
        replace_line('startup.acpl-ini', 0, 'filename: '+user_input+"\n")
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
            replace_line(ini_file, 4, "debug-state: "+user_input[1]+"\n")
            output = texts.console_modify_ini["debug-state-modified"].format(user_input[1])
        elif user_input[0] == "lang":
            replace_line(ini_file, 1, "lang: "+user_input[1]+"\n")
            output = texts.console_modify_ini["lang-modified"].format(user_input[1])
        elif user_input[0] == "use-colors":
            replace_line(ini_file, 6, "use-colors: "+user_input[1]+"\n")
            output = texts.console_modify_ini["use-colors-modified"].format(user_input[1])
        elif user_input[0] == "process-time-round-numbers":
            replace_line(ini_file, 7, "process-time-round-numbers: "+user_input[1]+"\n")
            output = "process-time-round-numbers modified with value {}.".format(user_input[1])
        elif user_input[0] == "help":
            if user_input[1] == "debug-state":
                print(texts.console_modify_ini['debug-state-help'].format(str(debug_state)))
            elif user_input[1] == "lang":
                print(texts.console_modify_ini['lang-help'].format(str(language)))
            elif user_input[1] == "use-colors":
                print(texts.console_modify_ini['use-colors-help'].format(str(bcolors.colors_used)))
            elif user_input[1] == "process-time-round-numbers":
                print(texts.console_modify_ini['process-time-round-numbers'].format(str(bcolors.colors_used)))
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
              f"\t- 'modify-ini' : {texts.console_help['modify-ini']}\n")

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
            url = "https://raw.githubusercontent.com/megat69/ACPL/master/libs/lib_"+user_input+".py"
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
            url = "https://raw.githubusercontent.com/megat69/ACPL/master/libs/lib_"+user_input+".py"
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
        replace_line('startup.acpl-ini', 0, 'filename: '+user_input+"\n")
        if not user_input.endswith(".acpl"):
            user_input += ".acpl"
        print(f"{bcolors.OKBLUE}{texts.console['compile-code-file'].format(user_input)}{bcolors.ENDC}")
        sleep(1.7)
        os.system("python compiler.py")

    else:
        output = texts.console["unknown-command"]

    if output != None:
        print(f"{bcolors.WARNING}{texts.console['output'].upper()} :{bcolors.ENDC}\n{output}")

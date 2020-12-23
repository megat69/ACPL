import os
from time import sleep
import sys
import json
from recurrent_classes import *
import requests
import platform
import shlex
import webbrowser
import tkinter as tk

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

    if lines.startswith("console-reloaded:"):
        lines = lines.replace("console-reloaded: ", "")
        if lines.startswith("True"):
            console_reloaded = True
            print(f"{bcolors.OKGREEN}{texts.console['console-correctly-reloaded']}\n{bcolors.ENDC}")
        else:
            console_reloaded = False
        replace_line(ini_file, 5, "console-reloaded: False\n")

    if lines.startswith("startup-check-update"):
        lines = lines.replace("startup-check-update: ", "", 1)
        check_update = lines.lower() != "false"
startup_file.close()

print(bcolors.BOLD + texts.console['bootup-message'].format(final_version, current_version) + bcolors.ENDC)
startup_file.close()
if check_update == "True" and console_reloaded is False:
    launch_py_file("updater_main")

while running:
    output = None
    user_input = input("\n>>> ")

    debug("in", lineno(), 1, user_input)

    if user_input != "redo":
        og_user_input = user_input

    if user_input == "redo":
        user_input = last_user_input

    if user_input.lower() == "end":
        print(f"{bcolors.OKBLUE}{texts.console['process-ended']}{bcolors.ENDC}")
        break

    elif user_input.startswith("run"):
        if user_input == "run":
            user_input = open_file_dialog(extensions="acpl")
            if user_input is not None:
                replace_line('startup.acpl-ini', 0, 'filename: ' + user_input + "\n")
            else:
                print(f"{bcolors.FAIL}Cannot run this file.{bcolors.ENDC}")
                continue
        else:
            user_input = user_input.replace("run ", "")
            replace_line('startup.acpl-ini', 0, 'filename: ' + user_input + "\n")
            if not user_input.endswith(".acpl"):
                user_input += ".acpl"

        print(f"{bcolors.OKBLUE}{texts.console['launch-code-file'].format(user_input)}{bcolors.ENDC}")
        sleep(1.7)
        launch_py_file("main")


    elif user_input.startswith("rerun"):
        print(f"{bcolors.OKBLUE}Running last file again...{bcolors.ENDC}")
        sleep(1.7)
        launch_py_file("main.py")

    elif user_input.startswith("version"):
        output = f"{texts.console['last-stable-release']} : {final_version}\n{texts.console['current-dev-build']} : " + current_version

    elif user_input.startswith("eval"):
        output = "Feature not working at the moment."
        """user_input = user_input.replace("eval ", "")
        old_run_file = final_filename
        replace_line('startup.ini', 0, "filename: temp.acpl\n")
        temp_file = open("temp.acpl", "w+", encoding="utf-8")
        temp_file.write(user_input)
        launch_py_file("main")
        sleep(3)
        replace_line('startup.ini', 0, "filename: "+old_run_file+"\n")
        temp_file.close()
        #os.remove("temp.acpl")"""

    elif user_input.startswith("setting"):
        window = tk.Tk()
        window.geometry("500x250")
        window.title("ACPL Settings")
        window.iconbitmap("ACPL_Icon.ico")

        def toggle_use_colors():
            global use_colors
            global grid_elements
            global tk, window
            use_colors = use_colors == False
            grid_elements[2][1]["text"] = str(use_colors)

        def toggle_open_compiled_file():
            global open_compiled_file
            global grid_elements
            global tk, window
            open_compiled_file = open_compiled_file == False
            grid_elements[4][1]["text"] = str(open_compiled_file)

        def toggle_leave_comments_at_compiling():
            global leave_comments_at_compiling
            global grid_elements
            global tk, window
            leave_comments_at_compiling = leave_comments_at_compiling == False
            grid_elements[5][1]["text"] = str(leave_comments_at_compiling)

        def toggle_startup_check_update():
            global startup_check_update
            global grid_elements
            global tk, window
            startup_check_update = startup_check_update == False
            grid_elements[6][1]["text"] = str(startup_check_update)

        def toggle_compile_ask_for_replace():
            global compile_ask_for_replace
            global grid_elements
            global tk, window
            compile_ask_for_replace = compile_ask_for_replace == False
            grid_elements[8][1]["text"] = str(compile_ask_for_replace)

        def save_settings():
            global grid_elements, language, debug_state, process_time_round_numbers, compiling_style
            # Saving language
            language = grid_elements[0][1].get()
            if language not in ("az", "de", "en", "fr", "it", "nl", "tr"):
                print(f"{bcolors.FAIL}Unknow language. Language set back to 'en'.{bcolors.ENDC}")
                grid_elements[0][1].delete(0, tk.END)
                grid_elements[0][1].insert(0, "en")
                language = "en"
            # Saving debug state
            debug_state = grid_elements[1][1].get()
            try:
                if int(debug_state) < 0:
                    print(f"{bcolors.FAIL}Cannot set debug state under 0.{bcolors.ENDC}")
                    debug_state = 0
                elif int(debug_state) > 3:
                    print(f"{bcolors.FAIL}Cannot set debug state over 3.{bcolors.ENDC}")
                    debug_state = 3
                else:
                    debug_state = int(debug_state)
            except ValueError:
                print(f"{bcolors.FAIL}Debug state has to be an integer.{bcolors.ENDC}")
                debug_state = 0
            grid_elements[1][1].delete(0, tk.END)
            grid_elements[1][1].insert(0, str(debug_state))
            # Saving process time round numbers
            try:
                process_time_round_numbers = int(grid_elements[3][1].get())
            except ValueError:
                print(f"{bcolors.FAIL}Process time round numbers has to be an integer.{bcolors.ENDC}")
                process_time_round_numbers = 6
            grid_elements[3][1].delete(0, tk.END)
            grid_elements[3][1].insert(0, str(process_time_round_numbers))
            # Saving compiling style
            compiling_style = grid_elements[7][1].get()

        # Setting up all the elements for the grid
        grid_elements = [[0, 0] for k in range(9)]
        grid_elements[0][0] = tk.Label(window, text="Language : ")
        grid_elements[0][1] = tk.Entry(window)
        grid_elements[0][1].insert(tk.END, language)
        grid_elements[1][0] = tk.Label(window, text="Debug state (int between 0 and 3) : ")
        grid_elements[1][1] = tk.Entry(window)
        grid_elements[1][1].insert(tk.END, str(debug_state))
        grid_elements[2][0] = tk.Label(window, text="Use colors : ")
        grid_elements[2][1] = tk.Button(window, text=str(use_colors), command=toggle_use_colors)
        grid_elements[3][0] = tk.Label(window, text="Numbers after the dot in the process time (integer) : ")
        grid_elements[3][1] = tk.Entry(window)
        grid_elements[3][1].insert(tk.END, str(process_time_round_numbers))
        grid_elements[4][0] = tk.Label(window, text="Open compiled file after compiling : ")
        grid_elements[4][1] = tk.Button(window, text=str(open_compiled_file), command=toggle_open_compiled_file)
        grid_elements[5][0] = tk.Label(window, text="Leave comments at compiling : ")
        grid_elements[5][1] = tk.Button(window, text=str(leave_comments_at_compiling), command=toggle_leave_comments_at_compiling)
        grid_elements[6][0] = tk.Label(window, text="Check updates at startup : ")
        grid_elements[6][1] = tk.Button(window, text=str(startup_check_update), command=toggle_startup_check_update)
        grid_elements[7][0] = tk.Label(window, text="Compiling style : ")
        grid_elements[7][1] = tk.Entry(window)
        grid_elements[7][1].insert(tk.END, str(compiling_style))
        grid_elements[8][0] = tk.Label(window, text="Ask for replace before compiling : ")
        grid_elements[8][1] = tk.Button(window, text=str(compile_ask_for_replace), command=toggle_compile_ask_for_replace)
        grid_elements.append(tk.Button(window, text="SAVE", command=save_settings, bd=4, bg="gray1", fg="orange red"))

        for i in range(len(grid_elements)-1):
            grid_elements[i][0].grid(row=i, column=0)
            grid_elements[i][1].grid(row=i, column=1)

        grid_elements[9].grid(row=9, column=0, columnspan=2)

        window.mainloop()
        print(f"{bcolors.FAIL}Settings closed and saved.{bcolors.ENDC}")
        replace_line("startup.acpl-ini", 1, f"lang: {language}\n")
        replace_line("startup.acpl-ini", 4, f"debug-state: {str(debug_state)}\n")
        replace_line("startup.acpl-ini", 6, f"use-colors: {str(use_colors)}\n")
        replace_line("startup.acpl-ini", 7, f"process-time-round-numbers: {str(process_time_round_numbers)}\n")
        replace_line("startup.acpl-ini", 9, f"open-compiled-file: {str(open_compiled_file)}\n")
        replace_line("startup.acpl-ini", 10, f"leave-comments-at-compiling: {str(leave_comments_at_compiling)}\n")
        replace_line("startup.acpl-ini", 11, f"startup-check-update: {str(startup_check_update)}\n")
        replace_line("startup.acpl-ini", 13, f"compile-ask-for-replace: {str(compile_ask_for_replace)}\n")
        # OLD modify-ini
        """
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
        """

    elif user_input.lower().startswith("doc"):
        webbrowser.open("https://github.com/megat69/ACPL/blob/master/README.md")

    elif user_input.lower() == "help":
        print(texts.console_help["available-commands"] + " :")
        print(f"\t- 'end' : {texts.console_help['end']}\n"
              f"\t- 'run' : {texts.console_help['run']}\n"
              f"\t- 'about' : {texts.console_help['about']}\n"
              f"\t- 'version' : {texts.console_help['version']}\n"
              f"\t- 'settings' : Opens up a dialog box which allows you to tweak your settings.\n"
              f"\t- 'update' : Launches the update program.\n"
              f"\t- 'pyrun' : Runs a specified python file\n"
              f"\t- 'compile' : Compiles an ACPL file to a Python file\n"
              f"\t- 'ini-content' : Displays the content of the ini file\n"
              f"\t- 'open' : Opens a specific file in its default program\n"
              f"\t- 'display' : Prints the content of a specified file.\n"
              f"\t- 'change-line'/'modify-line' : Modifies a specific line in a plain text file.\n"
              f"\t- 'redo' : Reuses the last command.\n"
              f"\t- 'lib <install:delete:doc> <lib_name>' : Respectively installs, delete, or gives the documentation of the specified lib.\n")

    elif user_input.lower() == "about":
        about = open(f"about_{language}.txt", "r", encoding="iso8859_15")
        for line in about.readlines():
            print(line, end="")
        about.close()

    elif user_input.lower() == "restart" or user_input.lower() == "reload":
        print(texts.console["reloading"])
        replace_line(ini_file, 5, "console-reloaded: True\n")
        sleep(2)
        launch_py_file("console")
        break

    elif user_input.lower() == "update":
        try:
            os.system("python updater_main.py")
            sys.exit()
        except:
            print(f"{bcolors.FAIL}Your system does not support the invocation of new Python processes.\n"
                  f"Please run the {bcolors.ITALICS}{bcolors.OKGREEN}updater_main.py{bcolors.ENDC}{bcolors.FAIL} "
                  f"script manually.{bcolors.ENDC}")
            sys.exit()
        #print(f"{bcolors.FAIL}Update checking has been temporarily disabled.\nThanks for your understanding.{bcolors.ENDC}")

    elif user_input.startswith("lib"):
        user_input = user_input.replace("lib ", "")
        if user_input.startswith("install"):
            user_input = user_input.replace("install ", "")
            url = "https://raw.githubusercontent.com/megat69/ACPL/master/acpl_libs/fx_" + user_input + ".py"
            r = requests.get(url)
            existing = r.status_code == 200
            if not existing:
                print("Error : Lib does not exist !")
                continue
            with open(f"acpl_libs/fx_{user_input}.py", "wb") as code:
                code.write(r.content)
            print(f"Library {user_input} installed !")
        elif user_input.startswith("delete"):
            user_input = user_input.replace("delete ", "", 1)
            try:
                os.remove(f"acpl_libs/fx_{user_input}.py")
                print(f"Deleted lib {user_input}.")
            except FileNotFoundError:
                print("Lib not installed, unable to uninstall.")
        elif user_input.startswith("doc"):
            user_input = user_input.replace("documentation", "", 1)
            user_input = user_input.replace("doc", "", 1)
            user_input = remove_prefix(user_input, user_input.startswith(" "))
            if not os.path.exists(f"acpl_libs/doc_{user_input}.md"):
                url = "https://raw.githubusercontent.com/megat69/ACPL/master/acpl_libs/doc_" + user_input + ".md"
                r = requests.get(url)
                existing = r.status_code == 200
                if not existing:
                    print("Error : Lib does not exist !")
                    continue
                with open(f"acpl_libs/doc_{user_input}.md", "wb") as code:
                    code.write(r.content)

            documentation = open(f"acpl_libs/doc_{user_input}.md")
            documentation_content = md_format(documentation.readlines())
            documentation.close()
            print(documentation_content)
            del documentation_content
        else:
            output = "Wrong amount of arguments."

    elif user_input.startswith("compile"):
        if user_input == "compile":
            user_input = open_file_dialog(extensions="acpl")
            if user_input is not None:
                user_input = [user_input, user_input]
            else:
                continue
        else:
            user_input = user_input.replace("compile ", "", 1)
            user_input = user_input.split(" ")
            if len(user_input) == 1:
                user_input = [user_input[0], user_input[0]]
            if not user_input[0].endswith(".acpl"):
                user_input[0] += ".acpl"
            if ("." in user_input[0] and not user_input[0].endswith(".acpl")) or (
                    "." in user_input[1] and not user_input[1].endswith(".acpl")):
                print(
                    f"{bcolors.FAIL}Unable to compile that kind of file (extension '.{user_input[0].split('.')[1]}').")
                continue
        replace_line('startup.acpl-ini', 0, 'filename: ' + user_input[0] + "\n")
        replace_line("startup.acpl-ini", 8, "compiled-file-filename: " + user_input[1] + "\n")
        launch_py_file("compiler")

    elif user_input.startswith("pyrun"):
        user_input = user_input.replace("pyrun ", "", 1)
        user_input = remove_suffix(user_input, condition=user_input.endswith("\n"))
        if not user_input.endswith(".py"):
            user_input += ".py"
        print(f"{bcolors.OKBLUE}Launching {user_input}.{bcolors.ENDC}")
        launch_py_file(user_input)
        print(f"{bcolors.OKBLUE}End of the file.{bcolors.ENDC}")

    elif user_input.lower().startswith("ide"):
        # Opens IDE
        print(f"{bcolors.OKBLUE}Opening ACPL IDE...{bcolors.ENDC}")
        launch_py_file("ide")
        print(f"{bcolors.OKBLUE}IDE closed.{bcolors.ENDC}")

    elif user_input.startswith("open"):
        user_input = user_input.replace("open ", "", 1)
        user_input = remove_suffix(user_input, condition=user_input.endswith("\n"))
        print(f"{bcolors.OKBLUE}Opening {user_input}.{bcolors.ENDC}")
        if platform.system() == "Windows":
            os.system("start " + user_input)
        else:
            os.system("open " + shlex.quote(user_input))
        print(f"{bcolors.OKGREEN}File opened successfully.{bcolors.ENDC}")

    elif user_input.startswith("ini-content"):
        startup_file = open(ini_file, "r")
        data = {}
        for line in startup_file.readlines():
            data[line.split(": ")[0]] = remove_suffix(line.split(": ")[1], line.split(": ")[1].endswith("\n"))
        for element in data:
            print(f"{element} : {data[element]}")
        startup_file.close()

    elif user_input.startswith("display"):
        user_input = user_input.replace("display ", "", 1)
        user_input = remove_suffix(user_input, condition=user_input.endswith("\n"))
        try:
            file = open(user_input, "r", encoding="utf-8")
            for file_line in file.readlines():
                print(file_line, end="")
            file.close()
            print(f"{bcolors.OKBLUE}File content ends here.{bcolors.ENDC}")
        except FileNotFoundError:
            print(f"{bcolors.FAIL}File not found.{bcolors.ENDC}")

    elif user_input.startswith("creator"): # Easter egg ?
        ascii_art = open("ascii-art.txt", "r")
        for ascii_line in ascii_art.readlines():
            print(ascii_line, end="")
        ascii_art.close()
        print("\n\nMerci d'avoir jeté un coup d'oeil au code.")

    elif user_input.startswith("change-line") or user_input.startswith("modify-line"):  # change-line <file> <line_number> <new_text>
        user_input = user_input.replace("change-line ", "", 1)
        user_input = user_input.replace("modify-line ", "", 1)
        user_input = user_input.split(" ")
        for i in range(3, len(user_input)):
            user_input[2] += " " + user_input[i]
        while len(user_input) > 3:
            user_input.pop(3)
        replace_line(user_input[0], user_input[1], user_input[2])
        print(f"Line {user_input[1]} modified in {user_input[0]} with value :\n{user_input[2]}")

    elif user_input.startswith("changelog"):
        changelog_file = open("changelog.md", "r")
        changelog = changelog_file.readlines()
        changelog_file.close()
        changelog = md_format(changelog)
        print(changelog)

    elif user_input.startswith("debug"):
        user_input = user_input.replace("debug ", "", 1)
        if not user_input.endswith(".acpl"):
            user_input += ".acpl"
        print(f"{bcolors.FAIL}Beginning to debug {user_input}...{bcolors.ENDC}")
        replace_line("startup.acpl-ini", 0, f"filename: {user_input}\n")
        replace_line("startup.acpl-ini", 14, "debugger-enabled: True\n")
        launch_py_file("main.py")

    else:
        output = texts.console["unknown-command"]
    last_user_input = og_user_input

    if output is not None:
        print(f"{bcolors.WARNING}{texts.console['output'].upper()} :{bcolors.ENDC}\n{output}")

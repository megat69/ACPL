import os
from time import sleep
import sys
import json
from recurrent_classes import *
import requests
import platform
import shlex
from pynput.keyboard import Key, Listener


def on_press(key):
    global pressed_key
    global debug_state
    global Key

    if debug_state > 0:
        print('{0} pressed'.format(key))
    pressed_key = key
    try:
        is_char = True
        pressed_key = pressed_key.char
    except AttributeError:
        is_char = False

    if pressed_key == Key.space:
        pressed_key = " "
        is_char = True
    elif pressed_key == Key.enter:
        if trigger_autocomplete() is False:
            pressed_key = "\n"
            is_char = True
        else:
            pressed_key = "NOINTERPRETATION"
    elif pressed_key == Key.esc or pressed_key == Key.down or pressed_key == Key.left or pressed_key == Key.right or pressed_key == Key.up or pressed_key == Key.backspace or pressed_key == Key.delete:
        is_char = True
    elif pressed_key == Key.tab:
        pressed_key = "\t"
        is_char = True

    if is_char is True:
        return False


def on_release(key):
    global debug_state
    global Key
    if debug_state > 0:
        print('{0} release'.format(key))
    if key == Key.esc:
        # Stop listener
        return False


def trigger_autocomplete():
    global lines
    global current_line
    global current_cursor_position
    global pressed_key

    if lines[current_line] == "pr" or lines[current_line] == "pri" or lines[current_line] == "prin":
        lines[current_line] = "print "
        current_cursor_position = 6
        return True
    elif lines[current_line] == "va":
        lines[current_line] = "var "
        current_cursor_position = 4
        return True
    elif lines[current_line] == "el" or lines[current_line] == "els":
        lines[current_line] = "else"
        current_cursor_position = 4
        return True
    elif lines[current_line] == "fo":
        lines[current_line] = "for "
        current_cursor_position = 4
        return True
    elif lines[current_line] == "wh" or lines[current_line] == "whi" or lines[current_line] == "whil":
        lines[current_line] = "while "
        current_cursor_position = 7
        return True
    else:
        return False

# ACPL IDE successfully opened.
print(bcolors.OKBLUE + texts.ide["IDE_SuccessfullyOpened"] + bcolors.ENDC)

# Part removed on 29/11/2020
# Action : File opening in command line.
# Replaced by dialog box.
"""
code_file_filename = input(f"{bcolors.OKBLUE}Enter code file filename : {bcolors.ENDC}")
if not code_file_filename.endswith(".acpl") and "." not in code_file_filename:
    code_file_filename += ".acpl"

if code_file_filename.startswith("ACPL_IDE_NEW "):
    user_input = code_file_filename.replace("ACPL_IDE_NEW ", "", 1)
    if os.path.exists(user_input):
        confirm = input(f"{bcolors.FAIL}This file ({user_input}) already exists. Are you sure you want to replace it ? (Yes/No) {bcolors.ENDC}")
        while confirm.lower() != "yes" and confirm.lower() != "no":
            confirm = input(f"{bcolors.FAIL}This file ({user_input}) already exists. Are you sure you want to replace it ? (Yes/No) {bcolors.ENDC}")
        if confirm.lower() == "yes":
            new_file = open(user_input, "w", encoding="utf-8")
            new_file.writelines(["\n"])
            new_file.close()
            code_file_filename = user_input
            confirm = None
    else:
        new_file = open(user_input, "w", encoding="utf-8")
        new_file.write("\n")
        new_file.close()
        code_file_filename = user_input
        user_input = None
while not os.path.exists(code_file_filename) or code_file_filename in ide_forbidden_files:
    code_file_filename = input(f"{bcolors.FAIL}Sorry, this file ({code_file_filename}) doesn't exist. Can you retry ?\nEnter the code file filename : {bcolors.ENDC}")
    if not code_file_filename.endswith(".acpl"):
        code_file_filename += ".acpl"
"""

try:
    config_file = open("startup.acpl-ini", "r")
except FileNotFoundError:
    print(texts.critic_errors["ImpossibleLoad_StartupIni"])
    sys.exit()

for config_line in config_file.readlines():
    if config_line.startswith("debug-state: "):  # debug
        config_line = config_line.replace("debug-state: ", "")
        debug_state = int(config_line)

config_file.close()

code_file_filename = open_file_dialog()
current_folder = os.path.dirname(code_file_filename)
current_filename = os.path.basename(code_file_filename)

acpl_ide_metadata = {}
if not os.path.exists(current_folder+"/.acpl_ide"):
    acpl_ide_metadata_file = open(current_folder+"/.acpl_ide", "w")
    acpl_ide_metadata_file.writelines(json.dumps(acpl_ide_metadata))
    acpl_ide_metadata_file.close()

with open(current_folder+"/.acpl_ide", "r") as f:
    acpl_ide_metadata = json.load(f)
    f.close()

print("\n\n")

# VARIABLES
running = True
try:
    current_line = acpl_ide_metadata[current_filename]["line"]
except KeyError:
    current_line = 0

try:
    current_cursor_position = acpl_ide_metadata[current_filename]["cursor_position"]
except KeyError:
    current_cursor_position = 0

# UNDEFINED VARIABLES
pressed_key = None

while running is True:
    # Read lines again
    code_file = open(code_file_filename, "r", encoding="utf-8")
    lines = code_file.readlines()
    code_file.close()

    # Setting up the displayed lines
    code_file = open(code_file_filename, "r", encoding="utf-8")
    displayed_lines = code_file.readlines()
    code_file.close()

    if len(lines) <= 10:
        loop_times = [0, len(lines)]
    else:
        if current_line < 5:
            loop_times = [0, 10]
        elif current_line > len(lines)-5:
            loop_times = [len(lines)-10, len(lines)]
        else:
            loop_times = [current_line-5, current_line+5]

    for i in range(loop_times[0], loop_times[1]):
        if lines[i].endswith("\n"):  # Break removal
            lines[i] = remove_suffix(lines[i])
            displayed_lines[i] = remove_suffix(displayed_lines[i])

        if i < 10:
            actual_line = "0" + str(i)
        else:
            actual_line = str(i)

        if i == current_line:  # Line to edit
            print(f"{bcolors.HEADER}({actual_line}) >>> {bcolors.ENDC}", end="")
            temp_line = split(displayed_lines[current_line])
            temp_line.insert(current_cursor_position, f"{bcolors.HEADER}|{bcolors.ENDC}")
            displayed_lines[current_line] = ""
            for char in temp_line:
                displayed_lines[current_line] += char
            del temp_line
        else:
            print(f"({actual_line})     ", end="")
        del actual_line

        # SYNTAX HIGHLIGHTING
        if code_file_filename.endswith(".acpl"):
            # green
            displayed_lines[i] = displayed_lines[i].replace("print", f"{bcolors.OKGREEN}print{bcolors.ENDC}{bcolors.WARNING}", 1)
            displayed_lines[i] = displayed_lines[i].replace("input", f"{bcolors.OKGREEN}input{bcolors.ENDC}{bcolors.WARNING}", 1)
            displayed_lines[i] = displayed_lines[i].replace("var", f"{bcolors.OKGREEN}var{bcolors.ENDC}{bcolors.WARNING}", 1)
            displayed_lines[i] = displayed_lines[i].replace("deletevar", f"{bcolors.OKGREEN}deletevar{bcolors.ENDC}{bcolors.WARNING}", 1)
            displayed_lines[i] = displayed_lines[i].replace("if", f"{bcolors.OKGREEN}{bcolors.ITALICS}if{bcolors.ENDC}{bcolors.WARNING}", 1)
            displayed_lines[i] = displayed_lines[i].replace("for", f"{bcolors.OKGREEN}{bcolors.ITALICS}for{bcolors.ENDC}{bcolors.WARNING}", 1)
            displayed_lines[i] = displayed_lines[i].replace("while", f"{bcolors.OKGREEN}{bcolors.ITALICS}while{bcolors.ENDC}{bcolors.WARNING}", 1)
            displayed_lines[i] = displayed_lines[i].replace("endif", f"{bcolors.OKGREEN}{bcolors.ITALICS}endif{bcolors.ENDC}{bcolors.WARNING}", 1)
            displayed_lines[i] = displayed_lines[i].replace("endfor", f"{bcolors.OKGREEN}{bcolors.ITALICS}endfor{bcolors.ENDC}{bcolors.WARNING}", 1)
            displayed_lines[i] = displayed_lines[i].replace("endwhile", f"{bcolors.OKGREEN}{bcolors.ITALICS}endwhile{bcolors.ENDC}{bcolors.WARNING}", 1)
            displayed_lines[i] = displayed_lines[i].replace("end if", f"{bcolors.OKGREEN}{bcolors.ITALICS}end if{bcolors.ENDC}{bcolors.WARNING}", 1)
            displayed_lines[i] = displayed_lines[i].replace("end for", f"{bcolors.OKGREEN}{bcolors.ITALICS}end for{bcolors.ENDC}{bcolors.WARNING}", 1)
            displayed_lines[i] = displayed_lines[i].replace("end while", f"{bcolors.OKGREEN}{bcolors.ITALICS}end while{bcolors.ENDC}{bcolors.WARNING}", 1)
            if displayed_lines[i].startswith("function"):
                displayed_lines[i] = displayed_lines[i].split(" ")
                displayed_lines[i][0] = displayed_lines[i][0].replace("function", f"{bcolors.OKGREEN}{bcolors.ITALICS}function{bcolors.ENDC}", 1)
                displayed_lines[i][1] = bcolors.WARNING + displayed_lines[i][1] + bcolors.ENDC + bcolors.FAIL
                displayed_lines[i] = recreate_string(displayed_lines[i], " ")
                displayed_lines[i] += bcolors.ENDC
            if displayed_lines[i].startswith("use_function"):
                displayed_lines[i] = displayed_lines[i].split(" ")
                displayed_lines[i][0] = displayed_lines[i][0].replace("use_function", f"{bcolors.OKGREEN}{bcolors.ITALICS}use_function{bcolors.ENDC}",1)
                displayed_lines[i][1] = bcolors.WARNING + displayed_lines[i][1] + bcolors.ENDC + bcolors.FAIL
                displayed_lines[i] = recreate_string(displayed_lines[i], " ")
                displayed_lines[i] += bcolors.ENDC
            # red
            displayed_lines[i] = displayed_lines[i].replace("<", f"{bcolors.FAIL}<")
            displayed_lines[i] = displayed_lines[i].replace(">", f">{bcolors.ENDC}")
            displayed_lines[i] = displayed_lines[i].replace("{", bcolors.FAIL+"{")
            displayed_lines[i] = displayed_lines[i].replace("}", "}"+bcolors.ENDC)
            displayed_lines[i] = displayed_lines[i].replace(":int", f"{bcolors.FAIL}:int{bcolors.WARNING}")
            displayed_lines[i] = displayed_lines[i].replace(":float", f"{bcolors.FAIL}:float{bcolors.WARNING}")
            displayed_lines[i] = displayed_lines[i].replace(":str", f"{bcolors.FAIL}:str{bcolors.WARNING}")
            displayed_lines[i] = displayed_lines[i].replace(":list", f"{bcolors.FAIL}:str{bcolors.WARNING}")
            # italics
            displayed_lines[i] = displayed_lines[i].replace("//", f"{bcolors.ITALICS}//", 1)
            displayed_lines[i] = displayed_lines[i].replace("#", f"{bcolors.ITALICS}#")
            # uncoloured
            displayed_lines[i] = displayed_lines[i].replace("=", f"{bcolors.ENDC}={bcolors.WARNING}")

            # destroys color at the end
            displayed_lines[i] += bcolors.ENDC
        print(displayed_lines[i])

    if loop_times[1] > 10:
        loop_times[1] = 10
    # {loop_times[1]} lines displayed out of {len(lines)}.
    print(bcolors.OKBLUE + texts.ide["DisplayedLines"].format(line1=loop_times[1], line2=len(lines)) + bcolors.ENDC)

    # Collect events until released
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    # Just adding a newline
    print("\n")

    if pressed_key != "NOINTERPRETATION":
        try:
            try:
                temp_line = split(lines[current_line])
            except IndexError:
                temp_line = [""]
            temp_line.insert(current_cursor_position, pressed_key)
            if pressed_key == "{":
                temp_line.insert(current_cursor_position+1, "}")
            elif pressed_key == "<":
                temp_line.insert(current_cursor_position+1, ">")
            elif pressed_key == "[":
                temp_line.insert(current_cursor_position + 1, "]")
            try:
                lines[current_line] = ""
            except IndexError:
                lines = [""]
                current_line = 0
            for char in temp_line:
                try:
                    lines[current_line] += char
                except TypeError:
                    pass
            del temp_line
            current_cursor_position += len(pressed_key)
            replace_line(code_file_filename, current_line, lines[current_line] + "\n")
            if pressed_key == "\n":
                current_line += 1
                current_cursor_position = 0
        except AttributeError:
            pass
        except TypeError:
            pass

        if pressed_key == Key.esc:
            user_input = input(f"{bcolors.OKBLUE}What do you want to do ?\nType 'quit' or 'end' to leave, 'new_file <filename>' to create a new_file, or 'open_file' to open an existing file, 'run' to run if it is a Python or ACPL file, or 'compile' in case of an ACPL file.\n{bcolors.ENDC}")
            if user_input == "quit" or user_input == "end":
                acpl_ide_metadata[current_filename] = {
                    "line": current_line,
                    "cursor_position": current_cursor_position
                }
                with open(current_folder + "/.acpl_ide", "w") as f:
                    json.dump(acpl_ide_metadata, f)
                    f.close()
                break
            elif user_input.startswith("new_file"):
                user_input = user_input.replace("new_file ", "", 1)
                if user_input not in ide_forbidden_files:
                    if os.path.exists(user_input):
                        confirm = input(f"{bcolors.FAIL}This file ({user_input}) already exists. Are you sure you want to replace it ? (Yes/No) {bcolors.ENDC}")
                        while confirm.lower() != "yes" and confirm.lower() != "no":
                            confirm = input(f"{bcolors.FAIL}This file ({user_input}) already exists. Are you sure you want to replace it ? (Yes/No) {bcolors.ENDC}")
                        if confirm.lower() == "yes":
                            new_file = open(user_input, "w", encoding="utf-8")
                            new_file.writelines([""])
                            new_file.close()
                            code_file_filename = user_input
                            del confirm
                    else:
                        new_file = open(user_input, "w", encoding="utf-8")
                        new_file.write("")
                        new_file.close()
                        code_file_filename = user_input
                else:
                    # This file is an ACPL system file, which means you cannot modify it.
                    print(bcolors.FAIL + texts.ide["ACPL_SystemFile"] + bcolors.ENDC)
                user_input = None
                continue
            elif user_input == "open_file":
                launch_py_file("ide")
                sys.exit()
            elif user_input == "run":
                if code_file_filename.endswith(".acpl"):
                    replace_line("startup.acpl-ini", 0, f"filename: {code_file_filename}\n")
                    launch_py_file("main")
                    sleep(2)
                elif code_file_filename.endswith(".py"):
                    os.system(f"python {code_file_filename}")
                    sleep(1)
                elif "." in code_file_filename:
                    extension = code_file_filename.split(".")[len(code_file_filename.split(".")) - 1]
                    # Unable to run that type of file (Extension : '{extension}').
                    print(bcolors.FAIL + texts.ide["UnableRunFile"].format(extension=extension) + bcolors.ENDC)
                    extension = None
                else:
                    print(bcolors.FAIL + texts.ide["UnableRunFile_NoExtension"] + bcolors.ENDC)

                print("\n\n")
            elif user_input == "compile":
                if code_file_filename.endswith(".acpl"):
                    replace_line("startup.acpl-ini", 0, f"filename: {code_file_filename}\n")
                    replace_line("startup.acpl-ini", 8,
                                 f"compiled-file-filename: {code_file_filename.replace('.acpl', '')}\n")
                    launch_py_file("compiler")
                    new_file = open(code_file_filename.replace('.acpl', '') + ".py", "r")
                    for line in new_file.readlines():
                        print(line, end="")
                    new_file.close()
                    sleep(2)
                elif "." in code_file_filename:
                    extension = code_file_filename.split(".")[len(code_file_filename.split(".")) - 1]
                    # Unable to run that type of file (Extension : '{extension}').
                    print(bcolors.FAIL + texts.ide["UnableRunFile"].format(extension=extension) + bcolors.ENDC)
                    extension = None
                else:
                    print(bcolors.FAIL + texts.ide["UnableRunFile_NoExtension"] + bcolors.ENDC)
        elif pressed_key == Key.backspace:
            # Detecting if the cursor is a the beginning of the line or not
            if current_cursor_position == 0:
                # Append line to last line
                if current_line > 0:  # Avoid IndexError
                    # Remove '\n' from previous line and adding the current one at the end of the new
                    lines[current_line-1] = remove_suffix(lines[current_line-1], lines[current_line-1].endswith("\n"))
                    current_cursor_position = len(lines[current_line-1])
                    lines[current_line-1] += lines[current_line]
                    lines[current_line] = ""

                    current_line -= 1
                    if current_cursor_position < 0:
                        current_cursor_position = 0
                    delete_line(code_file_filename, current_line+1)
                    replace_line(code_file_filename, current_line, lines[current_line]+"\n")
            else:
                # Delete char on the left
                # Splits the line in a list of all its characters, then removes the one at the cursor position
                lines[current_line] = split(lines[current_line])
                try:
                    lines[current_line].pop(current_cursor_position-1)
                except IndexError:
                    # Sorry, an unknown error occured.\nWe are unable to delete this character.\nPlease try again.
                    print(bcolors.FAIL + texts.ide["UnableToDeleteCharacter"] + bcolors.ENDC)
                    sleep(2)
                    pass
                lines[current_line] = recreate_string(lines[current_line])
                current_cursor_position -= 1
                if current_cursor_position < 0:
                    current_cursor_position = 0

                # Adds the line back in the file
                replace_line(code_file_filename, current_line, remove_suffix(lines[current_line], lines[current_line].endswith("\n"))+"\n")
            """try:
                temp_line = split(lines[current_line])
            except IndexError:
                temp_line = [""]
            try:
                temp_line.pop(current_cursor_position-1)
            except IndexError:
                lines.pop(current_line)
                replace_line(code_file_filename, current_line, "")
                continue
            try:
                lines[current_line] = ""
            except IndexError:
                lines = [""]
                current_line = 0
            for char in temp_line:
                try:
                    lines[current_line] += char
                except TypeError:
                    pass
            temp_line = None
            current_cursor_position -= 1
            replace_line(code_file_filename, current_line, lines[current_line] + "\n")"""
        elif pressed_key == Key.right:
            current_cursor_position += 1
            if current_cursor_position > len(lines[current_line]):
                current_cursor_position = len(lines[current_line])
        elif pressed_key == Key.left:
            current_cursor_position -= 1
            if current_cursor_position < 0:
                current_cursor_position = 0
        elif pressed_key == Key.up:
            current_line -= 1
            if current_line < 0:
                current_line = 0
            current_cursor_position = len(lines[current_line])
            if current_cursor_position < 0:
                current_cursor_position = 0
        elif pressed_key == Key.down:
            current_line += 1
            if current_line > len(lines) - 1:
                current_line = len(lines) - 1
            current_cursor_position = len(lines[current_line])
            if current_cursor_position < 0:
                current_cursor_position = 0
        elif pressed_key == Key.delete:
            try:
                temp_line = split(lines[current_line])
            except IndexError:
                temp_line = [""]
            try:
                temp_line.pop(current_cursor_position)
            except IndexError:
                replace_line(code_file_filename, current_line, lines[current_line])
                continue
            try:
                lines[current_line] = ""
            except IndexError:
                lines = [""]
                current_line = 0
            for char in temp_line:
                try:
                    lines[current_line] += char
                except TypeError:
                    pass
            del temp_line
            replace_line(code_file_filename, current_line, lines[current_line] + "\n")

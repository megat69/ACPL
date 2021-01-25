"""
This file implements auto-updates for the ACPL.
This file will update the other update file and the startup file.
"""
import os
import shutil
from recurrent_classes import *
from time import sleep

# Updating the main updater
print(bcolors.OKBLUE + texts.updates["RewritingElement"].format(element="updater_main.py") + bcolors.ENDC)
old_file = open("updater_main.py", "r", encoding="utf-8")
old_lines = old_file.readlines()
try:
    old_file = open("updater_main.py", "w", encoding="utf-8")
    new_file = open("update/updater_main.py", "r", encoding="utf-8")
    old_file.writelines(new_file.readlines())
    old_file.close()
    new_file.close()
    print(bcolors.OKBLUE + texts.updates["ElementRewritten"].format(element="updater_main.py") + bcolors.ENDC)
except:
    old_file.writelines(old_lines)
    old_file.close()
    print(bcolors.FAIL + texts.updates["CouldNotRewritElement"].format(element="updater_main") + bcolors.ENDC)
del old_lines

startup_file = open("startup.acpl-ini", "r")
new_startup_file = open("update/startup.acpl-ini", "r")

# Getting the old settings
old_settings = {}
for line in startup_file:
    line = remove_suffix(line, line.endswith("\n"))
    line = line.split(": ")
    old_settings[line[0]] = line[1]

# Getting the new settings
new_settings = {}
for line in new_startup_file:
    line = remove_suffix(line, line.endswith("\n"))
    line = line.split(": ")
    new_settings[line[0]] = line[1]

# Setting up final settings
final_settings = {}
for element in new_settings:
    if element != "version" and element in old_settings.keys():
        final_settings[element] = old_settings[element]
    else:
        final_settings[element] = new_settings[element]

# Putting final settings in startup.acpl-ini
# Closing the old files first
startup_file.close()
new_startup_file.close()
# Opening it in write mode
startup_file = open("startup.acpl-ini", "w", encoding="utf-8")
# Creating a list of its lines
new_startup_lines = []
for element in final_settings:
    new_startup_lines.append(f"{element}: {final_settings[element]}\n")
# Writing them inside and closing it
startup_file.writelines(new_startup_lines)
startup_file.close()

# Removing the temp files and folders
os.remove("update.zip")
shutil.rmtree(os.getcwd()+"/update", ignore_errors=True)

# Updating dependencies
print(f"{bcolors.OKBLUE}Updating dependencies...{bcolors.ENDC}")
os.system("pip install -r --upgrade requirements.txt")
print(f"{bcolors.OKGREEN}Dependencies updated successfully !{bcolors.ENDC}")

# Changelog
print(f"\n\n{bcolors.BOLD}{bcolors.OKGREEN}{texts.updates['UpdateApplied']}{bcolors.ENDC}")
sleep(2)
user_input = input(f"{texts.updates['SeeChangelog']} (yes/no)\n")
if user_input[0].lower() == "y":
    changelog_file = open("changelog.md", "r")
    changelog = changelog_file.readlines()
    changelog_file.close()
    changelog = md_format(changelog)
    print(changelog)

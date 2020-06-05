import urllib.request  # the lib that handles the url stuff
import requests
from zipfile import ZipFile
import os
import shutil
import glob
from time import sleep
from random import randrange
import psutil
import json
from recurrent_classes import *

def moveAllFilesinDir(srcDir, dstDir):
    # Check if both the are directories
    if os.path.isdir(srcDir) and os.path.isdir(dstDir) :
        # Iterate over all the files in source directory
        for filePath in glob.glob(srcDir + '\*'):
            # Move each file to destination Directory
            shutil.move(filePath, dstDir)
    else:
        print(f"{bcolors.FAIL}srcDir & dstDir should be Directories{bcolors.ENDC}")

def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()

def checkIfProcessRunning(processName):
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def update_program(url):
    r = requests.get(url)
    with open("new_version.zip", "wb") as code:
        code.write(r.content)
    if checkIfProcessRunning("console.py"): #process_exists("console.py"):
        os.system("taskkill /im console.py")
        console_was_running = True
    else:
        console_was_running = False
    with ZipFile("new_version.zip", 'r') as zip:
        # printing all the contents of the zip file
        #zip.printdir()
        files = zip.filelist
        for i in range(len(files)):
            files[i] = str(files[i].filename).replace("ACPL-master/", "")
            #print(files[i])
        print(f"{bcolors.WARNING}{texts.updates['old-files-deletion']}{bcolors.ENDC}\n")
        sleep(1)
        for i in range(1, len(files)):
            try:
                os.remove(files[i])
                print(f"{texts.updates['old-files-deletion-complete'].format(files[i])}")
            except FileNotFoundError:
                pass
            sleep(randrange(1, 8)/10)
        # extracting all the files
        sleep(1)
        print(f'{bcolors.WARNING}{texts.updates["extracting-all-files"]}{bcolors.ENDC}\n')
        sleep(2)
        ZipFile("new_version.zip", 'r').extractall()
        print(f"{bcolors.OKGREEN}{texts.updates['files-successfully-extracted']}{bcolors.ENDC}\n")
        sleep(1)
        moveAllFilesinDir(os.getcwd()+"/ACPL-master/", os.getcwd())
        zip.close()
        print(f"{bcolors.WARNING}{texts.updates['removing-temp-files']}{bcolors.ENDC}")
        sleep(1)
        os.remove("new_version.zip")
        os.rmdir(os.getcwd()+"/ACPL-master/")
        print(f'{bcolors.OKGREEN}{texts.updates["temp-files-removed"]}{bcolors.ENDC}\n\n')
        sleep(2)
        print(f"{bcolors.OKGREEN}{texts.updates['update-applied']}{bcolors.ENDC}\n")
        if console_was_running:
            print(f"{bcolors.HEADER}{texts.updates['console-restart']}{bcolors.ENDC}")
            with open("startup.acpl-ini", "r", encoding="utf-8") as ini_file:
                replace_line(ini_file, 5, "console-reloaded: True\n")
                os.system("python console.py")
                ini_file.close()

def ask_update_program(url):
    version = ""
    for chr in last_version:
        version += chr+"."
    print(f"{bcolors.WARNING}{texts.updates['update-disponible-message'].format(version)}{bcolors.ENDC}")
    answer = ""
    while answer.lower() != "yes" and answer.lower() != "no":
        answer = input(f"{bcolors.WARNING}{texts.updates['ask-install']} (Yes/No){bcolors.ENDC}\n")
    if answer.lower() == "yes":
        update_program(url)

data = urllib.request.urlopen("https://raw.githubusercontent.com/megat69/ACPL/master/startup.acpl-ini").readlines() # it's a file like object and works just like a file

for line in data:
    if str(line).startswith("b'"):
        line = str(line).replace("b'", "")
        line = str(line).replace("'", "")
    line = str(line).replace("\\r\\n", "")
    
    if str(line).startswith("lang: "):
        with open("startup.acpl-ini", "r", encoding="utf-8") as startup_file:
            line = startup_file.readlines()
            line = line[1]
            line = str(line).replace("lang: ", "")
            line = line.replace("\n", "")
            if line == "fr":
                language = "fr"
            elif line == "nl":
                language = "nl"
            else:
                language = "en"
            try:
                with open(language + ".json", "r", encoding="utf-8") as json_file:
                    texts = json.load(json_file)
                    json_file.close()
                    texts = Text(texts)
            except NameError:
                raise CriticError(texts.critic_errors["NameError_LanguageFile"])

    if str(line).startswith("version: "):
        line = line.replace("version: ", "")
        with open("startup.acpl-ini", "r", encoding="utf-8") as startup_file:
            for lines in startup_file.readlines():
                if lines.startswith("version: "):
                    lines = lines.replace("version: ", "")
                    lines = lines.replace("\n", "")
                    current_version = lines
                    break
            startup_file.close()

        #print(line, "|", current_version)

        current_version = current_version.split(".") # Version currently installed
        last_version = line.split(".") # Version disponible online

        if len(last_version) < 3:
            last_version.append("0")

        if len(current_version) < 3:
            current_version.append("0")

        if int(current_version[0]) < int(last_version[0]):
            ask_update_program('https://github.com/megat69/ACPL/archive/master.zip')
        elif int(current_version[1]) < int(last_version[1]):
            ask_update_program('https://github.com/megat69/ACPL/archive/master.zip')
        elif int(current_version[2]) < int(last_version[2]):
            ask_update_program('https://github.com/megat69/ACPL/archive/master.zip')
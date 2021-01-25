"""
This file implements auto-updates for the ACPL.
This one will update all the necessary file, except this one and the startup file.
"""
import requests
from recurrent_classes import *
import sys
import urllib.request
from packaging import version
import zipfile
from time import sleep
from random import randint

stop = False

# Test if internet is available
try:
    urllib.request.urlopen('http://google.com')
except:  # If impossible
    stop = True

if stop is False:
    # Import of startup file to get version
    startup_file = open("startup.acpl-ini", "r")

    # Defining of version as None
    local_version = None

    # Browse through startup file to get version
    for line in startup_file.readlines():
        if line.startswith("version"):
            line = line.replace("version: ", "", 1)
            line = remove_suffix(line, line.endswith("\n"))
            local_version = line

    # If version hasn't been found
    if local_version is None:
        print(bcolors.FAIL + texts.updates["WiFi_Off"] + bcolors.ENDC)
        stop = True

if stop is False:
# Getting last github version.
    response = requests.get("https://api.github.com/repos/megat69/ACPL/releases/latest")
    zip_link = response.json()['assets'][0]["browser_download_url"]
    github_version = response.json()["tag_name"]

    # Decide if an update is available on GitHub
    update = version.parse(github_version) > version.parse(local_version)

    if update is False:
        stop = True

if stop is False:
    # Ask the user if he wants to update
    # TEXT : A new version has been found !
    # Your version : {local_version}
    # GitHub version {github_version}
    print(bcolors.OKGREEN + texts.updates["NewVersionFound"].format(local_version=local_version,
                                                                    github_version=github_version) + bcolors.ENDC)

    update = input(f"{bcolors.OKBLUE}Do you want to update ? (yes/no){bcolors.ENDC} ")
    if update[0].lower() != "y":
        # Update cancelled.\n{bcolors.WARNING}If you want to update later, type 'update' in the console.
        print(bcolors.FAIL + texts.updates["UpdateCancelled"].format(WARNING=bcolors.WARNING) + bcolors.ENDC)
        stop = True

if stop is False:
    # Download the update as zip file
    r = requests.get(zip_link)
    existing = r.status_code == 200
    if not existing:
        print(bcolors.FAIL + texts.updates["ImpossibleDownloadError"] + bcolors.ENDC)
        stop = True
if stop is False:
    print(bcolors.OKBLUE + texts.updates["DownloadingUpdate"] + bcolors.ENDC)
    with open("update.zip", "wb") as code:
        code.write(r.content)
        code.close()
    print(bcolors.OKGREEN + texts.updates["UpdateSuccessfullyDownloaded"] + bcolors.ENDC + "\n\n")

    # Creating a folder for the zip content
    if not os.path.exists("update"):
        os.mkdir("update")
    # Extracting the zip
    print(bcolors.OKBLUE + texts.updates["ExtractingUpdate"] + bcolors.ENDC)
    with zipfile.ZipFile("update.zip","r") as zip_ref:
        zip_ref.extractall("update")
    print(bcolors.OKGREEN + texts.updates["UpdateSuccessfullyExtracted"] + bcolors.ENDC)

    # Getting the list of the new files
    updated_files = os.listdir("update")

    # Rewriting the old files
    for element in updated_files:
        if element != "updater_main.py" and element != "startup.acpl-ini":
            print(bcolors.OKBLUE + texts.updates["RewritingElement"].format(element=element) + bcolors.ENDC)
            old_file = open(element, "w", encoding="utf-8")
            new_file = open("update/"+element, "r", encoding="utf-8")
            try:
                old_file.writelines(new_file.readlines())
            except:
                pass
            old_file.close()
            new_file.close()
            # Random interval :P
            sleep(float(f"{randint(0, 1)}.{randint(0, 100)}"))
            print(bcolors.OKBLUE + texts.updates["ElementRewritten"].format(element=element) + bcolors.ENDC)

    launch_py_file("updater_others")

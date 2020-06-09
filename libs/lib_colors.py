version = "1.0"
lib_type = "variables"

from recurrent_classes import bcolors
import json
variables_container = VARIABLES_CONTAINER

variables_container["bcolors.HEADER"] = bcolors.HEADER
variables_container["bcolors.OKBLUE"] = bcolors.OKBLUE
variables_container["bcolors.OKGREEN"] = bcolors.OKGREEN
variables_container["bcolors.WARNING"] = bcolors.WARNING
variables_container["bcolors.FAIL"] = bcolors.FAIL
variables_container["bcolors.ENDC"] = bcolors.ENDC
variables_container["bcolors.BOLD"] = bcolors.BOLD
variables_container["bcolors.UNDERLINE"] = bcolors.UNDERLINE
variables_container["bcolors.ITALICS"] = bcolors.ITALICS

with open("var_transfer.json", "w", encoding="utf-8") as transfer_file:
    transfer_file.write(json.dumps(variables_container))
    transfer_file.close()
version = "1.0"
lib_type = "functions"

import os

if var_line.startswith("os"):
    var = var_line.replace("os ", "")
    os.system(var)
version = 1.0
lib_type = "functions"
import os
from recurrent_classes import replace_line

if var_line.startswith("run_file"):
    var = var_line.replace("run_file ", "")
    replace_line("startup.acpl-ini", 0, f"filename: {var}\n")
    os.system("python main.py")

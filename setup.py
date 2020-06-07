import os

libs_used = ["requests", "psutils", "shutil", "glob", "zipfile", "urllib.requests"]
for lib in libs_used:
    os.system(f"pip install {lib}")
import os
os.system("pip install -r requirements.txt")

startup_file = open("startup.acpl-ini", "r", encoding="utf-8")
startup_options = startup_file.readlines()
startup_file.close()

print("Hello !\nLet's begin with a quick setup of your settings.")
language = input("What language do you speak, from this list ? Type in the country code between parentheses.\n"
                 "- Azerbaijani (az)\n"
                 "- German (de)\n"
                 "- English (en)\n"
                 "- French (fr)\n"
                 "- Italian (it)\n"
                 "- Dutch (nl)\n"
                 "- Turkish (tr)\n"
                 "Type here : ")

print(f"Ok, I configured your language to '{language}'.\nBut for now, the setup has to be in English (sorry).")

use_colors = input("\033[93mDo you see weird characters at the beginning and the end of that sentence ? (yes/no) \033[0m")
if use_colors.lower() == "yes":
    use_colors = "False"
else:
    use_colors = "True"

open_compiled_file = input("The ACPL has the ability to compile ACPL files into Python files.\nAt the end of a compilation, do you want the ACPL interpreter to automatically open the file in your favourite text editor ? (yes/no) ")
open_compiled_file = f"{open_compiled_file.lower() == 'yes'}"

leave_comments_at_compiling = input("During compilation, do you want the comments you wrote in the ACPL file to be transcripted in the Python file ? (yes/no) ")
leave_comments_at_compiling = f"{leave_comments_at_compiling.lower() == 'yes'}"

print("Okay, you completed the setup :)\n\nKeep in mind that you can modify any of them using the 'modify-ini' console command.")

for i in range(len(startup_options)):
    if startup_options[i].startswith("lang"):
        startup_options[i] = f"lang: {language}\n"
    elif startup_options[i].startswith("use-colors"):
        startup_options[i] = f"use-colors: {use_colors}\n"
    elif startup_options[i].startswith("open-compiled-file"):
        startup_options[i] = f"open-compiled-file: {open_compiled_file}\n"
    elif startup_options[i].startswith("leave-comments-at-compiling"):
        startup_options[i] = f"leave-comments-at-compiling: {leave_comments_at_compiling}\n"

startup_file = open("startup.acpl-ini", "w", encoding="utf-8")
startup_file.writelines(startup_options)
startup_file.close()

print("I open you the console :)")
os.system("python console.py")

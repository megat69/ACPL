from recurrent_classes import *
import tkinter as tk
import re

def libs_to_import():
    return ("tkinter as tk",), tuple()

def requirements(file):
    if file == "var_methods":
        return "line_numbers", "var_type", "do_not_the_operator"
    elif file == "compiler_var_methods":
        return "line_numbers", "var_type", "is_lib"
    else:
        return ("line_numbers",)

def main(line, variables_container, other_args):
    """
    The GUI lib lets you create simple windows and GUI with ACPL.

    Syntax :
    ## Define a window :
    lib GUI create window <variable> [optional parameters]

    ## Display a window :
    lib GUI display <variable>
    """
    line_numbers = other_args[0]

    if str(line).startswith("GUI"):
        line = line.replace("GUI ", "", 1)
        line = remove_suffix(line, line.endswith("\n"))

        if line.startswith("create"):
            # To create a widget
            line = line.replace("create ", "", 1)

            if line.startswith("window"):
                line = line.replace("window ", "", 1)
                # Syntax : <variable> [param1=val1] [param2=val2]...
                line = line.split(" ")

                # Setting the variable to a Tkinter instance
                variables_container[line[0]] = tk.Tk()

                # If there are parameters
                if len(line) > 1:
                    for i in range(1, len(line)):
                        line[i] = line[i].split("=")

                        if line[i][0] == "size":
                            variables_container[line[0]].geometry(line[i][1])
                        elif line[i][0] == "title":
                            # So we get the whole title
                            line[i] = line[i][1]  # We know it's the title, we don't need it anymore.

                            # We recreate the string and basically get the title
                            temp = recreate_string(line, char_in_between=" ").replace(f"{line[0]} ", "", 1)
                            temp = temp.split("=")[0]
                            temp = temp.split("]")
                            temp = temp[len(temp)-1]
                            temp = remove_prefix(temp, temp.startswith(" "))
                            if temp.endswith("icon") or temp.endswith("background") or temp.endswith("color"):
                                temp = temp.split(" ")
                                temp.pop()
                                temp = recreate_string(temp, char_in_between=" ")
                            line[i] = ["title", temp]
                            del temp

                            variables_container[line[0]].title(line[i][1])
                        elif line[i][0] == "icon":
                            if not line[i][1].endswith(".ico"):
                                error(line_numbers, "ArgumentError", f"Extension for the icon should be '.ico' ; given '{line[i][0]}'")
                            try:
                                variables_container[line[0]].iconbitmap(line[i][1])
                            except tk._tkinter.TclError:
                                error(line_numbers, "FileNotFoundError", f"The file '{line[i][1]}' doesn't exist.\n"
                                                                         f"Unable to create the icon.")
                        elif line[i][0] == "background":
                            variables_container[line[0]]["bg"] = line[i][1]

            elif line.startswith("text"):
                # Syntax : text <variable> <window> <x|pack>
                # -x : <y> <text> [--columnspan:<value>]
                # -pack : <text>
                line = line.replace("text ", "", 1)

                optional_params = {
                    "align": "nsew",
                    "background": "#f0f0f0",
                    "color": "black"
                }

                if "--align" in line:
                    try:
                        optional_params["align"] = re.findall("--align:[a-zA-Z\-]*", line)[0].replace("--align:", "", 1)
                        line = line.replace(f" --align:{optional_params['align']}", "")
                    except IndexError:
                        pass
                    if optional_params["align"] == "top":
                        optional_params["align"] = "n"
                    elif optional_params["align"] == "top-right":
                        optional_params["align"] = "ne"
                    elif optional_params["align"] == "right":
                        optional_params["align"] = "e"
                    elif optional_params["align"] == "bottom-right":
                        optional_params["align"] = "se"
                    elif optional_params["align"] == "bottom":
                        optional_params["align"] = "s"
                    elif optional_params["align"] == "bottom-left":
                        optional_params["align"] = "sw"
                    elif optional_params["align"] == "left":
                        optional_params["align"] = "w"
                    elif optional_params["align"] == "top-left":
                        optional_params["align"] = "nw"
                    elif optional_params["align"] == "center":
                        optional_params["align"] = "nesw"
                    else:
                        error(line_numbers, "ArgumentError", f"Parameter '--align' cannot have the value '{optional_params['align']}'.")
                if "--background" in line:
                    try:
                        temp = line.split("--background:")[1]
                    except IndexError:
                        temp = "grey"
                    try:
                        temp = temp.split(" ")[0]
                    except IndexError:
                        pass
                    optional_params["background"] = temp
                    line = line.replace(f" --background:{optional_params['background']}", "")
                    del temp
                if "--color" in line:
                    try:
                        temp = line.split("--color:")[1]
                    except IndexError:
                        temp = "black"
                    try:
                        temp = temp.split(" ")[0]
                    except IndexError:
                        pass
                    optional_params["color"] = temp
                    line = line.replace(f" --color:{optional_params['color']}", "")
                    del temp

                # Support for newlines
                line = line.replace("$newline$", "\n")

                line = line.split(" ")
                print(line)
                if line[2] == "pack":
                    try:
                        line[3] = recreate_string(line[3:len(line)], " ")
                        variables_container[line[0]] = tk.Label(variables_container[line[1]], text=line[3],
                                                                bg=optional_params["background"],
                                                                fg=optional_params["color"])
                    except IndexError:
                        error(line_numbers, "ArgumentError", texts.errors["FunctionArgumentError"].format(args_required=3, args_nbr=len(line)))
                    try:
                        variables_container[line[0]].pack()
                    except tk._tkinter.TclError:
                        error(line_numbers, "OptionError", "Cannot use option pack when grid is being used.")
                else:
                    try:
                        line[4] = recreate_string(line[4:len(line)], " ")

                        # Column span option
                        if "--column_span" in line[4]:
                            try:
                                columnspan_value = int(line[4].split("--column_span:")[1])
                                line[4] = line[4].replace(f"--column_span:{str(columnspan_value)}", "")
                                line[4] = remove_suffix(line[4], line[4].endswith(" "))
                            except ValueError:
                                error(line_numbers, "ArgumentNotInt", "column_span : " + texts.errors["ArgumentNotInt"])
                        else:
                            columnspan_value = 1

                        variables_container[line[0]] = tk.Label(variables_container[line[1]], text=line[4],
                                                                bg=optional_params["background"],
                                                                fg=optional_params["color"])
                    except IndexError:
                        error(line_numbers, "ArgumentError", texts.errors["FunctionArgumentError"].format(args_required=3, args_nbr=len(line)))

                    try:
                        variables_container[line[0]].grid(row=int(line[2]), column=int(line[3]),
                                                          columnspan=columnspan_value,
                                                          sticky=optional_params["align"])
                    except ValueError:
                        error(line_numbers, "ArgumentNotInt", texts.errors["ArgumentNotInt"])
                    except tk._tkinter.TclError:
                        error(line_numbers, "OptionError", "Cannot use option grid when pack is being used.")

        elif line.startswith("display"):  # Syntax : display <variable>
            line = line.replace("display ", "", 1)
            try:
                variables_container[line].mainloop()
            except AttributeError:
                error(line_numbers, "AttributeError", f"Variable '{line}' is not a GUI instance.")

    return line, variables_container

def pytranslation(line, other_args):
    """
    ACPL Library for GUI creation. Function for ACPL compiler use.
    Syntax seen in 'main' function.
    """
    line_numbers = other_args[0]

    if str(line).startswith("GUI"):
        line = line.replace("GUI ", "", 1)
        line = remove_suffix(line, line.endswith("\n"))

        if line.startswith("create"):
            # Creating a widget
            line = line.replace("create ", "", 1)

            if line.startswith("window"):
                # Creating the default window
                line = line.replace("window ", "", 1)
                line = line.split(" ")

                # Setting the variable as tkinter instance
                temp_line = f"{line[0]} = tk.Tk()"

                # If there are parameters
                if len(line) > 1:
                    for i in range(1, len(line)):
                        temp_line += "\n"
                        line[i] = line[i].split("=")

                        if line[i][0] == "size":
                            temp_line += f"{line[0]}.geometry(\"{line[i][1]}\")"
                        elif line[i][0] == "title":
                            # So we get the whole title
                            line[i] = line[i][1]  # We know it's the title, we don't need it anymore.

                            # We recreate the string and basically get the title
                            temp = recreate_string(line, char_in_between=" ").replace(f"{line[0]} ", "", 1)
                            temp = temp.split("=")[0]
                            temp = temp.split("]")
                            temp = temp[len(temp) - 1]
                            temp = remove_prefix(temp, temp.startswith(" "))
                            if temp.endswith("icon") or temp.endswith("background") or temp.endswith("color"):
                                temp = temp.split(" ")
                                temp.pop()
                                temp = recreate_string(temp, char_in_between=" ")
                            line[i] = ["title", temp]
                            del temp

                            temp_line += f"{line[0]}.title(\"{line[i][1]}\")"
                        elif line[i][0] == "icon":
                            if not line[i][1].endswith(".ico"):
                                error(line_numbers, "ArgumentError", f"Extension for the icon should be '.ico' ; given '{line[i][0]}'")
                            temp_line += f"{line[0]}.iconbitmap(\"{line[i][1]}\")"
                        elif line[i][0] == "background":
                            temp_line += f"{line[0]}[\"bg\"] = \"{line[i][1]}\""

                line = temp_line
                del temp_line

            elif line.startswith("text"):
                # Text widget
                line = line.replace("text ", "", 1)

                optional_params = {
                    "align": "nsew",
                    "background": "#f0f0f0",
                    "color": "black"
                }

                if "--align" in line:
                    try:
                        optional_params["align"] = re.findall("--align:[a-zA-Z\-]*", line)[0].replace("--align:", "", 1)
                        line = line.replace(f" --align:{optional_params['align']}", "")
                    except IndexError:
                        pass
                    if optional_params["align"] == "top":
                        optional_params["align"] = "n"
                    elif optional_params["align"] == "top-right":
                        optional_params["align"] = "ne"
                    elif optional_params["align"] == "right":
                        optional_params["align"] = "e"
                    elif optional_params["align"] == "bottom-right":
                        optional_params["align"] = "se"
                    elif optional_params["align"] == "bottom":
                        optional_params["align"] = "s"
                    elif optional_params["align"] == "bottom-left":
                        optional_params["align"] = "sw"
                    elif optional_params["align"] == "left":
                        optional_params["align"] = "w"
                    elif optional_params["align"] == "top-left":
                        optional_params["align"] = "nw"
                    elif optional_params["align"] == "center":
                        optional_params["align"] = "nesw"
                    else:
                        error(line_numbers, "ArgumentError",
                              f"Parameter '--align' cannot have the value '{optional_params['align']}'.")
                if "--background" in line:
                    try:
                        temp = line.split("--background:")[1]
                    except IndexError:
                        temp = "grey"
                    try:
                        temp = temp.split(" ")[0]
                    except IndexError:
                        pass
                    optional_params["background"] = temp
                    line = line.replace(f" --background:{optional_params['background']}", "")
                    del temp
                if "--color" in line:
                    try:
                        temp = line.split("--color:")[1]
                    except IndexError:
                        temp = "black"
                    try:
                        temp = temp.split(" ")[0]
                    except IndexError:
                        pass
                    optional_params["color"] = temp
                    line = line.replace(f" --color:{optional_params['color']}", "")
                    del temp

                # Support for newlines
                line = line.replace("$newline$", "\\n")

                line = line.split(" ")
                temp_line = ""
                if line[2] == "pack":
                    try:
                        line[3] = recreate_string(line[3:len(line)], " ")
                        line[3] = line[3].replace('\"', '\\\"')
                        temp_line = f"{line[0]} = tk.Label({line[1]}, text=\"{line[3]}\", " \
                                                                f"bg=\"{optional_params['background']}\", " \
                                                                f"fg=\"{optional_params['color']}\")"
                    except IndexError:
                        error(line_numbers, "ArgumentError",
                              texts.errors["FunctionArgumentError"].format(args_required=3, args_nbr=len(line)))
                    try:
                        temp_line += f"\n{line[0]}.pack()"
                    except tk._tkinter.TclError:
                        error(line_numbers, "OptionError", "Cannot use option pack when grid is being used.")
                else:
                    try:
                        line[4] = recreate_string(line[4:len(line)], " ")

                        # Column span option
                        if "--column_span" in line[4]:
                            try:
                                columnspan_value = int(line[4].split("--column_span:")[1])
                                line[4] = line[4].replace(f"--column_span:{str(columnspan_value)}", "")
                                line[4] = remove_suffix(line[4], line[4].endswith(" "))
                            except ValueError:
                                error(line_numbers, "ArgumentNotInt", "column_span : " + texts.errors["ArgumentNotInt"])
                        else:
                            columnspan_value = 1

                        line[4] = line[4].replace('\"', '\\\"')
                        temp_line = f"{line[0]} = tk.Label({line[1]}, text=\"{line[4]}\", " \
                                                            f"bg=\"{optional_params['background']}\", " \
                                                            f"fg=\"{optional_params['color']}\")"
                    except IndexError:
                        error(line_numbers, "ArgumentError",
                              texts.errors["FunctionArgumentError"].format(args_required=3, args_nbr=len(line)))

                    try:
                        temp_line += f"\n{line[0]}.grid(row={int(line[2])}, column={int(line[3])}, " \
                                                          f"columnspan={columnspan_value}, " \
                                                          f"sticky=\"{optional_params['align']}\")"
                    except ValueError:
                        error(line_numbers, "ArgumentNotInt", texts.errors["ArgumentNotInt"])

                line = temp_line
                del temp_line

        elif line.startswith("display"):
            line = line.replace("display ", "", 1)
            line = f"{line}.mainloop()"

    return line, ("do_regroup", False, "do_not_the_operator", True)

def var_methods(line, variables_container, other_args):
    """
    The GUI lib lets you create simple windows and GUI with ACPL, as var method.

    Syntax :
    ## Define a window :
    var <name> = lib GUI create window [optional parameters]
    """
    line_numbers = other_args[0]
    method = line[2]

    if method.startswith("GUI"):
        method = method.replace("GUI ", "", 1)
        method = remove_suffix(method, method.endswith("\n"))
        method = remove_suffix(method, method.endswith(" "))

        if method.startswith("create"):
            # To create a widget
            method = method.replace("create ", "", 1)

            if method.startswith("window"):
                method = method.replace("window ", "", 1)
                # Syntax : [param1=val1] [param2=val2]...

                # Setting the variable to a Tkinter instance
                variables_container[line[0]] = tk.Tk()

                # If there are parameters
                if len(method) != 0:
                    method = method.split(" ")
                    for i in range(len(method)):
                        method[i] = method[i].split("=")

                        if method[i][0] == "size":
                            variables_container[line[0]].geometry(method[i][1])
                        elif method[i][0] == "title":
                            # So we get the whole title
                            method[i] = method[i][1]  # We know it's the title, we don't need it anymore.

                            # We recreate the string and basically get the title
                            temp = recreate_string(method, " ").replace(f"{method[0]} ", "", 1)
                            temp = temp.split("=")[0]
                            temp = temp.split("]")
                            temp = temp[len(temp) - 1]
                            temp = temp.split(" ")
                            temp.pop()
                            temp = recreate_string(temp, " ")
                            method[i] = ["title", temp]
                            del temp

                            variables_container[line[0]].title(method[i][1])
                        elif method[i][0] == "icon":
                            if not method[i][1].endswith(".ico"):
                                error(line_numbers, "ArgumentError",
                                      f"Extension for the icon should be '.ico' ; given '{line[i][0]}'")
                            try:
                                variables_container[line[0]].iconbitmap(method[i][1])
                            except tk._tkinter.TclError:
                                error(line_numbers, "FileNotFoundError", f"The file '{method[i][1]}' doesn't exist.\n"
                                                                           f"Unable to create the icon.")
                        elif method[i][0] == "background":
                            variables_container[line[0]]["bg"] = method[i][1]

            elif method.startswith("text"):
                # Syntax : text <window> <x|pack>
                # -x : <y> <text> [--columnspan:<value>]
                # -pack : <text>
                method = method.replace("text ", "", 1)

                optional_params = {
                    "align": "nsew",
                    "background": "#f0f0f0",
                    "color": "black"
                }

                if "--align" in method:
                    try:
                        optional_params["align"] = re.findall("--align:[a-zA-Z\-]*", method)[0].replace("--align:", "", 1)
                        method = method.replace(f" --align:{optional_params['align']}", "")
                    except IndexError:
                        pass
                    if optional_params["align"] == "top":
                        optional_params["align"] = "n"
                    elif optional_params["align"] == "top-right":
                        optional_params["align"] = "ne"
                    elif optional_params["align"] == "right":
                        optional_params["align"] = "e"
                    elif optional_params["align"] == "bottom-right":
                        optional_params["align"] = "se"
                    elif optional_params["align"] == "bottom":
                        optional_params["align"] = "s"
                    elif optional_params["align"] == "bottom-left":
                        optional_params["align"] = "sw"
                    elif optional_params["align"] == "left":
                        optional_params["align"] = "w"
                    elif optional_params["align"] == "top-left":
                        optional_params["align"] = "nw"
                    elif optional_params["align"] == "center":
                        optional_params["align"] = "nesw"
                    else:
                        error(line_numbers, "ArgumentError", f"Parameter '--align' cannot have the value '{optional_params['align']}'.")
                if "--background" in method:
                    try:
                        temp = method.split("--background:")[1]
                    except IndexError:
                        temp = "grey"
                    try:
                        temp = temp.split(" ")[0]
                    except IndexError:
                        pass
                    optional_params["background"] = temp
                    method = method.replace(f" --background:{optional_params['background']}", "")
                    del temp
                if "--color" in method:
                    try:
                        temp = method.split("--color:")[1]
                    except IndexError:
                        temp = "black"
                    try:
                        temp = temp.split(" ")[0]
                    except IndexError:
                        pass
                    optional_params["color"] = temp
                    method = method.replace(f" --color:{optional_params['color']}", "")
                    del temp

                # Support for newlines
                method = method.replace("$newline$", "\n")

                # Method 1: Pack ; Method 2 : Grid
                method = method.split(" ")
                if method[1] == "pack":
                    try:
                        method[2] = recreate_string(method[2:len(method)], " ")
                        variables_container[line[0]] = tk.Label(variables_container[method[0]],
                                                            text=method[2],
                                                            bg=optional_params["background"],
                                                            fg=optional_params["color"])
                    except IndexError:
                        error(line_numbers, "ArgumentError", texts.errors["FunctionArgumentError"].format(args_required=2, args_nbr=len(method)))
                    try:
                        variables_container[line[0]].pack()
                    except tk._tkinter.TclError:
                        error(line_numbers, "OptionError", "Cannot use option pack when grid is being used.")
                else:
                    try:
                        method[3] = recreate_string(method[3:len(method)], " ")

                        # Column span option
                        if "--column_span" in method[3]:
                            try:
                                columnspan_value = int(method[3].split("--column_span:")[1])
                                method[3] = method[3].replace(f"--column_span:{str(columnspan_value)}", "")
                                method[3] = remove_suffix(method[3], method[3].endswith(" "))
                            except ValueError:
                                error(line_numbers, "ArgumentNotInt", "column_span : " + texts.errors["ArgumentNotInt"])
                        else:
                            columnspan_value = 1

                        variables_container[line[0]] = tk.Label(variables_container[method[0]], text=method[3],
                                                                bg=optional_params["background"],
                                                                fg=optional_params["color"])
                    except IndexError:
                        error(line_numbers, "ArgumentError", texts.errors["FunctionArgumentError"].format(args_required=3, args_nbr=len(line)))

                    try:
                        variables_container[line[0]].grid(row=int(method[1]), column=int(method[2]),
                                                          columnspan=columnspan_value,
                                                          sticky=optional_params["align"])
                    except ValueError:
                        error(line_numbers, "ArgumentNotInt", texts.errors["ArgumentNotInt"])
                    except tk._tkinter.TclError:
                        error(line_numbers, "OptionError", "Cannot use option grid when pack is being used.")

    return recreate_string(line, " "), variables_container, ("do_not_the_operator", True)

def compiler_var_methods(line, other_args):
    """
    ACPL library for GUI creation. Translation for compiler var methods.
    Syntax in main() function.
    """
    line_numbers = other_args[0]
    var_type = other_args[1]
    is_lib = other_args[2]
    method = line[2]

    if method.startswith("GUI"):
        method = method.replace("GUI ", "", 1)
        method = remove_suffix(method, method.endswith(" "))
        method = remove_suffix(method, method.endswith("\n"))

        if method.startswith("create"):
            # To create a widget
            method = method.replace("create ", "", 1)

            if method.startswith("window"):
                method = method.replace("window ", "", 1)

                # Setting the variable to a Tkinter instance
                temp_method = "tk.Tk()"

                # If there are parameters
                if len(method) != 0:
                    method = method.split(" ")
                    for i in range(len(method)):
                        method[i] = method[i].split("=")
                        temp_method += "\n"

                        if method[i][0] == "size":
                            temp_method += f"{line[0]}.geometry(\"{method[i][1]}\")"
                        elif method[i][0] == "title":
                            # So we get the whole title
                            method[i] = method[i][1]  # We know it's the title, we don't need it anymore.

                            # We recreate the string and basically get the title
                            temp = recreate_string(method, " ").replace(f"{method[0]} ", "", 1)
                            temp = temp.split("=")[0]
                            temp = temp.split("]")
                            temp = temp[len(temp) - 1]
                            temp = temp.split(" ")
                            temp.pop()
                            temp = recreate_string(temp, " ")
                            temp = remove_suffix(temp, temp.endswith(" "))
                            method[i] = ["title", temp]
                            del temp

                            temp_method += f"{line[0]}.title(\"{method[i][1]}\")"
                        elif method[i][0] == "icon":
                            if not method[i][1].endswith(".ico"):
                                error(line_numbers, "ArgumentError",
                                      f"Extension for the icon should be '.ico' ; given '{method[i][1]}'")
                            temp_method += f"{line[0]}.iconbitmap(\"{method[i][1]}\")"
                        elif method[i][0] == "background":
                            temp_method += f"{line[0]}[\"bg\"] = \"{method[i][1]}\""
                        else:
                            temp_method = remove_suffix(temp_method, temp_method.endswith("\n"))

                method = temp_method
                del temp_method

            elif method.startswith("text"):
                method = method.replace("text ", "", 1)

                optional_params = {
                    "align": "nsew",
                    "background": "#f0f0f0",
                    "color": "black"
                }

                if "--align" in method:
                    try:
                        optional_params["align"] = re.findall("--align:[a-zA-Z\-]*", method)[0].replace("--align:", "", 1)
                        method = method.replace(f" --align:{optional_params['align']}", "")
                    except IndexError:
                        pass
                    if optional_params["align"] == "top":
                        optional_params["align"] = "n"
                    elif optional_params["align"] == "top-right":
                        optional_params["align"] = "ne"
                    elif optional_params["align"] == "right":
                        optional_params["align"] = "e"
                    elif optional_params["align"] == "bottom-right":
                        optional_params["align"] = "se"
                    elif optional_params["align"] == "bottom":
                        optional_params["align"] = "s"
                    elif optional_params["align"] == "bottom-left":
                        optional_params["align"] = "sw"
                    elif optional_params["align"] == "left":
                        optional_params["align"] = "w"
                    elif optional_params["align"] == "top-left":
                        optional_params["align"] = "nw"
                    elif optional_params["align"] == "center":
                        optional_params["align"] = "nesw"
                    else:
                        error(line_numbers, "ArgumentError", f"Parameter '--align' cannot have the value '{optional_params['align']}'.")
                if "--background" in method:
                    try:
                        temp = method.split("--background:")[1]
                    except IndexError:
                        temp = "grey"
                    try:
                        temp = temp.split(" ")[0]
                    except IndexError:
                        pass
                    optional_params["background"] = temp
                    method = method.replace(f" --background:{optional_params['background']}", "")
                    del temp
                if "--color" in method:
                    try:
                        temp = method.split("--color:")[1]
                    except IndexError:
                        temp = "black"
                    try:
                        temp = temp.split(" ")[0]
                    except IndexError:
                        pass
                    optional_params["color"] = temp
                    method = method.replace(f" --color:{optional_params['color']}", "")
                    del temp

                # Support for newlines
                method = method.replace("$newline$", "\\n")

                # Method 1: Pack ; Method 2 : Grid
                method = method.split(" ")
                if method[1] == "pack":
                    try:
                        method[2] = recreate_string(method[2:len(method)], " ").replace("\"", "\\\"")
                        temp_method = f"tk.Label({method[0]}, " \
                                                            f"text=\"{method[2]}\", " \
                                                            f"bg=\"{optional_params['background']}\", " \
                                                            f"fg={optional_params['color']})"
                    except IndexError:
                        error(line_numbers, "ArgumentError", texts.errors["FunctionArgumentError"].format(args_required=2, args_nbr=len(method)))

                    temp_method += f"\n{line[0]}.pack()"
                    method = temp_method
                    del temp_method
                else:
                    try:
                        method[3] = recreate_string(method[3:len(method)], " ").replace("\"","\\\"")

                        # Column span option
                        if "--column_span" in method[3]:
                            try:
                                columnspan_value = int(method[3].split("--column_span:")[1])
                                method[3] = method[3].replace(f"--column_span:{str(columnspan_value)}", "")
                                method[3] = remove_suffix(method[3], method[3].endswith(" "))
                            except ValueError:
                                error(line_numbers, "ArgumentNotInt", "column_span : " + texts.errors["ArgumentNotInt"])
                        else:
                            columnspan_value = 1

                        temp_method = f"tk.Label({method[0]}, text=\"{method[3]}\", " \
                                                            f"bg=\"{optional_params['background']}\", " \
                                                            f"fg=\"{optional_params['color']}\")"

                    except IndexError:
                        error(line_numbers, "ArgumentError", texts.errors["FunctionArgumentError"].format(args_required=3, args_nbr=len(line)))

                    temp_method += f"\n{line[0]}.grid(row=int({method[1]}), column=int({method[2]}), " \
                                                      f"columnspan={columnspan_value}, " \
                                                      f"sticky=\"{optional_params['align']}\")"

                    method = temp_method
                    del temp_method

        line[2] = method

    return recreate_string([line[0], line[1], line[2]], " "), ("is_lib", True)

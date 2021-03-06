![Discord users online](https://img.shields.io/discord/718802975153324093?label=Discord%20server) ![Repository size](https://img.shields.io/github/repo-size/megat69/ACPL?label=Repository%20size%20-%20files%20size) ![Downloads](https://img.shields.io/github/downloads/megat69/ACPL/total?label=Overall%20downloads) ![Stars](https://img.shields.io/github/stars/megat69/ACPL) ![Last release](https://img.shields.io/github/v/release/megat69/ACPL?label=Last%20release) ![OS support](https://img.shields.io/badge/OS%20Support-Windows-success) ![OS support](https://img.shields.io/badge/OS%20Support-Mac%2C%20Linux-orange) ![Commits](https://img.shields.io/github/commit-activity/w/megat69/ACPL?label=Commits) ![Last release date](https://img.shields.io/github/release-date/megat69/ACPL?label=Last%20release%20date)

![ACPL Logo](https://i.ibb.co/Yf6tfxH/ACPL-logo-color.png)

# ACPL
My own programming language (interpreted in Python).

This project has just been made for fun, for practice, and is actually useful (somehow)

If you want to use it, please credit me xD !

Big thanks to all the translators, and if you want to meet them, just join our [Discord](https://discord.gg/MBuKcUn) !

### REQUIRED LIBRARIES ###
Run `setup.py` to install all the required libraries.

### THINGS TO KNOW ###
Run the script `console.py` to have access to the ACPL console.

Available commands :
- `end` : Ends the console process.
- `run` : runs a specific file. Syntax : `run <file>`.
- `about` : Gives a special message from the author concerning the language ;)
- `version` : Gives the last stable version and the actual dev build.
- `settings` : Opens up a dialog box which allows you to tweak your settings
- `update` : Launches the update program.
- `pyrun` : Runs a specified python file
- `compile` : Compiles an ACPL file to a Python file
- `ini-content` : Displays the content of the ini file.
- `open` : Opens a specific file in its default program.
- `display` : Prints the content of a specified file.
- `change-line`/`modify-line` : Modifies a specific line in a plain text file.
- `redo` : Reuses the last command.
- `lib <install:delete:doc:update> <lib_name>` : Respectively installs, delete, or gives the documentation of the specified lib.
- `lib list <available|installed>` : Lists all installed libs or available libs, depending on which one you choose.
- `ls/dir [dir_to_map='./'] [*extensions]` : Returns a tree of the selected directory.

You can tweak your settings using the `settings` command.

### COMPILING ###
The language can be transpiled in Python using the following process.

It works very simply :
After setting the corresponding `ini` options with the `settings` console command, just type the following command : `transpile <ACPL_file> <final_python_file_filename>`
It will generate the corresponding python file with the name you inputted.

Your code can also be compiled into an auto-executable file as well !
- If your program does not use any library, then the compiler function is supported.
- If not, it might work, but is untested, and not supported either.
- Syntax : `compile <ACPL file> [Exe file filename=ACPL file filename] [--end-message:<bool> = True] [--disable-icon:<bool> = False]`
  + `ACPL file` is the file you want to compile. **THIS FILE HAS TO BE PLACED AT THE ACPL ROOT FOLDER !**
  + `Exe file filename` is the filename of the compiled exe file. If not specified, the default name will be the name of the original script.
  + `[--end-message:<bool> = True]` is a boolean that will define whether or not the file will have an end message (litterally : *`Press enter to continue..`* at the end of the script). Default : True.
  + `[--disable-icon:<bool> = False]` is a boolean that will define if you want to disable the ACPL icon as the exe file icon. Default : False. **ICONS CANNOT BE CREATED ON LINUX DEVICES !**

### DOCUMENTATION ###
Things to know :
This program works line per line, which means that it is **ONE INSTRUCTION PER LINE**.
You can also use a comma (`;`) to mark the end of the line, but it is not required.
This language also does not use quotes (`"`).

~~Plugin for [Sublime Text 3](https://www.sublimetext.com/3) (Syntax highlighting) disponible in the [wiki](https://github.com/megat69/ACPL/wiki/Sublime-Text---Color-Highlighting).~~ *Not remade for current version*
Plugin for ini file also disponible in the [wiki](https://github.com/megat69/ACPL/wiki/Sublime-Text---Color-Highlighting).

Before everything, open the console (file `console.py`). Type `help` inside if required.

Help for the console is not provided in the documentation.

#### comments #####
You can comment line per line with `#` or `//`.
Multiline comments are done with `/*` and `*/`.

#### print ####
You can use the print method to send something in the console.

**EXAMPLE 1 :**
*Input :*
`print Hello`
*Output :*
`Hello`

You can also inject variables inside it by typing `{<var_name>}`.

In practise, if we have a string variable named "pseudo" containing the value "TheAssassin", we can get this :

**EXAMPLE 2 :**
*Input :*
`print Hello, {pseudo} !`
*Output :*
`Hello, TheAssassin !`

It works with every type of variable.

Otherwise, you can use `<equation>` to make an equation.

With a variable `number` equals to ten, that we want to multiply by two :

*Input :*
`print 10 multiplied by 2 equals <{number}*2>`
*Output :*
`10 multiplied by 2 equals 20`

#### variables ####
Variables have to be defined clearly.
It follows the form `var[:var_type][--var_action] <var_name> <var_operator> <value>`.

`<var_name>`
The variable name.

`<var_operator>`
Can be :
- `=`
  - Default operator, assigns a brand new value to the variable.
- `+=`
  - *Addition/Concatenation* operator.
  - Adds the old variable value with the new one, or concatenates if the old and new variables are strings.
- `-=`
  - Substract operator
  - Substratcs the old variable to the new one.
- `*=`
  - Multiply operator
  - Multiplies the old variable with the new one.
- `/=`
  - Division operator
  - Divides the old variable with the new one.
- `//=`
  - **EUCLIDIAN** division operator.
  - Divides the old variable with the new, but only keeps the integer part.
- `%=`
  - Modulo operator
  - Keeps the rest of the euclidian division of the old and new variable.

`<value>`
It depends :

 - If integer, it is simply a whole number.
 - If float, as written earlier, the whole part and the decimal part are seprated by a dot (`.`).
 - If string, it is as many characters, symbols, and digits as you want.
 - If boolean, it is `true` or `false`. Every type of lower and upper case is accepted.
 - If list, see below, at **Lists** section
 
 `[:var_type]`
 This one is special ; you can force a variable type by typing `var:type` instead of `var`.

 The use of this parameter is strictly recommended.
 
 The current variable types are :
 - `int`
 - `float`
 - `bool`
 - `list` **(see down there)**
 - and `str`
 
**This is required if you want to use the compiler.**

`[--var_action]`
These are small functions that can modify a variable's content.

They can be :
- Syntax : `var[:type][--var_action]`
- `lowercase` : Sets the variable string to lower case
- `uppercase` : Sets the variable string to upper case
- `round:<number_after_dot:int>` : Puts the float variable to a round number, with `number_after_dot` numbers after the dot.
- `ceil` : Converts the float variable to the integer just above it.
- `replace`
  - Replaces elements of the string.
  - Syntax : `--replace:"<element_to_replace>""<replace_with>"["count"]`
  - The first `count` `element_to_replace` will be searched through the string and replaced by the `replace_with`.
  - If `count` is undefined, all the `element_to_replace` will be replaced by `replace_with`.
  - Example 1 *(Without `count`)* : `var:str--replace:"e""a" Test = Yeeeeeeeeeeeeeeeee` will result in `Yaaaaaaaaaaaaaaaaa`
  - Example 2 *(With `count`)* : `var:str--replace:"e""a""3" Test = Yeeeeeeeeeeeeeeeee` will result in `Yaaaeeeeeeeeeeeeee`
- `split`
  - Splits the string into a string
  - Syntax : `--split:"<separator>"`
  - Example 1 : `var:str--split:" " Test = This is a test string.` will result in `['This', 'is', 'a', 'test', 'string.']`
  - Example 2 : `var:str--split:"ng " Test = Testing string :D` will result in `['Testi', 'stri', ':D']`

*3.11 feature*
Var actions have their equivalents in values.
Instead of typing a direct value, you can use `var_action <var_action_name> [var_action_parameters] <value>` instead.
For special syntaxes, ask me on the [ACPL Discord](https://discord.gg/MBuKcUn).

**SPECIAL VALUES :**
 - It can also be special values :  you can meet the `input` method.
   It asks the user to type something in the console.
   Syntax : `input <text>`
   `<text>` is the text that will be asked to the user.
   You can also put `\n` to create a newline.

 - You can also do mathematical equations to affect variables.
   They can also contain variables.
   Syntax : `<equation>`

 - You can also define them as random.
   Therefore, type `random <first_number> [second_number]`.
   If both numbers are given, the result will be a random number between them.
   Else, it will be a random number between 0 and <first_number>.
   You can also replace numbers by variables.

 - You can use libraries as well.
   Type `lib <lib_name> <lib_syntax>` for that purpose.
   *This is assuming that the library you are using purposes functions for variables.*

**BUILT-IN VARIABLES :**        *Introduced in 3.11*
- `length`
  + Returns the length of the variable passed in parameter.
  + Syntax : `{length[<var name>]}`
- `true`
  + The boolean value `True`
- `false`
  + The boolean value `False`

**VARIABLE MODIFICATIONS :**          *Introduced in 3.11*
You can just type a variable's name to redifine it once it has been defined, instead of typing the old-fashion `var[:type] <name> = <value>` again !

Now, you just need to type that once, and then a single `<name>[:type] = <value>` will be understood !
- If the parameter `type` is not given, the type will be the type of the last variable's value.
- E.g., if you had a variable named `test` which was an integer, if you don't specify a new type, the variable will remain an integer.

**EXAMPLE 1 :**
We want to create a variable "pseudo" containing "TheAssassin".
*Input :*
`var:str pseudo = TheAssassin`
*To use it :*
`{pseudo}`

**EXAMPLE 2 :**
We want to ask the user for his pseudo :
*Input :*
`var:str pseudo = input What is your pseudo ? `

**EXAMPLE 3 :**
We want to calculate `3*(6**2)` and store it into a variable "operation".
*Input :*
`var:int operation = <3*(6**2)>`

**EXAMPLE 4 :**
We have a variable "age" containing the value `18`. We want to multiply it by 2 *(don't ask why xD)*
And then store it into "double"
*Input :*
`var double *= 2`

**EXAMPLE 5 :**
We ask the user for his age and we multiply it by 5.
*Input :*
```
var:int age = input What is your age ? 
var:int new_age = <2*{age}>
print Your new age is now {age} xD !
```
*Output (for this example, age equals 18) :*
`Your new age is now 90 xD !`

**EXAMPLE 6 :**
You want a random number between 1 and 50 for the Lotto.
*Input :*
`var:int Lotto = random 1 50`

#### lists ####
Lists are a special type of variable introduced in version 3.8, allowing to store multiple variables in a single one.
If you use C, it's some sort of dynamically changing array.

**How to declare a list :**
Type like the following ;
```
var:list <name> = list [ELEMENT 0] [ELEMENT 1] [ELEMENT 2]
```
Every element of the list has to be between brackets when you initialize it.
Also, in the example, I created a list containing only 3 elements ; but a list can contain as many as you want.

You can define the type of an element by typing `<type>:` right after the opening bracket. By default, this type will be `string`.

**How to add an element at the end of a list :**
Type like the following : 
```
var:list <name> = list.add <content>
```
The `<content>` will be appended at the end of the list.

**How to insert an element at a specific index of the list :**
Type like the following : 
```
var:list <name> = list.insert <index> <content>
```
*Keep in mind indexes start at 0.*

**How to remove an element from a list :**
Type like the following : 
```
var:list <name> = list.remove <index>
```
*Keep in mind indexes start at 0.*

**How to get a specific element from a list ?**
Just use it as a normal variable, this way : `{my_list[<index>]}`

You can also use a variable in place of the index, but **equations won't work**.

**How can I get the length of the list ?**
Simply by typing `{my_list[len]}` or `{my_list[length]}`.

*3.11 feature*
You can also use `{length[my_list]}`


#### if ####

The `if` function is made to check if a condition is true or false.

If true, it will execute the following instructions block ; if false, it won't.

No `else` or `elseif` at the moment.

**Syntax :**
```
if <condition>
<instructions>
endif
```

The condition can contain as many variables as you want, and is with these operators :
- `==` : compares if equal
- `!=` : compares if different
- `<` : compares if inferior
- `>` : compares if superior
- `<=` : compares if inferior or equal
- `>=` : compares if superior or equal
- `in` : compares if a string is inside another, or an element is iside a list.

You can join more by typing :
- `and`, if so, it will be true only if all conditions are true.
- `or`, if so, it will be true if at least one of the conditions is true.

Parenthesis are used for priority.

The `<instructions>` can be whatever.

#### for ####
You can loop for a certain amount of times using a for loop.

Syntax :
```
for <variable_name> <min> <max>
<instructions>
endfor
```

Both `end for` and `endfor` are possible.

`<variable_name>` should be a name for a variable.
This variable is going to be created for the loop, usable inside, and destroyed after.

It will be incremented every looping.

`<min>` is the default value of `<variable_name>`

`<max>` is the maximum value of the variable.

Example :

*Input :*
```
for i 3 5
print Hey ! It's the {i} looping !
endfor
print And now I'm out...
```
*Output :*
```
Hey ! It's the 3 looping !
Hey ! It's the 4 looping !
Hey ! It's the 5 looping !
And now I'm out...
```

*Notice you can place an `if` or `while` statement inside, but no other for loop.*

You can break the loop at any moment by using the `break` instruction, or go to the next loop iteration by typing `continue`.

#### while ####
The while loop will execute a bloc of instructions as long as a condition is true.

*Syntax :*
```
while <condition>
   <instructions>
endwhile
```

Both `endwhile` and `end while` are possible.

The conditions are the exact same as the `if`.

For this loop too, you can break the loop at any moment by using the `break` instruction, or go to the next loop by typing `continue`.


#### pause ####
You can pause for a certain amount of time using `pause` method.
Syntax : pause `<seconds>`
`<seconds>`
Can be an integer value, a float value, or a variable.
If you use a variable, the syntax is `pause {<variable_name>}`.
 
#### deletevar ####
You can delete an unnecessary variable and free memory with this instruction.

Simply type `deletevar <variable_name>` to do so.

*Example :*
`deletevar Test` will delete var `Test`.

*3.11 feature*
Delete multiple variables at once by separating the names of the variables you want to delete with commas.
*Example :*
`deletevar var1, var2, var3, another_var, etc`

#### functions ####
Functions allow to write some code once and reuse it as much as you want.

**How to define a function *(without parameters)* ?**
- Type `function <name>`
- Write the code of the function under it
- End by `endfunction` or `end function`
**How can I call a function *(without parameters)* ?**
- Type `use_function <function_name>`
**How to define a function *(with parameters)* ?**
- Add the parameter names (separated by spaces) after the  `function <name>`
- You can then use them inside the function as normal variables. But if you modify them, they'll become global variables.
- Example : `function hello first_name last_name`
**How can I call a function *(with parameters)* ?**
- Add the values of the parameters after the `use_function <function_name>`, separated by spaces.
- They can be hardcoded values, variables, or equations.
- Example, following the function defined above : `use_function hello TheAssassin71 {last_name}`

#### libraries ####
[For further detail, go to the wiki page.](https://github.com/megat69/ACPL/wiki/Libs)

[Lib creation tutorial](https://github.com/megat69/ACPL/wiki/Lib-creation)

You can download and install libs through the console commands.

Type `lib install <lib>` to install one and `lib delete <lib>` to delete one.

You can also do a `lib doc <lib>` to get a library documentation.

Every library can be seen at this link : [https://github.com/megat69/ACPL/tree/master/acpl_libs](https://github.com/megat69/ACPL/tree/master/acpl_libs)

To use one, declare at the beginning of your program `$use: <lib>`.

#### aliases ####
Define aliases using the `$alias` instruction.

This allows to use other names for functions.
*Example :*
- You want to call `print` bu using the C++ like `std::cout` function.
- You have to type `$alias print std::cout`.
- Typing `std::cout` in any line of the program will call the function `print`.

### 3.11.1
- New console commands
  - Added two new subcommands to `lib` command
  - `lib list <available|installed>`
    - Will, depending on whether you chose as parameter `available` or `installed`, show all the libs installed on your computer, or the ones available online.
  - `lib update <lib>`
    - As the name suggests, this command will update the lib of your choice.
    - With the recent 3.11 update, this command will come in handy.
- **COMPILER OPTIMIZATION**
  - New setting : `optimize-compiled-file`, as a boolean.
    - Default : True
  - Decides whether or not the transpiled Python file should be optimized.
  - Optimiaztion takes longer to build the Python file, but the final code runs faster and is simpler to read.

### 3.11
- Translation files are ready, just waiting for the translators.
  - Language 98% translatorsted in French.
- Files library
  - Can read files
  - Can write in files
- Lib access to variables
  - You can now use libs as variables
  - `var <name> = lib <lib_name> <lib_syntax>`
  - Example : `var file_content = lib files my_file.txt`
- Deletevar tweak
  - You can now delete multiple vars at once
  - Just separate the variables names by commas
  - Syntax : `deletevar <var1>, [var2], etc...`
- Var actions aliases
  - You can now use the var actions inline, by specifying it after the equal sign
  - Syntax : `var[:type] <name> = var_action <var_action_name> [var_action_parameters] <value>`
  - Some var actions used this way might require a different syntax, see the documentation for more info.
- Variable length
  - You can now use the variable 'length'
  - Syntax : `{length[<var_name>]}`
- New `ls`/`dir` command
  - Will build a file tree of the specified folder
  - Syntax : `dir [folder=./] **[extension=*]`
  - Example : `dir ./ py acpl` will diplay all acpl and Pytho files in the current folder
- Command aliases
  - Define aliases using the `$alias` instruction
  - Allows to use other names for functions
  - Example :
    - You want to call `print` bu using the C++ like `std::cout` function
    - You have to type `$alias print std::cout`.
- Equations have been disabled for `if` and `while` statements.
  - Who cares ? They are not needed there.
  - Might return in 3.11.1 or in 3.12
- **Full boolean implementation**
  - New *bool* type
  - Defined with new var type `:bool`
  - Value : either `True` or `False`.
  - New built-in variables : `true` and `false`, with the respective boolean values.
- **Var modifications, without re-assigment**
  - You can now just type a variable's name to redifine it once it has been defined, instead of typing the old-fashion `var[:type] <name> = <value>` again !
  - Now, you just need to type that once, and then a single `<name>[:type] = <value>` will be understood !
    + If the parameter `type` is not given, the type will be the type of the last variable's value.
    + E.g., if you had a variable named `test` which was an integer, if you don't specify a new type, the variable will remain an integer.
- **Compiler/Transpiler**
  - Command `compile` has been renamed to `transpile`, which corresponds more to what it actually does.
  - **A NEW COMPILER HAS BEEN INTRODUCED !**
  - Your code can now be compiled into an auto-executable file !
    + If your program does not use any library, then the compiler function is supported.
    + If not, it might work, but is untested, and not supported either.
  - Syntax : `compile <ACPL file> [Exe file filename=ACPL file filename] [--end-message:<bool> = True] [--disable-icon:<bool> = False]`
    + `ACPL file` is the file you want to compile. **THIS FILE HAS TO BE PLACED AT THE ACPL ROOT FOLDER !**
    + `Exe file filename` is the filename of the compiled exe file. If not specified, the default name will be the name of the original script.
    + `[--end-message:<bool> = True]` is a boolean that will define whether or not the file will have an end message (litterally : *`Press enter to continue..`* at the end of the script). Default : True.
    + `[--disable-icon:<bool> = False]` is a boolean that will define if you want to disable the ACPL icon as the exe file icon. Default : False. **ICONS CANNOT BE CREATED ON LINUX DEVICES !**

### 3.10.1
- Bugfixes
  - Corrected a shell from a past dev experience with command `ini-content`
    - Using that command made the console crash
    - Now fully fixed, with revamped version of the command
  - Corrected a problem with the `settings` command
    - When entering wrong values in input fields, and clicking save, the inputs weren't reset
    - It was just a dev error, now fully fixed.
  
### 3.10
- **Automatic updates**
  - If it upsets you to ALWAYS have to manually update your ACPL, then this release might be the last you'll download.
  - This update brings back the automatic updates, in a revamped way.
  - If a new release is available, it will ask you once you boot the console.
  - If you skip the update, you can still download it by using the console command 'update', or by running `updater_main.py`.
- Types in lists
  - You can define the type of an element in the list when you create it.
  - Syntax : `var:list my_list = list [int:1] [float:1.5] [bool:True] [str:Normal string] [Default is str]`
- Command line arguments for `main.py`
  - When invoking `main.py` from a command prompt, you can add the filename of an ACPL file at the end. It will automatically run it and override the one in the startup file.
- Condtions inside each other
  - **ELSE HAS BEEN REMOVED**
  - By popular opinion, nested `if`s have been preferred to the `else` statement.
  - You can now use multiple `if`s inside each other.
- New libs function
  - A new function is required for libs to get through the compiler : `libs_to_import()`
  - This function returns all the required libs by the final python file this way :
  - If the generated result does not require anything in order to work, just return a tuple containing to empty tuples, this way : `return (tuple(), tuple())`
  - If it only requires to import a full lib, (*example : `sys`*), the first tuple contains that lib : `return (("sys",), tuple())`
  - If you need more of those : `return (("sys", "math", "tkinter"), tuple())`
  - The other tuple contains all the functions from libs. If you want `from json import load`, then : `return (tuple(), (("json", "load"),))`
  - If you want `from json import load, dump`, then : `return (tuple(), (("json", "load, dump"),))`
  - And if you want `from json import load` and `from math import *` : `return (tuple(), (("json", "load"), ("math", "*")))`
- ACPL debugger
  - New console command `debug <file>`
  - This command will start a debugger that will tell you what happens in the ACPL program.
  - The program will tell you what instruction is being expected, what variables are existing at the end of the line, and let you continue it step by step or stop it. This possibility is available at every single line.
- Settings
  - The old rusty `modify-ini` command was very complicated, with many things to remember. *As its creator, I didn't remember those myself !*
  - This command has been changed to `settings`, and doesn't take any arguments.
  - This will pop up a dialog box that will let you customize your settings.
- Bugfixes
  - Lists were buggy with functions. They still are, but less.

### 3.9.1
Bugfixes *(thanks to PancakesLord)* :
- `setup.py`, if you entered a wrong country code, you couldn't launch the console or anything.
- On Linux systems or systems with multiple Python versions installed, you couldn't launch any file from any file. This is now fixed, using a more responsive technique than the older one.
- `msvcrt` lib was used, and kinda useless. It's been there for 7 months, without proper use, and it made the program crash on Linux systems. Now fixed.
Bug discovered, not fixed yet :
- If you create a variable, typed `int`, and you ask the user to input a value, if the user enters `e`, the variable will be equal to `2`, and if he enters `i`, it will be equal to `5`.
I have no idea of why this bug exists, and it probably won't be fixed for now.
  
Anyway, quick changes, just wanted to let you know.

### 3.9
- IDE
  - Added a memory system to the IDE
  - Every time you close the IDE, it will save the last cursor position, and it will set the cursor to the correct position once you open this file again.
- Redo
  - New console command
  - Re-iterates the last action you did
 - String manipulations
  - 2 new `var_actions` : `replace` and `split`
    - `replace`
      - Replaces elements of the string.
      - Syntax : `--replace:"<element_to_replace>""<replace_with>"["count"]`
      - The first `count` `element_to_replace` will be searched through the string and replaced by the `replace_with`.
      - If `count` is undefined, all the `element_to_replace` will be replaced by `replace_with`.
      - Example 1 *(Without `count`)* : `var:str--replace:"e""a" Test = Yeeeeeeeeeeeeeeeee` will result in `Yaaaaaaaaaaaaaaaaa`
      - Example 2 *(With `count`)* : `var:str--replace:"e""a""3" Test = Yeeeeeeeeeeeeeeeee` will result in `Yaaaeeeeeeeeeeeeee`
    - `split`
      - Splits the string into a string
      - Syntax : `--split:"<separator>"`
      - Example 1 : `var:str--split:" " Test = This is a test string.` will result in `['This', 'is', 'a', 'test', 'string.']`
      - Example 2 : `var:str--split:"ng " Test = Testing string :D` will result in `['Testi', 'stri', ':D']`
- **FUNCTIONS**
  - Major feature of the update
  - Functions allow to write some code once and reuse it as much as you want.
  - **How to define a function *(without parameters)* ?**
    - Type `function <name>`
    - Write the code of the function under it
    - End by `endfunction` or `end function`
  - **How can I call a function *(without parameters)* ?**
    - Type `use_function <function_name>`
  - **How to define a function *(with parameters)* ?**
    - Add the parameter names (separated by spaces) after the  `function <name>`
    - You can then use them inside the function as normal variables. But if you modify them, they'll become global variables.
    - Example : `function hello first_name last_name`
  - **How can I call a function *(with parameters)* ?**
    - Add the values of the parameters after the `use_function <function_name>`, separated by spaces.
    - They can be hardcoded values, variables, or equations.
    - Example, following the function defined above : `use_function hello TheAssassin71 {last_name}`
- Bugfix : When trying to set a specific element of a list, you just couldn't. Now fixed.
- **LIBS**
  - Biggest feature of the update
  - You can download and install libs through the console commands.
  - Type `lib install <lib>` to install one and `lib update <lib>` to update one.
  - If you want to uninstall any of them, type `lib delete <lib>`.
  - If you want to see a lib's documentation, type `lib doc <lib>`.
  - To use one, declare at the beginning of your program `$use: <lib>`.
  - Everyone can submit his lib on the [Discord](https://discord.gg/MBuKcUn), and I'll publish it every time (except some obvious exceptions (not enough optimized, dangerous, or NSFW)) ! [Tutorial here.](https://github.com/megat69/ACPL/wiki/Lib-creation)
  - Every library has its own documentation.
  - See them in the source code, and find `acpl_libs/doc_<lib>.md`, where `<lib>` is the library you're looking for.
  - You can look for **How to create a lib** in the [ACPL wiki](https://github.com/megat69/ACPL/wiki/Lib-creation)

### 3.8.1
- Disabled the `update` console command and automatic updates in general. This feature needs a rework.
- Created the `changelog` console command. This command allows you to see the latest changelog.

### 3.8.0
- Lists
  - New `list` variable type
  - New `list.add`, `list.insert`, and `list.remove` methods
  - Refer to the documentation.
- New setup
  - Now installs requirements correctly
  - Now allows you to tweak your settings at first launch
- Variables operators
  - Variables operators have been added.
  - Variable operators include : 
    - `+=`
    - `-=`
    - `*=`
    - `/=`
    - `//=`
    - `%=`
  - Variable operators act as if you were using the operation before the `=` on the variable value.
  - Syntax example : `var:int score += 5`
- Dialog boxes
  - Typing only `run` in the console will open a dialog box that will let you select a file to run.
  - The same goes on for the IDE, but this time, the dialog box opens anyway.

### 3.7.0
This update features a brand new IDE, accessible from the `ide` console command.
- IDE from `ide` console command :
  - Use the arrow keys to move in the text
  - Type text for the IDE to add the text
  - Auto-save functionality
  - Type `ACPL_IDE_NEW <filename>` to create a brand-new file, or just `<filename>` to open an existing one.
  - Press escape to access a few console commands :
    - `quit` / `end` : Closes the IDE
    - `run` : Runs the file **IF THE CURRENT FILE IS AN ACPL OR A PYTHON FILE**
    - `compile` : Compiles the file if the file is an ACPL file
    - `open` : Lets you open an existing file
    - `new <filename>` : Creates a new file and opens it.
- Also compiler bugfixes

Showcase videos : 
[Showcase part 1](https://streamable.com/3r2ubk)
[Showcase part 2](https://streamable.com/q58yqt)

### 3.6.0
- `var_actions` : small functions added to variables
  - Syntax : `var[:type][--var_action]`
  - `lowercase` : Sets the variable string to lower case
  - `uppercase` : Sets the variable string to upper case
  - `round:<number_after_dot:int>` : Puts the float variable to a round number, with `number_after_dot` numbers after the dot.
  - `ceil` : Converts the float variable to the integer just above it.
- **MASSIVE BUGFIXES**

### Changelog for 3.5.0
- Instruction "continue"
- Easter egg ?? 
- Boucle "while"
  - Executes a condition as long as it is true
  - Syntax : 
```
while <condition>
   <instructions>
endwhile
```
- modify-ini "compile-ask-for-replace"
- input type
  - if you put ":<type>", the variable will be of this type.
  - Types are : "int", "float", and "str".
  - It is required if you use the compiler.

### Changelog for 3.4
- **Compiler**
The biggest feature so far. It has been so much work preparing that.
It actually is an ACPL to Python compiler. *Or transpiler, btw*
It allows you to generate a Python file from an ACPL file, which is much easier to distribute, knowing how few people downloaded ACPL.
- **Console command : *pyrun***
This very simple command allows you, by the ACPL console, to run a Python file.
It's pretty easy, and allows you to check if your ACPL files compiled to Python are still working. If they are not, contact me.
- **Console command : *open***
Allows you to open a specified file in its default program.
That's as simple as it sounds.
- **Added console command *display***
  - Syntax : `display <file>`
  - Prints the raw content of the file in the console.
- **Added `break` instruction for loops.**
  - This instruction make you able to break the loop when you call it.
- **BUGFIXES**
It's quite explicit. But as you might have seen, 3.3.2 was VERY buggy.
It's now mostly fixed.
*Remember it's just a PreRelease btw*
- **Options *modify-ini***
  - `startup-check-update` : Boolean. Allows you to choose whether or not you prefer the ACPL console to check updates at startup or not.
  I find this very useful.
  - `open-compiled-file` : Boolean. If True, the brand new newly compiled file you just generated in Python will open in its default program.
  Quite neat, isn't it ?
  - `leave-comments-at-compiling` : Boolean *(again xD)*. If True, the single-line comments will be kept through compiling and will appear in the final compiled Python file. If False, they simply won't.
  - `compiling-style` : Chooses compiling style. If "compacted" or "collapsed", the compiled result will be very short and unclear. If "expanded", it will be much more readable /\*\ *Beware with that last ! It tends to leave a lot of blank lines.*


### Changelog for 3.3
- Added the support for equations.
It works this way :

*Input :*
`print 10 multiplied by 2 equals <{number}*2>`
*Output :*
`10 multiplied by 2 equals 20`

- Added the `deletevar` command.

### Changelog for 3.2.1
- Added `ini-content` command to the console.
This command allows you to see what's inside the ini file from the console.

### Changelog for 3.2
- Added `for` loop

### Changelog for 3.1
- Added if and else

## Changelog for 3.0
*Apply manually*
- Remade whole code
- Remade syntax
- Added a new option in the ini file
- Removed compiler
- Improved processing time

## Changelog for 3.0

### Changelog for 2.5
- Added a compiler ! You can now transpile your ACPL programs in Python !

### Changelog for 2.4
- New lib : colors
- Now able to access the code's variables in the libs ! Just look how it has been done in `libs/lib_colors.py`.

### Changelog for 2.3
- `if` and `else` are finally here !
  Go to the wiki for further information
- Italian translation !

### Changelog for 2.2
*Apply manually !*

- Added libs
- Added `lib` command to console
- Added a few features

### Changelog for 2.1
- Variables are usable everywhere again

## Changelog for 2.0
**TO APPLY MANUALLY**

*Older versions not compatible with this one !*
- No longer typed vars, they are now flexible, with new syntax !
- Rewrote the entire code, now simpler, faster, better, a with more functionalities !
- Now translated in Azerbaijani and Turkish !
- Updated the update checker, works better now.

### Changelog for 1.4.4
**EMERGENCY UPDATE - To apply manually**
- Big changes made to the updater.

### Changelog for 1.4.3
- Fixed a lot of bugs and shells.

### Changelog for 1.4.2
- Added option `use-colors` in the ini file, defining if it will use the colors or not in the console.

### Changelog for 1.4.1
- Language translated everywhere !

### Changelog for 1.4
- Now updates automatically !
- Supports dutch *Console and errors only*

### Changelog for 1.3
- Added custom error messages ;)
- Added multilingual support (french and english). *Console and errors only are supported at the moment.*

### Changelog for 1.2
- Added syntax highlighting for sublime text (`.acpl` and `.acpl-ini` files)
- Added multiple variable support in print
- Added a `reload` command for the console
- Upgraded `startup.acpl-ini`

## Changelog for 1.0
## **1.0 is here !**
- Added a console
- You can now run files named differently than "code.acpl" through the console
- Added a "startup.ini" files containing requirements for both console and compiler
- Added console commands (Watch more in the documentation)

### Changelog for 0.8
- Added the support for randomness in variable creation
- Added the support for round in int creation

### Changelog for 0.7
- Added the support for mathematical equations in variable creation

### Changelog for 0.6
- Added the `code.acpl` file containing a code sample.

### Changelog for 0.5
- Added inputs for all types
- Added pauses

### Changelog for 0.4

First official release.
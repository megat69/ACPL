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
  - Language 98% translated in French.
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

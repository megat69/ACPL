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
  - Type `lib install <lib>` to install one.
  - If you want to uninstall any of them, type `lib delete <lib>`.
  - If you want to see a lib's documentation, type `lib doc <lib>`.
  - To use one, declare at the beginning of your program `$use: <lib>`.
  - Everyone can submit his lib on the [Discord](https://discord.gg/MBuKcUn), and I'll publish it every time (except some obvious exceptions (not enough optimized, dangerous, or NSFW)) ! [Tutorial here.](https://github.com/megat69/ACPL/wiki/Lib-creation)
  - Every library has its own documentation.
  - See them in the source code, and find `acpl_libs/doc_<lib>.md`, where `<lib>` is the library you're looking for.
  - You can look for **How to create a lib** in the [ACPL wiki](https://github.com/megat69/ACPL/wiki/Lib-creation)
  
### 3.9.1
Bugfixes *(thanks to PancakesLord)* :
- `setup.py`, if you entered a wrong country code, you couldn't launch the console or anything.
- On Linux systems or systems with multiple Python versions installed, you couldn't launch any file from any file. This is now fixed, using a more responsive technique than the older one.
- `msvcrt` lib was used, and kinda useless. It's been there for 7 months, without proper use, and it made the program crash on Linux systems. Now fixed.
Bug discovered, not fixed yet :
- If you create a variable, typed `int`, and you ask the user to input a value, if the user enters `e`, the variable will be equal to `2`, and if he enters `i`, it will be equal to `5`.
I have no idea of why this bug exists, and it probably won't be fixed for now.
  
Anyway, quick changes, just wanted to let you know.
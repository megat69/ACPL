![Discord users online](https://img.shields.io/discord/718802975153324093?label=Discord%20server) ![Repository size](https://img.shields.io/github/repo-size/megat69/ACPL?label=Repository%20size%20-%20files%20size) ![Downloads](https://img.shields.io/github/downloads/megat69/ACPL/total?label=Overall%20downloads) ![Stars](https://img.shields.io/github/stars/megat69/ACPL) ![Last release](https://img.shields.io/github/v/release/megat69/ACPL?label=Last%20release) ![OS support](https://img.shields.io/badge/OS%20Support-Windows-success) ![OS support](https://img.shields.io/badge/OS%20Support-Mac%2C%20Linux-orange) ![Commits](https://img.shields.io/github/commit-activity/w/megat69/ACPL?label=Commits) ![Last release date](https://img.shields.io/github/release-date/megat69/ACPL?label=Last%20release%20date)

# ACPL
My own programming language (interpreted in Python).

This project has just been made for fun, and is completely useless ;)

But still, if you want to use it, please credit me xD !

Big thanks to all the translators, and if you want to meet them, just join our [Discord](https://discord.gg/MBuKcUn) !

### REQUIRED LIBRARIES ###
`psutil` and `requests` libraries needs to be installed separately.
You can also run `setup.py`.

### COMPILING ###
The language can be compiled in Python using the following process.

The most interesting thing about this update is the compiler, obviously.
It works very simply :
After setting the corresponding `ini` options with the `modify-ini` console command, just type the following command : `compile <ACPL_file> <final_python_file_filename>`
It will generate the corresponding python file with the name you inputted.

### DOCUMENTATION ###
Things to know :
This program works line per line, which means that it is **ONE INSTRUCTION PER LINE**.
You can also use a comma (`;`) to mark the end of the line, but it is not required.
This can be modified through the `startup.ini` file or the console.
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
It follows the form `var <var_name> = <value>`.

**Change for 2.0 :** No longer variable types

<var_name>
The variable name. Note that two variables with different types can have the same name, even if not recommended.

<value>
It depends :

 - If integer, it is simply a whole number.
 - If float, as written earlier, the whole part and the decimal part are seprated by a dot (`.`).
 - If string, it is as many characters, symbols, and digits as you want.
 - If boolean, it is `true` or `false`. Every type of lower and upper case is accepted.

**SPECIAL VALUES :**
 - It can also be special values :  you can meet the `input` method.
   It asks the user to type something in the console.
   Syntax : `input <text>`
   <text> is the text that will be asked to the user.
   You can also put `\n` to create a newline.

 - You can also do mathematical equations to affect variables.
   They can also contain variables.
   Syntax : `<equation>`
 - You can also define them as random.
   Therefore, type `random <first_number>, [second_number]`.
   If both numbers are given, the result will be a random number between them.
   Else, it will be a random number between 0 and <first_number>.
   You can also replace numbers by variables.

**EXAMPLE 1 :**
We want to create a variable "pseudo" containing "TheAssassin".
*Input :*
`var pseudo = TheAssassin`
*To use it :*
`{pseudo}`

**EXAMPLE 2 :**
We want to ask the user for his pseudo :
*Input :*
`var pseudo = input(What is your pseudo ? )`

**EXAMPLE 3 :**
We want to calculate `3*(6**2)` and store it into a variable "operation".
*Input :*
`var operation = 3*(6**2)`

**EXAMPLE 4 :**
We have a variable "age" containing the value `18`. We want to multiply it by 2 *(don't ask why xD)*
And then store it into "double"
*Input :*
`var double = 2*{age}`

**EXAMPLE 5 :**
We ask the user for his age and we multiply it by 5.
*Input :*
`int age = input What is your age ? 
int new_age = 2*{age}
print Your new age is now {age} xD !`
*Output (for this example, age equals 18) :*
`Your new age is now 90 xD !`

**EXAMPLE 6 :**
You want a random number between 1 and 50 for the Lotto.
*Input :*
`var Lotto = random 1, 50`

#### if ####

The `if` function is made to check if a condition is true or false.

If true, it will execute the following instructions block ; if false, two cases :
- There is nothing after : the program won't run the instructions block.
- It is an `else` : the program will run the instruction block after the else.

No `elseif` at the moment.

**Syntax :**

`if <condition>`

<instructions>
endif
`else`
<instructions>
endif

The condition can contain as many variables as you want, and is with these operators :
- `==` : compares if equal
- `!=` : compares if different
- `<` : compares if inferior
- `>` : compares if superior
- `<=` : compares if inferior or equal
- `>=` : compares if superior or equal
- `in` : compares if a string is inside another

You can join more by typing :
- `and`, if so, it will be true only if all conditions are true.
- `or`, if so, it will be true if at least one of the conditions is true.

The `<instructions>` can be whatever, but they need to have one more **TAB** than the if.

#### for ####
You can loop for a certain amount of times using a for loop.

Syntax :
```
for <variable_name> <min> <max>
<instructions>
endfor
```

Both `end for` and `endfor` are possible.

<variable_name> should be a name for a variable.
This variable is going to be created for the loop, usable inside, and destroyed after.

It will be incremented every looping.

<min> is the default value of <variable_name>

<max> is the maximum value of the variable.

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

*Notice you can place an `if` statement inside, but no other loop.*

You can break the loop at any moment by using the `break` instruction.


#### pause ####
You can pause for a certain amount of time using `pause` method.
Syntax : pause <seconds>
<seconds>
Can be an integer value, a float value, or a variable.
If you use a variable, the syntax is `pause {<variable_name>}.
 
#### deletevar ####
You can delete an unnecessary variable and free memory with this instruction.

Simply type `deletevar <variable_name>` to do so.

*Example :*
`deletevar Test` will delete var `Test`.
 
#### libraries ####
For further detail, go to the wiki page.

You can download and install libs through the console commands.

Type `lib install <lib>` to install one and `lib update <lib>` to update one.

To use one, declare at the beginning of your program `$use: <lib>`.

**Actual disponble libs :**

- String : basic string manipulations
- Wait_until_user_input : gives a new funtion to wait until user input.
- Run_file : allows you to run another ACPL code file.
- Os : allow you to run a system command.
- Colors : Allows you to put colors in your prints or variables ONLY IF the `use-colors` in the `startup.acpl-ini` is set to `True`.
- Files : Basic file manipulations. *Does not work very well*

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

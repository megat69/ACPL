# ACPL
My own programming language (compiled in Python).

This project has just been made for fun, and is completely useless ;)

But still, if you want to use it, please credit me xD !

### REQUIRED LIBRARIES ###
`psutil` and `requests` libraries needs to be installed separately.

### DOCUMENTATION ###
Actually, this program can only print, input, create variables, and pause.

Things to know :
This program works line per line, which means that it is **ONE INSTRUCTION PER LINE**.
You can also use a comma (`;`) to mark the end of the line, but it is not required.
The code has to be in the same folder than the `main.py` file, and inside a file named `code.acpl`.
This can be modified through the `startup.ini` file or the console.
This language also does not use quotes (`"`).

Plugin for [Sublime Text 3](https://www.sublimetext.com/3) (Syntax highlighting) disponible in the [wiki](https://github.com/megat69/ACPL/wiki/Sublime-Text---Color-Highlighting).
Plugin for ini file also disponible in the [wiki](https://github.com/megat69/ACPL/wiki/Sublime-Text---Color-Highlighting).

Before everything, open the console (file `console.py`). Type `help` inside if required.
Help for the console is not provided in the documentation.

#### comments #####
You can comment line per line with `#` or `//`.
There is no way to do multiline comments at the moment.

#### print ####
You can use the print method to send something in the console.

**EXAMPLE 1 :**
*Input :*
`print(Hello)`
*Output :*
`Hello`

You can also inject variables inside it by typing `{<var_type> <var_name>}`.
In practise, if we have a string variable named "pseudo" containing the value "TheAssassin", we can get this :

**EXAMPLE 2 :**
*Input :*
`print(Hello, {str pseudo} !)`
*Output :*
`Hello, TheAssassin !`

It works with every type of variable.

#### variables ####
Variables have to be defined clearly.
It follows the form `<var_type> <var_name> = <value>`.
<var_type> 
It exists 4 variable types :

 - Int : Stores an integer number, which can be everything from minus infinite to plus infinite. Syntax : `int`
 - Float : Stores a floating number. The whole part and the decimal part are seprated by a comma (`;`) or a dot (`.`). Syntax : `float`
 - String : Stores as many characters as you want. No quotes required. Syntax : `str` or `string`
 - Boolean : Stores a binary value (true or false). Syntax : `bool` or `boolean`

<var_name>
The variable name. Note that two variables with different types can have the same name, even if not recommended.

<value>
It depends :
 - If integer, it is simply a whole number.
 - If float, as written earlier, the whole part and the decimal part are seprated by a comma (`;`) or a dot (`.`).
 - If string, it is as many characters, symbols, and digits as you want.
 - If boolean, it is `true` or `false`. Every type of lower and upper case is accepted.
**SPECIAL VALUES :**
 - It can also be special values : in case of a all types (except `bool`) you can meet the `input` method.
   It asks the user to type something in the console.
   Syntax : `input(<text>)`
   <text> is the text that will be asked to the user.
 - You can also do mathematical equations to affect variables. Those equations **CAN NOT** contain any space.
   They can also contain ***ONE*** variable.
   Syntax : `math <equation>`
   As always, a variable is gotten by the syntax `{<type> <name>}`
 - You can also define them as random.
   Therefore, type `random(<first_number>, [second_number])`.
   If both numbers are given, the result will be a random number between them.
   Else, it will be a random number between 0 and <first_number>.
   *Variables are not usable inside at the moment.*
**MODIFIERS :**
 - Actually, only one exists : `--round`.
   It is only available for int types and it rounds the result.
   Syntax : `int <var_name> = <value> --round`

**EXAMPLE 1 :**
We want to create a variable "pseudo" containing "TheAssassin".
*Input :*
`str pseudo = TheAssassin`
*To use it :*
`{str pseudo}`

**EXAMPLE 2 :**
We want to ask the user for his pseudo :
*Input :*
`str pseudo = input(What is your pseudo ? )`

**EXAMPLE 3 :**
We want to calculate `3*(6^2)` and store it into a variable "operation".
*Input :*
`int operation = math 3*(6^2)`

**EXAMPLE 4 :**
We have a variable (type int) "age" containing the value `18`. We want to multiply it by 2 *(don't ask why xD)*
And then store it into "double"
*Input :*
`int double = 2*{int age}`

**EXAMPLE 5 :**
We ask the user for his age and we multiply it by 5.
*Input :*
`int age = input(What is your age ? )
int new_age = 2*{int age}
print(Your new age is now {int age} xD !)`
*Output (for this example, age equals 18) :*
`Your new age is now 90 xD !`

**EXAMPLE 6 :**
You want a random number between 1 and 50 for the Lotto.
*Input :*
`int Lotto = random(1, 50)`

#### pause ####
You can pause for a certain amount of time using `pause` method.
Syntax : pause(<seconds>)
<seconds>
Can be an integer value, a float value, or a variable (`int` or `float` only).
If you use a variable, the syntax is `pause({<variable_type> <variable_name>}).

## Changelog for 1.4.4
**EMERGENCY UPDATE - To apply manually**
- Big changes made to the updater.

## Changelog for 1.4.3
- Fixed a lot of bugs and shells.

## Changelog for 1.4.2
- Added option `use-colors` in the ini file, defining if it will use the colors or not in the console.

## Changelog for 1.4.1
- Language translated everywhere !

## Changelog for 1.4
- Now updates automatically !
- Supports dutch *Console and errors only*

## Changelog for 1.3
- Added custom error messages ;)
- Added multilingual support (french and english). *Console and errors only are supported at the moment.*

## Changelog for 1.2
- Added syntax highlighting for sublime text (`.acpl` and `.acpl-ini` files)
- Added multiple variable support in print
- Added a `reload` command for the console
- Upgraded `startup.acpl-ini`

## Changelog for 1.0
### **1.0 is here !**
- Added a console
- You can now run files named differently than "code.acpl" through the console
- Added a "startup.ini" files containing requirements for both console and compiler
- Added console commands (Watch more in the documentation)

## Changelog for 0.8
- Added the support for randomness in variable creation
- Added the support for round in int creation

## Changelog for 0.7
- Added the support for mathematical equations in variable creation

## Changelog for 0.6
- Added the `code.acpl` file containing a code sample.

## Changelog for 0.5
- Added inputs for all types
- Added pauses

## Changelog for 0.4

First official release.

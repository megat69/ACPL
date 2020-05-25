# ACPL
My own programming language (compiled in Python).

### DOCUMENTATION ###
Actually, this program can only print, input, and create variables.

Things to know :
This program works line per line, which means that it is **ONE INSTRUCTION PER LINE**.
You can also use a comma (`;`) to mark the end of the line, but it is not required.
The code has to be in the same folder than the `main.py` file, and inside a file named `code.acpl`.
This language also does not use quotes (`"`).

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

You can also inject ***ONE*** variable inside it by typing `{<var_type> <var_name>}`.
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
 - You can also do mathematical equations to affect variables
   They can also contain ***ONE*** variable.
   Syntax : `math <equation>`
   As always, a variable is gotten by the syntax `{<type> <name>}`

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

#### pause ####
You can pause for a certain amount of time using `pause` method.
Syntax : pause(<seconds>)
<seconds>
Can be an integer value, a float value, or a variable (`int` or `float` only).
If you use a variable, the syntax is `pause({<variable_type> <variable_name>}).

## Changelog for 0.7
- Added the support for mathematical equations in variable creation

## Changelog for 0.6
- Added the `code.acpl` file containing a code sample.

## Changelog for 0.5
- Added inputs for all types
- Added pauses

## Changelog for 0.4

First official release.

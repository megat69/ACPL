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
The variable name.

<value>
It depends :
 - If integer, it is simply a whole number.
 - If float, as written earlier, the whole part and the decimal part are seprated by a comma (`;`) or a dot (`.`).
 - If string, it is as many characters, symbols, and digits as you want.
 - If boolean, it is `true` or `false`. Every type of lower and upper case is accepted.
**SPECIAL VALUES :**
It can also be special values : in case of a string, you can meet the `input` method.
It asks the user to type something in the console.
Syntax : `input(<text>)`
<text> is the text that will be asked to the user.

## Changelog for 0.4

First official release.

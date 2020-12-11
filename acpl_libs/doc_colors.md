## Colors ACPL lib
This lib adds 9 new variables to your disposal, each of them making color in `print`s possible !

### Install 
Go on your ACPL console and type `lib install colors`.

### Usage 
#### Import
To use the color variables, you need to import the lib first.

Therefore, type `$use: colors` at the beginning of your code.

Then, you will need to import them.

To do so, type `lib colors import` at the beginning of your code. 

#### Variable names
You get access to :
- Colors : 
  - `colors_BLUE`
  - `colors_PINK`
  - `colors_GREEN`
  - `colors_YELLOW`
  - `colors_RED`
- Formatting : 
  - `colors_UNDERLINE`
  - `colors_BOLD`
  - `colors_ITALICS`
    
Also, you will need to end **EVERY OF THEM** using `colors_END`.

Otherwise, your code will bug as hell.

### Example
```
$use: colors
lib colors import
print {colors_GREEN}My text in green with {colors_ITALICS}italics{colors_END}{colors_GREEN} !{colors_END}
```

## GUI ACPL lib 

### Overview
The GUI lib lets you create simple windows and GUI with ACPL.

Full documentation in the *Usage* section.

### Install 
Go on your ACPL console and type `lib install GUI`.

### Usage
#### Window creation
Create a window with the following syntax : `lib GUI create window <variable> [param1=value1]...`

Also available as var method : `var <name> = lib GUI create window [param1=value1]...`

**AVAILABLE PARAMETERS :**
- *size* :
  - Value : string
  - Using the following syntax : `<height:int>x<width:int>`
- *title* :
  - String containing the title
- *icon* :
  - Path to the `.ico` file for the icon
- ~~*background* :~~
  - ~~String with the name of one of the Python Tkinter colors~~
  - ***Support dropped at the moment.***
  
  
#### Windows displaying
**This instruction has to go last, and is a blocking instruction !**

Type `lib GUI display <window>`

#### Text creation
Create bits of text using the following syntax : `lib GUI create text <variable> <window> <x y|pack> [--param1:value1]...`

Let's explain this last parameter, that will make the other parameters depend.

If you choose the option `pack`, then the text will just be appended under the last text you created, and at the center of the window.

If you instead want to align more and have more control over the style, use the `<x> <y>` coordinates.
These will create a grid, and your text will be placed at row n°`<x>` and column n°`<y>`.

**You cannot use both at once ! You can either use the grid OR the packing, but not both at the same time !**

**Optional parameters :**
- *Globals*
  - `align`
    - Defines the text alignment (in the whole window for the packing, in the cell for the grid)
    - String
    - Contains `top`, `left`, `right`, `bottom`, a combination of two of them, or `center`
  - `background` and `color`
    - One of the Python Tkinter supported colors.
- *GRID ONLY*
  - `columnspan`
    - Defines the number of columns that will be used for this cell.
    - Integer, cannot be zero or negative.
    - Default : 1
  
Also available as var action, with syntax `var <name> = lib GUI create text <window> <x y|pack> <text> [--param1:value1]`
  
### Example
Example 1, creation of a window containing "Hello World !", without optional colors.
```
$use: GUI
var window = lib GUI create window
lib GUI create text my_text window pack Hello World !
lib GUI display window
```

Example 2, creation of a window containing some sample text, with optional colors and parameters.

Run it to see a demo of the ACPL GUI lib.
```
$use: GUI
var window = lib GUI create window size=400x500 title=ACPL GUI lib demo ! icon=ACPL_Icon.ico
var my_text = lib GUI create text window 0 0 Top-left text. --align:top-left --background:green --color:white
var my_text = lib GUI create text window 0 1 Top-right text. --align:top-right --background:yellow --color:grey60
var my_text = lib GUI create text window 1 0 Bottom-left text. --align:bottom-left --background:OliveDrab2 --color:wheat1
var my_text = lib GUI create text window 1 1 Bottom-right text. --align:bottom-right --background:DodgerBlue2 --color:chartreuse2
lib GUI display window
```

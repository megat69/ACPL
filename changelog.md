### 3.8
- Lists
Biggest feature of this update, lists allow to store multiple variables in a single one.
If you use C, it's some sort of dynamically changing array.

**How to declare a list :**
Type like the following ;
```
var:list <name> = list [ELEMENT 0] [ELEMENT 1] [ELEMENT 2]
```
Every element of the list has to be between brackets when you initialize it.
Also, in the example, I created a list containing only 3 elements ; but a list can contain as many as you want.

**How to add an element at the end of a list :**
Type like the following : 
```
var:list <name> = list.add <content>
```
The <content> will be appended at the end of the list.

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

- New setup
  - The new setup will install correctly the requirements, and will also ask you to set your settings.
  - Settings include : 
    - Language
    - Color use
    - File opening at compiling
    - Comments left at compiling

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

Overall, a pretty big update.
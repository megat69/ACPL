## Files ACPL lib 

### Overview
The files lib lets you read and write in files using ACPL.

Full documentation in the *Usage* section.

### Install 
Go on your ACPL console and type `lib install files`.

### Usage
#### Reading from files
To read from a file, you need to use the `read` instruction.

Syntax : `lib files read <file> <return_var> [optional parameters]`

- The `file` argument corresponds to the file you want to read from.
- The `return_var` argument corresponds to the NAME of the variable that will take the value of the text contained in the file.
  - The returned value is a list of strings.
- The optional parameters :
  - `--remove_newlines` : If used, all the `\n` at the end of each list element will be removed.
    
#### Writing in a file
To write in a file, you need to use the `write` instruction.

Syntax : `lib files write <file> <var_from> [optional parameters]`

- The `file` argument corresponds to the file you want to write into.
- The `var_from` argument corresponds to the NAME of the variable that contains the text you want to write.
  - This variable can be :
    - A string ; in that case, only one line will be written into the file.
    - A list ; in that case, each element of the list ending with `\n` will be written into the file.
- The optional parameters :
  - `--write_mode:a` : If this parameter is used, the text will be appended at the end of the file, instead of replacing the old one.
    
### Example
```
$use: files
# Importing the lib

lib files read file_to_read.txt old_text
# It just reads the text in the file 'file_to_read.txt'
# and stores it in the variable 'old_text'.

print Old text in file_to_read.txt : {old_text}
# Prints the old text in file_to_read

var:str text_to_paste = It just works.
# Creates a string variable
lib files write file_to_read.txt text_to_paste
# Replaces the old text in 'file_to_read.txt' with the
# content of 'text_to_paste'.
```
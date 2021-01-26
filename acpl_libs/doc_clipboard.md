## Clipboard ACPL lib
This lib allows you to copy a string to the clipboard, or to get what is in the clipboard at the moment.

### Install
Go on your ACPL console and type `lib install clipboard`.

### Usage
#### Copy
To copy a string to the clipboard, use the function `lib clipboard copy <value>`

#### Get
To get the content of the clipboard, use the function `lib clipboard get <return_var>` where `<return_var>` is a variable name. This variable will take the value of the clipboard content.

Also available as var method :
- Syntax : `var <name> = lib clipboard get`
- After this line, you can change type if wanted :
  - Syntax : `<name>:<type> = {<name>}`
    
### Example
```
$use: clipboard
var:str string_to_copy = input Input a string to copy to the clipboard : 
lib clipboard copy {string_to_copy}
var:str return_var = lib clipboard get
print {return_var}
```

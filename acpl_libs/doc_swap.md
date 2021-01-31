## Swap ACPL lib

### Overview
This lib lets you swap two variable's values with just one line.

### Install 
Go on your ACPL console and type `lib install swap`.

### Usage
Syntax : `lib swap <var1> <var2>`

### Example
```
$use: swap
var:int var1 = 0
var:int var2 = 1

print {var1}, {var2}
lib swap var1 var2
print {var1}, {var2}
```

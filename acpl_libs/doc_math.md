## Math ACPL lib 

### Install 
Go on your ACPL console and type `lib install math`.

### Usage
The `math` library gives access to four functions. 
All of them follow the syntax `lib math <function> <return_variable> <value>`.
`return_variable` corresponds to the variable that will get the value returned by the function.
`value` is the value that will be given to the function.
`function` is one of the following :
- `sqrt` : Returns the square root of the given value.
  - If the value is negative, the function will return an error and stop the code execution.
- `fabs` : Returns the absolute value of the given value.
- `factorial` : Returns the factorial of the given value.
  - If the value is negative, the function will return an error and stop the code execution.
- `floor` : Returns the integer part of the given value.

### Example :
```
$use: math
var:int number = 9
lib math sqrt number {number}
print The square root of the number is {number}.
```
Will print '3.0'.

## ACPL lib 'Wait_until_user_input'
Waits until user presses 'Enter'

### Install
Go on your ACPL console and type `lib install wait_until_user_input`.

### Usage
Type `lib wait_until_user_input [method:bool/string]`
If `method` is not defined or equals `False`, it will wait for the user to press 'Enter'.
If `method` equals `True`, it will display "Press enter to continue..." and wait for the user to press 'Enter'.
If `method` is a string, it will display that string and wait for the user to press 'Enter'.

### Example
```
lib wait_until_user_input true
```

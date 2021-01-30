# SystemVerilog Interface Checker for Python
### NOTICE
This tool currently does not meet requirements. The parsing is way too strict,
with things like slight whitespace variations causing a false negative. More
work needs to be done in the future.

A handy Python module that can compare two SV files, and ensure that the module
interfaces match. Particularly good for making sure one doesn't make the mistake
of mixing up `logic [1:0]` with `logic`, and the like.

The main meat of this module is done with the existing Hdlparse library by Kevin
Thibedeau, the repo of which can be found [here](https://github.com/kevinpt/hdlparse).

Do note that the Hdlparse library here is slightly modified, with the following
summary of changes:
- Modifications made to port the library to Python3, as Python2 is now
  deprecated
- Changed the Verilog lexer to work properly with SystemVerilog constructs
- Removed the VHDL lexer, as who even uses VHDL nowadays anyway?

## Requirements
- Python 3.X

## Usage
Clone this repo into the directory that contains the Python file that needs it,
and import in the Python file:
```python
import svinterface
```

The main function to use is the `checkInterface` function. Arguments are:
```
checkInterface(refFile, testFile, specificModules=None)
    refFile (str):          Path to the reference .sv file. This file should
                            contain the *correct* module interfaces.
    testFile (str):         Path to the .sv file to test. The modules in here
                            will be compared to those in the reference file.
    specificModule ([str]): List of what specific modules (strings) you'd like
                            to check. If left unspecified then the function will
                            check all modules.
```
This function will return an empty string if there are no errors, otherwise it
will return some error message.

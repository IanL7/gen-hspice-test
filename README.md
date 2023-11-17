# gen_hspice_test

A simple python script to generate hspice test contents for a logic
function with provided inputs. The test contents generated will 
exhaustively test the logic function (all cases of the truth table).

# Running

Run `python3 ght.py' followed by a set of arguments.
- The first argument is the DUT name
- Any argument after the DUT name will be treated as
  input names (inputs to the DUT)

## Example 

`python3 ght.py adder a b > test.sp`
- This will output the test contents to a file named test.sp
- DUT name will be "adder"
- Inputs will be "a", "b"

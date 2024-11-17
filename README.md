# CSV Unit Tester
## Description

The **CSV Unit Tester** simplifies and accelerates the process of validating Python functions by using structured test cases. With support for multiple assertion types and dynamic module imports, it helps detect discrepancies in outputs and exceptions effectively, providing detailed feedback. This tool simplifies the creation and execution of unit tests, provides quick and easy testing of Python function 

## Getting Started

### Dependencies

* Python 3.7 or higher
* termcolor == 2.3 0
* OS: Windows 10 / macOS / Linux

### Installing

1. Clone the repository:
   ```bash
   git clone https://github.com/i-HamidZafar/csv-unit-tester.git
   cd csv-unit-tester
   ```
2. Ensure Python is installed and accessible via the command line.

### Executing Program

1. Prepare your test cases in a CSV file (e.g., `test_cases.csv`) with the format:
   ```csv
   fun_call,expected_output
   `add(|2|,|3|)`, 5
   `divide(|4|,|0|)\`, `}ZeroDivisionError{`
   ```
2. Create or specify the Python file to test (e.g., `module_to_test.py`).
3. Run the tester:
   ```bash
   python project.py module_to_test.py test_cases.csv
   ```
4. View results in the terminal.

## Usage Guide
Rules for preparing the test_cases.csv file:

* first line of file(exact): `fun_call,expected_result` (File Header)
* fun_call and expected output should be enclosed with backtick ( ` ) symbol unless the expected_output is a numeric value then you can type it exact and seperated by , .
* Writing fun_call in test_cases.csv:<br>
  _Rules for specifying datatypes:_
  ```csv
  Strings  (enclosed in { e.g {str{   ).
  Integers (enclosed in | e.g |int|   ).
  Floats   (enclosed in } e.g }float} ).
  ```
  fun_call example: "test("hi", 2, 11.22)" :
  ```bash
  `test({"hi"{, |2|, }11.22})`
  ```
* Writing expected_output in test_cases.csv:<br>
  _Assertion Modes:_
  ```bash
  Equality ( equal assertion test e.g: `check(|2|)`, 2 ).
  Inequality ( not equal assertion test e.g: `check(|2|)`,`]2[` ).
  Greater Than ( greater than assertion test e.g: `check(|2|)`, `>2>` ).
  Less Than ( greater than assertion test e.g: `check(|2|)`, `<2<` ).
  Greater Than or Equal To ( greater than or equal to assertion test e.g: `check(|2|)`, `\>2|` ).
  Less Than or Equal To ( greater than or equal to assertion test e.g: `check(|2|)`, `<2|` ).
  Exception Raising (Exception raise type assertion e.g: `divide( }2.02},|0| )`, `}ZeroDivisionError{` ).
  ```
NOTE: Giving Exception name surrounded like <exception| or >exception| symbols is considered a passed test if function call  raises the given exception. 

### Common Issues

* File Header not correct.
* Not enclosing the fun_call and expected_output with ` (backtick) symbol.
* Ensure the function names in the CSV match those in the module and provided module file name is correct.
* Verify the correct delimiters (`|`, `{`, `}` e.t.c) for arguments datatypes and assertion types.
* Check the Python version and install missing dependencies if needed.

### EXAMPLE 
* **test_cases.csv:** <br>
  ![image](https://github.com/user-attachments/assets/61661862-801a-4f53-be3c-8db1f52cce8f)


* **test.py:** <br>
![image](https://github.com/user-attachments/assets/cf3646a2-1752-40fb-ba3c-094f63951b91)

* **OUTPUT:**<br>
![image](https://github.com/user-attachments/assets/92b58dcc-cf14-4e21-9d2f-e1861111c567)






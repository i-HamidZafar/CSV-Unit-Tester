import sys
import csv, re
from termcolor import colored

def check_args():
    if len(sys.argv) != 3: 
        print(colored(":| usage: python tester.py <test_module.py> <test_cases.csv>", "red"))
        sys.exit(1)
    elif not sys.argv[1].endswith(".py"):
        print(colored(":| Not a Python file", "red"))
        sys.exit(1)
    filename = sys.argv[2]
    return filename

def execute_file_tests(file_name): 
    
    tests_module = import_module()
    file_ext = sys.argv[2][-4:]

    if file_ext != ".csv":
        sys.exit(print(colored(":| not a .csv file", "red")))

    try:
        with open(file_name) as test_cases_file:
            print(colored(f":) {file_name} File Found", "cyan"))
            reader = csv.DictReader(test_cases_file,delimiter=',', quotechar="`")
            
            for row in reader:
                fun_call = row["fun_call"].strip()
                expected_result = row["expected_result"].strip()
                run_test(fun_call, expected_result, tests_module)

    except FileNotFoundError:
        print( colored(f":| {file_name} File Not Found", "red") )
        sys.exit(1)


def import_module(module_name = sys.argv[1][:-3]): 
    try:
        module=  __import__(module_name)
        print (colored(f":) {module} Module Found", "cyan"))
        return module
    except ModuleNotFoundError:
        sys.exit( print(colored(":| Module not found", "red")) )

def run_test( fun_call, expected_output, module ):
    
    assert_flag = 1
    try:
        fun_name = get_fun_name(fun_call)
        is_exception, expected_output, assert_flag = check_assertion(expected_output)
        
        

        fun_reference = get_fun_reference(fun_name, module)

        args= get_fun_args(fun_call)
        test_args = get_parsed_args(args)

        test_output = str(fun_reference(*test_args))

        if assert_flag != 1:
            test_status = get_test_status(test_output, expected_output, fun_call, assert_mode= assert_flag)
        else:
            test_status = get_test_status(test_output, expected_output, fun_call)

        print(test_status)

    except Exception as  e:
        handle_expection(e, fun_call, expected_output, assert_flag, fun_name, is_exception)
        


def check_assertion(expected_output):
    assert_flag = 1
    is_exception = True if expected_output[0] == "}" and expected_output[-1] == "{" else False

    if is_exception:
        expected_output = expected_output[1:-1]
        return is_exception, expected_output, assert_flag
    elif expected_output[0] == "]" and expected_output[-1] == "[": #not equal assertion
        assert_flag = 0
    elif expected_output[0] == ">" and expected_output[-1] == ">": # greater than assertion
        assert_flag = 2
    elif expected_output[0] == "<" and expected_output[-1] == "<": # less than assertion
        assert_flag = -2
    elif expected_output[0] == ">" and expected_output[-1] == "|": # greater than equal  assertion
        assert_flag = 3
    elif expected_output[0] == "<" and expected_output[-1] == "|": # less than equal assertion
        assert_flag = -1         

    if assert_flag != 1: expected_output = expected_output[1:-1]
    return is_exception, expected_output, assert_flag

def get_fun_name(fun_call):
    if fun_call.find("(") != -1 and fun_call[-1] == ')':
        return fun_call[0:fun_call.find("(")]
    else:
        raise Exception("CHECK YOUR FUNCTION CALL FORMAT")


def get_fun_reference(name, module):
    return getattr(module, name )


def get_fun_args(signature):
    return signature[ signature.find( "(" ) + 1 : -1]    


def test(fun_reference, args):
    args = get_parsed_args(args)
    return fun_reference(*args)

def get_parsed_args(args):
    args_list = []

    i = 0
    while i < len(args): 

        #string type argument
        if args[i] == '{':
            i = append_arg(args_list, i, "{", args)

        #integer type argument
        elif args[i] == '|':
            
            i = append_arg(args_list, i, "|", args)
        #float type argument
        elif args[i] == '}':
            i = append_arg(args_list, i, "}", args)
        else:
            i += 1
    return args_list


def append_arg(args, i, arg_type, arguments):
    start = i + 1  

    arg = ""
    rest_string= arguments[start: ]
    if arg_type == "{":
        if rest_string.find("{") != -1:
            arg = rest_string[ : rest_string.find('{')]
            args.append(arg.strip(f"\""))

        else:
            raise Exception("CHECK YOUR FUNCTION CALL DATA TYPE FORMATTING")
    elif arg_type == "|":
        if rest_string.find("|") != -1:
            arg = rest_string[ : rest_string.find('|')]
            args.append( int(arg.strip("|")) )

        else:
            raise Exception("CHECK YOUR FUNCTION CALL DATA TYPE FORMATTING")
    elif arg_type == "}":
        if rest_string.find("}") != -1:
            arg = rest_string[ : rest_string.find('}')]
            args.append( float(arg.strip("}")) )

        else:
            raise Exception("CHECK YOUR FUNCTION CALL DATA TYPE FORMATTING")

    arg_len = len(arg)

    end = start + arg_len + 1
    i = end + 1

    return i #index to continue from


def get_test_status(output, expected_output, fun_call, assert_mode=1):
    if assert_mode == 1:
        if output == expected_output:
            test_status = (colored(f":) {fun_call} == {expected_output} |Passed|", "green"))

        else:
            test_status = colored(f":( {fun_call} == {expected_output} |Failed| [TEST_OUTPUT]-> {output}", "red")
        
    elif assert_mode == 0:
        if output != expected_output:
            test_status = colored(f":) {fun_call} != {expected_output} |Passed|", "green")
        else:
            test_status = colored(f":( {fun_call} != {expected_output} |Failed| [TEST_OUTPUT]-> {output}", "red")
        
    elif assert_mode == 2:
        if output > expected_output:
            test_status = colored(f":) {fun_call} > {expected_output} |Passed|", "green")
        else:
            test_status = colored(f":( {fun_call} > {expected_output} |Failed| [TEST_OUTPUT]-> {output}", "red")

    elif assert_mode == -1:
        if output <= expected_output:
            test_status = colored(f":) {fun_call} <= {expected_output} |Passed|", "green")
        else:
            test_status = colored(f":( {fun_call} <= {expected_output} |Failed| [TEST_OUTPUT]-> {output}", "red")

    elif assert_mode == -2:
        if output < expected_output:
            test_status = colored(f":) {fun_call} < {expected_output} |Passed|", "green")
        else:
            test_status = colored(f":( {fun_call} < {expected_output} |Failed| [TEST_OUTPUT]-> {output}", "red")

    elif assert_mode == 3:
        if output >= expected_output:
                test_status = colored(f":) {fun_call} >= {expected_output} |Passed|", "green")
        else:
            test_status = colored(f":( {fun_call} >= {expected_output} |Failed| [TEST_OUTPUT]-> {output}", "red")
    
    return test_status
        


def handle_expection(e, fun_call, expected_output, assert_flag, fun_name, is_exception):
    condition = expected_output == e.__class__.__name__ and assert_flag == 1 and is_exception
    if condition:
            test_status = colored(f":) {fun_call} raises {expected_output} |Passed|", "green")

    elif e.__class__.__name__ == "AttributeError" :    
        fun_not_found_msg = colored(f"|{fun_name} function not found in {sys.argv[1]}|", "red")
        condition_msg = f"{fun_call} != {expected_output}"
        status = "|Failed|"
        output = "[TEST_OUTPUT]->" + " " + fun_not_found_msg
        test_status = colored(f":( {condition_msg} {status} {output}", "red")

    elif (assert_flag == 0 ): 
        if str(e.__class__.__name__) != expected_output:
            test_status = colored(f":) {fun_call} != {expected_output} |Passed| [TEST_OUTPUT]-> raises |{e.__class__.__name__}| -> {str(e)}", "green")
        else:
            test_status = colored(f":( {fun_call} != {expected_output} |Failed| [TEST_OUTPUT]-> raises |{e.__class__.__name__}| -> {str(e)}", "red")

    elif assert_flag == 2:
        test_status = colored(f":( {fun_call} > {expected_output} |Failed| [TEST_OUTPUT]-> raises |{e.__class__.__name__}| -> {str(e)}", "red")

    elif assert_flag == -2 and expected_output == str(e):
        test_status = colored(f":( {fun_call} < {expected_output} |Failed| [TEST_OUTPUT]-> raises |{e.__class__.__name__}| -> {str(e)}", "red")

    elif assert_flag == 3 or assert_flag == -1:
        if expected_output == str(e.__class__.__name__) :
            test_status = colored(f":( {fun_call} >= {expected_output} |Passed| [TEST_OUTPUT]-> raises |{e.__class__.__name__}| -> {str(e)}", "green")

        else:
            test_status = colored(f":) {fun_call} >= {expected_output} |Failed| [TEST_OUTPUT]-> raises |{e.__class__.__name__}| -> {str(e)}", "red")

    else:
        test_status = colored(f":( {fun_call} == {expected_output} |Failed| [TEST_OUTPUT]-> raises |{e.__class__.__name__}| -> {str(e)}", "red")

    print (test_status)



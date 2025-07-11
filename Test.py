import ast
import textwrap
from Extract import func_extraction, class_extraction, full_extraction


class_func = """
        class User1:
            def one():
                pass
        class User2:
            def two():
                pass
        class User3:
            def three():
                pass
        class User4:
            def four():
                pass
        class User5:
            def five():
                pass
        class User6:
            def six():
                pass
    """
    
    
def test_class():
    code_class = textwrap.dedent(class_func)
    extract = ast.parse(code_class)
    result = class_extraction(extract)
    
    assert "ClassDef: User1" in result
    assert "ClassDef: User2" in result
    assert "ClassDef: User3" in result    
    assert "ClassDef: User4" in result
    assert "ClassDef: User5" in result
    assert "ClassDef: User6" in result
    
    
# Test functions
def test_func():
    code_func = textwrap.dedent(class_func)
    extract = ast.parse(code_func)
    result = func_extraction(extract)
    
    assert "FunctionDef: one" in result
    assert "FunctionDef: two" in result
    assert "FunctionDef: three" in result
    assert "FunctionDef: four" in result
    assert "FunctionDef: five" in result
    assert "FunctionDef: six" in result


# Test arguments
def test_args():
    code_arg = textwrap.dedent('''
def calculate(x, y, op="+"):
    return x + y if op == "+" else x - y
'''
)
    extract = ast.parse(code_arg)
    result = func_extraction(extract)
    
    assert "Arg: x" in result
    assert "Arg: y" in result
    assert "Arg: op" in result
    
    
def test_returns():
    code_returns = textwrap.dedent('''
def give_number():
    return 42

def is_ready():
    return True

def make_string(name):
    return f"Hi, {name}"

def get_nothing():
    return None
''')
    extract = ast.parse(code_returns)
    result = func_extraction(extract)
    
    assert "Return: Constant" in result
    assert "Return: Constant" in result
    assert "Return: JoinedStr" in result
    assert "Return: Constant" in result
    
    
# Test everything using todo.py
def test_full():
    with open("todo.py", "r") as f:
        code = f.read()
    extract = ast.parse(code)
    result = full_extraction(extract)
    
    # Class names
    assert "ClassDef: Task" in result
    assert "ClassDef: TodoList" in result
    
    # Function names
    assert "FunctionDef: __init__" in result
    assert "FunctionDef: mark_done" in result
    assert "FunctionDef: __str__" in result
    assert "FunctionDef: add_task" in result
    assert "FunctionDef: remove_task" in result
    assert "FunctionDef: list_tasks" in result
    assert "FunctionDef: is_empty" in result
    assert "FunctionDef: get_pending_tasks" in result
    assert "FunctionDef: load_tasks_from_dicts" in result
    assert "FunctionDef: main" in result

    # Args
    assert "Arg: self" in result
    assert "Arg: title" in result
    assert "Arg: priority" in result
    assert "Arg: tasks" in result or "Arg: *tasks" in result
    assert "Arg: index" in result
    assert "Arg: show_all" in result
    assert "Arg: task_data" in result

    # Return types
    assert "Return: Constant" in result or "Return: Name" in result
    assert any("Return:" in line for line in result) 
    
    
    
test_class()
test_func()
test_args()
test_returns()
test_full()
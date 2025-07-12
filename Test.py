import ast
import textwrap
import unittest
from Extract import func_extraction, class_extraction, full_extraction

# Currently, UT prints out prompt.

class_func = """
        class User1:
            def one():
                pass
        class User2:
            def two():
                pass
        class User3:
            # test ne
            def three():
            # test ne
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

# In ra prompt
def print_prompt(prompt):
    for j in prompt:
        print(j)
    print("--------------------------------------------------")

# In ra result
def print_result(result):
    count = 0
    for i in result:
        print(f"{count}. {i}")
        count += 1
    print()
    print("--------------------------------------------------")
    
# Test classes
class TestExampleCode(unittest.TestCase):
    # Test classes
    def test_class(self):
        code_class = textwrap.dedent(class_func)
        extract = ast.parse(code_class)
        prompt = []
        result, _, prompt = class_extraction(extract, 0, 0, prompt)
        
        self.assertIn("ClassDef: User1", result)
        self.assertIn("ClassDef: User2", result)
        self.assertIn("ClassDef: User3", result)    
        self.assertIn("ClassDef: User4", result)
        self.assertIn("ClassDef: User5", result)
        self.assertIn("ClassDef: User6", result)
        
        print_prompt(prompt)
        # print_result(result)
    
    
    # Test functions
    def test_func(self):
        code_func = textwrap.dedent(class_func)
        extract = ast.parse(code_func)
        prompt = []
        result, _, prompt = func_extraction(extract, 0, 0, prompt)
        
        self.assertIn("def one():", result)
        self.assertIn("def two():", result)
        self.assertIn("def three():", result)
        self.assertIn("def four():", result)
        self.assertIn("def five():", result)
        self.assertIn("def six():", result)
        
        print_prompt(prompt)
        # print_result(result)
    
    
    # Test returns
    def test_returns(self):
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
        prompt = []
        result, _, prompt = func_extraction(extract, 0, 0, prompt)
        
        self.assertIn("return: Constant", result)
        self.assertIn("return: Constant", result)
        self.assertIn("return: JoinedStr", result)
        self.assertIn("return: Constant", result)

        print_prompt(prompt)
        # print_result(result)
        
class TestTodoExtraction(unittest.TestCase):  
    # Test full source code
    def test_full(self):
        result, prompt = full_extraction("todo.py")

        # Class names
        self.assertIn("ClassDef: Task", result)
        self.assertIn("ClassDef: TodoList", result)

        # Function names
        self.assertIn("def __init__(self, title, priority):", result)
        self.assertIn("def mark_done(self):", result)
        self.assertIn("def __str__(self):", result)
        self.assertIn("def __init__(self):", result)
        self.assertIn("def add_task(self, *tasks):", result)
        self.assertIn("def remove_task(self, index):", result)
        self.assertIn("def list_tasks(self, show_all):", result)
        self.assertIn("def is_empty(self):", result)
        self.assertIn("def get_pending_tasks(self):", result)
        self.assertIn("def load_tasks_from_dicts(self, task_data):", result)
        self.assertIn("def main():", result)

        # Return types
        self.assertTrue(
            "return: Constant" in result or "return: Name" in result
        )
        self.assertTrue(
            any("return:" in line for line in result)
        )
        
        print_prompt(prompt)
        # print_result(result)  
    
    
    
if __name__ == '__main__':
    unittest.main()
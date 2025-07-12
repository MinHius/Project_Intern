import ast
import unittest
from Extract import func_extraction, class_extraction, full_extraction

# Currently, UT prints out prompt.
with open("todo.py", "r") as f:
    code = f.read()
extract = ast.parse(code)

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
    print("--------------------------------------------------")
    
# Test individual units, no format
class TestExtracted_1_Units(unittest.TestCase):
    # Test classes
    def test_class(self):
        prompt = []
        result, _, prompt = class_extraction(extract, 0, 0, prompt)
        
        self.assertIn("ClassDef: TaskInterface", result)
        self.assertIn("ClassDef: Task", result)
        self.assertIn("ClassDef: TodoList", result)    
        
        print(" Classes - no format")
        print("--------------------------------------------------")
        # print_prompt(prompt)
        print_result(result)
    
    
    # Test functions + comments + returns
    def test_func(self):
        prompt = []
        result, _, prompt = func_extraction(extract, 0, 0, prompt)
        
        self.assertIn("def main():", result)
        self.assertIn("def mark_done(self):", result)
        self.assertIn("def __str__(self):", result)
        self.assertIn("def __init__(self, title, priority):", result)
        self.assertIn("def mark_done(self):", result)
        self.assertIn("def __init__(self):", result)
        self.assertIn("def add_task(self, *tasks):", result)
        self.assertIn("def remove_task(self, index):", result)
        self.assertIn("def list_tasks(self, show_all):", result)
        self.assertIn("def is_empty(self):", result)
        self.assertIn("def get_pending_tasks(self):", result)
        self.assertIn("def load_tasks_from_dicts(self, task_data):", result)
    
        # Test returns
        self.assertIn("return: Constant", result)
        self.assertIn("return: Name", result)
        self.assertIn("return: JoinedStr", result)
        self.assertIn("return: Compare", result)
        self.assertIn("return: ListComp", result)

        print(" Functions, returns and comments - no formats")
        print("--------------------------------------------------")
        # print_prompt(prompt)
        print_result(result)

# Test full extraction, no format
class TestExtracted_2_Full(unittest.TestCase):  
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
        
        print(" Full signatures - no formats")
        print("--------------------------------------------------")
        # print_prompt(prompt)
        print_result(result)  
    
# ==============================================================

# Test individual units, with prompt format
class TestPrompt_3_Units(unittest.TestCase):
    # Test classes
    def test_class(self):
        expected_output = ['0|ClassDef: TaskInterface', '1|ClassDef: Task', '2|ClassDef: TodoList']
        prompt = []
        result, _, prompt = class_extraction(extract, 0, 0, prompt)
        
        # Check full output - strict
        self.assertEqual(expected_output, prompt)
        
        print(" Classes - formatted")
        print("--------------------------------------------------")
        print_prompt(prompt)
        # print_result(result)
        

    # Test functions + comments + returns
    def test_func_return_cmt(self):
        expected_output = ['0|# Simple test run', '1|def main():', '2|', '3|# Mark this task as completed', '4|def mark_done(self):', '5|', '6|# Return a user-friendly string representation'
                           , '7|def __str__(self):', '8|', '9|# Create a new task with a title and priority (1=high, 5=low)', '10|def __init__(self, title, priority):', '11|', '12|# Mark this task as completed'
                           , '13|def mark_done(self):', '14|   return: Constant', '15|', '16|# Return a user-friendly string representation', '17|def __str__(self):', '18|   return: JoinedStr'
                           , '19|', '20|# Initialize an empty todo list', '21|def __init__(self):', '22|', '23|# Add one or more tasks', '24|def add_task(self, *tasks):'
                           , '25|', '26|# Remove a task by index', '27|def remove_task(self, index):', '28|   return: Name', '29|   return: Constant', '30|', '31|# List tasks, optionally filtering completed ones'
                           , '32|def list_tasks(self, show_all):', '33|', '34|# Return True if no tasks are stored', '35|def is_empty(self):', '36|   return: Compare', '37|'
                           , '38|# Return a list of incomplete tasks', '39|def get_pending_tasks(self):', '40|   return: ListComp', '41|', '42|# Create and load tasks from a list of dicts', '43|def load_tasks_from_dicts(self, task_data):'
                           ]
        prompt = []
        result, _, prompt = func_extraction(extract, 0, 0, prompt)
        
        self.assertEqual(expected_output, prompt)
        
        print(" Functions, returns and comments - formatted")
        print("--------------------------------------------------")
        print_prompt(prompt)
        # print_result(result)
    
# Test full extraction, with prompt format
class TestPrompt_4_Full(unittest.TestCase):
    # Test full source code
    def test_full(self):
        result, prompt = full_extraction("todo.py")
        expected_output = ['0|from abc import ABC', '1|from abc import abstractmethod', '2|', '3|ClassDef: TaskInterface', '4|   # Mark this task as completed', '5|   def mark_done(self):'
                           , '6|', '7|   # Return a user-friendly string representation', '8|   def __str__(self):', '9|', '10|ClassDef: Task', '11|   # Create a new task with a title and priority (1=high, 5=low)'
                           , '12|   def __init__(self, title, priority):', '13|', '14|   # Mark this task as completed', '15|   def mark_done(self):', '16|      return: Constant', '17|'
                           , '18|   # Return a user-friendly string representation', '19|   def __str__(self):', '20|      return: JoinedStr', '21|', '22|ClassDef: TodoList'
                           , '23|   # Initialize an empty todo list', '24|   def __init__(self):', '25|', '26|   # Add one or more tasks', '27|   def add_task(self, *tasks):', '28|'
                           , '29|   # Remove a task by index', '30|   def remove_task(self, index):', '31|      return: Name', '32|      return: Constant', '33|'
                           , '34|   # List tasks, optionally filtering completed ones', '35|   def list_tasks(self, show_all):', '36|', '37|   # Return True if no tasks are stored'
                           , '38|   def is_empty(self):', '39|      return: Compare', '40|', '41|   # Return a list of incomplete tasks', '42|   def get_pending_tasks(self):'
                           , '43|      return: ListComp', '44|', '45|   # Create and load tasks from a list of dicts', '46|   def load_tasks_from_dicts(self, task_data):', '47|'
                           , '48|# Simple test run', '49|def main():'
                           ]

        
        self.assertEqual(expected_output, prompt)

        print(" Full signatures - formatted")
        print("--------------------------------------------------")
        print_prompt(prompt)
        # print_result(result)  
        
        
if __name__ == '__main__':
    unittest.main()
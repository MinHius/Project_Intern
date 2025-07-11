import ast

# Read .py test file
with open("todo.py", "r") as f:
    code = f.read()

# Extract classes and functions using ast
extract = ast.parse(code)

#Print classes and functions
for node in ast.walk(extract):
    if isinstance(node, (ast.ClassDef)):
        print()
        print(type(node).__name__, node.name)
    
    
    if isinstance(node, (ast.FunctionDef)):
        print()
        print(type(node).__name__, node.name)
        # Arguments
        for arg in node.args.args:
            print(f"  Arg: {arg.arg}")
        
        for return_ in ast.walk(node):
            if isinstance(return_, ast.Return):
                print("Returns:", type(return_.value).__name__)
            

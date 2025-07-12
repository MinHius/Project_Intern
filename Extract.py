import ast

# result: Parse list with no format for UT and outputs.
# prompt: Parse list containing formats for API prompt.

# Extract many types of arguments
def get_func_signature(node: ast.FunctionDef):
    args = []
    for arg in node.args.args:
        args.append(arg.arg)

    # *args
    if node.args.vararg:
        args.append(f"*{node.args.vararg.arg}")

    # **kwargs
    if node.args.kwarg:
        args.append(f"**{node.args.kwarg.arg}")

    return f"def {node.name}({', '.join(args)}):"

# Extract classes only
def class_extraction(extract, count, level, prompt):
    result = []
    indent = '   ' * level
    # Print classes
    for node in ast.walk(extract):
        if isinstance(node, (ast.ClassDef)):
            doc = ast.get_docstring(node)
            if doc:
                result.append(f"# {doc}")
                prompt.append(f"{count}|{indent}#  {doc}")
                count += 1
            else:    
                result.append(type(node).__name__ + ': ' + node.name)
                prompt.append(f"{count}|{indent}{type(node).__name__}: {node.name}")
                count += 1
    return result, count, prompt
            
# Extract functions with arguments and return value.
def func_extraction(extract, count, level, prompt):
    result = []
    indent = '   ' * level
    for i, node in enumerate(ast.walk(extract)):
        # Print functions
        if isinstance(node, (ast.FunctionDef)):
            if result:
                prompt.append(f"{count}|")
                count += 1
                
            doc = ast.get_docstring(node)
            if doc:
                result.append(f"# {doc}")
                prompt.append(f"{count}|{indent}# " + doc)
                count += 1
                
            
            args = [arg.arg for arg in node.args.args]
            func_line = get_func_signature(node)
            result.append(str(func_line))
            prompt.append(f"{str(count)}|{indent}{func_line}")
            count += 1
            
            
            # Print return values
            for return_ in ast.walk(node):
                if isinstance(return_, ast.Return):
                   result.append(f"return: {type(return_.value).__name__}")
                   prompt.append(f"{count}|{'   ' * (level + 1)}return: {type(return_.value).__name__}")
                   count += 1
  
    return result, count, prompt
        

def full_extraction(extract):
    count = 0
    level = 0
    indent = '   ' * level
    result = []
    prompt = []
    end_imports = True
    
    with open("todo.py", "r") as f:
        code = f.read()
    extract = ast.parse(code)
    
    for node in ast.walk(extract):
        # Extract imports
        if isinstance(node, ast.Import):
            for alias in node.names:
                result.append(f"import {alias.name}")
                prompt.append(f"{str(count)}|{indent}import {alias.name}")
                count += 1
                end_imports = False
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                result.append(f"from {module} import {alias.name}")
                prompt.append(f"{str(count)}|{indent}from {module} import {alias.name}")
                count += 1
                end_imports = False
        else:
            if end_imports == False:
                prompt.append(f"{count}|")
                count += 1
                end_imports = True
                
                
        if isinstance(node, (ast.ClassDef)):
            # Extract class
            x, count, prompt = class_extraction(node, count, level, prompt)
            result = result + x
        
            # Extract functions within classes if exist
            x, count, prompt = func_extraction(node, count, level + 1, prompt)
            result = result + x
            prompt.append(f"{count}|")
            count += 1

    # Top-level functions 
    for i, node in enumerate(extract.body):
        if isinstance(node, ast.FunctionDef):
            x, y, prompt = func_extraction(node, count, level, prompt)
            result += x
            count = y
            if i < len(extract.body) - 1:
                prompt.append(f"{count}|")
                count += 1
                
            
        
    return result, prompt

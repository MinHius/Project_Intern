import ast

# Extract classes only
def class_extraction(extract):
    result = []
    # Print classes
    for node in ast.walk(extract):
        if isinstance(node, (ast.ClassDef)):
            result.append(type(node).__name__ + ': ' + node.name)
    return result
            
# Extract functions with arguments and return value.
def func_extraction(extract):
    result = []
    for node in ast.walk(extract):
        # Print functions
        if isinstance(node, (ast.FunctionDef)):
            result.append(type(node).__name__ + ': ' + node.name)
            
            # Print arguments (variables)
            for arg in node.args.args:
                result.append(f"Arg: {arg.arg}")
            
            # Print return values
            for return_ in ast.walk(node):
                if isinstance(return_, ast.Return):
                    result.append(f"Return: {type(return_.value).__name__}")
            
    return result
        

def full_extraction(extract):
    result = []
    # Print classes
    for node in ast.walk(extract):
        if isinstance(node, (ast.ClassDef)):
            result.append(type(node).__name__ + ': ' + node.name)
        
        # Print functions
        if isinstance(node, (ast.FunctionDef)):
            result.append(type(node).__name__ + ': ' + node.name)
            
            # Print arguments (variables)
            for arg in node.args.args:
                for arg in node.args.args:
                    result.append(f"Arg: {arg.arg}")          # → normal args like 'self', 'title', 'priority'

                if node.args.vararg:
                    result.append(f"Arg: *{node.args.vararg.arg}")  # → special *args like '*tasks'
            
            # Print return values
            for return_ in ast.walk(node):
                if isinstance(return_, ast.Return):
                   result.append(f"Return: {type(return_.value).__name__}")
                   
    return result

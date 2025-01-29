import ast
import os
import subprocess
from analyzer import analyzer, parse  # Import necessary components from analyzer.py

def analyze_file(file_path):
    """Analyze a Python file for errors."""
    with open(file_path, 'r') as file:
        code = file.read()

    # Syntax Analysis
    try:
        ast.parse(code)
    except SyntaxError as e:
        print(f"Syntax Error on line {e.lineno}: {e.msg}")
        suggest_fix("syntax", e.msg, e.lineno)

    # Static Analysis
    print("\nRunning mypy for type checks...")
    result = os.path.isfile(file_path)
    result = subprocess.run(["mypy", file_path], capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout.strip())
        parse_mypy_errors(result.stdout.strip())

    # Token Analysis
    print("\nRunning token analysis...")
    try:
        tokens = parse(file_path)
        if tokens:
            print("Token analysis results:")
            for token in tokens:
                print(token)
        else:
            print("No tokens found.")
    except Exception as e:
        print(f"Token analysis failed: {str(e)}")

def suggest_fix(error_type, message, line_no):
    """Suggest fixes for common errors."""
    suggestions = {
        "syntax": "Check for mismatched parentheses, colons, or improper indentation.",
        "name": "Ensure all variables or functions used are defined.",
        "type": "Verify type annotations and use appropriate types for variables.",
    }
    suggestion = suggestions.get(error_type, "Refer to provided suggestion.")
    print(f"Suggestion for line {line_no}: {suggestion}")

def parse_mypy_errors(output):
    """Parse mypy output for errors."""
    lines = output.split("\n")
    for line in lines:
        if line.strip():
            parts = line.split(":")
            if len(parts) >= 4:
                file_name = parts[0].strip()
                line_no = parts[1].strip()
                error_message = ":".join(parts[3:]).strip()
                print(f"File: {file_name}, Line: {line_no}, Error: {error_message}")
                suggest_mypy_fix(error_message, line_no)

def suggest_mypy_fix(error_message, line_no):
    """Suggest fixes based on mypy error messages."""
    fixes = {
        "incompatible type": "Check the type annotations and ensure the types match the expected signature.",
        "missing return": "Add a return statement with the appropriate type as per the function annotation.",
        "cannot determine type": "Add explicit type annotations to the variable or function.",
    }

    for error_key, suggestion in fixes.items():
        if error_key in error_message.lower():
            print(f"Suggestion for line {line_no}: {suggestion}")
            return

    print(f"Suggestion for line {line_no}: Kindly review the line and refer to the error message provided.")

if __name__ == "__main__":
    file_path = "test.smple"  # Default filename
    if os.path.isfile(file_path):
        analyze_file(file_path)
    else:
        print(f"File '{file_path}' does not exist. Please create the file or provide a valid file path.")

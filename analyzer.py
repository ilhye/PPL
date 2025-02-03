import re
import json

# Tokens
INTEGERS = r'\d+'
FLOAT = r'[\d+\.\d+]'
VARIABLES = r'[a-zA-Z0-9_]+'
ASSIGN = '='
CONDITION = ['if', 'else', 'elif']
LOOPS = ['for', 'while']
COMMENT = r'/\*([a-zA-Z]+)\*/'
END, PAUSE = '.', ','
ADD, SUBTRACT, MULTIPLY, DIVIDE = '+', '-', '*', '/'  # Arithmetic operators
# Comparison operators
EQUAL, NOT_EQUAL, LESS_THAN, GREATER_THAN, LESS_THAN_EQUAL, GREATER_THAN_EQUAL = '==', '!=', '<', '>', '<=', '>='
NOT, AND, OR = '!', '&&', '||'  # Logical operators
# Assignment operators
ADD_ASSIGN, SUBTRACT_ASSIGN, MULTIPLY_ASSIGN, DIVIDE_ASSIGN = '+=', '-=', '*=', '/='
INPUT, OUTPUT = 'input', 'display'
KEYWORDS = ['true', 'false', 'and',
            'or', 'not', 'in', 'is', 'break', 'continue', 'return',]


# Define the token types
class token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        # Return a more readable string representation of the token
        return f"Token: {self.type}, Lexeme: {self.value}"


class lexerOne:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line = 1
        self.current_char = self.text[self.pos]
        self.tokens = []  # Store tokens as an instance variable
        self.variables = {}
        processing = ''

    # Advance the 'pos' pointer and set the 'current_char' variable
    def advance(self):
        self.pos += 1

        if self.current_char == '\n':
            self.line += 1

        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    # Skip whitespaces
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    # Extract full word
    def extract_fullword(self):
        word = ''

        # Check if the current character is a letter or an underscore
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_' or re.match(FLOAT, self.current_char)):
            word += self.current_char
            self.advance()
        return word

    # Extract numbers 1001
    def extract_number(self):
        number = ''
        has_decimal = False

        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if has_decimal:
                    break
                has_decimal = True

            number += self.current_char
            self.advance()

        # Determine whether it's an INTEGER or FLOAT token
        if '.' in number:
            return token('FLOAT', number)
        else:
            return token('INTEGER', number)

    def handle_symbols(self):
        symbol = self.current_char
        self.advance()

        if symbol in ['<', '>', '!', '=', '+', '-', '*', '/'] and self.current_char == '=':
            symbol += self.current_char
            self.advance()
        elif symbol == '&' and self.current_char == '&':
            symbol += self.current_char
            self.advance()
        elif symbol == '|' and self.current_char == '|':
            symbol += self.current_char
            self.advance()

        return symbol

    def variable_assign(self):
        while self.current_char is not None and self.current_char != ".":
            if re.match(VARIABLES, self.current_char):
                var_name = self.extract_fullword()
                self.skip_whitespace()

                if self.current_char == ASSIGN:
                    self.advance()
                    self.skip_whitespace()

                    var_value = self.extract_fullword()

                    if var_value in self.variables:
                        # Retrieve stored value
                        var_value = self.variables[var_value]

                    self.variables[var_name] = var_value  # Store in dictionary
                    # Debugging output
                    print(f"Assigned: {var_name} = {self.variables[var_name]}")
            else:
                self.advance()
        return self.variables

    # Perform arithmetic and assignment operations
    def arithmetic_op(self):
        tokens = self.tokens
        last_variable = None  # Store last seen variable name

        for i, token in enumerate(tokens):
            if token.type == 'VARIABLES':
                last_variable = token.value  # Store variable name as a string

            if token.type in ['ADD', 'SUBTRACT', 'MULTIPLY', 'DIVIDE']:
                left = tokens[i - 1]
                right = tokens[i + 1]

                # Convert token values to numbers
                left_val = self.variables.get(left.value, left.value)
                right_val = self.variables.get(right.value, right.value)

                left_val = float(left_val) if '.' in str(
                    left_val) else int(left_val)
                right_val = float(right_val) if '.' in str(
                    right_val) else int(right_val)

                # Perform operation and store result

                if token.type == 'ADD':
                    self.variables[last_variable] = left_val + right_val
                elif token.type == 'SUBTRACT':
                    self.variables[last_variable] = left_val - right_val
                elif token.type == 'MULTIPLY':
                    self.variables[last_variable] = left_val * right_val
                elif token.type == 'DIVIDE':
                    if right_val != 0:
                        self.variables[last_variable] = left_val / right_val
                    else:
                        print("Error: Division by zero")
                        continue

                # print(f"{last_variable} = {self.variables[last_variable]}")  # Debug output

        return self.variables  # Ensure variables are returned and stored properly
    
    def comparison_op(self):
        tokens = self.tokens
        last_var = None
        

        for i, token in enumerate(tokens):
            # Check if the token is a variable
            if token.type == 'VARIABLES':
                last_var = token.value  # Store the variable name
                
            # Check if the token is a conditional operator (e.g., 'if', 'else', 'elif')
            if token.type == 'CONDITION':
                # Handle the condition token (store or process if needed)
                print(f"Condition detected: {token.value}")
                last_var = token.value  # Store condition for reference if needed (adjust as necessary)
            '''
            requires yung ano is nasa loob ng variables
            '''
            # Check for comparison operators like '==', '!=', '<', '>', etc.
            if token.type in ['EQUAL', 'NOT_EQUAL', 'LESS_THAN', 'GREATER_THAN', 'LESS_THAN_EQUAL', 'GREATER_THAN_EQUAL']:
                left = tokens[i - 1]
                right = tokens[i + 1]

                # Ensure the values are the same type before comparing
                if left.type in ['INTEGER', 'FLOAT'] and right.type in ['INTEGER', 'FLOAT']:
                    left_val = float(left.value) if left.type == 'FLOAT' else int(left.value)
                    right_val = float(right.value) if right.type == 'FLOAT' else int(right.value)

                    # Perform the comparison
                    if token.type == 'EQUAL':
                        self.variables[last_var] = left_val == right_val
                    elif token.type == 'NOT_EQUAL':
                        self.variables[last_var] = left_val != right_val
                    elif token.type == 'LESS_THAN':
                        self.variables[last_var] = left_val < right_val
                    elif token.type == 'GREATER_THAN':
                        self.variables[last_var] = left_val > right_val
                    elif token.type == 'LESS_THAN_EQUAL':
                        self.variables[last_var] = left_val <= right_val
                    elif token.type == 'GREATER_THAN_EQUAL':
                        self.variables[last_var] = left_val >= right_val

            self.advance()  # Move to the next token
        return self.variables


    def logical_op(self):
        tokens = self.tokens
        last_var = None

        for i, token in enumerate(tokens):
            if token.type == 'VARIABLES':
                last_var = token.value  # Store variable name as a string

            if token.type in ['AND', 'OR', 'NOT']:
                left = tokens[i - 1]
                right = tokens[i + 1]

                left_val = bool(int(left.value)) if left.type in [
                    'INTEGER', 'FLOAT'] else bool(left.value)
                right_val = bool(int(right.value)) if right.type in [
                    'INTEGER', 'FLOAT'] else bool(right.value)

                if token.type == 'NOT':
                    self.variables[last_var] = not right_val
                elif token.type == 'AND':
                    self.variables[last_var] = left_val and right_val
                elif token.type == 'OR':
                    self.variables[last_var] = left_val or right_val

            self.advance()
        return self.variables

    # Display output
    def display_output(self):
        tokens = self.tokens

        for i, token in enumerate(tokens):
            if token.type == 'OUTPUT' and token.value == 'display':
                if i + 1 < len(tokens):
                    var_name = tokens[i + 1].value

                    if var_name in self.variables:
                        print(f"{var_name} = {self.variables[var_name]}")
                    else:
                        print(f"Error: Variable '{var_name}' is not defined.")

    def conditional_statements(self):
        tokens = self.tokens
     
        for i, token in enumerate(tokens):
            if token.type == 'CONDITION' and token.value in ['if', 'else', 'elif']:
                if i + 1 < len(tokens):
                    var_name = tokens[i + 1].value

                    if var_name in self.variables:
                        if self.variables[var_name] == True:
                            print(f"Condition '{token.value}' is True")
                        elif self.variables[var_name] == False:
                            print(f"Condition '{token.value}' is False")
                    else:
                        print(f"Error: Variable '{var_name}' is not defined.")
    
    # Loop statements
    def loop_statements(self):
        tokens = self.tokens
        i = 0

        # Loop through the tokens
        while i < len(tokens):
            token = tokens[i]

            if token.type == 'LOOP' and token.value == 'while':
                if i + 1 < len(tokens):
                    # Get the condition variable after 'while'
                    condition_var = tokens[i + 1].value

                    if condition_var not in self.variables:
                        print(f"Error: Condition variable '{condition_var}' is not defined.")
                        i += 1
                        continue

                    i += 2

                    iteration_count = 0

                    # Loop through the tokens inside the 'while' loop
                    while self.variables.get(condition_var, False):
                        iteration_count += 1

                        # Terminate the loop if it exceeds 20 iterations
                        if iteration_count > 20:
                            for _ in range(20):
                                print(condition_var) 
                            print("Loop terminated after 20 iterations.")
                            break

                        while i < len(tokens):
                            current_token = tokens[i]

                            if current_token.type == 'OUTPUT' and current_token.value == 'display':
                                if i + 1 < len(tokens):
                                    display_var = tokens[i + 1].value

                                    if display_var in self.variables:
                                        print(f"{display_var} = {self.variables[display_var]}") 
                                    else:
                                        print(f"Error: Variable '{display_var}' is not defined.")
                                i += 2  

                            elif current_token.type == 'END' and current_token.value == '.':
                                i += 1
                                break  

                            else:
                                i += 1

                        # Check the condition variable
                        if condition_var not in self.variables or not self.variables[condition_var]:
                            break  

                else:
                    print("Error: Incomplete 'while' loop syntax.")
                    i += 1

            # Move to the next token
            else:
                i += 1

    def analyzer(self):
        tokens = []

        # Loop through the text
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            # Check if the current character is a number
            if self.current_char.isdigit() or (self.current_char == '.' and self.current_char[-1].isdigit()):
                tokens.append(self.extract_number())
                continue

            # Check if the current character is a letter or an underscore
            elif self.current_char.isalpha() and self.current_char not in [INPUT, OUTPUT]:
                word = self.extract_fullword()

                if word.lower() == OUTPUT:
                    tokens.append(token('OUTPUT', word))
                elif word.lower() == INPUT:
                    tokens.append(token('INPUT', word))
                elif word in KEYWORDS:
                    tokens.append(token('KEYWORD', word))
                elif word in CONDITION:
                    tokens.append(token('CONDITION', word))
                elif word in LOOPS:
                    tokens.append(token('LOOP', word))
                elif re.match(VARIABLES, word):
                    tokens.append(token('VARIABLES', word))

            # Check for delimiter
            elif self.current_char == END:
                tokens.append(token('END', self.current_char))
            elif self.current_char == PAUSE:
                tokens.append(token('PAUSE', self.current_char))

            # Check for assignment, logical and comparison operators
            elif self.current_char in ['<', '>', '=', '!', '+', '-', '*', '/', '&', '|']:
                compare_op = self.handle_symbols()

                if compare_op == GREATER_THAN_EQUAL:
                    tokens.append(token('GREATER_THAN_EQUAL', compare_op))
                elif compare_op == LESS_THAN_EQUAL:
                    tokens.append(token('LESS_THAN_EQUAL', compare_op))
                elif compare_op == EQUAL:
                    tokens.append(token('EQUAL', compare_op))
                elif compare_op == NOT_EQUAL:
                    tokens.append(token('NOT_EQUAL', compare_op))
                elif compare_op == ASSIGN:
                    tokens.append(token('ASSIGN', compare_op))
                elif compare_op == GREATER_THAN:
                    tokens.append(token('GREATER_THAN', compare_op))
                elif compare_op == LESS_THAN:
                    tokens.append(token('LESS_THAN', compare_op))
                elif compare_op == ADD_ASSIGN:
                    tokens.append(token('ADD_ASSIGN', compare_op))
                elif compare_op == SUBTRACT_ASSIGN:
                    tokens.append(token('SUBTRACT_ASSIGN', compare_op))
                elif compare_op == MULTIPLY_ASSIGN:
                    tokens.append(token('MULTIPLY_ASSIGN', compare_op))
                elif compare_op == DIVIDE_ASSIGN:
                    tokens.append(token('DIVIDE_ASSIGN', compare_op))
                elif compare_op == ADD:
                    tokens.append(token("ADD", compare_op))
                elif compare_op == SUBTRACT:
                    tokens.append(token("SUBTRACT", compare_op))
                elif compare_op == MULTIPLY:
                    tokens.append(token("MULTIPLY", compare_op))
                elif compare_op == DIVIDE:
                    tokens.append(token("DIVIDE", compare_op))
                elif compare_op == AND:
                    tokens.append(token("AND", compare_op))
                elif compare_op == OR:
                    tokens.append(token("OR", compare_op))
                elif compare_op == NOT:
                    tokens.append(token("NOT", compare_op))

            else:
                raise Exception(f'Invalid character {
                                self.current_char} on line {self.line}')

            self.advance()

        self.tokens = tokens
        return tokens


def parse(file):
    if not file.endswith('.smple'):
        print('Invalid file type')
    else:
        contents = open(file, 'r').read()
        analyzer_instance = lexerOne(contents)
        tokens = analyzer_instance.analyzer()
        analyzer_instance.arithmetic_op()
        analyzer_instance.comparison_op()
        analyzer_instance.logical_op()
        analyzer_instance.variable_assign()
        analyzer_instance.display_output()
        analyzer_instance.loop_statements()
        analyzer_instance.conditional_statements()
        return tokens

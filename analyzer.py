import re

# Tokens
INTEGERS = r'\d+'
FLOAT = r'[\d+\.\d+]'
VARIABLES = r'[a-zA-Z0-9_]+'
ASSIGN = '='
CONDITION = 'condition'
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
            'or', 'not', 'in', 'is', 'break', 'continue', 'return']

FUNCTION = {'function', 'main'}
LEFT_CURLY_BRACE, RIGHT_CURLY_BRACE = '{', '}'
LEFT_PARENTHESIS, RIGHT_PARENTHESIS = '(', ')' 


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
        self.tokens = []  

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
        
    # Handle two symbols
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
    
    # Lexical analyzer
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

            # Check if the current character is a keyword, condition, variable or loop
            elif self.current_char.isalpha() and self.current_char not in [INPUT, OUTPUT]:
                word = self.extract_fullword()

                if word.lower() == OUTPUT:
                    tokens.append(token('OUTPUT', word))
                elif word.lower() == INPUT:
                    tokens.append(token('INPUT', word))
                elif word in FUNCTION:
                    tokens.append(token('FUNCTION', word))
                elif word in KEYWORDS:
                    tokens.append(token('KEYWORD', word))
                elif word == CONDITION:
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

            # Check for parentheses and curly braces
            elif self.current_char == LEFT_CURLY_BRACE:
                tokens.append(token('LEFT_CURLY_BRACE', self.current_char))
            elif self.current_char == RIGHT_CURLY_BRACE:
                tokens.append(token('RIGHT_CURLY_BRACE', self.current_char))
            elif self.current_char == LEFT_PARENTHESIS:
                tokens.append(token('LEFT_PARENTHESIS', self.current_char))
            elif self.current_char == RIGHT_PARENTHESIS:
                tokens.append(token('RIGHT_PARENTHESIS', self.current_char))

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
                raise Exception(f'Invalid character {self.current_char} on line {self.line}')

            self.advance()

        self.tokens = tokens
        return tokens

# Parse the file
def parse(file):
    if not file.endswith('.smple'):
        print('Invalid file type')
    else:
        contents = open(file, 'r').read()
        analyzer_instance = lexerOne(contents)
        tokens = analyzer_instance.analyzer()
        return tokens

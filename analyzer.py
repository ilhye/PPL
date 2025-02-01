import json
import re
from sys import argv

# Class to store the token and lexeme
class token:
    def __init__(self, token, lexeme):
        self.token = token
        self.lexeme = lexeme

    def __str__(self):
        return f"Token: {self.token}, Lexeme: {self.lexeme}"


# Class to analyze the contents of the file
class analyzer:
    def __init__(self, contents):
        self.contents = contents
        self.variables = {}

        with open('tokens.json') as file:
            self.lexerData = json.load(file)

    # Function to tokenize the contents of the file
    def tokenize(self):
        # Replace all whitespaces with commasF
        no_whitespace = self.contents.replace(' ', ',').replace(
            "\t", ",").replace("\n", ",").replace("\r", "")

        token_array = no_whitespace.split(",")
        results = []

        # Iterate over the lexerData dictionary and print the token and lexeme for the given lexeme
        for part in token_array:
            commentRegEx = re.match(r'/\*([a-zA-Z\s]+)\*/', part)
            if re.match(r'/\*.*\*/', part):
                results.append(token('COMMENT_CONTENT', commentRegEx.group(1)))
            elif part.isidentifier() and part not in ['input', 'display', r'/\*([a-zA-Z]+)\*/']:
                results.append(token('IDENTIFIER', part))
            elif part.isdigit():
                results.append(token('INT', part))
            elif re.match(r'^\d+\.\d+$', part):
                results.append(token('FLOAT', part))
            elif part == "True" or part == "False":
                results.append(token('BOOL', part))
            elif re.match(r"\"[^\"]*\"", part):
                results.append(token('STRING', part))
            else:
                for _, value in self.lexerData.items():
                    for i in value:
                        if part == i['lexeme']:
                            results.append(token(i['token'], i['lexeme']))
                            break

        return results

    # Function to handle variables and arithmetic operations
    def variable(self):
        tokens = self.tokenize()

        # Iterate over the tokens
        for i, current_token in enumerate(tokens):

            # Check if the current token is an identifier
            if current_token.token == 'IDENTIFIER':
                if i < len(tokens) - 2 and tokens[i+1].token == 'EQU':
                    print("\nCurrent Token:", current_token.lexeme)

            # Check if the current token is an arithmetic operator
            if current_token.token in ['ADD', 'SUB', 'MUL', 'DIV', 'MOD']:

                # Get the left and right lexemes
                if i > 0 and i < len(tokens) - 1:
                    left = tokens[i-1]
                    right = tokens[i+1]

                    # Convert lexemes to integers if they are integers
                    left_value = int(
                        left.lexeme) if left.token == "INT" else left.lexeme
                    right_value = int(
                        right.lexeme) if right.token == "INT" else right.lexeme

                    # Perform arithmetic operations
                    if current_token.token == 'ADD':
                        result = left_value + right_value
                        print("ADD:", result)
                    elif current_token.token == 'SUB':
                        result = left_value - right_value
                        print("SUB:", result)
                    elif current_token.token == 'MUL':
                        result = left_value * right_value
                        print("MUL:", result)
                    elif current_token.token == 'DIV':
                        result = left_value / right_value
                        print("DIV:", result)
                    elif current_token.token == 'MOD':
                        result = left_value % right_value
                        print("MOD:", result)

        self.variables[current_token.lexeme] = result
        print("\nStored Variables:", self.variables)

# Function to display the tokens and lexemes
def parse(file):
    # Check if the file is a .smple file
    if not file.endswith('.smple'):
        raise ValueError('File must be a .smple file')
    else:
        # Read the contents of the file
        contents = open(file, 'r').read()
        analyzer_instance = analyzer(contents)
        tokens = analyzer_instance.tokenize()
        analyzer_instance.variable()
        return tokens

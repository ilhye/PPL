import json
import re


class token:
    def __init__(self, token, lexeme):
        self.token = token
        self.lexeme = lexeme

    def __str__(self):
        return f"Token: {self.token}, Lexeme: {self.lexeme}"


class analyzer:
    def __init__(self, contents):
        self.contents = contents
        # self.comments = []

    def tokenize(self):
        with open('tokens.json') as file:
            lexerData = json.load(file)

        no_whitespace = self.contents.replace(' ', ',').replace(
            "\t", ",").replace("\n", ",").replace("\r", "")
        no_duplicate = list(set(no_whitespace.split(",")))
        results = []

        # Iterate ovtoker the lexerData dictionary and print the token and lexeme for the given lexeme
        # Check if the lexeme is a number, float, boolean, string, comment, or identifier
        for part in no_duplicate:
            if re.match(r'/\*.*\*/', part):
                results.append(token('COMMENT_CONTENT', part))
            elif part.isdigit():
                results.append(token('INT', part))
            elif re.match(r'^\d+\.\d+$', part):
                results.append(token('FLOAT', part))
            elif part == "True" or part == "False":
                results.append(token('BOOL', part))
            elif re.match(r"\"[^\"]*\"", part):
                results.append(token('STRING', part))
            elif part.isidentifier() and part not in ["input", "output", r'/\*([a-zA-Z]+)\*/']:
                results.append(token('IDENTIFIER', part))

            # Check if the lexeme is a keyword
            for _, value in lexerData.items():
                for i in value:
                    if part == i['lexeme']:
                        results.append(token(i['token'], i['lexeme']))

        return results


def parse(file):
    if not file.endswith('.smple'):
        raise ValueError('File must be a Python file')
    else:
        contents = open(file, 'r').read()
        tokens = analyzer(contents).tokenize()
        return tokens

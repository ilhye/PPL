import json

class token:
    def __init__(self, token, lexeme):
        self.token = token
        self.lexeme = lexeme

    def __str__(self):
        return f"Token: {self.token}, Lexeme: {self.lexeme}"

class analyzer:
    def __init__(self, contents):
        self.contents = contents
    
    def tokenize(self):
        with open('tokens.json') as file:
            lexerData = json.load(file)
        
        no_whitespace = self.contents.replace(' ', ',').replace("\t", ",").replace("\n", ",").replace("\r", "")
        no_duplicate = list(set(no_whitespace.split(",")))
        split_contents = [part for part in no_duplicate if part]

        results = []
        # Iterate over the lexerData dictionary and print the token and lexeme for the given lexeme
        for part in split_contents:
            for _,value in lexerData.items():
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
from sys import *
from analyzer import *

if __name__ == "__main__":
    # check if the file is passed as an argument
    # if not, then print an error message
    # if it is, then parse the file
    # and print the tokens]
    # arg
    file = argv[1]
    tokens = parse(file)
    for token in tokens:
        print(token)
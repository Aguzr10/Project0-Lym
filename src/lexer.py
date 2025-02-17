# Written by: 
# Juliana Vera, code: 202411275 email: j.veraq@uniandes.edu.co
# Alejandro Guzmán code: 202410186 email: a.guzmanr2@uniandes.edu.co

def lexer(code):
    """
    Lexical analyzer for the robot language.
    Converts code into a list of tokens.
    Manages keywords, symbols, directions and numbers.
    Does not use external libraries or classes.
    """

    # list of keywords (excluding ":" which is taken as its own symbol")
    keywords = {
        "proc", "while", "if", "else", "repeatTimes", "for", "move", "jump", "goto",
        "turn", "face", "put", "pick", "canPut", "canPick", "pop", "facing", "canMove",
        "canJump", "not", "do", "then", "toThe", "inDir", "ofType", "with"
    }

    # set of symbols that need to be recognized
    symbols = {"|", "[", "]", ".", ":=", ":"}

    # insert spaces around symbols to separate them from other tokens

    code = code.replace(":=", " := ")

    code = code.replace(":", " : ")

    code = code.replace("[", " [ ")
    code = code.replace("]", " ] ")
    code = code.replace("|", " | ")
    code = code.replace(".", " . ")

    # convert into list of tokens based on spaces
    words = code.split()

    tokens = []  # final token list, every token is a tuple, classified below

    for word in words:
        if word in keywords:
            tokens.append(("KEYWORD", word))
        elif word in symbols:
            tokens.append(("SYMBOL", word))
        elif word.startswith("#"):
            tokens.append(("DIRECTION", word))
        elif word.isdigit():
            tokens.append(("NUMBER", word))
        else:
            tokens.append(("IDENTIFIER", word))

    return tokens

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



def parser(tokens):
    
    """
    Verifies if the syntax of the code is correct.
    """
    
    pos = 0
    
    def current_token():
        return tokens[pos] if pos < len(tokens) else None
    
    def advance():
        # advances to the next token and returns True if there are more tokens
        
        nonlocal pos
        pos += 1
        return pos < len(tokens)
    
    def parse_procedure():
        # verifies procedure structure
        
        if current_token() is None or current_token()[0] != "IDENTIFIER":
            return False
        advance()
        
        if current_token() is not None or current_token()[0] == "SYMBOL" and current_token()[1] == ":":
            advance()
            if current_token() is None or current_token()[0] != "IDENTIFIER":
                return False
            advance()
            
        if current_token() is None or current_token()[0] != "SYMBOL" or current_token()[1] != "[":
            return False
        advance()
        
        return parse_block()
    
    def parse_block():
        # verifies structure within a code
        
        while current_token() is not None and current_token()[0] != "SYMBOL" and current_token()[1] != "]":
            advance()
            
        if current_token() is None or current_token()[0] != "SYMBOL" or current_token()[1] != "]":
            return False
        
        advance()
        return True
    
    while pos < len(tokens):
        if current_token()[0] == "KEYWORD" and current_token()[1] == "proc":
            advance()
            if not parse_procedure():
                return False
            else: 
                return False
    
    return True
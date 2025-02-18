# Written by: 
# Juliana Vera, code: 202411275 email: j.veraq@uniandes.edu.co
# Alejandro Guzmán code: 202410186 email: a.guzmanr2@uniandes.edu.co

def lexer(code):
    """
    Lexical analyzer for the robot language.
    Converts code into a list of tokens.
    Manages keywords, symbols, directions, and numbers.
    Does not use external libraries or classes.
    """
    
    # List of keywords
    keywords = {
        "proc", "while", "if", "else", "repeatTimes", "for", "move", "jump", "goto",
        "turn", "face", "put", "pick", "canPut", "canPick", "pop", "facing", "canMove",
        "canJump", "not", "do", "then", "toThe", "inDir", "ofType", "with"
    }
    
    # Set of symbols to be recognized
    symbols = {"|", "[", "]", ".", ":=", ":"}
    
    # Insert spaces around symbols to separate them from other tokens
    code = code.replace(":=", " := ")
    code = code.replace(":", " : ")
    code = code.replace("[", " [ ")
    code = code.replace("]", " ] ")
    code = code.replace("|", " | ")
    code = code.replace(".", " . ")
    
    # Convert into a list of tokens based on spaces
    words = code.split()
    
    tokens = []  # Each token is a tuple: (type, value)
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
    Returns True if the program follows the language rules; otherwise, False.
    """
    pos = 0
    procedures = {}       # Dictionary: procedure name -> list of parameters
    variables = set()     # Set of declared variables

    def current_token():
        return tokens[pos] if pos < len(tokens) else None

    def advance():
        nonlocal pos
        pos += 1
        return pos < len(tokens)

    def skip_line_number():
        # If the current token is a NUMBER and is used as a line number, skip it.
        if current_token() and current_token()[0] == "NUMBER":
            advance()

    def parse_variable_declaration():
        # Expects: | var1 var2 ... |
        if current_token() is None or current_token()[0] != "SYMBOL" or current_token()[1] != "|":
            return False
        advance()  # Skip opening "|"
        while current_token() is not None and current_token()[0] == "IDENTIFIER":
            variables.add(current_token()[1])
            advance()
        if current_token() is None or current_token()[0] != "SYMBOL" or current_token()[1] != "|":
            return False
        advance()  # Skip closing "|"
        return True

    def parse_procedure():
        # Skip any line number tokens
        while current_token() and current_token()[0] == "NUMBER":
            advance()
        # Expect: IDENTIFIER (procedure name)
        if current_token() is None or current_token()[0] != "IDENTIFIER":
            return False
        proc_name = current_token()[1]
        advance()
        # Expect: SYMBOL ":" 
        if current_token() is None or current_token()[0] != "SYMBOL" or current_token()[1] != ":":
            return False
        advance()  # Skip ":"
        
        # Parse parameters (optional)
        params = []
        # First parameter (if exists)
        if current_token() and current_token()[0] == "IDENTIFIER":
            params.append(current_token()[1])
            advance()
        # Additional parameters in the form: IDENTIFIER, ":" IDENTIFIER
        while current_token() and current_token()[0] == "IDENTIFIER":
            connector = current_token()[1]
            advance()
            if current_token() is None or current_token()[0] != "SYMBOL" or current_token()[1] != ":":
                # If no colon, assume parameters ended.
                break
            advance()  # Skip ":"
            if current_token() is None or current_token()[0] != "IDENTIFIER":
                return False
            params.append(current_token()[1])
            advance()
        
        procedures[proc_name] = params
        
        # Expect: SYMBOL "[" to start the procedure block
        if current_token() is None or current_token()[0] != "SYMBOL" or current_token()[1] != "[":
            return False
        advance()  # Skip "["
        if not parse_block():
            return False
        return True

    def parse_block():
        # Parse tokens until a closing bracket "]" is encountered.
        while current_token() is not None and not (current_token()[0] == "SYMBOL" and current_token()[1] == "]"):
            # Skip line numbers in block
            while current_token() and current_token()[0] == "NUMBER":
                advance()
            # If a new procedure definition starts within the block
            if current_token() and current_token()[0] == "KEYWORD" and current_token()[1] == "proc":
                advance()  # Skip "proc"
                if not parse_procedure():
                    return False
            # If an identifier is found, it must be either a variable or a procedure call.
            elif current_token() and current_token()[0] == "IDENTIFIER":
                ident = current_token()[1]
                if ident not in variables and ident not in procedures:
                    print(f"Error: Identifier '{ident}' is not declared.")
                    return False
                advance()
            else:
                advance()
        if current_token() is None or current_token()[0] != "SYMBOL" or current_token()[1] != "]":
            return False
        advance()  # Skip closing "]"
        return True

    # Main parsing loop:
    while pos < len(tokens):
        skip_line_number()
        if current_token() is None:
            break
        if current_token()[0] == "SYMBOL" and current_token()[1] == "|":
            if not parse_variable_declaration():
                return False
        elif current_token()[0] == "KEYWORD" and current_token()[1] == "proc":
            advance()  # Skip "proc"
            if not parse_procedure():
                return False
        else:
            # Skip any token we don't specifically process
            advance()
    
    return True
# Written by: 
# Juliana Vera, code: 202411275 email: j.veraq@uniandes.edu.co
# Alejandro Guzmán code: 202410186 email: a.guzmanr2@uniandes.edu.co

def lexer(code):
    """
    Lexical analyzer for the robot language.
    Converts code into a list of tokens.
    Manages keywords, symbols, directions, and numbers.
    """
    keywords = {
        "proc", "while", "if", "else", "repeatTimes", "for", "move", "jump", 
        "goto", "turn", "face", "put", "pick", "canPut", "canPick", "pop", 
        "facing", "canMove", "canJump", "not", "do", "then", "toThe", "inDir", 
        "ofType", "with", "new", "var", "exec"
    }
    
    symbols = {"|", "[", "]", ".", ":=", ":", "=", "(", ")", ",", "{", "}", ";"}
    
    # Insert spaces around symbols to tokenize properly
    code = code.replace(":=", " := ")
    for sym in symbols:
        code = code.replace(sym, f" {sym} ")
    
    tokens = []
    words = code.split()
    
    for word in words:
        word_lower = word.lower()
        if word_lower in keywords:
            tokens.append(("KEYWORD", word_lower))
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
    pos = 0
    procedures = {}
    variables = set()

    def current_token():
        return tokens[pos] if pos < len(tokens) else None

    def advance():
        nonlocal pos
        pos += 1

    def match(expected_type, expected_value=None):
        token = current_token()
        if token and token[0] == expected_type and (expected_value is None or token[1] == expected_value):
            advance()
            return True
        return False

    def parse_variable_declaration():
        if not match("SYMBOL", "|"):
            return False
        while current_token() and current_token()[1] != "|":
            if not match("IDENTIFIER"):
                return False
            variables.add(tokens[pos - 1][1])
            if current_token() and current_token()[1] == ",":
                advance()
        return match("SYMBOL", "|")

    def parse_procedure():
        if not match("KEYWORD", "proc"):
            return False
        if not match("IDENTIFIER"):
            return False
        proc_name = tokens[pos - 1][1]
        procedures[proc_name] = []

        if match("SYMBOL", ":"):
            while current_token() and current_token()[0] == "IDENTIFIER":
                procedures[proc_name].append(current_token()[1])
                advance()
        
        if not match("SYMBOL", "["):
            return False
        while current_token() and current_token()[1] != "]":
            if not parse_statement():
                return False
        return match("SYMBOL", "]")

    def parse_if():
        if not match("KEYWORD", "if"):
            return False
        if not parse_condition():
            return False
        if not match("KEYWORD", "then"):
            return False
        if not parse_block():
            return False
        if current_token() and current_token()[1] == "else":
            advance()
            if not parse_block():
                return False
        return True

    def parse_while():
        if not match("KEYWORD", "while"):
            return False
        if not parse_condition():
            return False
        if not match("KEYWORD", "do"):
            return False
        if not parse_block():
            return False
        return True

    def parse_procedure_call():
        if not match("IDENTIFIER"):
            return False
        proc_name = tokens[pos - 1][1]
        if not match("SYMBOL", ":"):
            return False
        while current_token() and current_token()[1] != ".":
            if not match("NUMBER") and not match("IDENTIFIER"):
                return False
            if current_token() and current_token()[1] == ",":
                advance()
        return match("SYMBOL", ".")

    def parse_condition():
        if match("SYMBOL", "("):
            if not parse_expression():
                return False
            return match("SYMBOL", ")")
        return parse_expression()

    def parse_expression():
        if not match("IDENTIFIER") and not match("NUMBER"):
            return False
        return True

    def parse_block():
        if not match("SYMBOL", "["):
            return False
        while current_token() and current_token()[1] != "]":
            if not parse_statement():
                return False
        return match("SYMBOL", "]")

    def parse_statement():
        if current_token()[0] == "KEYWORD":
            if current_token()[1] == "if":
                return parse_if()
            elif current_token()[1] == "while":
                return parse_while()
        elif current_token()[0] == "IDENTIFIER":
            if current_token()[1] in procedures:
                return parse_procedure_call()
        return match("SYMBOL", ".")

    # Main parsing logic
    while pos < len(tokens):
        if current_token()[0] == "SYMBOL" and current_token()[1] == "|":
            if not parse_variable_declaration():
                return False
        elif current_token()[0] == "KEYWORD" and current_token()[1] == "proc":
            if not parse_procedure():
                return False
        else:
            advance()
    
    return True

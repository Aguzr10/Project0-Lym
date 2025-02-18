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

    def parse_variable_declaration():
        advance()  # Skip 'new'
        if not (current_token()[0] == "KEYWORD" and current_token()[1] == "var"):
            return False
        advance()  # Skip 'var'
        
        while True:
            if current_token()[0] != "IDENTIFIER":
                return False
            var_name = current_token()[1]
            variables.add(var_name)
            advance()

            if current_token() and current_token()[1] == "=":
                advance()  # Skip '='
                if current_token()[0] not in ["NUMBER", "IDENTIFIER"]:
                    return False
                advance()
            
            if current_token() and current_token()[1] == ",":
                advance()
            else:
                break
        return True

    def parse_procedure():
        proc_name = current_token()[1]
        advance()
        
        if current_token()[1] != ":":
            return False
        advance()  # Skip ':'
        
        params = []
        while current_token() and current_token()[0] == "IDENTIFIER":
            params.append(current_token()[1])
            advance()
        
        procedures[proc_name] = params
        
        if current_token()[1] != "[":
            return False
        advance()  # Skip '['
        
        while current_token() and current_token()[1] != "]":
            if not parse_statement():
                return False
        advance()  # Skip ']'
        return True

    def parse_if():
        advance()  # Skip 'if'
        if not parse_condition():
            return False
        if not parse_block():
            return False
        if current_token() and current_token()[1] == "else":
            advance()  # Skip 'else'
            if not parse_block():
                return False
        return True

    def parse_while():
        advance()  # Skip 'while'
        if not parse_condition():
            return False
        if not parse_block():
            return False
        return True

    def parse_procedure_call():
        proc_name = current_token()[1]
        advance()
        
        if current_token()[1] != "(":
            return False
        advance()  # Skip '('
        
        while current_token() and current_token()[1] != ")":
            if current_token()[0] not in ["NUMBER", "IDENTIFIER"]:
                return False
            advance()
            if current_token() and current_token()[1] == ",":
                advance()
        
        if current_token()[1] != ")":
            return False
        advance()  # Skip ')'
        return True

    def parse_condition():
        if current_token()[1] == "(":
            advance()  # Skip '('
            if not parse_expression():
                return False
            if current_token()[1] != ")":
                return False
            advance()  # Skip ')'
        else:
            if not parse_expression():
                return False
        return True

    def parse_expression():
        if current_token()[0] not in ["IDENTIFIER", "NUMBER"]:
            return False
        advance()
        return True

    def parse_block():
        if current_token()[1] != "{":
            return False
        advance()
        
        while current_token() and current_token()[1] != "}":
            if not parse_statement():
                return False
        advance()
        return True

    def parse_statement():
        token = current_token()
        if token[0] == "KEYWORD":
            if token[1] == "if":
                return parse_if()
            elif token[1] == "while":
                return parse_while()
        elif token[0] == "IDENTIFIER":
            if token[1] in procedures:
                return parse_procedure_call()
        advance()
        return True

    # Main parsing logic
    while pos < len(tokens):
        token = current_token()
        if token[0] == "KEYWORD":
            if token[1] == "new":
                if not parse_variable_declaration():
                    return False
            elif token[1] == "proc":
                advance()
                if not parse_procedure():
                    return False
            else:
                advance()
        else:
            advance()
    
    return True
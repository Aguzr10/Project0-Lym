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
        if current_token()[1] != "|":
            return False
        advance()  # Skip '|'
        
        while current_token()[1] != "|":
            if current_token()[0] != "IDENTIFIER":
                return False
            variables.add(current_token()[1])
            advance()
            if current_token()[1] == ",":
                advance()
        
        advance()  # Skip '|'
        return True

    def parse_procedure():
        if current_token()[0] != "IDENTIFIER":
            return False
        proc_name = current_token()[1]
        advance()
        
        if current_token()[1] != ":":
            return False
        advance()  # Skip ':'
        
        params = []
        while current_token()[0] == "IDENTIFIER":
            params.append(current_token()[1])
            advance()
            if current_token()[1] == "and":
                advance()
        
        procedures[proc_name] = params
        
        if current_token()[1] != "[":
            return False
        advance()  # Skip '['
        
        if not parse_variable_declaration():
            return False
        
        while current_token()[1] != "]":
            if not parse_statement():
                return False
        advance()  # Skip ']'
        return True

    def parse_if():
        advance()  # Skip 'if'
        if not parse_condition():
            return False
        if current_token()[1] != "then":
            return False
        advance()  # Skip 'then'
        if not parse_block():
            return False
        if current_token()[1] == "else":
            advance()  # Skip 'else'
            if not parse_block():
                return False
        return True

    def parse_while():
        advance()  # Skip 'while'
        if not parse_condition():
            return False
        if current_token()[1] != "do":
            return False
        advance()  # Skip 'do'
        if not parse_block():
            return False
        return True

    def parse_procedure_call():
        proc_name = current_token()[1]
        advance()
        
        if current_token()[1] != "(":
            return False
        advance()  # Skip '('
        
        while current_token()[1] != ")":
            if current_token()[0] not in ["NUMBER", "IDENTIFIER"]:
                return False
            advance()
            if current_token()[1] == ",":
                advance()
        
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
        
        while current_token()[1] != "}":
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
            elif token[1] == "repeatTimes":
                return parse_repeat_times()
            elif token[1] == "for":
                return parse_for()
            elif token[1] == "move":
                return parse_move()
            elif token[1] == "jump":
                return parse_jump()
            elif token[1] == "goto":
                return parse_goto()
            elif token[1] == "turn":
                return parse_turn()
            elif token[1] == "face":
                return parse_face()
            elif token[1] == "put":
                return parse_put()
            elif token[1] == "pick":
                return parse_pick()
            elif token[1] == "nop":
                advance()
                return True
        elif token[0] == "IDENTIFIER":
            if token[1] in procedures:
                return parse_procedure_call()
        advance()
        return True

    def parse_repeat_times():
        advance()  # Skip 'repeatTimes'
        if not parse_expression():
            return False
        if current_token()[1] != "repeat":
            return False
        advance()  # Skip 'repeat'
        if not parse_block():
            return False
        return True

    def parse_for():
        advance()  # Skip 'for'
        if not parse_expression():
            return False
        if current_token()[1] != "repeat":
            return False
        advance()  # Skip 'repeat'
        if not parse_block():
            return False
        return True

    def parse_move():
        advance()  # Skip 'move'
        if not parse_expression():
            return False
        if current_token()[1] == "toThe":
            advance()  # Skip 'toThe'
            if not parse_direction():
                return False
        elif current_token()[1] == "inDir":
            advance()  # Skip 'inDir'
            if not parse_orientation():
                return False
        return True

    def parse_jump():
        advance()  # Skip 'jump'
        if not parse_expression():
            return False
        if current_token()[1] == "toThe":
            advance()  # Skip 'toThe'
            if not parse_direction():
                return False
        elif current_token()[1] == "inDir":
            advance()  # Skip 'inDir'
            if not parse_orientation():
                return False
        return True

    def parse_goto():
        advance()  # Skip 'goto'
        if not parse_expression():
            return False
        if current_token()[1] != "with":
            return False
        advance()  # Skip 'with'
        if not parse_expression():
            return False
        return True

    def parse_turn():
        advance()  # Skip 'turn'
        if not parse_direction():
            return False
        return True

    def parse_face():
        advance()  # Skip 'face'
        if not parse_orientation():
            return False
        return True

    def parse_put():
        advance()  # Skip 'put'
        if not parse_expression():
            return False
        if current_token()[1] != "ofType":
            return False
        advance()  # Skip 'ofType'
        if not parse_type():
            return False
        return True

    def parse_pick():
        advance()  # Skip 'pick'
        if not parse_expression():
            return False
        if current_token()[1] != "ofType":
            return False
        advance()  # Skip 'ofType'
        if not parse_type():
            return False
        return True

    def parse_direction():
        if current_token()[1] not in ["#left", "#right", "#front", "#back"]:
            return False
        advance()
        return True

    def parse_orientation():
        if current_token()[1] not in ["#north", "#south", "#west", "#east"]:
            return False
        advance()
        return True

    def parse_type():
        if current_token()[1] not in ["#balloons", "#chips"]:
            return False
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

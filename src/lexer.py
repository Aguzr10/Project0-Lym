# Written by: 
# Juliana Vera, code: 202411275 email: j.veraq@uniandes.edu.co
# Alejandro Guzmán code: 202410186 email: a.guzmanr2@uniandes.edu.co

def lexer(code):
    keywords = {
        "proc", "while", "if", "else", "repeatTimes", "for", "move", "jump", "goto",
        "turn", "face", "put", "pick", "canPut", "canPick", "pop", "facing", "canMove",
        "canJump", "not", "do", "then", "toThe", "inDir", "ofType", "with"
    }    
    
    symbols = {"|", "[", "]", ".", ":=", ":"}
    
    
    tokens = []
    
    words = code.replace("\n", " ").split()
    
    for word in words: 
        if word in keywords:
            tokens.append("KEYWORD", word)
        elif word in symbols:
            tokens.append("SYMBOL", word)
        elif word.isdigit():
            tokens.append("NUMBER", word)
        else:
            tokens.append("IDENTIFIER", word)
    
    return tokens
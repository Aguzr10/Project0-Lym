# Written by: 
# Juliana Vera, code: 202411275 email: j.veraq@uniandes.edu.co
# Alejandro Guzmán code: 202410186 email: a.guzmanr2@uniandes.edu.co

def lexer(code):
    """
    Analizador léxico para el lenguaje del robot.
    Convierte el código en una lista de tokens.
    Maneja palabras clave, símbolos, direcciones y números.
    No usa librerías externas ni clases.
    """

    # Lista de palabras clave (sin los ":" ya que se separarán)
    keywords = {
        "proc", "while", "if", "else", "repeatTimes", "for", "move", "jump", "goto",
        "turn", "face", "put", "pick", "canPut", "canPick", "pop", "facing", "canMove",
        "canJump", "not", "do", "then", "toThe", "inDir", "ofType", "with"
    }

    # Conjunto de símbolos que necesitamos reconocer
    # Incluye "|" , "[" , "]", "." , ":=" y ":" (este último para separar palabras clave)
    symbols = {"|", "[", "]", ".", ":=", ":"}

    # Nota: Cualquier token que comience con '#' se clasifica como dirección
    # (por ejemplo, "#north", "#south", etc.)

    # Pre-procesamiento: Insertar espacios alrededor de los símbolos para separarlos.
    # Primero, separar el símbolo compuesto ":=".
    code = code.replace(":=", " := ")
    # Luego, separar el símbolo ":".
    code = code.replace(":", " : ")
    # Separar los corchetes, el pipe y el punto.
    code = code.replace("[", " [ ")
    code = code.replace("]", " ] ")
    code = code.replace("|", " | ")
    code = code.replace(".", " . ")

    # Convertir a lista de tokens "crudos" (basados en espacios)
    words = code.split()

    tokens = []  # Lista final de tokens (cada token es una tupla: (tipo, valor))

    # Clasificar cada token
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
            # Se asume que cualquier otro token es un identificador
            tokens.append(("IDENTIFIER", word))

    return tokens

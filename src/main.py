from lexer import tokenize
from parser import parse

def leer_archivo(nombre_archivo):
    with open(nombre_archivo, "r") as file:
        return file.read()

if __name__ == "__main__":
    codigo = leer_archivo("codigo.txt")
    tokens = tokenize(codigo)
    resultado = parse(tokens)
    print(resultado)  # "Sí" o "No"

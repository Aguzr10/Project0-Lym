from logic import lexer, parser


def leer_archivo(nombre_archivo):
    with open(nombre_archivo, "r") as file:
        return file.readlines()  # Devuelve una lista de líneas

if __name__ == "__main__":
    lineas = leer_archivo("codigo.txt")  
    codigo = "".join(lineas)  # Convierte la lista en una sola cadena

    tokens = lexer(codigo)
    resultado = parser(tokens)
    print(resultado)  # "Sí" o "No"
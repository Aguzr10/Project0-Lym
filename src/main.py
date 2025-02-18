# Written by: 
# Juliana Vera, code: 202411275 email: j.veraq@uniandes.edu.co
# Alejandro Guzmán code: 202410186 email: a.guzmanr2@uniandes.edu.co

from logic import lexer
from logic import parser

def read_file():
    """
    Prompts the user for the file name and reads it.
    Returns the contents of the file as a text string.
    """
    filename = input("Enter the file name: ")
    
    try:
        with open(filename, "r") as file:
            return file.read()  # Read the entire file as a single string
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return None

if __name__ == "__main__":
    codigo = read_file()
    
    if codigo is not None:  
        tokens = lexer(codigo)
        result = parser(tokens)  
        
        if result:
            print("The code is valid!")
        else:
            print("The code is not valid.")

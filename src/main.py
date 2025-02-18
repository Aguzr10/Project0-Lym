# Written by: 
# Juliana Vera, code: 202411275 email: j.veraq@uniandes.edu.co
# Alejandro Guzmán code: 202410186 email: a.guzmanr2@uniandes.edu.co

import os
from logic import lexer
from logic import parser

def read_file():
    """
    Reads the file from the desktop or current working directory using just the file name.
    Returns the contents of the file as a text string.
    """
    # Get the file name from the user
    filename = input("Enter the file name: ")

    # Get the user's desktop path
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    
    # First try to open from the desktop
    file_path = os.path.join(desktop_path, filename)
    
    try:
        with open(file_path, "r") as file:
            return file.read()  # Read the entire file as a single string
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found on the Desktop.")
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
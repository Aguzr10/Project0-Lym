# Test files

from logic import lexer, parser

# Test files
test_files = [
    {
        "name": "codigo_valido2",
        "content": """
|nom x y one|
proc putChips : n andBalloons : m [
|c, b|
c := n .
b := m .
put : c ofType : # chips . put: b ofType : # balloons ]
proc goNorth [
while : canMove : 1 inDir : # north do: [ move : 1 InDir : # north . ]
]
proc goWest [
if: canMove : 1 InDir : # west then : [ move : 1 InDir : # west ] else
: [nop .]]
[
goTo : 3 with : 3 .
putChips : 2 andBalloons : 1 .
]
"""
    },
    {
        "name": "codigo_invalido",
        "content": """
|t1 t2|
proc move: n [ 
move: 1 inDir: #north . 
]
turnRight: 1 .
"""
    },
    {
        "name": "codigo_valido",
        "content": """
|t1 t2 t3|
proc move: n [ 
move: 1 inDir: #north . 
]
proc turnRight [ 
turn: #right . 
]
"""
    }
]

for test_file in test_files:
    print(f"Testing {test_file['name']}")
    tokens = lexer(test_file['content'])
    if parser(tokens):
        print("Valid syntax")
    else:
        print("Invalid syntax")
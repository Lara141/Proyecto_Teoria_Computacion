from lexer import tokenizar
from parser import Parser

# Ejemplo de código en el lenguaje LCR
codigo_prueba = """
si la humedad es menor a 30
o la temperatura es mayor a 35
entonces detener bomba de agua 2

"""

tokens, error_lexico = tokenizar(codigo_prueba)

print("Tokens encontrados:\n")


if error_lexico:
    print(f"✗ {error_lexico}")

else:

    for token in tokens:
        print(token)
        

    try:

        parser = Parser(tokens)

        ast = parser.parsear()

        print("\n✓ La cadena pertenece al lenguaje.")

        print("\nAST generado:\n")

        print(ast)

    except RuntimeError as error:

        print(f"\n✗ {error}")
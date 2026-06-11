from lexer import tokenizar
from parser import Parser

codigo_prueba = """
SI (humedad < 3 Y temperatura >= 4) ENTONCES BOMBA_1 = APAGADO;
"""

try:
    tokens = tokenizar(codigo_prueba)

    print("Tokens encontrados:")
    for token in tokens:
        print(token)

    parser = Parser(tokens)
    parser.parsear()

    print("\n✓ La cadena pertenece al lenguaje.")

except RuntimeError as error:
    print(f"\n✗ {error}")
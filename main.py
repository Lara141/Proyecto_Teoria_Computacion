from lexer import tokenizar
from parser import Parser

codigo_prueba = """
SI (humedad < 3 Y temperatura >= 212) ENTONCES BOMBA_1 = APAGADO;
"""

tokens, error_lexico = tokenizar(codigo_prueba)

print("Tokens encontrados:")
for token in tokens:
    print(token)

if error_lexico:
    print(f"\n✗ {error_lexico}")
else:
    try:
        parser = Parser(tokens)
        parser.parsear()

        print("\n✓ La cadena pertenece al lenguaje.")

    except RuntimeError as error:
        print(f"\n✗ {error}")
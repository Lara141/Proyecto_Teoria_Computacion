"""Programa principal para demostrar el lexer y parser del lenguaje LCR.
Este módulo contiene un ejemplo de uso del analizador léxico (lexer)
y el analizador sintáctico (parser) para validar código en el lenguaje
LCR (Lenguaje de Control de Riego).
Proceso:
    1. Tokenización: Convierte el código fuente en una secuencia de tokens.
    2. Análisis Sintáctico: Verifica que los tokens sigan la gramática del lenguaje.
    3. Reporte: Indica si el código es válido o muestra el error encontrado.
"""

from lexer import tokenizar
from parser import Parser

# Ejemplo de código en el lenguaje LCR
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
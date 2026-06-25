import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from lexer import tokenizar
from parser import Parser



# CASOS DE PRUEBA SINTÁCTICOS INVÁLIDOS


casos_prueba = [

    {
        "id": 1,
        "descripcion": "Falta la condición después de 'si'",
        "codigo": "si entonces prender bomba de agua 1"
    },

    {
        "id": 2,
        "descripcion": "Falta el valor numérico",
        "codigo": "si la temperatura es mayor a entonces prender bomba de agua"
    },

    {
        "id": 3,
        "descripcion": "Falta la palabra clave 'entonces'",
        "codigo": "si la humedad es menor a 20 prender bomba de agua"
    },

    {
        "id": 4,
        "descripcion": "Falta la acción luego de 'entonces'",
        "codigo": "si interrupcion operador entonces"
    }

]



# MOTOR DE PRUEBAS


print("=" * 70)
print("CASOS DE PRUEBA DEL ANALIZADOR SINTÁCTICO (INVÁLIDOS)")
print("=" * 70)

for caso in casos_prueba:

    print(f"\nCaso {caso['id']}")
    print(f"Descripción : {caso['descripcion']}")
    print(f"Entrada     : {caso['codigo']}")

    tokens, error_lexico = tokenizar(caso["codigo"])

    if error_lexico:

        print(f"✓ Error léxico detectado correctamente.")
        print(error_lexico)

        continue

    try:

        parser = Parser(tokens)

        parser.parsear()

        print("✗ ERROR: la cadena fue aceptada cuando debía rechazarse.")

    except RuntimeError as error:

        print("✓ Error sintáctico detectado correctamente.")
        print(error)

print("\nPruebas finalizadas.")
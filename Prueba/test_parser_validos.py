import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from lexer import tokenizar
from parser import Parser
# ==========================================
# CASOS DE PRUEBA SINTÁCTICOS VÁLIDOS
# ==========================================

casos_prueba = [

    {
        "id": 1,
        "descripcion": "Regla simple de automatización",
        "codigo": "si la temperatura es mayor a 30 entonces prender bomba de agua 1"
    },

    {
        "id": 2,
        "descripcion": "Regla de control con acción de detención",
        "codigo": "si la humedad es menor a 20 entonces detener bomba de agua"
    },

    {
        "id": 3,
        "descripcion": "Regla compuesta con condición lógica",
        "codigo": "si la humedad es menor a 20 y la temperatura es mayor a 35 entonces prender bomba de agua 2"
    },

    {
        "id": 4,
        "descripcion": "Regla de interrupción manual",
        "codigo": "si interrupcion operador entonces detener bomba de agua"
    },

    {
    "id": 5,
    "descripcion": "Activación manual de bomba de agua",
    "codigo": "si interrupcion operador entonces prender bomba de agua 1"
    },

{
    "id": 6,
    "descripcion": "Desactivación manual del sistema térmico",
    "codigo": "si interrupcion operador entonces detener sistema termico"
},

{
    "id": 7,
    "descripcion": "Activación manual de alarma sonora",
    "codigo": "si interrupcion operador entonces prender alarma sonora"
},

{
    "id": 8,
    "descripcion": "Activación manual del notificador visual",
    "codigo": "si interrupcion operador entonces prender notificador visual"
},

]

print("=" * 70)
print("CASOS DE PRUEBA DEL ANALIZADOR SINTÁCTICO")
print("=" * 70)

for caso in casos_prueba:

    print(f"\nCaso {caso['id']}")
    print(f"Descripción : {caso['descripcion']}")
    print(f"Entrada     : {caso['codigo']}")

    tokens, error = tokenizar(caso["codigo"])

    if error:

        print(f"✗ Error Léxico: {error}")

        continue

    try:

        parser = Parser(tokens)

        ast = parser.parsear()

        print("✓ Cadena aceptada por el analizador sintáctico.")
        print("✓ AST generado correctamente.")

    except RuntimeError as e:

        print(f"✗ {e}")

print("\nPruebas finalizadas.")
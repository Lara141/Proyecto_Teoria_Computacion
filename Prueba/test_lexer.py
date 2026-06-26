import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from lexer import tokenizar

casos_prueba = [
    {
        "id": 1,
        "descripcion": "Camino feliz - Instrucción simple",
        "codigo": "si la temperatura es mayor a 30 entonces activar sistema termico"
    },
    {
       "id": 2,
        "descripcion": "Error léxico por carácter inválido (@)",
        "codigo": "si movimiento @ entonces"
    },
    {
         "id": 3,
        "descripcion": "Interrupción directa y ID opcional numérico",
        "codigo": "si interrupcion operador entonces detener bomba de agua 1"
    },
    {
        "id": 4,
        "descripcion": "Error léxico por token mal formado / falta de cierre",
        "codigo": "si [temporizador"
    }
]

print("Iniciando pruebas del Analizador Léxico...\n" + "="*60)

for caso in casos_prueba:
    print(f"\nCaso {caso['id']}: {caso['descripcion']}")
    print(f"Entrada textual: '{caso['codigo']}'")
    
    tokens, error_lexico = tokenizar(caso['codigo'])
    
    if error_lexico:
        print(f"Salida obtenida: ✗ {error_lexico}")
    else:
        cantidad_tokens = len(tokens)
        print(f"Salida obtenida: ✓ {cantidad_tokens} tokens válidos identificados correctamente.")
        nombres_tokens = [t.tipo for t in tokens]
        print(f"Tokens generados: {nombres_tokens}")

print("\n" + "="*60 + "\nPruebas léxicas finalizadas.")
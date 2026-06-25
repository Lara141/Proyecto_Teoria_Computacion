from lexer import tokenizar
from parser import Parser

# ==========================================
# 1. DEFINIR LOS CASOS DE PRUEBA
# ==========================================
casos_prueba = [
    {
        "id": 1,
        "descripcion": "Camino feliz - Instrucción simple",
        "codigo": "si la temperatura es mayor a 30 entonces detener bomba de agua 2"
    },
    {
        "id": 2,
        "descripcion": "Condición compuesta y acción compuesta",
        "codigo": "si la humedad es menor a 20 y el movimiento es igual a 1 entonces activar sistema termico y prender alarma sonora"
    },
    {
        "id": 3,
        "descripcion": "Interrupción directa sin números",
        "codigo": "si interrupcion operador entonces detener bomba de agua"
    },
    {
        "id": 4,
        "descripcion": "ERROR: Falta palabra clave 'entonces'",
        "codigo": "si el estado es igual a 0 apagar notificador visual"
    },
    {
        "id": 5,
        "descripcion": "ERROR: Acción inexistente ('romper')",
        "codigo": "si el temporizador es distinto de 0 entonces romper alarma sonora"
    }
]

# ==========================================
# 2. MOTOR DE PRUEBAS
# ==========================================
print("Iniciando pruebas del Analizador Sintáctico...\n" + "="*60)

for caso in casos_prueba:
    print(f"\nCaso {caso['id']}: {caso['descripcion']}")
    print(f"Entrada: '{caso['codigo']}'")
    
    # Paso 1: Tokenizar (Lexer)
    tokens, error_lexico = tokenizar(caso['codigo'])
    
    if error_lexico:
        print(f"Salida obtenida: ✗ {error_lexico}")
        continue
        
    # Paso 2: Parsear (Parser sintáctico)
    try:
        parser = Parser(tokens)
        ast = parser.parsear()
        print("Salida obtenida: ✓ Éxito. La cadena pertenece al lenguaje y generó un AST válido.")
        
        # Opcional: Si querés imprimir el AST generado de los casos exitosos, descomentá la línea de abajo:
        # print(f"AST: {ast}")
        
    except RuntimeError as error:
        # Aquí atrapamos los errores que programaste con "raise RuntimeError" en tu parser.py
        print(f"Salida obtenida: ✗ {error}")

print("\n" + "="*60 + "\nPruebas finalizadas.")
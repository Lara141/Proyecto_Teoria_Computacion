from lexer import tokenizar

# ==========================================
# 1. DEFINIR LOS CASOS DE PRUEBA
# ==========================================
casos_prueba = [
    {
        "id": 1,
        "descripcion": "Camino feliz - Instrucción simple",
        # Representa: [SI] [VARIABLE_CLIMATICA] [SUPERIOR_A] [DATO_NUMERICO] [ENTONCES] [PRENDER_ACCION] [SISTEMA_TERMICO]
        "codigo": "si la temperatura es mayor a 30 entonces activar sistema termico"
    },
    {
        "id": 2,
        "descripcion": "Interrupción directa y ID opcional numérico",
        # Representa: [SI] [INTERRUPCION_OPERADOR] [ENTONCES] [DETENER_ACCION] [BOMBA_AGUA] [NUMERO]
        "codigo": "si interrupcion operador entonces detener bomba de agua 2"
    },
    {
        "id": 3,
        "descripcion": "Error léxico por carácter inválido (@)",
        # Simula la inserción de un símbolo no mapeado en las expresiones regulares
        "codigo": "si el movimiento @ entonces"
    },
    {
        "id": 4,
        "descripcion": "Error léxico por símbolo suelto / mal formado",
        # En tu lexer, al usar expresiones regulares sin corchetes, un error de 
        # "token mal formado" se captura mediante caracteres desconocidos.
        "codigo": "si temporizador {"
    }
]

# ==========================================
# 2. MOTOR DE PRUEBAS DEL LEXER
# ==========================================
print("Iniciando pruebas del Analizador Léxico...\n" + "="*60)

for caso in casos_prueba:
    print(f"\nCaso {caso['id']}: {caso['descripcion']}")
    print(f"Entrada textual: '{caso['codigo']}'")
    
    # Pasamos el texto por tu analizador léxico
    tokens, error_lexico = tokenizar(caso['codigo'])
    
    if error_lexico:
        # Se imprime el error si encontró un carácter inválido
        print(f"Salida obtenida: ✗ {error_lexico}")
    else:
        # Si no hay error, contamos cuántos tokens válidos generó
        cantidad_tokens = len(tokens)
        print(f"Salida obtenida: ✓ {cantidad_tokens} tokens válidos identificados correctamente.")
        
        # Generamos una lista solo con los nombres de los tipos de tokens para la tabla
        nombres_tokens = [t.tipo for t in tokens]
        print(f"Tokens generados: {nombres_tokens}")

print("\n" + "="*60 + "\nPruebas léxicas finalizadas.")
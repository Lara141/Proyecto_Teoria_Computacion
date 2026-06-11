import re

# 1. Definimos la estructura de un Token
class Token:
    def __init__(self, tipo, valor, linea):
        self.tipo = tipo      # Ejemplo: 'NUMERO', 'SENSOR', 'SI'
        self.valor = valor    # Ejemplo: '50', 'humedad', 'SI'
        self.linea = linea    # Útil para reportar errores más adelante

    def __repr__(self):
        return f"Token({self.tipo}, '{self.valor}', Línea: {self.linea})"

# 2. Definimos las reglas de nuestro lenguaje LCR usando Expresiones Regulares
# ¡El orden importa! Las reglas más específicas van primero.
REGLAS_TOKENS = [
    ('SI',             r'\bSI\b'),
    ('ENTONCES',       r'\bENTONCES\b'),
    ('SENSOR',         r'\b(humedad|temperatura)\b'),
    ('ACTUADOR',       r'\b(BOMBA_1|BOMBA_2)\b'),
    ('ESTADO',         r'\b(ENCENDIDO|APAGADO)\b'),
    ('OP_LOGICO',      r'\b(Y|O)\b'),
    ('NUMERO',         r'\d+'),                     # Uno o más dígitos numéricos
    ('OP_RELACIONAL',  r'==|!=|>=|<=|<|>'),
    ('ASIGNACION',     r'='),
    ('PUNTO_Y_COMA',   r';'),
    ('PAREN_IZQ',      r'\('),
    ('PAREN_DER',      r'\)'),
    ('ESPACIOS',       r'[ \t]+'),                  # Espacios y tabulaciones (los vamos a ignorar)
    ('SALTO_LINEA',    r'\n'),                      # Para llevar la cuenta de las líneas
    ('DESCONOCIDO',    r'.'),                       # Cualquier otro carácter (generará error)
]

# 3. Función principal del Lexer
def tokenizar(codigo_fuente):
    tokens = []
    linea_actual = 1
    
    # Unimos todas las reglas en una sola gran expresión regular
    patron_general = '|'.join(f'(?P<{nombre}>{patron})' for nombre, patron in REGLAS_TOKENS)
    
    # Escaneamos el texto buscando coincidencias
    for coincidencia in re.finditer(patron_general, codigo_fuente):
        tipo = coincidencia.lastgroup
        valor = coincidencia.group()
        
        if tipo == 'ESPACIOS':
            continue # Ignoramos los espacios en blanco
        elif tipo == 'SALTO_LINEA':
            linea_actual += 1
            continue
        elif tipo == 'DESCONOCIDO':
            raise RuntimeError(f"Error Léxico: Carácter no válido '{valor}' en la línea {linea_actual}")
            
        # Si es un token válido, lo agregamos a nuestra lista
        tokens.append(Token(tipo, valor, linea_actual))
        
    return tokens

# 4. ¡Prueba de fuego!
if __name__ == '__main__':
    # Código de prueba escrito en tu Lenguaje de Configuración de Riego
    codigo_prueba = """
    SI (humedad < 30 Y temperatura >= 25) ENTONCES BOMBA_1 = ENCENDIDO;
    """
    
    try:
        resultado = tokenizar(codigo_prueba)
        print("¡Análisis Léxico Exitoso!\nTokens encontrados:")
        for token in resultado:
            print(token)
    except RuntimeError as error:
        print(error)
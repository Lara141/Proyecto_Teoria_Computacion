import re


# 1. Definimos la estructura de un Token
class Token:
    """ Representa un token identificado por el lexer.
    Un token es la unidad léxica más pequeña del lenguaje LCR,
    que incluye información sobre su tipo, valor y ubicación en el código.
     Atributos:
        tipo (str): Categoría del token (ej: 'NUMERO', 'SENSOR', 'SI', 'OP_LOGICO').
        valor (str): El contenido literal del token (ej: '50', 'humedad', 'SI').
        linea (int): Número de línea donde aparece el token en el código fuente.
    """
    def __init__(self, tipo, valor, linea):
        """ Inicializa un nuevo token.
         Args:
            tipo (str): Tipo o categoría del token.
            valor (str): Valor literal del token.
            linea (int): Número de línea del token en el código fuente.
        """
        self.tipo = tipo      # Ejemplo: 'NUMERO', 'SENSOR', 'SI'
        self.valor = valor    # Ejemplo: '50', 'humedad', 'SI'
        self.linea = linea    # Útil para reportar errores más adelante

    def __repr__(self):
        """Retorna una representación legible del token."""
        return f"Token({self.tipo}, '{self.valor}', Línea: {self.linea})"

# 2. Definimos las reglas de nuestro lenguaje LCR usando Expresiones Regulares
# El orden importa..... Las reglas más específicas van primero.
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
    """
    Realiza el análisis léxico del código fuente y genera una lista de tokens.  
    Esta función escanea el código fuente carácter por carácter utilizando
    expresiones regulares para identificar y clasificar cada token según
    las reglas definidas en REGLAS_TOKENS.   
    Args:
        codigo_fuente (str): El código fuente a analizar.   
    Returns:
        tuple: Una tupla (tokens, error) donde:
            - tokens (list[Token]): Lista de tokens identificados.
            - error (str|None): Mensaje de error léxico o None si no hay errores. 
    Ejemplo:
        >>> codigo = "SI (humedad < 3) ENTONCES BOMBA_1 = APAGADO;"
        >>> tokens, error = tokenizar(codigo)
        >>> if not error:
        ...     print(len(tokens))
        ...     11
    """
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
            return tokens, f"Error Léxico: Carácter no válido '{valor}' en la línea {linea_actual}"
            
        # Si es un token válido, lo agregamos a nuestra lista
        tokens.append(Token(tipo, valor, linea_actual))
        
    return tokens, None


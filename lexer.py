import re


# ==========================
# ESTRUCTURA DEL TOKEN
# ==========================

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

        self.tipo = tipo
        self.valor = valor
        self.linea = linea



    def __repr__(self):
        """Retorna una representación legible del token."""
        return f"Token({self.tipo}, '{self.valor}', Línea: {self.linea})"



# ==========================
# REGLAS DEL LEXER
# ==========================


REGLAS_TOKENS = [

    # ---------- Palabras clave ----------
    ('SI', r'\bsi\b'),
    ('ENTONCES', r'\bentonces\b'),

    # ---------- Operadores lógicos ----------
    ('Y', r'\by\b'),
    ('O', r'\bo\b'),

    # ---------- Condición especial ----------
    ('INTERRUPCION_OPERADOR', r'\binterrupcion operador\b'),

    # ---------- Variables ----------
    ('VARIABLE_CLIMATICA', r'\b(temperatura|humedad)\b'),
    ('SENSOR_MOVIMIENTO', r'\bmovimiento\b'),
    ('TEMPORIZADOR', r'\btemporizador\b'),
    ('ESTADO_SISTEMA', r'\bestado\b'),

    # ---------- Relaciones ----------
    ('SUPERIOR_A', r'\bmayor a\b'),
    ('INFERIOR_A', r'\bmenor a\b'),
    ('EQUIVALENTE_A', r'\bigual a\b'),
    ('DIFERENTE_DE', r'\bdistinto de\b'),

    # ---------- Valores ----------
    ('NUMERO', r'\d+'),

    # ---------- Acciones ----------
    ('PRENDER_ACCION', r'\b(prender|activar)\b'),
    ('DETENER_ACCION', r'\b(detener|apagar)\b'),

    # ---------- Actuadores ----------
    ('BOMBA_AGUA', r'\bbomba de agua\b'),
    ('SISTEMA_TERMICO', r'\bsistema termico\b'),
    ('NOTIFICADOR_VISUAL', r'\bnotificador visual\b'),
    ('ALARMA_SONORA', r'\balarma sonora\b'),

    # ---------- Palabras que no aportan significado ----------
    ('IGNORAR', r'\b(el|la|los|las|es|un|una)\b'),

    # ---------- Espacios ----------
    ('ESPACIOS', r'[ \t]+'),

    # ---------- Saltos ----------
    ('SALTO_LINEA', r'\n'),

    # ---------- Error ----------
    ('DESCONOCIDO', r'.')
]


# ==========================
# ANALIZADOR LÉXICO
# ==========================

def tokenizar(codigo_fuente):



    tokens = []
    linea_actual = 1

    patron_general = '|'.join(
        f'(?P<{nombre}>{patron})'
        for nombre, patron in REGLAS_TOKENS
    )

    for coincidencia in re.finditer(
        patron_general,
        codigo_fuente,
        re.IGNORECASE
    ):

        tipo = coincidencia.lastgroup
        valor = coincidencia.group()

        # Ignorar espacios y palabras auxiliares
        if tipo in ('ESPACIOS', 'IGNORAR'):
            continue

        # Contar líneas
        elif tipo == 'SALTO_LINEA':
            linea_actual += 1
            continue


        # Error léxico
        elif tipo == 'DESCONOCIDO':
            return (
                tokens,
                f"Error Léxico: Carácter no válido '{valor}' en la línea {linea_actual}"
            )

        # Agregar token
        tokens.append(
            Token(
                tipo,
                valor,
                linea_actual
            )
        )

    return tokens, None
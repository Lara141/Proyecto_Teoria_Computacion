class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def actual(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consumir(self, tipo_esperado):
        token = self.actual()

        if token is None:
            raise RuntimeError(
                f"Error sintáctico: se esperaba {tipo_esperado}, pero se llegó al final."
            )

        if token.tipo != tipo_esperado:
            raise RuntimeError(
                f"Error sintáctico en línea {token.linea}: "
                f"se esperaba {tipo_esperado} y se encontró "
                f"{token.tipo} ('{token.valor}')"
            )

        self.pos += 1

    def parsear(self):
        self.instruccion()

        if self.actual() is not None:
            token = self.actual()
            raise RuntimeError(
                f"Error sintáctico en línea {token.linea}: "
                f"token inesperado '{token.valor}'"
            )

    def instruccion(self):
        self.consumir('SI')
        self.consumir('PAREN_IZQ')

        self.condicion()

        self.consumir('PAREN_DER')
        self.consumir('ENTONCES')
        self.consumir('ACTUADOR')
        self.consumir('ASIGNACION')
        self.consumir('ESTADO')
        self.consumir('PUNTO_Y_COMA')

    def condicion(self):
        self.comparacion()

        while (
            self.actual() is not None and
            self.actual().tipo == 'OP_LOGICO'
        ):
            self.consumir('OP_LOGICO')
            self.comparacion()

    def comparacion(self):
        self.consumir('SENSOR')
        self.consumir('OP_RELACIONAL')
        self.consumir('NUMERO')
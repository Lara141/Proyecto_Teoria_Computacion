class Parser:
    """
    Analizador sintáctico (parser) para el lenguaje LCR.
    Realiza el análisis sintáctico de una secuencia de tokens,
    verificando que cumplan con las reglas gramaticales del lenguaje.
    Utiliza técnicas de análisis descendente recursivo (recursive descent parsing).
    Atributos:
        tokens (list[Token]): Lista de tokens a analizar.
        pos (int): Posición actual en la lista de tokens.
    """
    def __init__(self, tokens):
        """
        Inicializa el parser con una lista de tokens.
        
        Args:
            tokens (list[Token]): Lista de tokens generados por el lexer.
        """
        self.tokens = tokens
        self.pos = 0

    def actual(self):
        """
        Retorna el token actual sin consumirlo.
        
        Returns:
            Token: El token en la posición actual, o None si se llegó al final.
        """
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consumir(self, tipo_esperado):
        """
        Verifica y consume un token del tipo esperado.
        
        Comprueba que el token actual sea del tipo especificado.
        Si es válido, avanza la posición al siguiente token.
        En caso contrario, lanza una excepción.
        
        Args:
            tipo_esperado (str): Tipo de token que se espera encontrar.
        
        Raises:
            RuntimeError: Si el token no coincide con el tipo esperado
                         o si se llegó al final de la lista de tokens.
        """
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
        """
        Inicia el análisis sintáctico desde el símbolo inicial.
        
        Verifica que todos los tokens correspondan a una instrucción válida
        y que no haya tokens adicionales después de la instrucción.
        
        Raises:
            RuntimeError: Si hay un error sintáctico en el código.
        """
        self.instruccion()

        if self.actual() is not None:
            token = self.actual()
            raise RuntimeError(
                f"Error sintáctico en línea {token.linea}: "
                f"token inesperado '{token.valor}'"
            )

    def instruccion(self):
        """
        Analiza una instrucción del lenguaje LCR.
        
        Sintaxis: SI (condicion) ENTONCES ACTUADOR = ESTADO;
        
        Raises:
            RuntimeError: Si la estructura de la instrucción no es válida.
        """
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
        """
        Analiza una condición booleana.
        
        Una condición puede ser una o más comparaciones
        unidas por operadores lógicos (Y, O).
        Sintaxis: comparacion (OP_LOGICO comparacion)*
        
        Raises:
            RuntimeError: Si la condición no es válida.
        """
        self.comparacion()

        while (
            self.actual() is not None and
            self.actual().tipo == 'OP_LOGICO'
        ):
            self.consumir('OP_LOGICO')
            self.comparacion()

    def comparacion(self):
        """
        Analiza una comparación entre un sensor y un valor numérico.
        
        Sintaxis: SENSOR OP_RELACIONAL NUMERO
        Ejemplo: humedad < 50
        
        Raises:
            RuntimeError: Si la comparación no es válida.
        """
        self.consumir('SENSOR')
        self.consumir('OP_RELACIONAL')
        self.consumir('NUMERO')
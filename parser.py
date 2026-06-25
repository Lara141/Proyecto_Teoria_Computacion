from ast_lcr import *


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    # ==========================
    # UTILIDADES
    # ==========================

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

        return token

    # ==========================
    # PARSER PRINCIPAL
    # ==========================

    def parsear(self):

        regla = self.instruccion()

        if self.actual() is not None:

            token = self.actual()

            raise RuntimeError(
                f"Error sintáctico en línea {token.linea}: "
                f"token inesperado '{token.valor}'"
            )

        return ProgramaNode([regla])

    # ==========================
    # INSTRUCCION
    # ==========================

    def instruccion(self):

        self.consumir('SI')

        condicion = self.escenario()

        self.consumir('ENTONCES')

        reaccion = self.reaccion()

        return ReglaNode(
            condicion=condicion,
            reaccion=reaccion
        )

    # ==========================
    # ESCENARIO
    # ==========================

    def escenario(self):

        izquierda = self.condicion_simple()

        token = self.actual()

        if token and token.tipo in ('Y', 'O'):

            operador = self.consumir(
                token.tipo
            ).valor

            derecha = self.escenario()

            return CondicionBinariaNode(
                operador=operador,
                izquierda=izquierda,
                derecha=derecha
            )

        return izquierda

    # ==========================
    # CONDICION SIMPLE
    # ==========================

    def condicion_simple(self):

        token = self.actual()

        if token.tipo == 'INTERRUPCION_OPERADOR':

            self.consumir(
                'INTERRUPCION_OPERADOR'
            )

            return CondicionInterrupcionNode()

        entidad = self.entidad_observable()

        relacion = self.relacion()

        valor = self.numero()

        return CondicionRelacionalNode(
            entidad_observable=entidad,
            relacion=relacion,
            valor=valor
        )

    # ==========================
    # ENTIDAD OBSERVABLE
    # ==========================

    def entidad_observable(self):

        token = self.actual()

        tipos_validos = (

            'VARIABLE_CLIMATICA',
            'SENSOR_MOVIMIENTO',
            'TEMPORIZADOR',
            'ESTADO_SISTEMA'

        )

        if token and token.tipo in tipos_validos:

            return self.consumir(
                token.tipo
            ).valor

        raise RuntimeError(
            "Se esperaba una entidad observable."
        )

    # ==========================
    # RELACION
    # ==========================

    def relacion(self):

        token = self.actual()

        tipos_validos = (

            'SUPERIOR_A',
            'INFERIOR_A',
            'EQUIVALENTE_A',
            'DIFERENTE_DE'

        )

        if token and token.tipo in tipos_validos:

            return self.consumir(
                token.tipo
            ).valor

        raise RuntimeError(
            "Se esperaba un operador relacional."
        )

    # ==========================
    # NUMERO
    # ==========================

    def numero(self):

        token = self.consumir(
            'NUMERO'
        )

        return token.valor
    
    # ==========================
    # REACCION
    # ==========================

    def reaccion(self):

        acciones = []

        acciones.append(
            self.accion_ejecutable()
        )

        while (
            self.actual() is not None
            and self.actual().tipo == 'Y'
        ):

            self.consumir('Y')

            acciones.append(
                self.accion_ejecutable()
            )

        if len(acciones) == 1:
            return acciones[0]

        return ReaccionCompuestaNode(
            acciones=acciones
        )

    # ==========================
    # ACCION EJECUTABLE
    # ==========================

    def accion_ejecutable(self):

        token = self.actual()

        if token is None:
            raise RuntimeError(
                "Se esperaba una acción."
            )

        if token.tipo == 'PRENDER_ACCION':

            accion = self.consumir(
                'PRENDER_ACCION'
            ).valor

        elif token.tipo == 'DETENER_ACCION':

            accion = self.consumir(
                'DETENER_ACCION'
            ).valor

        else:

            raise RuntimeError(
                "Se esperaba una acción válida."
            )

        entidad, identificador = self.entidad_actuadora()

        return AccionNode(
            accion=accion,
            entidad_actuadora=entidad,
            id_opcional=identificador
        )

    # ==========================
    # ENTIDAD ACTUADORA
    # ==========================

    def entidad_actuadora(self):

        token = self.actual()

        if token is None:
            raise RuntimeError(
                "Se esperaba una entidad actuadora."
            )

        tipos_validos = (
            'BOMBA_AGUA',
            'SISTEMA_TERMICO',
            'NOTIFICADOR_VISUAL',
            'ALARMA_SONORA'
        )

        if token.tipo not in tipos_validos:

            raise RuntimeError(
                "Se esperaba una entidad actuadora válida."
            )

        entidad = self.consumir(
            token.tipo
        ).valor

        identificador = None

        if (
            self.actual() is not None
            and self.actual().tipo == 'NUMERO'
        ):

            identificador = self.consumir(
                'NUMERO'
            ).valor

        return (
            entidad,
            identificador
        )
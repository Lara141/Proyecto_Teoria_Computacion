from dataclasses import dataclass
from typing import List, Optional


# ==========================
# CLASE BASE
# ==========================

class NodoAST:
    pass


# ==========================
# PROGRAMA
# ==========================

@dataclass
class ProgramaNode(NodoAST):
    reglas: List['ReglaNode']


# ==========================
# REGLA
# ==========================

@dataclass
class ReglaNode(NodoAST):
    condicion: NodoAST
    reaccion: NodoAST


# ==========================
# CONDICIONES
# ==========================

@dataclass
class CondicionRelacionalNode(NodoAST):
    entidad_observable: str
    relacion: str
    valor: str


@dataclass
class CondicionInterrupcionNode(NodoAST):
    pass


@dataclass
class CondicionBinariaNode(NodoAST):
    operador: str          # y / o
    izquierda: NodoAST
    derecha: NodoAST


# ==========================
# ACCIONES
# ==========================

@dataclass
class AccionNode(NodoAST):
    accion: str            # prender, apagar, activar, detener
    entidad_actuadora: str
    id_opcional: Optional[str]


@dataclass
class ReaccionCompuestaNode(NodoAST):
    acciones: List[NodoAST]
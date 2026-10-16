"""
Etapa 2 - ANÁLISIS SINTÁCTICO
Entrada : lista de tokens producida por el analizador léxico.
Salida  : árbol sintáctico (una sentencia por elemento).

Gramática:
    PROGRAMA     -> SENTENCIA*
    SENTENCIA    -> DECLARACION | ASIGNACION | EXPRESION ;
    DECLARACION  -> TIPO IDENTIFICADOR ;
    ASIGNACION   -> IDENTIFICADOR = EXPRESION ;
    EXPRESION    -> ARITMETICA ( OP_RELACIONAL ARITMETICA )*
    ARITMETICA   -> TERMINO ( (+ | -) TERMINO )*
    TERMINO      -> FACTOR ( (* | /) FACTOR )*
    FACTOR       -> NUMERO | CADENA | BOOLEANO | IDENTIFICADOR | ( EXPRESION )
"""
from dataclasses import dataclass, field
from typing import List


# ------------------------------------------------------------------ nodos del árbol
@dataclass
class Literal:
    tipo: str          # ENTERO, REAL, CADENA, BOOLEANO
    lexema: str


@dataclass
class Ident:
    nombre: str


@dataclass
class BinOp:
    op: str
    izq: object
    der: object


@dataclass
class Declaracion:
    tipo_token: object
    ident: object
    tokens: List = field(default_factory=list)


@dataclass
class Asignacion:
    ident: object
    expr: object
    tokens: List = field(default_factory=list)


@dataclass
class ExpresionSuelta:
    expr: object
    tokens: List = field(default_factory=list)


def prefijo(e):
    """Representación de la estructura: (+ edad (* a 2))"""
    if isinstance(e, Literal):
        return e.lexema
    if isinstance(e, Ident):
        return e.nombre
    return f"({e.op} {prefijo(e.izq)} {prefijo(e.der)})"


def texto(tokens):
    return " ".join(t.lexema for t in tokens).replace(" ;", ";")


class ErrorSintactico(Exception):
    pass


RELACIONALES = {"OP_MAYOR", "OP_MENOR", "OP_MAYOR_IGUAL", "OP_MENOR_IGUAL", "OP_IGUAL", "OP_DISTINTO"}


class AnalizadorSintactico:
    def analizar(self, tokens, mostrar=True):
        self.t, self.i = tokens, 0
        programa = []
        while self.i < len(self.t):
            programa.append(self._sentencia())
        if mostrar:
            self.informe(programa)
        return programa

    # ---- utilidades
    def _ver(self, desp=0):
        k = self.i + desp
        return self.t[k] if k < len(self.t) else None

    def _esperar(self, tipo, descripcion):
        tok = self._ver()
        if tok is None or tok.tipo != tipo:
            donde = f"línea {tok.linea}, cerca de '{tok.lexema}'" if tok else "al final del programa"
            raise ErrorSintactico(f"{donde}: se esperaba {descripcion}")
        self.i += 1
        return tok

    # ---- sentencias
    def _sentencia(self):
        ini, tok, sig = self.i, self._ver(), self._ver(1)
        if tok.tipo.startswith("TIPO_"):
            self.i += 1
            ident = self._esperar("IDENTIFICADOR", "un identificador")
            self._esperar("PUNTO_Y_COMA", "';'")
            return Declaracion(tok, ident, self.t[ini:self.i])
        if tok.tipo == "IDENTIFICADOR" and sig is not None and sig.tipo == "ASIGNACION":
            self.i += 2
            expr = self._expresion()
            self._esperar("PUNTO_Y_COMA", "';'")
            return Asignacion(tok, expr, self.t[ini:self.i])
        expr = self._expresion()
        self._esperar("PUNTO_Y_COMA", "';'")
        return ExpresionSuelta(expr, self.t[ini:self.i])

    # ---- expresiones
    def _binaria(self, sub, tipos):
        izq = sub()
        while self._ver() is not None and self._ver().tipo in tipos:
            op = self._ver().lexema
            self.i += 1
            izq = BinOp(op, izq, sub())
        return izq

    def _expresion(self):
        return self._binaria(self._aritmetica, RELACIONALES)

    def _aritmetica(self):
        return self._binaria(self._termino, {"OP_SUMA", "OP_RESTA"})

    def _termino(self):
        return self._binaria(self._factor, {"OP_MULT", "OP_DIV"})

    def _factor(self):
        tok = self._ver()
        if tok is None:
            raise ErrorSintactico("el programa termina donde se esperaba una expresión")
        self.i += 1
        if tok.tipo == "NUMERO_ENTERO":
            return Literal("ENTERO", tok.lexema)
        if tok.tipo == "NUMERO_REAL":
            return Literal("REAL", tok.lexema)
        if tok.tipo == "LITERAL_CADENA":
            return Literal("CADENA", tok.lexema)
        if tok.tipo == "LITERAL_BOOLEANO":
            return Literal("BOOLEANO", tok.lexema)
        if tok.tipo == "IDENTIFICADOR":
            return Ident(tok.lexema)
        if tok.tipo == "PAREN_IZQ":
            e = self._expresion()
            self._esperar("PAREN_DER", "')'")
            return e
        raise ErrorSintactico(f"línea {tok.linea}: se esperaba una expresión y se encontró '{tok.lexema}'")

    @staticmethod
    def informe(programa):
        print("ETAPA 2 - ANÁLISIS SINTÁCTICO\n")
        for s in programa:
            if isinstance(s, Declaracion):
                regla, extra = "DECLARACION -> TIPO IDENTIFICADOR ;", ""
            elif isinstance(s, Asignacion):
                regla, extra = "ASIGNACION  -> IDENTIFICADOR = EXPRESION ;", f"   expresión: {prefijo(s.expr)}"
            else:
                regla, extra = "EXPRESION ;", f"   estructura: {prefijo(s.expr)}"
            print(f"  [OK] {texto(s.tokens):<28} {regla}{extra}")
        print(f"\n  {len(programa)} sentencias sintácticamente correctas.\n")

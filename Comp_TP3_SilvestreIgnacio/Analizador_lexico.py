"""
Etapa 1 - ANÁLISIS LÉXICO
Entrada : código fuente (texto).
Salida  : lista de tokens (tipo, lexema, línea).
"""
import re
from typing import NamedTuple


class Token(NamedTuple):
    tipo: str
    lexema: str
    linea: int

    def __str__(self):
        return f"{self.tipo}({self.lexema})"


class ErrorLexico(Exception):
    pass


# Palabras reservadas: tanto la forma del código (int, float...) como la del enunciado (entero, real...)
RESERVADAS = {
    "int": "TIPO_ENTERO", "entero": "TIPO_ENTERO",
    "float": "TIPO_REAL", "real": "TIPO_REAL",
    "String": "TIPO_CADENA", "cadena": "TIPO_CADENA",
    "boolean": "TIPO_BOOLEANO", "booleano": "TIPO_BOOLEANO",
    "verdadero": "LITERAL_BOOLEANO", "falso": "LITERAL_BOOLEANO",
    "true": "LITERAL_BOOLEANO", "false": "LITERAL_BOOLEANO",
}

PATRON = re.compile(
    r'(?P<ESPACIO>[ \t\r]+)'
    r'|(?P<NUEVA_LINEA>\n)'
    r'|(?P<LITERAL_CADENA>"[^"\n]*")'
    r'|(?P<NUMERO_REAL>\d+\.\d+)'
    r'|(?P<NUMERO_ENTERO>\d+)'
    r'|(?P<PALABRA>[^\W\d]\w*)'
    r'|(?P<OP_IGUAL>==)|(?P<OP_DISTINTO>!=)'
    r'|(?P<OP_MAYOR_IGUAL>>=)|(?P<OP_MENOR_IGUAL><=)'
    r'|(?P<ASIGNACION>=)'
    r'|(?P<OP_MAYOR>>)|(?P<OP_MENOR><)'
    r'|(?P<OP_SUMA>\+)|(?P<OP_RESTA>-)|(?P<OP_MULT>\*)|(?P<OP_DIV>/)'
    r'|(?P<PUNTO_Y_COMA>;)|(?P<PAREN_IZQ>\()|(?P<PAREN_DER>\))'
)


class AnalizadorLexico:
    def analizar(self, codigo, mostrar=True):
        tokens, pos, linea = [], 0, 1
        while pos < len(codigo):
            m = PATRON.match(codigo, pos)
            if not m:
                raise ErrorLexico(f"línea {linea}: carácter no reconocido {codigo[pos]!r}")
            tipo, lexema = m.lastgroup, m.group()
            pos = m.end()
            if tipo == "NUEVA_LINEA":
                linea += 1
            elif tipo == "ESPACIO":
                continue
            else:
                if tipo == "PALABRA":
                    tipo = RESERVADAS.get(lexema, "IDENTIFICADOR")
                tokens.append(Token(tipo, lexema, linea))
        if mostrar:
            self.informe(tokens)
        return tokens

    @staticmethod
    def informe(tokens):
        print("ETAPA 1 - ANÁLISIS LÉXICO")
        linea_actual = None
        for t in tokens:
            if t.linea != linea_actual:
                linea_actual = t.linea
                print(f"\n  Línea {t.linea}: ", end="")
            print(t, end="  ")
        print(f"\n\n  Total: {len(tokens)} tokens. Sin errores léxicos.\n")

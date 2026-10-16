"""
TP3 - Compiladores: Análisis Semántico (validación de tipos y reglas semánticas)

Entrada : código fuente (ya válido léxica y sintácticamente).
Salida  : tabla de símbolos, tipo de cada expresión, errores semánticos y veredicto final.

Este módulo contiene el analizador (tokenizador mínimo + tabla de símbolos +
reglas de tipos). Cada Ejercicio_N.py lo importa y analiza su propio código.
"""
import re

# ---------------------------------------------------------------- léxico (mínimo)
TIPOS = {
    "int": "ENTERO", "entero": "ENTERO",
    "float": "REAL", "real": "REAL",
    "String": "CADENA", "cadena": "CADENA",
    "boolean": "BOOLEANO", "booleano": "BOOLEANO",
}
BOOLEANOS = {"verdadero", "falso", "true", "false"}
NUMERICOS = {"ENTERO", "REAL"}

TOKEN_RE = re.compile(
    r'\s*(?:(?P<REAL>\d+\.\d+)|(?P<ENTERO>\d+)|"(?P<CADENA>[^"]*)"'
    r'|(?P<ID>[^\W\d]\w*)|(?P<OP>==|!=|>=|<=|[-+*/><=;()]))'
)


def tokenizar(texto):
    tokens, pos = [], 0
    texto = texto.rstrip()
    while pos < len(texto):
        m = TOKEN_RE.match(texto, pos)
        if not m:
            raise ValueError(f"Carácter inesperado en: {texto[pos:pos + 10]!r}")
        pos = m.end()
        tipo = m.lastgroup
        valor = m.group(tipo)
        if tipo == "ID":
            if valor in TIPOS:
                tipo = "TIPO"
            elif valor in BOOLEANOS:
                tipo = "BOOL"
        tokens.append((tipo, valor))
    return tokens


# ---------------------------------------------------------------- semántico
class AnalizadorSemantico:
    def __init__(self):
        self.tabla = {}      # identificador -> tipo
        self.errores = []    # mensajes de error
        self.toks = []
        self.i = 0

    # ---- utilidades del recorrido de tokens
    def _ver(self):
        return self.toks[self.i] if self.i < len(self.toks) else (None, None)

    def _tomar(self):
        t = self._ver()
        self.i += 1
        return t

    def _error(self, msg):
        self.errores.append(msg)
        return None

    # ---- reglas de tipos
    @staticmethod
    def _promover(a, b):
        return "REAL" if "REAL" in (a, b) else "ENTERO"

    def _tipo_binario(self, op, a, b):
        if a is None or b is None:
            return None  # el error ya fue informado antes
        if op == "+":
            if a in NUMERICOS and b in NUMERICOS:
                return self._promover(a, b)
            if a == b == "CADENA":
                return "CADENA"
            return self._error(f"el operador '+' no se puede aplicar a {a} y {b}")
        if op in ("-", "*", "/"):
            if a in NUMERICOS and b in NUMERICOS:
                return self._promover(a, b)
            return self._error(f"el operador '{op}' requiere operandos numéricos (recibió {a} y {b})")
        if op in (">", "<", ">=", "<="):
            if a in NUMERICOS and b in NUMERICOS:
                return "BOOLEANO"
            return self._error(f"el operador '{op}' requiere operandos numéricos (recibió {a} y {b})")
        if op in ("==", "!="):
            if a == b:
                return "BOOLEANO"
            return self._error(f"el operador '{op}' compara valores del mismo tipo (recibió {a} y {b})")
        return self._error(f"operador desconocido '{op}'")

    # ---- expresiones (precedencia: comparación < suma/resta < producto/división)
    def _expresion(self):
        izq = self._aditiva()
        while self._ver()[1] in (">", "<", ">=", "<=", "==", "!="):
            op = self._tomar()[1]
            izq = self._tipo_binario(op, izq, self._aditiva())
        return izq

    def _aditiva(self):
        izq = self._multiplicativa()
        while self._ver()[1] in ("+", "-"):
            op = self._tomar()[1]
            izq = self._tipo_binario(op, izq, self._multiplicativa())
        return izq

    def _multiplicativa(self):
        izq = self._primario()
        while self._ver()[1] in ("*", "/"):
            op = self._tomar()[1]
            izq = self._tipo_binario(op, izq, self._primario())
        return izq

    def _primario(self):
        tipo, valor = self._tomar()
        if tipo in ("ENTERO", "REAL", "CADENA"):
            return tipo
        if tipo == "BOOL":
            return "BOOLEANO"
        if tipo == "ID":
            if valor not in self.tabla:
                return self._error(f"el identificador '{valor}' no fue declarado")
            return self.tabla[valor]
        if valor == "(":
            t = self._expresion()
            self._tomar()  # ')'
            return t
        return self._error(f"expresión inesperada ({valor})")

    # ---- sentencias
    def _compatible(self, destino, origen):
        return destino == origen or (destino == "REAL" and origen == "ENTERO")

    def analizar_sentencia(self, tokens):
        """Devuelve (descripción, ok)."""
        self.toks, self.i = tokens, 0
        n_err = len(self.errores)

        # Declaración: TIPO ID
        if tokens[0][0] == "TIPO":
            tipo = TIPOS[tokens[0][1]]
            nombre = tokens[1][1]
            if nombre in self.tabla:
                self._error(f"declaración duplicada: '{nombre}' ya fue declarado como {self.tabla[nombre]}")
                return "declaración", False
            self.tabla[nombre] = tipo
            return f"declaración -> {nombre}: {tipo}", True

        # Asignación: ID = expresión
        if len(tokens) > 1 and tokens[0][0] == "ID" and tokens[1][1] == "=":
            nombre = tokens[0][1]
            self.i = 2
            t_expr = self._expresion()
            if nombre not in self.tabla:
                self._error(f"el identificador '{nombre}' no fue declarado")
                return "asignación", False
            t_var = self.tabla[nombre]
            if t_expr is None:
                return "asignación", False
            if not self._compatible(t_var, t_expr):
                self._error(f"tipos incompatibles: no se puede asignar {t_expr} a '{nombre}' ({t_var})")
                return f"asignación -> variable {t_var} / expresión {t_expr}", False
            return f"asignación -> variable {t_var} / expresión {t_expr}", True

        # Expresión suelta
        t = self._expresion()
        ok = len(self.errores) == n_err
        return (f"expresión -> tipo {t}" if ok else "expresión"), ok

    def analizar(self, codigo, mostrar=True):
        sentencias = [s.strip() for s in codigo.split(";") if s.strip()]
        resultados = []
        for s in sentencias:
            n_antes = len(self.errores)
            desc, ok = self.analizar_sentencia(tokenizar(s + ";")[:-1])
            resultados.append((s + ";", desc, ok, self.errores[n_antes:]))
        if mostrar:
            self.informe(resultados)
        return resultados

    def informe(self, resultados):
        print("  Tabla de símbolos:")
        if self.tabla:
            for nombre, tipo in self.tabla.items():
                print(f"    {nombre:<12} {tipo}")
        else:
            print("    (vacía)")
        print("  Análisis sentencia por sentencia:")
        for src, desc, ok, errs in resultados:
            print(f"    [{'VÁLIDA  ' if ok else 'INVÁLIDA'}] {src:<26} {desc}")
            for e in errs:
                print(f"               └─ error semántico: {e}")
        if self.errores:
            print(f"  RESULTADO: RECHAZADO ({len(self.errores)} error/es semántico/s). "
                  "No continúa a la siguiente etapa.")
        else:
            print("  RESULTADO: ACEPTADO. Puede continuar a la siguiente etapa.")

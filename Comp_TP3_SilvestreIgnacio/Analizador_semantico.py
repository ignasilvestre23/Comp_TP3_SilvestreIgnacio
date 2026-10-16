"""
Etapa 3 - ANÁLISIS SEMÁNTICO
Entrada : árbol sintáctico producido por el analizador sintáctico.
Salida  : tabla de símbolos, tipo de cada expresión, errores semánticos y veredicto.

Reglas del lenguaje (las del enunciado del TP3):
  + entre numéricos (ENTERO/REAL) o entre CADENA   |  - * /  solo numéricos
  > < >= <=  solo numéricos -> BOOLEANO            |  == !=  mismo tipo -> BOOLEANO
  Asignación: tipos iguales, o ENTERO -> REAL (conversión implícita sin pérdida)
"""
from Analizador_sintactico import (Literal, Ident, BinOp, Declaracion, Asignacion,
                                   prefijo, texto)

NUMERICOS = {"ENTERO", "REAL"}
NOMBRE_TIPO = {"TIPO_ENTERO": "ENTERO", "TIPO_REAL": "REAL",
               "TIPO_CADENA": "CADENA", "TIPO_BOOLEANO": "BOOLEANO"}


class AnalizadorSemantico:
    def __init__(self):
        self.tabla = {}       # identificador -> tipo
        self.errores = []
        self.pasos = []       # (operación, tipo) de la sentencia en curso

    def _error(self, msg):
        self.errores.append(msg)
        return None

    # ---- tipo de una operación binaria
    def _regla(self, op, a, b):
        num = a in NUMERICOS and b in NUMERICOS
        res = "REAL" if "REAL" in (a, b) else "ENTERO"
        if op == "+":
            if num:
                return res
            if a == b == "CADENA":
                return "CADENA"
            return self._error(f"el operador '+' solo se aplica entre numéricos o entre cadenas (recibió {a} y {b})")
        if op in ("-", "*", "/"):
            return res if num else self._error(f"el operador '{op}' requiere operandos numéricos (recibió {a} y {b})")
        if op in (">", "<", ">=", "<="):
            return "BOOLEANO" if num else self._error(f"el operador '{op}' requiere operandos numéricos (recibió {a} y {b})")
        if op in ("==", "!="):
            return "BOOLEANO" if a == b else self._error(f"el operador '{op}' compara valores del mismo tipo (recibió {a} y {b})")
        return self._error(f"operador desconocido '{op}'")

    # ---- tipo de una expresión (de las hojas hacia la raíz)
    def _tipo(self, e):
        if isinstance(e, Literal):
            return e.tipo
        if isinstance(e, Ident):
            if e.nombre not in self.tabla:
                return self._error(f"el identificador '{e.nombre}' no fue declarado")
            return self.tabla[e.nombre]
        izq, der = self._tipo(e.izq), self._tipo(e.der)
        if izq is None or der is None:
            return None
        t = self._regla(e.op, izq, der)
        if t:
            self.pasos.append((prefijo(e), t))
        return t

    # ---- sentencias
    def _declaracion(self, s):
        nombre, tipo = s.ident.lexema, NOMBRE_TIPO[s.tipo_token.tipo]
        if nombre in self.tabla:
            self._error(f"declaración duplicada: '{nombre}' ya fue declarado como {self.tabla[nombre]}")
            return "declaración"
        self.tabla[nombre] = tipo
        return f"declaración -> {nombre}: {tipo}"

    def _asignacion(self, s):
        nombre = s.ident.lexema
        t_expr = self._tipo(s.expr)
        if nombre not in self.tabla:
            self._error(f"el identificador '{nombre}' no fue declarado")
            return "asignación"
        t_var = self.tabla[nombre]
        if t_expr is None:
            return "asignación"
        if not (t_var == t_expr or (t_var == "REAL" and t_expr == "ENTERO")):
            self._error(f"tipos incompatibles: no se puede asignar {t_expr} a '{nombre}' ({t_var})")
        return f"asignación -> variable {t_var} / expresión {t_expr}"

    def analizar(self, programa, mostrar=True):
        resultados = []
        for s in programa:
            n, self.pasos = len(self.errores), []
            if isinstance(s, Declaracion):
                desc = self._declaracion(s)
            elif isinstance(s, Asignacion):
                desc = self._asignacion(s)
            else:
                t = self._tipo(s.expr)
                desc = f"expresión -> tipo {t}" if t else "expresión"
            resultados.append((s, desc, self.errores[n:], list(self.pasos)))
        if mostrar:
            self.informe(resultados)
        return resultados

    def informe(self, resultados):
        print("ETAPA 3 - ANÁLISIS SEMÁNTICO\n")
        print("  Tabla de símbolos:")
        for nombre, tipo in self.tabla.items():
            print(f"    {nombre:<14} {tipo}")
        if not self.tabla:
            print("    (vacía)")
        print("\n  Sentencia por sentencia:")
        for s, desc, errs, pasos in resultados:
            marca = "INVÁLIDA" if errs else "VÁLIDA  "
            print(f"    [{marca}] {texto(s.tokens):<28} {desc}")
            if len(pasos) > 1:
                print("               tipo de cada operación: " +
                      "; ".join(f"{op} -> {t}" for op, t in pasos))
            for e in errs:
                print(f"               error semántico: {e}")
                print("               token(s) encontrados: " + " ".join(str(t) for t in s.tokens))
        print()
        if self.errores:
            print(f"  RESULTADO FINAL: RECHAZADO ({len(self.errores)} error/es semántico/s). "
                  "No continúa a la siguiente etapa de la compilación.")
        else:
            print("  RESULTADO FINAL: ACEPTADO. Puede continuar a la siguiente etapa de la compilación.")

"""
TP3 - Compiladores | Ejercicio 9: Expresiones complejas
"""
from Analizador_semantico import AnalizadorSemantico

CODIGO = """
    entero edad; entero experiencia; real sueldo; real bono;
    edad + experiencia; sueldo + bono; sueldo + experiencia;
    edad * experiencia + 10; sueldo / 2 + bono;
"""

if __name__ == "__main__":
    print("EJERCICIO 9 - Expresiones complejas")
    print("=" * 60)
    AnalizadorSemantico().analizar(CODIGO)

"""
TP3 - Compiladores | Ejercicio 5: Expresiones aritméticas
"""
from Analizador_semantico import AnalizadorSemantico

CODIGO = """
    entero edad; entero años; real promedio;
    edad + años; edad * 2; promedio + edad; promedio / 2;
"""

if __name__ == "__main__":
    print("EJERCICIO 5 - Expresiones aritméticas")
    print("=" * 60)
    AnalizadorSemantico().analizar(CODIGO)

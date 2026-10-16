"""
TP3 - Compiladores | Ejercicio 8: Análisis de un bloque
"""
from Analizador_semantico import AnalizadorSemantico

CODIGO = """
    entero edad; real altura; cadena nombre;
    edad = 25; altura = 1.83; nombre = "Juan";
    edad = nombre; altura = edad + 10;
"""

if __name__ == "__main__":
    print("EJERCICIO 8 - Análisis de un bloque")
    print("=" * 60)
    AnalizadorSemantico().analizar(CODIGO)

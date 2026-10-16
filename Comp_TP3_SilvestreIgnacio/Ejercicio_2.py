"""
TP3 - Compiladores | Ejercicio 2: Asignaciones compatibles
"""
from Analizador_semantico import AnalizadorSemantico

CODIGO = """
    int edad; float altura; String nombre;
    edad = 25; altura = 1.83; nombre = "Juan";
"""

if __name__ == "__main__":
    print("EJERCICIO 2 - Asignaciones compatibles")
    print("=" * 60)
    AnalizadorSemantico().analizar(CODIGO)

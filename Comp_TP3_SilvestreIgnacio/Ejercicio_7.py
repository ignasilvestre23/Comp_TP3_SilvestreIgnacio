"""
TP3 - Compiladores | Ejercicio 7: Declaración duplicada
"""
from Analizador_semantico import AnalizadorSemantico

CODIGO = """
    int edad; float altura; String nombre; int edad;
"""

if __name__ == "__main__":
    print("EJERCICIO 7 - Declaración duplicada")
    print("=" * 60)
    AnalizadorSemantico().analizar(CODIGO)

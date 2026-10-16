"""
TP3 - Compiladores | Ejercicio 1: Identificación de tipos
"""
from Analizador_semantico import AnalizadorSemantico

CODIGO = """
    int edad; float altura; String nombre; boolean activo;
"""

if __name__ == "__main__":
    print("EJERCICIO 1 - Identificación de tipos")
    print("=" * 60)
    AnalizadorSemantico().analizar(CODIGO)

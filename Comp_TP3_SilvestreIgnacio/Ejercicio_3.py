"""
TP3 - Compiladores | Ejercicio 3: Incompatibilidad de tipos
"""
from Analizador_semantico import AnalizadorSemantico

CODIGO = """
    int edad; String nombre; float altura;
    edad = "Juan"; nombre = 25; altura = "1.83";
"""

if __name__ == "__main__":
    print("EJERCICIO 3 - Incompatibilidad de tipos")
    print("=" * 60)
    AnalizadorSemantico().analizar(CODIGO)

"""
TP3 - Compiladores | Ejercicio 6: Operadores y tipos
"""
from Analizador_semantico import AnalizadorSemantico

CODIGO = """
    int edad; String nombre; boolean activo;
    edad + 10; nombre + " Perez"; edad > 18; activo == verdadero; nombre > 10;
"""

if __name__ == "__main__":
    print("EJERCICIO 6 - Operadores y tipos")
    print("=" * 60)
    AnalizadorSemantico().analizar(CODIGO)

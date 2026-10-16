"""
TP3 - Compiladores | Ejercicio 4: Identificadores no declarados
"""
from Analizador_semantico import AnalizadorSemantico

CODIGO = """
    int edad; float altura; String nombre;
    edad = 25; peso = 70; nombre = "Juan"; altura = 1.83;
"""

if __name__ == "__main__":
    print("EJERCICIO 4 - Identificadores no declarados")
    print("=" * 60)
    AnalizadorSemantico().analizar(CODIGO)

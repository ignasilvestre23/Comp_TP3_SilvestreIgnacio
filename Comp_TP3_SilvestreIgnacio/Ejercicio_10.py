"""
TP3 - Compiladores | Ejercicio 10: Integral
"""
from Analizador_semantico import AnalizadorSemantico

CODIGO = """
    int edad; float altura; float peso; String nombre; boolean activo;
    edad = 25; altura = 1.83; peso = 70.5; nombre = "Juan"; activo = verdadero;
    edad = altura; peso = edad + 10; nombre = edad; activo = edad > 18;
"""

if __name__ == "__main__":
    print("EJERCICIO 10 - Integral")
    print("=" * 60)
    AnalizadorSemantico().analizar(CODIGO)

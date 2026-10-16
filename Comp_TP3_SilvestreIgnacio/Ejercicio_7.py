"""
TP3 - Compiladores | Ejercicio 7: Declaración duplicada
Nota: las expresiones sueltas llevan ';' al final para que cierren como sentencia.
"""
from Compilador import ejecutar

CODIGO = """
    int edad;
    float altura;
    String nombre;
    int edad;
"""

if __name__ == "__main__":
    ejecutar("EJERCICIO 7 - Declaración duplicada", CODIGO)

"""
TP3 - Compiladores | Ejercicio 1: Identificación de tipos
Nota: las expresiones sueltas llevan ';' al final para que cierren como sentencia.
"""
from Compilador import ejecutar

CODIGO = """
    int edad;
    float altura;
    String nombre;
    boolean activo;
"""

if __name__ == "__main__":
    ejecutar("EJERCICIO 1 - Identificación de tipos", CODIGO)

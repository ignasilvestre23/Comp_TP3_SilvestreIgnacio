"""
TP3 - Compiladores | Ejercicio 3: Detección de incompatibilidad de tipos
Nota: las expresiones sueltas llevan ';' al final para que cierren como sentencia.
"""
from Compilador import ejecutar

CODIGO = """
    int edad;
    String nombre;
    float altura;
    edad = "Juan";
    nombre = 25;
    altura = "1.83";
"""

if __name__ == "__main__":
    ejecutar("EJERCICIO 3 - Detección de incompatibilidad de tipos", CODIGO)

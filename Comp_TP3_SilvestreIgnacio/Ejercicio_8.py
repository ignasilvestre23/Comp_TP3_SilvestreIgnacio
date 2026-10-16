"""
TP3 - Compiladores | Ejercicio 8: Análisis semántico de un bloque
Nota: las expresiones sueltas llevan ';' al final para que cierren como sentencia.
"""
from Compilador import ejecutar

CODIGO = """
    entero edad;
    real altura;
    cadena nombre;

    edad = 25;
    altura = 1.83;
    nombre = "Juan";

    edad = nombre;
    altura = edad + 10;
"""

if __name__ == "__main__":
    ejecutar("EJERCICIO 8 - Análisis semántico de un bloque", CODIGO)

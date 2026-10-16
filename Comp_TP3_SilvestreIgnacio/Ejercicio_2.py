"""
TP3 - Compiladores | Ejercicio 2: Asignaciones compatibles
Nota: las expresiones sueltas llevan ';' al final para que cierren como sentencia.
"""
from Compilador import ejecutar

CODIGO = """
    int edad;
    float altura;
    String nombre;
    edad = 25;
    altura = 1.83;
    nombre = "Juan";
"""

if __name__ == "__main__":
    ejecutar("EJERCICIO 2 - Asignaciones compatibles", CODIGO)

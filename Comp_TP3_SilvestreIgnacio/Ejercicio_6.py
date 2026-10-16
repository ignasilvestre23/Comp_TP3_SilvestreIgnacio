"""
TP3 - Compiladores | Ejercicio 6: Operadores y tipos
Nota: las expresiones sueltas llevan ';' al final para que cierren como sentencia.
"""
from Compilador import ejecutar

CODIGO = """
    int edad;
    String nombre;
    boolean activo;
    edad + 10;
    nombre + " Perez";
    edad > 18;
    activo == verdadero;
    nombre > 10;
"""

if __name__ == "__main__":
    ejecutar("EJERCICIO 6 - Operadores y tipos", CODIGO)

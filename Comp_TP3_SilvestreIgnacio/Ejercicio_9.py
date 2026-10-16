"""
TP3 - Compiladores | Ejercicio 9: Análisis semántico con expresiones complejas
Nota: las expresiones sueltas llevan ';' al final para que cierren como sentencia.
"""
from Compilador import ejecutar

CODIGO = """
    entero edad;
    entero experiencia;
    real sueldo;
    real bono;
    edad + experiencia;
    sueldo + bono;
    sueldo + experiencia;
    edad * experiencia + 10;
    sueldo / 2 + bono;
"""

if __name__ == "__main__":
    ejecutar("EJERCICIO 9 - Análisis semántico con expresiones complejas", CODIGO)

"""
TP3 - Compiladores | Ejercicio 5: Expresiones aritméticas
Nota: las expresiones sueltas llevan ';' al final para que cierren como sentencia.
"""
from Compilador import ejecutar

CODIGO = """
    entero edad;
    entero años;
    real promedio;
    edad + años;
    edad * 2;
    promedio + edad;
    promedio / 2;
"""

if __name__ == "__main__":
    ejecutar("EJERCICIO 5 - Expresiones aritméticas", CODIGO)

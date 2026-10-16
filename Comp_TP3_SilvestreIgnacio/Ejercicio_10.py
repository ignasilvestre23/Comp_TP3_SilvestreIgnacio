"""
TP3 - Compiladores | Ejercicio 10: Integral
Nota: las expresiones sueltas llevan ';' al final para que cierren como sentencia.
"""
from Compilador import ejecutar

CODIGO = """
    int edad;
    float altura;
    float peso;
    String nombre;
    boolean activo;

    edad = 25;
    altura = 1.83;
    peso = 70.5;
    nombre = "Juan";
    activo = verdadero;

    edad = altura;
    peso = edad + 10;
    nombre = edad;
    activo = edad > 18;
"""

if __name__ == "__main__":
    ejecutar("EJERCICIO 10 - Integral", CODIGO)

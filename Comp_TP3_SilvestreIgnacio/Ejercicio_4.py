"""
TP3 - Compiladores | Ejercicio 4: Uso de identificadores no declarados
Nota: las expresiones sueltas llevan ';' al final para que cierren como sentencia.
"""
from Compilador import ejecutar

CODIGO = """
    int edad;
    float altura;
    String nombre;
    edad = 25;
    peso = 70;
    nombre = "Juan";
    altura = 1.83;
"""

if __name__ == "__main__":
    ejecutar("EJERCICIO 4 - Uso de identificadores no declarados", CODIGO)

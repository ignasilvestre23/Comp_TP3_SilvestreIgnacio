"""
Encadena las tres etapas: léxico -> sintáctico -> semántico.
La salida de cada etapa es la entrada de la siguiente.
"""
from Analizador_lexico import AnalizadorLexico, ErrorLexico
from Analizador_sintactico import AnalizadorSintactico, ErrorSintactico
from Analizador_semantico import AnalizadorSemantico


def ejecutar(titulo, codigo):
    print("=" * 76)
    print(titulo)
    print("=" * 76)
    print("CÓDIGO FUENTE:")
    for linea in codigo.strip().splitlines():
        print("   ", linea.strip())
    print()
    try:
        tokens = AnalizadorLexico().analizar(codigo)           # texto   -> tokens
        arbol = AnalizadorSintactico().analizar(tokens)         # tokens  -> árbol
    except (ErrorLexico, ErrorSintactico) as e:
        print(f"ERROR ({type(e).__name__}): {e}")
        print("El programa se rechaza: no llega al análisis semántico.")
        return
    AnalizadorSemantico().analizar(arbol)                       # árbol   -> semántica

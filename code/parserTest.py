import ply.yacc as yacc 
from lexerTest import tokens

# Regla para suma y resta, CORRECTAMENTE dividida en varias líneas
def p_expresion(p):
    '''
    expresion : expresion PLUS termino
              | expresion MINUS termino
    '''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    else:
        p[0] = p[1] - p[3]

# Expresión que es solo un término
def p_expresion_termino(p):
    'expresion : termino'
    p[0] = p[1]
    
# Término que es un número
def p_termino_num(p):
    'termino : NUM'
    p[0] = p[1]
    
# Error de sintaxis
def p_error(p):
    print("error de sintaxis")

# Crear el parser
parser = yacc.yacc()

# Programa principal
if __name__ == '__main__':
    while True:
        try:
            s = input('calc > ')
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)
        print(result)

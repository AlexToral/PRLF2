import ply.lex as lex
from uploadXML import XMLLoader as XML

tokens = [
    'LT', 'GT', 'SLASH',
    'TAG_NAME',
    'ATTRIBUTE_NAME',
    'EQUALS',
    'ATTRIBUTE_VALUE'
]

# Tokens simples
t_LT = r'<'
t_EQUALS = r'='
t_ignore = ' \t \n'

# Tokens más complejos

def t_GT(t):
    r'>'
    print(f"Token GT encontrado: {t}")
    return t

def t_SLASH(t):
    r'/'
    print(f"Token SLASH encontrado: {t}")
    return t

def t_TAG_NAME(t):
    r'cfdi:[A-Za-z_][A-Za-z0-9_:.-]*'
    return t

def t_ATTRIBUTE_NAME(t):
    r'[A-Za-z_][A-Za-z0-9_:.-]*'
    return t

def t_ATTRIBUTE_VALUE(t):
    r'"[^"]*"'
    return t

def t_error(t):
    print(f"[LÉXICO] Caracter ilegal: '{t.value[0]}'")
    t.lexer.skip(1)

# Construir lexer
lexer = lex.lex()

# Prueba
if __name__ == "__main__":
    xml = XML("./XML'S/A-252.xml")
    xml.cargar()
    data = xml.contenido  # acceder directamente al contenido, no a mostrar_contenido()

    lexer.input(data)
    print("\n[TOKENS ENCONTRADOS]:\n")
    for token in lexer:
        print(token)

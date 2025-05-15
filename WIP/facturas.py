import ply.lex as lex
from uploadXML import XMLLoader as XML

tokens = [
    'LT', 'GT', 'SLASH', 'SLASH_GT',
    'TAG_NAME', 'ATTRIBUTE_NAME',
    'EQUALS', 'ATTRIBUTE_VALUE'
]

# Orden correcto: tokens más específicos primero
def t_SLASH_GT(t):
    r'/>'  
    return t

# Tokens simples
t_LT = r'<'
t_GT = r'>'
t_SLASH = r'/'
t_EQUALS = r'='
t_ignore = ' \t\n'

# Tokens complejos
def t_TAG_NAME(t):
    r'cfdi:[A-Za-z_][A-Za-z0-9_:.-]*'
    return t

def t_ATTRIBUTE_NAME(t):
    r'[A-Za-z_][A-Za-z0-9_:.-]*'
    return t

def t_ATTRIBUTE_VALUE(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]  # Elimina las comillas
    return t

def t_error(t):
    print(f"[LÉXICO] Caracter ilegal: '{t.value[0]}'")
    t.lexer.skip(1)

# Construir lexer
lexer = lex.lex()

# Prueba
if __name__ == "__main__":
    xml = XML("./XML'S/test.xml")
    xml.cargar()
    data = xml.contenido

    lexer.input(data)
    print("\n[TOKENS ENCONTRADOS]:\n")
    for token in lexer:
        print(token)

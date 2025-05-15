import ply.lex as lex
from uploadXML import XMLLoader as XML

tokens = [
    "LT",
    "GT",
    "SLASH",
    "SLASH_GT",
    "TAG_NAME",
    "ATTRIBUTE_NAME",
    "EQUALS",
    "ATTRIBUTE_VALUE"
]


# Tokens
def t_SLASH_GT(t):
    r'/>'  # debe ir primero
    return t

def t_LT(t):
    r'<'
    return t

def t_GT(t):
    r'>'
    return t

def t_SLASH(t):
    r'/'
    return t

def t_EQUALS(t):
    r'='
    return t

t_ignore = ' \t\n'

# Tokens complejo

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

# Test

if __name__ == "__main__":
    xml = XML("./XML'S/test.xml")
    xml.cargar()
    data = xml.contenido
    lexer.input(data)
    for token in lexer:
        print(token)

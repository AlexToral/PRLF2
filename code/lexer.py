import ply.lex as lex

tokens = [
    "MENOR" # <
    "MAYOR" # >
    "SLASH" # /
    "IGUAL" # =
    "COMILLAS" # "
    "NOMBRE_TAG" # cfdi:Receptor  | cfdi:Comprobante
    "TEXTO" # texto
]

t_MENOR = r'<'
t_MAYOR = r'>'
t_SLASH = r'/'
t_IGUAL = r'='
t_COMILLAS = r'"'

def t_NOMBRE_TAG(t):
    r'cfdi:[a-zA-Z_][a-zA-Z0-9_:.-]*'
    return t

def t_VALOR(t):
    r'[^<>"=\s]+'
    return t

t_ignore = ' \t\n'

def t_error(t):
    print(f"[LÉXICO] Carácter inválido: {t.value[0]}")
    t.lexer.skip(1)
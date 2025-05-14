import ply.lex as lex

tokens = ("NUM", "PLUS","MINUS")

t_PLUS = r'\+'
t_MINUS = r'-'

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t'

def t_error(t):
    print(f"Caracter ilegal: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()



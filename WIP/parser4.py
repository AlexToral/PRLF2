import ply.yacc as yacc
from facturas import tokens  # Importa los tokens desde tu lexer
from uploadXML import XMLLoader as XML

# Reglas de precedencia (si es necesario)
precedence = ()

# Reglas gramaticales
def p_comprobante(p):
    '''comprobante : LT TAG_NAME atributos GT emisor receptor conceptos LT SLASH TAG_NAME GT'''

    if p[2] != 'cfdi:Comprobante' or p[10] != 'cfdi:Comprobante':
        print("❌ Error: Las etiquetas de apertura y cierre de Comprobante no coinciden")
    else:
        print(f"{p[2]}: ✅ Comprobante estructurado correctamente")

def p_emisor(p):
    '''emisor : LT TAG_NAME atributos SLASH GT
                | LT TAG_NAME atributos SLASH_GT'''
    if p[2] != 'cfdi:Emisor':
        print("❌ Error: Se esperaba <cfdi:Emisor />")
    else:
        print(f"{p[2]}: ✅ Emisor correcto")

def p_receptor(p):
    '''receptor : LT TAG_NAME atributos SLASH GT
        | LT TAG_NAME atributos SLASH_GT'''
    if p[2] != 'cfdi:Receptor':
        print("❌ Error: Se esperaba <cfdi:Receptor />")
    else:
        print(f"{p[2]}:✅ Receptor correcto")

def p_conceptos(p):
    '''conceptos : LT TAG_NAME GT concepto LT SLASH TAG_NAME GT'''
    if p[2] != 'cfdi:Conceptos' or p[7] != 'cfdi:Conceptos':
        print("❌ Error: <cfdi:Conceptos> mal estructurado")
    else:
        print(f"{p[2]}:✅ Conceptos correcto")

def p_concepto(p):
    '''concepto : LT TAG_NAME atributos SLASH GT
                | LT TAG_NAME atributos SLASH_GT'''
    if p[2] != 'cfdi:Concepto':
        print("❌ Error: Se esperaba <cfdi:Concepto />")
    else:
        print(f"{p[2]}: ✅ Concepto correcto")


def p_atributos(p):
    '''atributos : atributo atributos
                 | atributo'''
    # Acepta múltiples atributos

def p_atributo(p):
    '''atributo : ATTRIBUTE_NAME EQUALS ATTRIBUTE_VALUE'''
    pass  # Aquí podrías verificar semánticamente los nombres y formatos si quieres

# Regla de error
def p_error(p):
    if p:
        print(f"❌ la linea es: {p} Error de sintaxis en '{p.value}'")
    else:
        print("❌ Error de sintaxis al final del archivo")


# Construir el parser
parser = yacc.yacc()

# Prueba
if __name__ == "__main__":
    from facturas import lexer
    xml = XML("./XML'S/Version4.xml")
    xml.cargar()
    data = xml.contenido
    test_input = data
    lexer.input(test_input)
    parser.parse(test_input, lexer=lexer)

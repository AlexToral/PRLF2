import ply.yacc as yacc
from uploadXML import XMLLoader as XML
from lexer4 import tokens

# Variables globales del parser
valid = True
emisor_attrs = {}
receptor_attrs = {}

# Reglas sintácticas

def p_tag_autocontenida(p):
    'tag : LT TAG_NAME atributos SLASH_GT'
    # Manejar <cfdi:Emisor ... />
    p[0] = {'tag': p[2], 'attrs': p[3], 'children': []}


def p_comprobante(p):
    '''
    comprobante : LT TAG_NAME atributos GT emisor receptor conceptos LT SLASH TAG_NAME GT
    '''
    if p[2] != 'cfdi:Comprobante' or p[10] != 'cfdi:Comprobante':
        print(" Las etiquetas <cfdi:Comprobante> no coinciden")
        global valid
        valid = False
    else:
        print("[SINTÁCTICO] ✅ Nodo <cfdi:Comprobante> estructuralmente correcto")

def p_emisor(p):
    'emisor : LT TAG_NAME atributos SLASH_GT'
    global valid, emisor_attrs
    if p[2] != 'cfdi:Emisor':
        print("[SINTÁCTICO] ❌ Se esperaba <cfdi:Emisor>")
        valid = False
    else:
        emisor_attrs = p[3]
        print("[SINTÁCTICO] ✅ Nodo <cfdi:Emisor> correcto")

def p_receptor(p):
    'receptor : LT TAG_NAME atributos SLASH_GT'
    global valid, receptor_attrs
    if p[2] != 'cfdi:Receptor':
        print("[SINTÁCTICO] ❌ Se esperaba <cfdi:Receptor>")
        valid = False
    else:
        receptor_attrs = p[3]
        print("[SINTÁCTICO] ✅ Nodo <cfdi:Receptor> correcto")

def p_conceptos(p):
    'conceptos : LT TAG_NAME GT concepto LT SLASH TAG_NAME GT'
    global valid
    if p[2] != 'cfdi:Conceptos' or p[7] != 'cfdi:Conceptos':
        
        print("[SINTÁCTICO] ❌ Etiquetas <cfdi:Conceptos> no coinciden")
        valid = False
    else:
        print("[SINTÁCTICO] ✅ Nodo <cfdi:Conceptos> correcto")

def p_concepto(p):
    'concepto : LT TAG_NAME atributos SLASH_GT'
    global valid
    if p[2] != 'cfdi:Concepto':
        print("[SINTÁCTICO] ❌ Se esperaba <cfdi:Concepto>")
        valid = False
    else:
        print("[SINTÁCTICO] ✅ Nodo <cfdi:Concepto> correcto")

def p_atributos(p):
    '''
    atributos : atributo atributos
              | atributo
              | empty
    '''
    if len(p) == 3:
        p[0] = {**p[1], **p[2]}
    elif len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = {}

def p_atributo(p):
    'atributo : ATTRIBUTE_NAME EQUALS ATTRIBUTE_VALUE'
    p[0] = {p[1]: p[3]}

def p_empty(p):
    'empty :'
    p[0] = {}

def p_error(p):
    global valid
    if p:
        print(f"[SINTÁCTICO] ❌ Error de sintaxis en: {p}")
    else:
        print("[SINTÁCTICO] ❌ Error de sintaxis al final del archivo")
    valid = False

# Construcción del parser
parser = yacc.yacc()

if __name__ == "__main__":
    from lexer4 import lexer
    xml = XML("./XML'S/test.xml")
    xml.cargar()
    data = xml.contenido
    test_input = data

    # Reset variables antes del parseo
    valid = True
    emisor_attrs = {}
    receptor_attrs = {}

    parser.parse(test_input, lexer=lexer)

    if not valid:
        print("[SEMÁNTICO] ❌ El archivo contiene errores sintácticos.")
    else:
        errores = []
        if "Rfc" not in emisor_attrs or emisor_attrs["Rfc"] == "":
            errores.append("El atributo obligatorio Rfc está ausente o vacío en <cfdi:Emisor>.")
        if "Rfc" not in receptor_attrs or receptor_attrs["Rfc"] == "":
            errores.append("El atributo obligatorio Rfc está ausente o vacío en <cfdi:Receptor>.")

        if errores:
            print("[SEMÁNTICO] ❌ El archivo es inválido por las siguientes razones:")
            for e in errores:
                print(f" - {e}")
        else:
            print("[SEMÁNTICO] ✅ El archivo CFDI es válido.")

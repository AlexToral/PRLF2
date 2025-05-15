import ply.yacc as yacc
from uploadXML import XMLLoader as XML
from lexer4 import tokens

# Variables globales del parser
valid = True
emisor_attrs = {}
receptor_attrs = {}

# Reglas sintácticas

def p_comprobante(p):
    '''comprobante : LT TAG_NAME atributos GT emisor receptor conceptos LT SLASH TAG_NAME GT'''
    global valid
    if p[2] != 'cfdi:Comprobante' or p[10] != 'cfdi:Comprobante':
        print("[SINTÁCTICO] ❌ Las etiquetas <cfdi:Comprobante> no coinciden")
        valid = False
    else:
        attrs = p[3]
        esperados = ['Version', 'Fecha', 'Total', 'SubTotal', 'Moneda', 'TipoDeComprobante', 'LugarExpedicion', 'Exportacion', 'xmlns:cfdi']
        faltantes = [a for a in esperados if a not in attrs]
        if faltantes:
            print(f"[SEMÁNTICO] ❌ Faltan atributos en <cfdi:Comprobante>: {', '.join(faltantes)}")
            valid = False
        else:
            print("[SINTÁCTICO] ✅ Nodo <cfdi:Comprobante> correcto con atributos válidos")

def p_emisor(p):
    'emisor : LT TAG_NAME atributos SLASH_GT'
    global valid
    if p[2] != 'cfdi:Emisor':
        print("[SINTÁCTICO] ❌ Nodo <cfdi:Emisor> incorrecto")
        valid = False
    else:
        esperados = ['Rfc', 'Nombre', 'RegimenFiscal']
        faltantes = [a for a in esperados if a not in p[3]]
        if faltantes:
            print(f"[SEMÁNTICO] ❌ Faltan atributos en <cfdi:Emisor>: {', '.join(faltantes)}")
            valid = False
        else:
            print("[SINTÁCTICO] ✅ Nodo <cfdi:Emisor> correcto")


def p_receptor(p):
    'receptor : LT TAG_NAME atributos SLASH_GT'
    global valid
    if p[2] != 'cfdi:Receptor':
        print("[SINTÁCTICO] ❌ Nodo <cfdi:Receptor> incorrecto")
        valid = False
    else:
        esperados = ['Rfc', 'Nombre', 'DomicilioFiscalReceptor', 'RegimenFiscalReceptor', 'UsoCFDI']
        faltantes = [a for a in esperados if a not in p[3]]
        if faltantes:
            print(f"[SEMÁNTICO] ❌ Faltan atributos en <cfdi:Receptor>: {', '.join(faltantes)}")
            valid = False
        else:
            print("[SINTÁCTICO] ✅ Nodo <cfdi:Receptor> correcto")

def p_conceptos(p):
    'conceptos : LT TAG_NAME GT lista_conceptos LT SLASH TAG_NAME GT'
    global valid
    if p[2] != 'cfdi:Conceptos' or p[6] != 'cfdi:Conceptos':
        print("[SINTÁCTICO] ❌ Etiquetas <cfdi:Conceptos> no coinciden")
        valid = False
    else:
        print("[SINTÁCTICO] ✅ Nodo <cfdi:Conceptos> correcto")

def p_lista_conceptos(p):
    '''lista_conceptos : lista_conceptos concepto
                       | concepto'''

def p_concepto(p):
    'concepto : LT TAG_NAME atributos SLASH_GT'
    global valid
    if p[2] != 'cfdi:Concepto':
        print("[SINTÁCTICO] ❌ Se esperaba <cfdi:Concepto>")
        valid = False
    else:
        esperados = ['ClaveProdServ', 'Cantidad', 'ClaveUnidad', 'Descripcion', 'ValorUnitario', 'Importe']
        faltantes = [attr for attr in esperados if attr not in p[3]]
        if faltantes:
            print(f"[SEMÁNTICO] ❌ Faltan atributos en <cfdi:Concepto>: {', '.join(faltantes)}")
            valid = False
        else:
            print("[SINTÁCTICO] ✅ Nodo <cfdi:Concepto> correcto")

def p_atributos(p):
    '''atributos : atributos atributo
                 | atributo'''
    if len(p) == 2:
        p[0] = dict([p[1]])
    else:
        p[0] = p[1]
        p[0].update([p[2]])

def p_atributo(p):
    'atributo : ATTRIBUTE_NAME EQUALS ATTRIBUTE_VALUE'
    p[0] = (p[1], p[3].strip('"'))


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

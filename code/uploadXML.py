class XMLLoader:
    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo
        self.contenido = ""

    def cargar(self):
        try:
            with open(self.ruta_archivo, 'r', encoding='utf-8') as archivo:
                lineas = archivo.readlines()

                # Omitir la línea que inicia con "<?xml"
                self.contenido = ''.join(
                    linea for linea in lineas if not linea.strip().startswith("<?xml")
                )

                print("[INFO] Archivo cargado correctamente.\n")
        except FileNotFoundError:
            print(f"[ERROR] No se encontró el archivo: {self.ruta_archivo}")
        except Exception as e:
            print(f"[ERROR] Ocurrió un problema al leer el archivo: {e}")

# Uso de ejemplo
if __name__ == "__main__":
    ruta_origen = "./XML'S/A-252.xml"

    xml = XMLLoader(ruta_origen)
    xml.cargar()
    Data = xml.contenido
    print(Data)

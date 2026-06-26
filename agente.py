import os
from dotenv import load_dotenv
from pypdf import PdfReader
from langchain_groq import ChatGroq

# Cargar la clave API desde el archivo .env
load_dotenv()

# Obtener la clave API
clave_api = os.environ.get("GROQ_API_KEY")
if not clave_api:
    raise ValueError("GROQ_API_KEY no encontrada en .env")

# Crear conexión con el modelo
modelo = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=clave_api,
    temperature=0
)

print("Conexión con el modelo creada correctamente")

# Función para leer el contenido del PDF y devolverlo como texto
def leer_documento(ruta_pdf):
    try:
        lector = PdfReader(ruta_pdf)                                # En la variable lector se guarda el contenido del PDF utilizando la clase PdfReader
        texto_completo = ""                                         
        for pagina in lector.pages:                                 # Ciclo que recorre cada pagina del PDF por medio de la variable lector que utiliza el .pages para acceder a cada pagina
            texto_completo += pagina.extract_text()                 # Se extrae el texto de cada página y se concatena al texto_completo
        return texto_completo
    except FileNotFoundError as fe:
        print("No se encontró el archivo del documento.")
        print("El error fue:", fe)
        return ""

# Función para limpiar la pregunta del usuario (mayúsculas/minúsculas mezcladas, espacios extra)
def limpiar_pregunta(texto):
    texto_limpio = " ".join(texto.lower().split())
    return texto_limpio

# Prueba de la función
ruta_documento = "documentos/PoliticasJosephsInnovations.pdf"
contenido_documento = leer_documento(ruta_documento)
print(limpiar_pregunta("   HOLA   Como ESTAS  "))
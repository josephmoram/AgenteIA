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
        lector = PdfReader(ruta_pdf)
        texto_completo = ""
        for pagina in lector.pages:
            texto_completo += pagina.extract_text()
        return texto_completo
    except FileNotFoundError as fe:
        print("No se encontró el archivo del documento.")
        print("El error fue:", fe)
        return ""

# Prueba de la función
ruta_documento = "documentos/PoliticasJosephsInnovations.pdf"
contenido_documento = leer_documento(ruta_documento)
print(contenido_documento[:100])
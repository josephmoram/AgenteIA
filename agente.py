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

# Función que recibe una pregunta y responde usando el documento como contexto
def preguntar_al_agente(pregunta, contexto):
    instruccion_sistema = f"""Eres el asistente virtual de Joseph's Innovations, una tienda
    en línea que vende laptops, accesorios y artículos de tecnología en Costa Rica.

    Reglas que debes seguir siempre:
    1. Respondé únicamente con la información que aparece en el documento de abajo.
    2. Nunca menciones que existe un documento, una base de datos o un archivo. Simplemente
    da la respuesta como si la supieras de memoria, como parte de tu trabajo en la tienda.
    3. Si la persona te saluda (hola, buenas, cómo estás, etc.), respondé el saludo de forma
    breve y cordial, y preguntale cuál es su consulta.
    4. Si la pregunta no tiene relación con Joseph's Innovations ni con la información
    disponible, respondé de forma cordial que solo podés responder preguntas relacionadas
    con la empresa Joseph's Innovations.
    5. Después de dar una respuesta sobre la empresa, preguntá amablemente si hay algo más
    en lo que puedas ayudar.

    Información de la empresa:
    {contexto}"""

    mensajes = [
        {"role": "system", "content": instruccion_sistema},
        {"role": "user", "content": pregunta}
    ]

    respuesta = modelo.invoke(mensajes)
    return respuesta.content

# Agente IA que responde preguntas sobre las políticas, devoluciones, garantías y productos de la tienda Joseph's Innovations
if __name__ == "__main__":
    ruta_documento = "documentos/PoliticasJosephsInnovations.pdf"               # Ruta del documento PDF que contiene la información de la empresa
    contenido_documento = leer_documento(ruta_documento)                        # Se llama la función leer_documento para obtener el contenido del PDF y se guarda en la variable contenido_documento

    # Ciclo que solicita al usuario una pregunta hasta que se ingrese una pregunta válida (no vacía)
    pregunta_limpia = ""
    while pregunta_limpia == "":
        pregunta = input("Escribe una pregunta sobre las políticas, devoluciones, garantías o productos de la tienda Joseph's Innovations: ")
        pregunta_limpia = limpiar_pregunta(pregunta)
        if pregunta_limpia == "":
            print("Pregunta vacía. Escribe algo para consultar.")

    try:
        respuesta = preguntar_al_agente(pregunta_limpia, contenido_documento)
        print(f"Pregunta: {pregunta}")
        print(f"Respuesta: {respuesta}")
    except Exception as error:
        print("Ocurrió un error al consultar al agente.")
        print("El error fue:", error)
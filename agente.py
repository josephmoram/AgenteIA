import os
from dotenv import load_dotenv
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
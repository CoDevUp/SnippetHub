# Importando la url del .env
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Cargar las variables de entorno
load_dotenv()

# Leer la URL desde el archivo .env
MONGO_URL = "mongodb+srv://jhonaguirre1:638123MARIO@cluster0.7bm1rsu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Crear el cliente y base de datos
client = AsyncIOMotorClient(MONGO_URL)
db = client["snippetHub_app"]
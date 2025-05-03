
# Importando la url del .env

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Cargar las variables de entorno
load_dotenv()

# Leer la URL desde el archivo .env
MONGO_URL = os.getenv("MONGO_URL")

# Crear el cliente y base de datos
client = AsyncIOMotorClient(MONGO_URL)
db = client["snippetHub_app"]
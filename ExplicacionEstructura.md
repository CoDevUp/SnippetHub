🔸 main.py
Es el punto de entrada de la aplicación FastAPI.
Aquí registras los routers (users, snippets, etc.).
Aquí se configura el middleware, CORS, y arranca el servidor.

🔸 database.py
Responsable de la conexión y configuración de la base de datos.
Centraliza la sesión (SessionLocal) y engine de SQLAlchemy.
Permite usar Depends(get_db) en tus rutas.

🔸 models.py
Define las tablas de la base de datos (con SQLAlchemy).
Cada clase representa una tabla: User, Snippet, etc.
Aquí defines relaciones (ForeignKey, relationship).
Se usa para generar el esquema de base de datos.

🔸 routers/
Contiene los módulos que agrupan las rutas (endpoints).
users.py: registro, login, obtener perfil.
snippets.py: crear, editar, listar snippets.


🔸 schemas/
Contiene los modelos de entrada y salida para la API (con Pydantic).
user.py: modelos como UserCreate, UserRead, UserLogin.
snippet.py: SnippetCreate, SnippetOut, etc.

➡️ Esto separa la lógica de validación/datos del modelo real de la BD (models.py), que puede tener campos sensibles como contraseñas hash.

🔸 frontend/
Contiene el HTML, CSS y JS del cliente.

index.html: muestra los snippets, comentarios, etc.

login.html y register.html: formularios de autenticación.

scripts.js: maneja peticiones fetch() a la API (login, creación de snippets, etc).

➡️ Así puedes trabajar el frontend de forma independiente del backend. En un futuro podrías incluso migrar esto a React o Vue sin cambiar el backend.
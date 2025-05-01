#Registar un usuario (sin base de datos por el momento)
#Se realiza en la memoria por el momento

class User:
    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password = password   #aun no se encripta la contraseña



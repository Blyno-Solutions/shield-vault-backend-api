from cryptography.fernet import Fernet


class SecurityService:

    def __init__(self, key: bytes):
        self.fernet = Fernet(key)

    def encrypt(self, data: str) -> str:
        encrypted = self.fernet.encrypt(data.encode())
        return encrypted.decode()

    def decrypt(self, token: str) -> str:
        decrypted = self.fernet.decrypt(token.encode())
        return decrypted.decode()

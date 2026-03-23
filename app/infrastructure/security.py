import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from typing import Optional, Union
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SecurityService:
    def __init__(self, key: Optional[bytes] = None):
        if key is None:
            self.key = Fernet.generate_key()
            logger.warning(
                "No encryption key provided. Generated a new key for development."
            )
        else:
            self.key = key
        self.fernet = Fernet(self.key)

    @classmethod
    def from_password(
        cls, password: str, salt: Optional[bytes] = None
    ) -> "SecurityService":
        if salt is None:
            salt = os.urandom(16)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return cls(key)

    def encrypt(self, data: Union[str, bytes]) -> bytes:
        if not data:
            raise ValueError("Cannot encrypt empty data")

        if isinstance(data, str):
            data_bytes = data.encode("utf-8")
        elif isinstance(data, bytes):
            data_bytes = data
        else:
            raise TypeError(f"Expected str or bytes, got {type(data).__name__}")

        try:
            encrypted = self.fernet.encrypt(data_bytes)
            return encrypted
        except Exception as e:
            logger.error(f"Encryption failed: {str(e)}")
            raise

    def decrypt(self, encrypted_data: bytes) -> str:
        if not encrypted_data:
            raise ValueError("Cannot decrypt empty data")

        try:
            decrypted_bytes = self.fernet.decrypt(encrypted_data)
            decrypted = decrypted_bytes.decode("utf-8")
            return decrypted
        except Exception as e:
            logger.error(f"Decryption failed: {str(e)}")
            raise ValueError("Decryption failed: Invalid key or corrupted data")

    def encrypt_file(self, file_path: str, output_path: Optional[str] = None) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        if output_path is None:
            output_path = file_path + ".encrypted"

        with open(file_path, "rb") as f:
            file_data = f.read()

        encrypted_data = self.encrypt(file_data)

        with open(output_path, "wb") as f:
            f.write(encrypted_data)

        return output_path

    def decrypt_file(self, file_path: str, output_path: Optional[str] = None) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        if output_path is None:
            if file_path.endswith(".encrypted"):
                output_path = file_path[:-10]
            else:
                output_path = file_path + ".decrypted"

        with open(file_path, "rb") as f:
            encrypted_data = f.read()

        decrypted_data = self.decrypt(encrypted_data)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(decrypted_data)

        return output_path

    def get_key_base64(self) -> str:
        return base64.urlsafe_b64encode(self.key).decode("utf-8")

    @staticmethod
    def validate_key(key: bytes) -> bool:
        try:
            Fernet(key)
            return True
        except Exception:
            return False

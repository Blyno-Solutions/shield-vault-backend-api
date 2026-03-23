import os
import base64
from typing import Optional, Union, Tuple
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SecurityService:
    KEY_SIZE = 32
    NONCE_SIZE = 12

    def __init__(self, key: Optional[bytes] = None):
        if key is None:
            self.key = os.urandom(self.KEY_SIZE)
            logger.info("Generated new AES-256 key")
        else:
            if len(key) != self.KEY_SIZE:
                raise ValueError(f"Key must be {self.KEY_SIZE} bytes for AES-256")
            self.key = key
        self._aesgcm = AESGCM(self.key)

    @classmethod
    def from_password(
        cls, password: str, salt: Optional[bytes] = None
    ) -> Tuple["SecurityService", bytes]:
        if salt is None:
            salt = os.urandom(16)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=cls.KEY_SIZE,
            salt=salt,
            iterations=480000,
        )
        key = kdf.derive(password.encode())
        return cls(key), salt

    def encrypt(self, data: Union[str, bytes]) -> bytes:
        if not data:
            raise ValueError("Cannot encrypt empty data")

        if isinstance(data, str):
            data_bytes = data.encode("utf-8")
        else:
            data_bytes = data

        nonce = os.urandom(self.NONCE_SIZE)
        ciphertext = self._aesgcm.encrypt(nonce, data_bytes, None)
        return nonce + ciphertext

    def decrypt(self, encrypted_data: bytes) -> bytes:
        if not encrypted_data:
            raise ValueError("Cannot decrypt empty data")

        if len(encrypted_data) < self.NONCE_SIZE:
            raise ValueError("Decryption failed: Invalid key or corrupted data")

        nonce = encrypted_data[: self.NONCE_SIZE]
        ciphertext = encrypted_data[self.NONCE_SIZE :]

        try:
            plaintext = self._aesgcm.decrypt(nonce, ciphertext, None)
            return plaintext
        except Exception:
            raise ValueError("Decryption failed: Invalid key or corrupted data")

    def decrypt_to_string(self, encrypted_data: bytes) -> str:
        return self.decrypt(encrypted_data).decode("utf-8")

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

        logger.info(f"File encrypted: {file_path} -> {output_path}")
        return output_path

    def decrypt_file(self, file_path: str, output_path: Optional[str] = None) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        if output_path is None:
            output_path = file_path.replace(".encrypted", ".decrypted")

        with open(file_path, "rb") as f:
            encrypted_data = f.read()

        decrypted_data = self.decrypt(encrypted_data)

        with open(output_path, "wb") as f:
            f.write(decrypted_data)

        logger.info(f"File decrypted: {file_path} -> {output_path}")
        return output_path

    def get_key_base64(self) -> str:
        return base64.urlsafe_b64encode(self.key).decode("utf-8")

    @staticmethod
    def validate_key(key: bytes) -> bool:
        return len(key) == SecurityService.KEY_SIZE

    @staticmethod
    def generate_key() -> bytes:
        return os.urandom(SecurityService.KEY_SIZE)

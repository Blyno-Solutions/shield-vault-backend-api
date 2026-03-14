import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
import tempfile
from app.infrastructure.security import SecurityService

class TestSecurityService:
    def setup_method(self):
        self.service = SecurityService()
        self.test_string = "Hello, Shield Vault!"
        self.test_bytes = b"Hello, Shield Vault!"
    
    def test_encrypt_decrypt_string_success(self):
        encrypted = self.service.encrypt(self.test_string)
        assert encrypted != self.test_string.encode()
        assert isinstance(encrypted, bytes)
        decrypted = self.service.decrypt(encrypted)
        assert decrypted == self.test_string
    
    def test_encrypt_decrypt_bytes_success(self):
        encrypted = self.service.encrypt(self.test_bytes)
        decrypted = self.service.decrypt(encrypted)
        assert decrypted == self.test_string
    
    def test_empty_string_encryption(self):
        with pytest.raises(ValueError, match="Cannot encrypt empty data"):
            self.service.encrypt("")
    
    def test_empty_bytes_encryption(self):
        with pytest.raises(ValueError, match="Cannot encrypt empty data"):
            self.service.encrypt(b"")
    
    def test_empty_data_decryption(self):
        with pytest.raises(ValueError, match="Cannot decrypt empty data"):
            self.service.decrypt(b"")
    
    def test_invalid_key_decryption(self):
        encrypted = self.service.encrypt(self.test_string)
        wrong_service = SecurityService()
        with pytest.raises(ValueError, match="Decryption failed"):
            wrong_service.decrypt(encrypted)
    
    def test_invalid_data_type_encryption(self):
        with pytest.raises(TypeError):
            self.service.encrypt(123)
    
    def test_corrupted_data_decryption(self):
        encrypted = self.service.encrypt(self.test_string)
        corrupted = bytearray(encrypted)
        corrupted[10] = corrupted[10] ^ 0xFF
        corrupted = bytes(corrupted)
        with pytest.raises(ValueError, match="Decryption failed"):
            self.service.decrypt(corrupted)
    
    def test_very_long_string(self):
        long_string = "A" * 1000000
        encrypted = self.service.encrypt(long_string)
        decrypted = self.service.decrypt(encrypted)
        assert decrypted == long_string
    
    def test_special_characters(self):
        special = "!@#$%^&*()_+{}[]|\\:;\"'<>,.?/~`你好🌍"
        encrypted = self.service.encrypt(special)
        decrypted = self.service.decrypt(encrypted)
        assert decrypted == special
    
    def test_key_validation(self):
        valid_key = self.service.key
        assert SecurityService.validate_key(valid_key) is True
        invalid_key = b"not a valid key"
        assert SecurityService.validate_key(invalid_key) is False
    
    def test_password_derived_key(self):
        password = "my-secret-password"
        service = SecurityService.from_password(password)
        encrypted = service.encrypt(self.test_string)
        decrypted = service.decrypt(encrypted)
        assert decrypted == self.test_string
    
    def test_file_encryption_decryption(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write(self.test_string)
            temp_file = f.name
        
        try:
            encrypted_file = self.service.encrypt_file(temp_file)
            assert os.path.exists(encrypted_file)
            
            decrypted_file = self.service.decrypt_file(encrypted_file)
            assert os.path.exists(decrypted_file)
            
            with open(decrypted_file, 'r') as f:
                content = f.read()
            assert content == self.test_string

            if os.path.exists(encrypted_file):
                os.unlink(encrypted_file)
            if os.path.exists(decrypted_file):
                os.unlink(decrypted_file)
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_nonexistent_file_encryption(self):
        with pytest.raises(FileNotFoundError):
            self.service.encrypt_file("nonexistent_file.txt")
    
    def test_get_key_base64(self):
        key_b64 = self.service.get_key_base64()
        assert isinstance(key_b64, str)
        assert len(key_b64) > 0

class TestSecurityServiceEdgeCases:
    def test_unicode_strings(self):
        service = SecurityService()
        test_strings = [
            "Hello, 世界",
            "🌍🌎🌏",
            "𝕿𝖍𝖊 𝖖𝖚𝖎𝖈𝖐 𝖇𝖗𝖔𝖜𝖓 𝖋𝖔𝖝",
            "∮ E⋅da = Q,  n → ∞, ∑ f(i) = ∏ g(i)",
        ]
        for test_string in test_strings:
            encrypted = service.encrypt(test_string)
            decrypted = service.decrypt(encrypted)
            assert decrypted == test_string
    
    def test_multiple_encryptions_same_data(self):
        service = SecurityService()
        data = "Same data"
        encrypted1 = service.encrypt(data)
        encrypted2 = service.encrypt(data)
        assert encrypted1 != encrypted2
        assert service.decrypt(encrypted1) == data
        assert service.decrypt(encrypted2) == data
    
    def test_very_large_data(self):
        service = SecurityService()
        large_data = "X" * 10_000_000
        encrypted = service.encrypt(large_data)
        decrypted = service.decrypt(encrypted)
        assert decrypted == large_data
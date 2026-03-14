from cryptography.fernet import Fernet
from app.infrastructure.security_service import SecurityService


def test_encrypt_decrypt():
    key = Fernet.generate_key()
    service = SecurityService(key)

    data = "hello"
    encrypted = service.encrypt(data)
    decrypted = service.decrypt(encrypted)

    assert decrypted == data


def test_empty_string():
    key = Fernet.generate_key()
    service = SecurityService(key)

    data = ""
    encrypted = service.encrypt(data)
    decrypted = service.decrypt(encrypted)

    assert decrypted == data


def test_wrong_key():
    key1 = Fernet.generate_key()
    key2 = Fernet.generate_key()

    service1 = SecurityService(key1)
    service2 = SecurityService(key2)

    data = "secret"
    encrypted = service1.encrypt(data)

    try:
        service2.decrypt(encrypted)
        assert False
    except Exception:
        assert True

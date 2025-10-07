# -*- coding: utf-8 -*-
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.backends import default_backend
import keyring
import getpass
import os
import base64

class AESEncryption:
    """
    Clase para manejar cifrado AES-CBC con HMAC-SHA256
    Formato: IV(16) + HMAC(32) + Ciphertext(variable)
    """
    def __init__(self, key: bytes):
        self.key = key
        self.backend = default_backend()
    
    def encrypt(self, plaintext: bytes) -> bytes:
        """Cifra datos usando AES-CBC + HMAC-SHA256"""
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        plaintext_padded = self._pad_pkcs7(plaintext)
        ciphertext = encryptor.update(plaintext_padded) + encryptor.finalize()
        
        h = hmac.HMAC(self.key, hashes.SHA256(), backend=self.backend)
        h.update(iv + ciphertext)
        mac = h.finalize()
        
        return iv + mac + ciphertext
    
    def decrypt(self, ciphertext: bytes) -> bytes:
        """Descifra datos usando AES-CBC + HMAC-SHA256"""
        if len(ciphertext) < 48:
            raise ValueError("Ciphertext too short")
        
        iv = ciphertext[:16]
        mac = ciphertext[16:48]
        encrypted_data = ciphertext[48:]
        
        h = hmac.HMAC(self.key, hashes.SHA256(), backend=self.backend)
        h.update(iv + encrypted_data)
        try:
            h.verify(mac)
        except Exception:
            raise ValueError("HMAC verification failed - data may be corrupted")
        
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(encrypted_data) + decryptor.finalize()
        return self._unpad_pkcs7(padded_plaintext)
    
    def _pad_pkcs7(self, data: bytes, block_size: int = 16) -> bytes:
        """Aplica padding PKCS7"""
        padding_length = block_size - (len(data) % block_size)
        padding = bytes([padding_length] * padding_length)
        return data + padding
    
    def _unpad_pkcs7(self, data: bytes) -> bytes:
        """Quita padding PKCS7"""
        if len(data) == 0:
            raise ValueError("Cannot unpad empty data")
        padding_length = data[-1]
        if padding_length > 16 or padding_length == 0:
            raise ValueError("Invalid padding")
        return data[:-padding_length]

def get_encryption_key():
    """Obtiene la clave de encriptación desde el keyring del sistema"""
    service_name = "KeyPass"
    username = getpass.getuser()
    
    try:
        key_str = keyring.get_password(service_name, username)
        
        if key_str:
            key = base64.b64decode(key_str)
        else:
            key = os.urandom(32)
            keyring.set_password(service_name, username, base64.b64encode(key).decode('utf-8'))
            
    except Exception as e:
        raise Exception(f"Failed to access system keyring: {e}. Please ensure keyring is properly configured.")
    
    return AESEncryption(key)

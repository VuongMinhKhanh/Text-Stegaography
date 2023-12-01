import pyAesCrypt
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding


def encrypt_file(text, key):
    text = text.encode('utf-8')
    padder = padding.PKCS7(128).padder()  # assuming AES block size is 128 bits

    padded_data = padder.update(text) + padder.finalize()

    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(key),
                    modes.CFB(iv),
                    backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return iv + ciphertext


def decrypt_file(ciphertext, key):
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]

    cipher = Cipher(algorithms.AES(key),
                    modes.CFB(iv),
                    backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Use PKCS7 unpadding
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(decrypted_data) + unpadder.finalize()

    return plaintext.decode('utf-8')
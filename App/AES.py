import pyAesCrypt
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding


def encrypt_file(input_file, output_file, key):
    with open(input_file, 'rb') as file:
        plaintext = file.read()

    padder = padding.PKCS7(128).padder()  # assuming AES block size is 128 bits

    padded_data = padder.update(plaintext) + padder.finalize()

    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key),
                    modes.CFB(iv),
                    backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    with open(output_file, 'wb') as file:
        file.write(iv + ciphertext)


# Hàm giải mã file
def decrypt_file(input_file, output_file, key):
    with open(input_file, 'rb') as file:
        data = file.read()

    iv = data[:16]
    ciphertext = data[16:]

    cipher = Cipher(algorithms.AES(key),
                    modes.CFB(iv),
                    backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(
        128).unpadder()  # assuming AES block size is 128 bits
    plaintext = unpadder.update(decrypted_data) + unpadder.finalize()

    with open(output_file, 'wb') as file:
        file.write(plaintext)


filename = "file.txt"
key = os.urandom(32)
encrypt_file(filename, filename + '.enc', key)

decrypt_file(filename + '.enc', filename + '.dec', key)

from aes import AES
import os

if __name__ == "__main__":
    plaintext = "The lazy dog jumps over the brown fox"
    key = os.urandom(16)
    # iv = os.urandom(16)
    iv = b'\x00' * 16
    aes = AES(key)
    ciphertext = aes.encrypt(plaintext.encode(), iv)
    # ! This is not the same as plaintext !! DEBUG
    decrypted = aes.decrypt(ciphertext, iv)

    print(plaintext, ciphertext, decrypted)

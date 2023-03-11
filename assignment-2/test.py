from aes import AES

if __name__ == "__main__":
    zeros = b'0' * 16
    key = zeros
    iv = zeros
    plaintext = "hello world!"
    aes = AES(key)
    ciphertext = aes.encrypt(plaintext.encode(), iv)
    decrypted = aes.decrypt(ciphertext, iv)
    print(plaintext, ciphertext, decrypted)

from aes import AES
from tabulate import tabulate

if __name__ == "__main__":

    # First input pair
    # key = bytes([0x7e, 0xca, 0x58, 0x88, 0x41, 0xe2, 0xbf,
    #             0x67, 0x44, 0xbd, 0xec, 0xb3, 0x83, 0x17, 0xe5, 0xe3])
    # iv = bytes([0x4e, 0x68, 0x83, 0x64, 0xdf, 0x24, 0xa7,
    #            0x97, 0x2e, 0xcd, 0x11, 0xc0, 0x5c, 0x4c, 0x92, 0xb])

    # Second input pair
    key = bytes([0xd3, 0xcc, 0x34, 0x60, 0xae, 0xec, 0xe7, 0x78,
                 0x33, 0xd7, 0x16, 0x5d, 0x2e, 0x9a, 0x7b, 0xba])
    iv = bytes([0xa9, 0xaa, 0xf9, 0xa3, 0x7f, 0x57, 0x7d, 0x93,
                0x3, 0x26, 0x9, 0x52, 0xf6, 0x8b, 0xf4, 0xf])

    print("Key:")
    print(tabulate([[hex(i) for i in key]], tablefmt="fancy_grid"))
    print("IV:")
    print(tabulate([[hex(i) for i in iv]], tablefmt="fancy_grid"))

    plaintext = "Hello, world!"
    aes = AES(key)
    ciphertext = aes.encrypt(plaintext.encode(), iv)
    decrypted = aes.decrypt(ciphertext, iv)
    print(f"Plaintext: {plaintext}")
    print(f"Ciphertext: {ciphertext}")
    print(f"Decrypted Ciphertext: {decrypted.decode()}")

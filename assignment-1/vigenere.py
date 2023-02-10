import itertools
import string


def encrypt(plaintext, key):
    # Shift each letter in plaintext by the corresponding letter in key
    key_iter = itertools.cycle(map(ord, key))
    ciphertext = ""
    for letter in plaintext:
        if letter in string.ascii_lowercase:
            ciphertext += chr(ord('a') + (
                (next(key_iter) - ord('a') + ord(letter) -
                    ord('a') + 2) % 26))
        else:
            ciphertext += letter
    return ciphertext


def decrypt(ciphertext, key):
    # Decryption is the same as encryption, but with the inverse key
    key_inv = ""
    for k in key:
        key_inv += chr(ord('a') + (22 - (ord(k) - ord('a'))) % 26)
    return encrypt(ciphertext, key_inv)


def brute_force_solve(ciphertext, key_length):
    pass


if __name__ == "__main__":
    c1 = encrypt("hello hi how are you", "abcd")
    p1 = decrypt(c1, "abcd")
    print(c1, p1)

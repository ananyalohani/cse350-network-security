import itertools
import string
from random import choice

PLAINTEXT_LENGTH = 512  # Always a multiple of N
N = 8  # Number of columns in the hash table
M = PLAINTEXT_LENGTH // N  # Number of N-bit blocks in the input


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


def is_recognizable(plaintext):
    # Return True if plaintext p satisfies p = (s, Hash(s))
    s = plaintext[:PLAINTEXT_LENGTH]
    hash_s = plaintext[PLAINTEXT_LENGTH:]
    if hash_fn(s) == hash_s:
        return True
    return False


def hash_fn(plaintext):
    # Return a plaintext p that satisfies p = (s, Hash(s))
    p_hash = ['' for _ in range(M)]
    for i in range(M):
        p_hash[i] = plaintext[i * N]
        for j in range(1, N):
            p_hash[i] = chr(ord('a') + (ord(p_hash[i]) - ord('a') +
                            ord(plaintext[i * N + j]) - ord('a')) % 26)
    return ''.join(p_hash)


def brute_force_solve(ciphertext, key_length):
    pass


if __name__ == "__main__":
    plaintexts = [(''.join(choice(string.ascii_lowercase)
                           for _ in range(PLAINTEXT_LENGTH))) for _ in range(5)]
    plaintexts = [(p + hash_fn(p)) for p in plaintexts]
    ciphertexts = [encrypt(p, "abcd") for p in plaintexts]
    decrypted = [decrypt(c, "abcd") for c in ciphertexts]
    print([plaintexts[i] == decrypted[i] for i in range(len(plaintexts))])

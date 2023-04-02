import random
import hashlib
import math
import json
import base64


def hash(message):
    return hashlib.sha256(message.encode("utf-8")).hexdigest()


def is_prime(n):
    if n == 2:
        return True
    if n % 2 == 0 or n <= 1:
        return False

    sqr = int(math.sqrt(n)) + 1

    for divisor in range(3, sqr, 2):
        if n % divisor == 0:
            return False
    return True


def generate_key_pair():
    primes = []
    for i in range(3, 1000):
        if is_prime(i):
            primes.append(i)
    p = random.choice(primes)
    q = random.choice(primes)
    while p == q:
        q = random.choice(primes)
    n = p * q
    phi_n = (p - 1) * (q - 1)

    while True:
        e = random.randrange(2, phi_n)
        if gcd(e, phi_n) == 1:
            break

    d = modinv(e, phi_n)

    public_key = (n, e)
    private_key = (n, d)
    return public_key, private_key


def encrypt(message, public_key):
    hashed = hash(message)
    message = message.encode("utf-8")

    n, e = public_key
    block_size = get_block_size(n)
    padded_blocks = []

    for i in range(0, len(message), block_size):
        block = message[i : i + block_size]
        padded_block = pad(block, block_size)
        padded_blocks.append(padded_block)

    encrypted_blocks = []
    for block in padded_blocks:
        int_message = int.from_bytes(block, "big")
        int_ciphertext = pow(int_message, e, n)
        encrypted_block = int_ciphertext.to_bytes(get_num_bytes(n), "big")
        encrypted_blocks.append(encrypted_block)

    ciphertext = b"".join(encrypted_blocks)
    print("e", str(ciphertext))
    ciphertext = base64.b64encode(ciphertext).decode("ascii")
    return json.dumps({"hash": hashed, "message": ciphertext})


def decrypt(encrypted, private_key):
    encrypted = json.loads(encrypted)
    hashed = encrypted["hash"]
    ciphertext = encrypted["message"]
    ciphertext = base64.b64decode(ciphertext)
    print("d", str(ciphertext))

    n, d = private_key
    block_size = get_block_size(n)
    num_blocks = len(ciphertext) // get_num_bytes(n)

    decrypted_blocks = []
    for i in range(num_blocks):
        block = ciphertext[i * get_num_bytes(n) : (i + 1) * get_num_bytes(n)]
        int_ciphertext = int.from_bytes(block, "big")
        int_message = pow(int_ciphertext, d, n)
        decrypted_block = int_message.to_bytes(block_size, "big")
        decrypted_blocks.append(decrypted_block)

    message = b"".join(decrypted_blocks)
    message = unpad(message).decode("utf-8")

    if hash(message) != hashed:
        raise Exception("Invalid signature")

    return message


def pad(message, block_size):
    padding_size = block_size - len(message) % block_size
    padding = b"\x00" * (padding_size - 1) + b"\x01"
    padded_message = message + padding
    return padded_message


def unpad(message):
    i = len(message) - 1
    while message[i] == 0:
        i -= 1
    if message[i] != 1:
        raise ValueError("Invalid padding")
    return message[:i]


def get_block_size(n):
    return (n.bit_length() + 7) // 8


def get_num_bytes(n):
    return (n.bit_length() + 7) // 8


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def modinv(a, m):
    # Computes the modular inverse of a modulo m using the extended Euclidean algorithm
    t, new_t = 0, 1
    r, new_r = m, a

    while new_r != 0:
        quotient = r // new_r
        t, new_t = new_t, t - quotient * new_t
        r, new_r = new_r, r - quotient * new_r

    if r > 1:
        raise ValueError("a is not invertible modulo m")
    if t < 0:
        t = t + m

    return t

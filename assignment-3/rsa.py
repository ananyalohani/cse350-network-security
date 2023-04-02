import hashlib
import random


class RSA:
    def __init__(self):
        primes = [i for i in range(3, 1000) if self.is_prime(i)]
        p = random.choice(primes)
        q = random.choice(primes)
        while p == q:
            q = random.choice(primes)
        self.n = p * q
        self.phi = (p - 1) * (q - 1)
        self.e = self.get_e()
        self.d = self.get_d()
        self.public_key = (self.e, self.n)
        self.private_key = (self.d, self.n)

    def is_prime(self, n):
        for i in range(2, n // 2 + 1):
            if n % i == 0:
                return False
        return True

    def get_e(self):
        for i in range(2, self.phi):
            if self.gcd(i, self.phi) == 1:
                return i

    def get_d(self):
        for i in range(2, self.phi):
            if (i * self.e) % self.phi == 1:
                return i

    def gcd(self, a, b):
        if a == 0:
            return b
        return self.gcd(b % a, a)

    def encrypt(self, m):
        return pow(m, self.e, self.n)

    def decrypt(self, c):
        return pow(c, self.d, self.n)

    def sign(self, m):
        hashed = hashlib.sha256()
        hashed.update(m.encode())
        hashed = int(hashed.hexdigest(), 16)
        return self.encrypt(hashed)

    def verify(self, m, s):
        hashed = hashlib.sha256()
        hashed.update(m.encode())
        hashed = int(hashed.hexdigest(), 16)
        return hashed == self.decrypt(s)

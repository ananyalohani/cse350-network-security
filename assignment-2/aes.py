import galois
from tabulate import tabulate


class AES(object):
    """
    A class that implements the AES encryption algorithm with 10 rounds in CBC mode.

    ...

    Attributes
    ----------
    KEY_SIZE : int
        the size of the key in bytes (16)
    N_ROUNDS : int
        the number of rounds (10)
    SBOX : list
        the S-box used for SubBytes in encryption
    INV_SBOX : list
        the inverse S-box used for SubBytes in decryption
    RC : list
        the round constants used for round key generation

    master_key : bytes
        the master key used for encryption and decryption
    round_keys : list
        the round keys generated from the master key
    gf : galois.Galois
        the Galois field (2**8) used for multiplication in MixColumns

    Methods
    -------
    left_rotate(word) -> bytes :
        Rotates a word (a 4-byte sequence) to the left by one byte.
    bytes_to_blocks(data) -> list :
        Converts a byte string into a list of n-byte blocks.
    blocks_to_bytes(blocks) -> bytes :
        Converts a list of blocks into a byte string.
    xor(a, b) -> bytes :
        Performs the XOR operation between two byte strings of the same length.
    pad_msg(msg) -> bytes :
        Pads a message to a length that is a multiple of 128 bits.
    unpad_msg(msg) -> bytes :
        Removes the padding from a message.

    get_round_keys(key) -> list :
        Generates a list of 11 round keys from the master key.

    add_round_key(state, round_key) -> list :
        Performs the AddRoundKey step of the encryption & decryption process.
    sub_bytes(state, inv=False) -> list :
        Performs the SubBytes step of the encryption & decryption process.
    shift_rows(state, inv=False) -> list :
        Performs the ShiftRows step of the encryption & decryption process.
    mix_columns(state, inv=False) -> list :
        Performs the MixColumns step of the encryption & decryption process.
    encrypt(state, iv) -> bytes :
        Encrypts a message using the AES algorithm in CBC mode.
    decrypt(state, iv) -> bytes :
        Decrypts an encrypted message using the AES algorithm in CBC mode.
    """

    KEY_SIZE = 16
    N_ROUNDS = 10

    SBOX = [
        0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5,
        0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
        0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0,
        0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
        0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC,
        0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
        0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A,
        0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
        0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0,
        0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
        0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B,
        0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
        0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85,
        0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
        0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5,
        0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
        0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17,
        0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
        0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88,
        0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
        0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C,
        0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
        0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9,
        0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
        0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6,
        0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
        0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E,
        0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
        0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94,
        0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
        0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68,
        0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
    ]

    INV_SBOX = [
        0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38,
        0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
        0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87,
        0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
        0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D,
        0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
        0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2,
        0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
        0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16,
        0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
        0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA,
        0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
        0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A,
        0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
        0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02,
        0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
        0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA,
        0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
        0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85,
        0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
        0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89,
        0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
        0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20,
        0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
        0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31,
        0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
        0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D,
        0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
        0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0,
        0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
        0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26,
        0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D
    ]

    RC = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]

    def __init__(self, key):
        """
        Initializes a new instance of the AES class with the given key.

        Parameters:
        key (bytes): A byte string representing the encryption key. Must have a length of 16 bytes.
        """

        assert len(key) == 16, "Key must be 16 bytes long"

        self.master_key = key
        self.round_keys = self.get_round_keys(key)
        self.gf = galois.GF(2**8)

    def left_rotate(self, word):
        """
        Rotates a word (a 4-byte sequence) to the left by one byte.

        Parameters:
        word (bytes): A 4-byte sequence to be rotated.

        Returns:
        bytes: The rotated 4-byte sequence.
        """
        return word[1:] + word[:1]

    def bytes_to_blocks(self, data, n=4):
        """
        Converts a byte string into a list of n-byte blocks.

        Parameters:
        data (bytes): The byte string to be converted into blocks.
        n (int): The number of bytes in each block. Default is 4.

        Returns:
        list: A list of n-byte blocks.
        """
        return [list(data[i:i+n]) for i in range(0, len(data), n)]

    def blocks_to_bytes(self, blocks):
        """
        Converts a list of blocks into a byte string.

        Parameters:
        blocks (list): A list of blocks, where each block is a list of n-byte sequences.

        Returns:
        bytes: The byte string obtained by concatenating the blocks.
        """
        return bytes(sum(blocks, []))

    def xor(self, a, b):
        """
        Performs the XOR operation between two byte strings of the same length.

        Parameters:
        a (bytes): The first byte string.
        b (bytes): The second byte string.

        Returns:
        bytes: The byte string resulting from the XOR operation.
        """
        return bytes(i ^ j for i, j in zip(a, b))

    def pad_msg(self, msg):
        """
        Pads a message to a length that is a multiple of 128 bits.

        Parameters:
        msg (bytes): The byte string representing the message.

        Returns:
        bytes: The padded message.
        """
        pad_len = 16 - len(msg) % 16
        return msg + bytes([pad_len]) * pad_len

    def unpad_msg(self, msg):
        """
        Removes the padding from a message.

        Parameters:
        msg (bytes): The byte string representing the padded message.

        Returns:
        bytes: The unpadded message.
        """
        return msg[:-msg[-1]]

    def get_round_keys(self, key):
        """
        Generates a list of 11 round keys from the master key.

        Parameters:
        key (bytes): The byte string representing the master key.

        Returns:
        list: A list of round keys, where each key is a list of 4 32-bit words.
        """
        key_cols = self.bytes_to_blocks(key)
        i = 0

        while len(key_cols) < (self.N_ROUNDS + 1) * 4:
            word = list(key_cols[-1])

            if len(key_cols) % 4 == 0:
                word = [self.SBOX[b] for b in self.left_rotate(word)]
                word[0] ^= self.RC[i]
                i += 1

            word = self.xor(word, key_cols[-4])
            key_cols.append(list(word))
        return [key_cols[4*i: 4*(i+1)] for i in range(len(key_cols) // 4)]

    def add_round_key(self, state, round_key):
        """
        Performs the AddRoundKey step of the encryption & decryption process.

        Parameters:
        state (list): A matrix representing the current state of the encryption process.
        round_key (bytes): A list representing the round key to be XORed with the state.

        Returns:
        list: The resulting state matrix after the AddRoundKey step.
        """
        for i in range(4):
            for j in range(4):
                state[i][j] ^= round_key[i][j]
        return state

    def sub_bytes(self, state, inv=False):
        """
        Performs the SubBytes step of the encryption & decryption process.

        Parameters:
        state (list): A matrix representing the current state of the encryption process.
        inv (bool): If True, the inverse SubBytes operation is performed for decryption.
        Default is False.

        Returns:
        list: The resulting state matrix after the SubBytes step.
        """
        for i in range(4):
            for j in range(4):
                if not inv:
                    state[i][j] = self.SBOX[state[i][j]]
                else:
                    state[i][j] = self.INV_SBOX[state[i][j]]
        return state

    def shift_rows(self, state, inv=False):
        """
        Performs the ShiftRows step of the encryption & decryption process.

        Parameters:
        state (list): A matrix representing the current state of the encryption process.
        inv (bool): If True, the inverse ShiftRows operation is performed for decryption.
        Default is False.

        Returns:
        list: The resulting state matrix after the ShiftRows step.
        """
        shift = [
            [0, 1, 2, 3],
            [1, 2, 3, 0],
            [2, 3, 0, 1],
            [3, 0, 1, 2]
        ] if not inv else [
            [0, 3, 2, 1],
            [1, 0, 3, 2],
            [2, 1, 0, 3],
            [3, 2, 1, 0]
        ]
        state_copy = [row[:] for row in state]
        for i in range(4):
            for j in range(4):
                state[i][j] = state_copy[shift[i][j]][j]
        return state

    def mix_columns(self, state, inv=False):
        """
        Performs the MixColumns step of the encryption & decryption process.

        Parameters:
        state (list): A matrix representing the current state of the encryption process.
        inv (bool): If True, the inverse MixColumns operation is performed for decryption.
        Default is False.

        Returns:
        list: The resulting state matrix after the MixColumns step.
        """
        mc = self.gf([
            [0x02, 0x03, 0x01, 0x01],
            [0x01, 0x02, 0x03, 0x01],
            [0x01, 0x01, 0x02, 0x03],
            [0x03, 0x01, 0x01, 0x02]
        ] if not inv else [
            [0x0E, 0x0B, 0x0D, 0x09],
            [0x09, 0x0E, 0x0B, 0x0D],
            [0x0D, 0x09, 0x0E, 0x0B],
            [0x0B, 0x0D, 0x09, 0x0E]
        ])
        return [list(map(int, mc @ self.gf(col))) for col in state]

    def encrypt(self, plaintext, iv):
        """
        Encrypts a message using the AES algorithm in CBC mode.

        Parameters:
        plaintext (bytes): The byte string representing the message to be encrypted.
        iv (bytes): The byte string representing the initialization vector. Must have a length of 16 bytes.

        Returns:
        bytes: The byte string representing the encrypted message.
        """
        assert len(iv) == 16, "IV must be 16 bytes long"

        plaintext = self.pad_msg(plaintext)
        plaintext_blocks = self.bytes_to_blocks(plaintext, 16)
        ciphertext_blocks = []
        prev = iv

        block_count = 0
        for block in plaintext_blocks:
            block_count += 1
            tables = []

            state = self.bytes_to_blocks(self.xor(block, prev))
            state = self.add_round_key(state, self.round_keys[0])

            for i in range(1, self.N_ROUNDS):
                state = self.sub_bytes(state)
                state = self.shift_rows(state)
                state = self.mix_columns(state)
                state = self.add_round_key(state, self.round_keys[i])

                if i == 1 or i == 9:
                    transpose = list(map(list, zip(*state)))
                    table = f"\nBlock {block_count}, Encryption Round {i}\n"
                    table += tabulate([[hex(x) for x in row] for row in transpose],
                                      headers=["a0", "a1", "a2", "a3"], tablefmt="fancy_grid")
                    tables.append(table)

            state = self.sub_bytes(state)
            state = self.shift_rows(state)
            state = self.add_round_key(state, self.round_keys[-1])

            block = self.blocks_to_bytes(state)
            ciphertext_blocks.append(block)
            prev = block

            for i in range(len(tables[0].splitlines())):
                for table in tables:
                    print(table.splitlines()[i], end="\t")
                print()
            print()

        return b''.join(ciphertext_blocks)

    def decrypt(self, ciphertext, iv):
        """
        Decrypts an encrypted message using the AES algorithm in CBC mode.

        Parameters:
        ciphertext (bytes): The byte string representing the message to be decrypted.
        iv (bytes): The byte string representing the initialization vector. Must have a length of 16 bytes.

        Returns:
        bytes: The byte string representing the decrypted message.
        """
        assert len(iv) == 16, "IV must be 16 bytes long"
        assert len(
            ciphertext) % 16 == 0, "Ciphertext must be a multiple of 16 bytes"

        ciphertext_blocks = self.bytes_to_blocks(ciphertext, 16)
        plaintext_blocks = []
        prev = iv

        block_count = 0
        for block in ciphertext_blocks:
            block_count += 1
            tables = []

            state = self.bytes_to_blocks(block)
            state = self.add_round_key(state, self.round_keys[-1])
            state = self.shift_rows(state, inv=True)
            state = self.sub_bytes(state, inv=True)

            for i in range(self.N_ROUNDS - 1, 0, -1):
                if i == 1 or i == 9:
                    transpose = list(map(list, zip(*state)))
                    table = f"\nBlock {block_count}, Decryption Round {10 - i}\n"
                    table += tabulate([[hex(x) for x in row] for row in transpose],
                                      headers=["a0", "a1", "a2", "a3"], tablefmt="fancy_grid")
                    tables.append(table)

                state = self.add_round_key(state, self.round_keys[i])
                state = self.mix_columns(state, inv=True)
                state = self.shift_rows(state, inv=True)
                state = self.sub_bytes(state, inv=True)

            state = self.add_round_key(state, self.round_keys[0])
            plaintext_blocks.append(
                self.xor(self.blocks_to_bytes(state), prev))
            prev = block

            for i in range(len(tables[0].splitlines())):
                for table in tables:
                    print(table.splitlines()[i], end="\t")
                print()
            print()

        return self.unpad_msg(b''.join(plaintext_blocks))

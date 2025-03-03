import hashlib

def hash_to_bit_vector(X, bit_length):
    X_bytes = str(X).encode()
    hash_digest = hashlib.sha256(X_bytes).digest()
    bit_vector = ''.join(f'{byte:08b}' for byte in hash_digest)
    return bit_vector[:bit_length]

# #!/usr/bin/env python3
# """124‑bit AES‑GCM encryption with a 30‑digit numeric key + salt.

# The script shows:
# * generation of a random 30‑digit integer (the “password”),
# * derivation of a 124‑bit‑ish key with PBKDF2‑HMAC + a random salt,
# * encryption with AES‑GCM (includes authentication tag),
# * decryption and verification,
# * a tiny demo that encrypts → prints ciphertext → decrypts → prints original.
# """

# install with: pip install cryptography

import os
import base64
import secrets
from typing import Tuple

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


# ----------------------------------------------------------------------
# 1️⃣ 30‑digit numeric key (the “password”) – cryptographically random
# ----------------------------------------------------------------------
def generate_30digit_number() -> int:
    """Return a uniformly distributed integer in the range [10^29, 10^30‑1]."""
    lower = 10**29                # 1_000_000_000_000_000_000_000_000_000
    upper = 10**30 - 1           # 9_999_999_999_999_999_999_999_999_999
    # secrets.randbelow() is inclusive of the bound, so we shift the range.
    return secrets.randbelow(upper - lower + 1) + lower


# ----------------------------------------------------------------------
# 2️⃣ Convert the numeric password →


# 124‑bit key with PBKDF2‑HMAC + salt
# ----------------------------------------------------------------------    
# salt length: 16 bytes (128 bits) is a common choice for PBKDF2


# def derive_key(password: str, salt: bytes, iterations: int = 100_000) -> bytes:
#     """Derive a 124‑bit key from the password and salt using PBKDF2‑HMAC."""
#     # Use SHA256 as the hash function for PBKDF2
#     kdf = PBKDF2HMAC(
#         algorithm=hashes.SHA256(),
#         length=16,  # 16 bytes = 128 bits (we'll truncate to 124 bits later)
#         salt=salt,
#         iterations=iterations,
#     )
#     key = kdf.derive(password.encode())
#     # Truncate to 124 bits (15.5 bytes), but since we can't have half a byte, we take 15 bytes
#     return key[:15]  # Return the first 15 bytes (120 bits) for AES-GCM

# bit length of the key for AES-GCM can be 128, 192, or 256 bits. Since we want 124 bits, we can use a 128-bit key and ignore the last 4 bits. However, AES-GCM requires a key length of either 16 bytes (128 bits), 24 bytes (192 bits), or 32 bytes (256 bits). Therefore, we will derive a 128-bit key and use it for AES-GCM, while ensuring that the effective key length is around 124 bits by using a strong KDF with sufficient iterations.
# We will derive a 128-bit key and use it for AES-GCM, while ensuring that the effective key length is around 124 bits by using a strong KDF with sufficient iterations.
# The key derivation function (KDF) will produce a 128-bit key, but we will consider it as a 124-bit key for our purposes, since the last 4 bits can be ignored without significantly affecting security.
# The salt should be random and unique for each encryption operation to ensure that the same password does not produce the same key, which enhances security against precomputed attacks.
# The number of iterations for PBKDF2 should be sufficiently high (e.g., 100,000 or more) to make brute-force attacks computationally expensive.

# ----------------------------------------------------------------------
# 3️⃣ AES‑GCM encryption (includes authentication tag)
# ----------------------------------------------------------------------
def encrypt(plaintext: bytes, key: bytes) -> Tuple[bytes, bytes, bytes
]:
    """Encrypt the plaintext using AES‑GCM with the given key.

    Returns a tuple of (nonce, ciphertext, tag).
    """
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)  # 12 bytes (96 bits) is a common choice for GCM nonce
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)  # No additional authenticated data
    return nonce, ciphertext[:-16], ciphertext[-16:]  # Split ciphertext and tag

# ----------------------------------------------------------------------\
# 4️⃣ Decryption and verification
# ----------------------------------------------------------------------
# advance encription method with AES-GCM, PBKDF2-HMAC, and a 30-digit numeric key. The code includes functions for generating a random 30-digit number, deriving a key from the password and salt, encrypting plaintext using AES-GCM, and decrypting the ciphertext while verifying its authenticity. The encryption process uses a random nonce and produces an authentication tag to ensure data integrity.
# methouds include:
# - generate_30digit_number(): Generates a random 30-digit integer to be used as a password.
# - derive_key(): Derives a 124-bit key from the password and salt using PBKDF2-HMAC with SHA256.
# - encrypt(): Encrypts the plaintext using AES-GCM with the derived key, returning the nonce, ciphertext, and authentication tag.  
 # 
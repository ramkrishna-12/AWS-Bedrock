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
def derive_key(password: str, salt: bytes, iterations: int = 100_000) -> bytes:
    """Derive a 124‑bit key from the password and salt using PBKDF2‑HMAC."""
    # Use SHA256 as the hash function for PBKDF2
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=16,  # 16 bytes = 128 bits (we'll truncate to 124 bits later)
        salt=salt,
        iterations=iterations,
    )
    key = kdf.derive(password.encode())
    # Truncate to 124 bits (15.5 bytes), but since we can't have half a byte, we take 15 bytes
    return key[:15]  # Return the first 15 bytes (120 bits) for AES-GCM


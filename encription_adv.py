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
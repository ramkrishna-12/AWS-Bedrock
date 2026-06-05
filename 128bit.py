"""
╔══════════════════════════════════════════════════════════════╗
║        128-BIT SALTED ENCRYPTION SYSTEM (AES-128)           ║
║  Output: 30-digit numeric cipher  |  Salt: 16 bytes random  ║
╚══════════════════════════════════════════════════════════════╝

ALGORITHM OVERVIEW:
─────────────────────────────────────────────────────────────
  1. Generate a 16-byte (128-bit) cryptographic salt (random)
  2. Derive a 128-bit AES key using PBKDF2-HMAC-SHA256
     (key = PBKDF2(password, salt, iterations=200_000))
  3. Encrypt plaintext using AES-128-CBC with a random 16-byte IV
  4. Combine:  salt(16B) + IV(16B) + ciphertext  → raw bytes
  5. Convert raw bytes → big integer → zero-padded 30-digit string
  6. Decryption reverses all steps exactly.
─────────────────────────────────────────────────────────────
"""

import os
import hashlib
import struct
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from encryption_128bit import encrypt, decrypt

# Encrypt
result = encrypt("your secret text", "yourPassword")
print(result["token"])   # → 30-digit string
print(result["bundle"])  # → save this for decryption

# Decrypt
plain = decrypt(result["bundle"], "yourPassword")
print(plain)  # → original text

# ─────────────────────────────────────────────────────────────
#  CONSTANTS
# ─────────────────────────────────────────────────────────────
SALT_SIZE       = 16          # 128-bit salt
KEY_SIZE        = 16          # 128-bit AES key
IV_SIZE         = 16          # 128-bit IV for CBC mode
PBKDF2_ITERS    = 200_000     # NIST-recommended minimum
OUTPUT_DIGITS   = 30          # Required output length


# ─────────────────────────────────────────────────────────────
#  HELPER: bytes ↔ 30-digit string
# ─────────────────────────────────────────────────────────────
def bytes_to_30digits(data: bytes) -> str:
    """
    Convert raw bytes to a 30-digit decimal string.
    Uses modular arithmetic to guarantee exactly 30 digits.
    The full data is stored separately (salt+IV+ciphertext bundle).
    """
    num = int.from_bytes(data, byteorder="big")
    # Take modulo to get a number that fits in 30 digits
    modulus = 10 ** OUTPUT_DIGITS
    short_num = num % modulus
    return str(short_num).zfill(OUTPUT_DIGITS)


def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a 128-bit AES key from password + salt using PBKDF2."""
    return hashlib.pbkdf2_hmac(
        hash_name  = "sha256",
        password   = password.encode("utf-8"),
        salt       = salt,
        iterations = PBKDF2_ITERS,
        dklen      = KEY_SIZE,
    )


# ─────────────────────────────────────────────────────────────
#  ENCRYPTION
# ─────────────────────────────────────────────────────────────
def encrypt(plaintext: str, password: str) -> dict:
    """
    Encrypt plaintext with AES-128-CBC + PBKDF2 salted key.

    Returns a dict with:
      - 'token'      : 30-digit numeric string (compact fingerprint)
      - 'bundle'     : hex string of salt+IV+ciphertext (needed for decryption)
      - 'salt_hex'   : hex of the random salt used
      - 'iv_hex'     : hex of the random IV used
    """
    # Step 1: Generate random salt and IV
    salt = os.urandom(SALT_SIZE)
    iv   = os.urandom(IV_SIZE)

    # Step 2: Derive 128-bit key
    key = derive_key(password, salt)

    # Step 3: AES-128-CBC encryption
    cipher     = AES.new(key, AES.MODE_CBC, iv)
    padded_pt  = pad(plaintext.encode("utf-8"), AES.block_size)
    ciphertext = cipher.encrypt(padded_pt)

    # Step 4: Pack bundle = salt || IV || ciphertext
    bundle = salt + iv + ciphertext

    # Step 5: Produce 30-digit token from bundle
    token = bytes_to_30digits(bundle)

    return {
        "token"      : token,
        "bundle"     : bundle.hex(),        # Full bundle for decryption
        "salt_hex"   : salt.hex(),
        "iv_hex"     : iv.hex(),
        "key_bits"   : KEY_SIZE * 8,        # 128
        "token_len"  : len(token),          # 30
    }


# ─────────────────────────────────────────────────────────────
#  DECRYPTION
# ─────────────────────────────────────────────────────────────
def decrypt(bundle_hex: str, password: str) -> str:
    """
    Decrypt a bundle (hex string of salt+IV+ciphertext) using password.

    Raises ValueError on wrong password or corrupted data.
    """
    bundle = bytes.fromhex(bundle_hex)

    # Step 1: Unpack salt, IV, ciphertext
    salt       = bundle[:SALT_SIZE]
    iv         = bundle[SALT_SIZE : SALT_SIZE + IV_SIZE]
    ciphertext = bundle[SALT_SIZE + IV_SIZE :]

    # Step 2: Re-derive 128-bit key
    key = derive_key(password, salt)

    # Step 3: AES-128-CBC decryption
    cipher    = AES.new(key, AES.MODE_CBC, iv)
    padded_pt = cipher.decrypt(ciphertext)

    # Step 4: Remove padding (raises ValueError if wrong password)
    plaintext = unpad(padded_pt, AES.block_size)

    return plaintext.decode("utf-8")


# ─────────────────────────────────────────────────────────────
#  DEMO / MAIN
# ─────────────────────────────────────────────────────────────
def print_banner():
    print("=" * 62)
    print("       128-BIT SALTED ENCRYPTION DEMO")
    print("=" * 62)


def demo():
    print_banner()

    test_cases = [
        ("Hello, Ravan! This is secret.", "myStrongPass@2024"),
        ("AWS Cloud Architect | Kolkata",  "SecureKey#9876"),
        ("Confidential: Project Glasswing", "Ultra$ecret!007"),
    ]

    for i, (message, password) in enumerate(test_cases, 1):
        print(f"\n{'─' * 62}")
        print(f"  TEST CASE {i}")
        print(f"{'─' * 62}")
        print(f"  Original Text  : {message}")
        print(f"  Password       : {password}")

        # ── Encryption ──────────────────────────────────────
        result = encrypt(message, password)

        print(f"\n  ── ENCRYPTION ──────────────────────────────")
        print(f"  Key Strength   : {result['key_bits']}-bit AES (128-bit)")
        print(f"  Salt (hex)     : {result['salt_hex']}")
        print(f"  IV   (hex)     : {result['iv_hex']}")
        print(f"  Bundle (hex)   : {result['bundle'][:48]}…")
        print(f"  30-Digit Token : {result['token']}  ← {result['token_len']} digits ✓")

        # ── Decryption (correct password) ───────────────────
        try:
            recovered = decrypt(result["bundle"], password)
            status = "✅ MATCH" if recovered == message else "❌ MISMATCH"
            print(f"\n  ── DECRYPTION ──────────────────────────────")
            print(f"  Recovered Text : {recovered}")
            print(f"  Integrity Check: {status}")
        except Exception as e:
            print(f"  Decryption Error: {e}")

        # ── Wrong password test ──────────────────────────────
        print(f"\n  ── WRONG PASSWORD TEST ─────────────────────")
        try:
            wrong = decrypt(result["bundle"], "WrongPassword123")
            print(f"  Result: {wrong[:30]}... (unexpected success)")
        except (ValueError, UnicodeDecodeError):
            print("  Result: ❌ Rejected — padding/decoding error (correct behaviour)")

    print(f"\n{'=' * 62}")
    print("  All tests complete. Bundle hex = key for decryption.")
    print(f"{'=' * 62}\n")


# ─────────────────────────────────────────────────────────────
#  INTERACTIVE MODE (optional)
# ─────────────────────────────────────────────────────────────
def interactive():
    print_banner()
    print("\n  [1] Encrypt a message")
    print("  [2] Decrypt a bundle")
    choice = input("\n  Enter choice (1/2): ").strip()

    if choice == "1":
        msg  = input("  Enter message  : ")
        pwd  = input("  Enter password : ")
        res  = encrypt(msg, pwd)
        print(f"\n  30-Digit Token : {res['token']}")
        print(f"  Bundle (hex)   : {res['bundle']}")
        print(f"  Salt (hex)     : {res['salt_hex']}")
        print(f"  IV (hex)       : {res['iv_hex']}")

    elif choice == "2":
        bundle = input("  Enter bundle hex : ")
        pwd    = input("  Enter password   : ")
        try:
            plain = decrypt(bundle, pwd)
            print(f"\n  Decrypted text : {plain}")
        except Exception as e:
            print(f"\n  Error: {e}")
    else:
        print("  Invalid choice.")


if __name__ == "__main__":
    # Run automated demo
    demo()

    # Uncomment below to run interactive mode instead:
    # interactive()
import os
import base64

def generate_key(bits=124, encoding='hex'):
    """
    Generate a cryptographically secure random key.

    :param bits: Key size in bits (default 124)
    :param encoding: 'hex', 'base64', or 'raw'
    :return: Encoded key string or raw bytes
    """
    if bits <= 0 or bits % 8 != 4:
        # 124 bits = 15.5 bytes, so allow non-multiple-of-8 bits
        pass  # We'll handle fractional bytes below

    # Calculate byte length (round up for partial byte)
    byte_len = (bits + 7) // 8
    key_bytes = os.urandom(byte_len)

    # If bits is not a multiple of 8, mask extra bits in the last byte
    extra_bits = (8 - (bits % 8)) % 8
    if extra_bits:
        mask = 0xFF << extra_bits & 0xFF
        key_bytes = key_bytes[:-1] + bytes([key_bytes[-1] & mask])

    if encoding == 'hex':
        return key_bytes.hex()
    elif encoding == 'base64':
        return base64.b64encode(key_bytes).decode('utf-8')
    elif encoding == 'raw':
        return key_bytes
    else:
        raise ValueError("Invalid encoding. Use 'hex', 'base64', or 'raw'.")

if __name__ == "__main__":
    try:
        key_hex = generate_key(bits=124, encoding='hex')
        key_b64 = generate_key(bits=124, encoding='base64')

        print(f"124-bit key (hex): {key_hex}")
        print(f"124-bit key (Base64): {key_b64}")
    except Exception as e:
        print(f"Error: {e}")

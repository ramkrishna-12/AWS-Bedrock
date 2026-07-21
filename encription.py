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

# encription.py is a Python script that provides a function to generate a cryptographically secure random key of a specified bit length. The key can be returned in different encodings: hexadecimal, Base64, or raw bytes. The script includes error handling for invalid encoding options and ensures that the generated key adheres to the specified bit length, even if it is not a multiple of 8. The example usage demonstrates generating and printing a 124-bit key in both hexadecimal and Base64 formats.
# encription with adding salt is a Python script that provides a function to generate a cryptographically secure random key of a specified bit length. The key can be returned in different encodings: hexadecimal, Base64, or raw bytes. The script includes error handling for invalid encoding options and ensures that the generated key adheres to the specified bit length, even if it is not a multiple of 8. The example usage demonstrates generating and printing a 124-bit key in both hexadecimal and Base64 formats.
# salt is a random value added to the key generation process to enhance security. In this script, the salt is not explicitly implemented, but it can be incorporated by combining the generated key with a random salt value before encoding. This would make the key more resistant to attacks, as the same input would produce different outputs due to the added randomness from the salt.
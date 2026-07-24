import secrets

bust = secrets.token_hex(100000000)
print(bust)

# # Python code
# import secrets

# # Function to generate a secure token with a specified number of characters
# def generate_secure_token(length):
#     """
#     Generates a secure hexadecimal token.

#     Parameters:
#     length (int): Number of characters in the token. Note: token_hex() generates
#                   2 characters per byte, so we need length/2 bytes.

#     Returns:
#     str: A secure hexadecimal token.
#     """
#     # Calculate the number of bytes needed
#     num_bytes = (length + 1) // 2  # Add 1 to handle odd lengths
#     token = secrets.token_hex(num_bytes)
#     return token[:length]  # Trim to the exact desired length

# # Example: Generate a 128-character token
# large_token = generate_secure_token(128)

# print("Generated Secure Token:")
# print(large_token)
# print("Length:", len(large_token))
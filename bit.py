# encript and decrypt a message using XOR operation 
# The XOR operation is a bitwise operator that takes two bits and returns 1 if they are different and 0 if they are the same.
# In this example, we will use the XOR operation to encrypt and decrypt a message using a key. The key will be repeated if it is shorter than the message.

# The encrypt_message function takes a message and a key as input and returns the encrypted message. It iterates through each character in the message, applies the XOR operation with the corresponding character in the key (using modulo to repeat the key if necessary), and constructs the encrypted message.

def encrypt_message(message, key):
    encrypted = ""
    for i in range(len(message)):
        encrypted += chr(ord(message[i]) ^ ord(key[i % len(key)]))
    return encrypted

def decrypt_message(encrypted_message, key):
    decrypted = ""
    for i in range(len(encrypted_message)):
        decrypted += chr(ord(encrypted_message[i]) ^ ord(key[i % len(key)]))
    return decrypted 
# Example usage 
if __name__ == "__main__":
    original_message = "Hello, World!"
    
    key = "mysecretkey"
    encrypted_message = encrypt_message(original_message, key)      
    print(f"Encrypted Message: {encrypted_message}")
    decrypted_message = decrypt_message(encrypted_message, key) 
    print(f"Decrypted Message: {decrypted_message}")        

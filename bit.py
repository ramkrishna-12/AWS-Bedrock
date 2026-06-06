

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

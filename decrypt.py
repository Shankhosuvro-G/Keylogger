from cryptography.fernet import Fernet

# Your secret key for decryption. Keep this secure and consistent with the encryption key.
encryption_key = b'qoW3PipWdH6pgbsERsnPbLptNh5LvUsVPlUpMG4CHsQ='

encrypted_file = 'encrypted_keystrokes.txt'
decrypted_file = 'decrypted_keystrokes.txt'

# Initialize the Fernet cipher with the encryption key
cipher = Fernet(encryption_key)

def decrypt_file(filename):
    with open(filename, 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = cipher.decrypt(encrypted_data)
    with open(decrypted_file, 'wb') as file:
        file.write(decrypted_data)

# Decrypt the encrypted file
decrypt_file(encrypted_file)

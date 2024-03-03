from cryptography.fernet import Fernet

# Encryption Key (you need to store this securely)
key = b'yGidZu033m1WccdrS6gvqL5KTVRvFTPNuIq4TvOXoz4='

cipher = Fernet(key)

encrypted_file = 'keystrokes.txt'
decrypted_file = 'decrypted_keystrokes.txt'

# Read encrypted data from the file
with open(encrypted_file, 'rb') as f:
    encrypted_data = f.read()

# Decrypt the data
decrypted_data = cipher.decrypt(encrypted_data)

# Write decrypted data to a new file
with open(decrypted_file, 'wb') as f:
    f.write(decrypted_data)

print("Decryption successful. Decrypted log file saved as", decrypted_file)

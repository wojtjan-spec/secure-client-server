import socket
import sys
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.backends import default_backend

# Define server host and port
HOST = '127.0.0.1'

if len(sys.argv) < 3:
    print("Usage: python client.py <port> <public_key_file>")
    sys.exit(1)

# Get port number and public key file from command line arguments
PORT = int(sys.argv[1])
PUBLIC_KEY_FILE = sys.argv[2]

# Generate a session key to be used for symmetric encryption
session_key = b'4\xb4\x87\xd7V\x8b\xad'

# Load server's public key from file
with open(PUBLIC_KEY_FILE, "rb") as key_file:
    public_key = serialization.load_pem_public_key(
        key_file.read(),
        backend=default_backend()
    )

# Create socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Connect to server
    s.connect((HOST, PORT))

    # Encrypt the session key using the server's public key
    encrypted_session_key = public_key.encrypt(
        session_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Send the encrypted session key as the initialization message
    s.sendall(encrypted_session_key)

    # Send a message to the server
    message = "Hello, server!"
    s.sendall(message.encode())

    # Receive data from server
    data = s.recv(1024)

    # Print received data
    print(f"Received from server: {data.decode()}")

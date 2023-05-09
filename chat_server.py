import socket
import sys
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.backends import default_backend

# Define host and port to listen on
HOST = '127.0.0.1'

if len(sys.argv) < 4:
    print("Usage: python server.py <port> <data_file> <private_key_file>")
    sys.exit(1)

# Get port number, data file and private key file from command line arguments
PORT = int(sys.argv[1])
DATA_FILE = sys.argv[2]
PRIVATE_KEY_FILE = sys.argv[3]

# Load server's private key from file
with open(PRIVATE_KEY_FILE, "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )

# Create socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Bind socket to specified host and port
    s.bind((HOST, PORT))
    # Listen for incoming connections
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")

    # Wait for a client to connect
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")

        # Receive initialization message from client
        encrypted_session_key = conn.recv(1024)

        # Decrypt the session key using the server's private key
        session_key = private_key.decrypt(
            encrypted_session_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        print(f"Session key: {session_key}")

        # Open data file and read contents
        with open(DATA_FILE, 'r') as f:
            data = f.read()

        # Decrypt data with session key
        decrypted_data = decrypt(data, session_key)

        # Send decrypted data back to client
        conn.sendall(decrypted_data.encode())

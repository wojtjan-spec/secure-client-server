import socket
import sys
import os

from helper_symmetric import decrypt_symmetric, encrypt_symmetric
from helper_asymmetric import encrypt_asymmetric
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

def main():
	if len(sys.argv) < 4:
		print("Usage: python server.py <host> <port> <server_key_file>")
		sys.exit(1)

	# Define server host and port
	PORT = int(sys.argv[1])
	HOST = sys.argv[2]
	PUBLIC_KEY_FILE = sys.argv[3]
	
	# Generate a session key to be used for symmetric encryption
	salt = os.urandom(16)
	kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
	session_key = kdf.derive(b"secret")

	# Load server's public key from file
	public_key_file_name = PUBLIC_KEY_FILE
	with open(public_key_file_name + '.txt', "rb") as key_file:
		public_key = serialization.load_pem_public_key(
        	key_file.read(),
        	backend=default_backend()
    )

	# Create socket object
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		# Connect to server
		s.connect((HOST, PORT))

		# Encrypt the session key using the server's public key
		encrypted_session_key = encrypt_asymmetric(public_key, session_key)

		# Send the encrypted session key as the initialization message
		s.sendall(encrypted_session_key)

		while True:
    		# Send data to server
			text = input("> ")
			message = bytes([len(text)]) + text.encode()
			if len(message) >= 256:
				raise ValueError("message exceeding 256 bytes")

			encrypted_message = encrypt_symmetric(message, session_key)
			s.sendall(encrypted_message)

    		# Receive data from server
			data = s.recv(1024)

    		# Decrypt received data
			response = decrypt_symmetric(data, session_key)

			# Extract message length byte
			message_length = response[0]

            # Extract message string
			message_string = response[1:message_length+1].decode()
			print(message_string)
			
			# Exit connection if quit message was received from the server
			if message_string == "connection terminated":
				return 0

if __name__ == '__main__':
	main()
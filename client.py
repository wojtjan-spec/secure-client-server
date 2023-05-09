import socket
import sys
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
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
	session_key = b'4\xb4\x87\xd7V\x8b\xad'

	# Load server's public key from file
	public_key_file_name = PUBLIC_KEY_FILE
	with open(public_key_file_name + '.pem', "rb") as key_file:
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
        ))

		# Send the encrypted session key as the initialization message
		s.sendall(encrypted_session_key)

    	# Send data to server
		text = input("> ")
		message = text
		s.sendall(message.encode())

    	# Receive data from server
		data = s.recv(1024)

    	# Print received data
		print("Received from server: ",  {data.decode()})

if __name__ == '__main__':
	main()
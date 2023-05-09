import socket
import sys
import csv
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.backends import default_backend

# Define host and port to listen on
HOST = '127.0.0.1'

database_dictionary = {
    1: "type",
    2: "game_id",
    3: "home_team",
    4: "away_team",
    5: "week",
    6: "season", 
    7: "home_score",
    8: "away_score"
}

def get_item_from_data_base(database, search_id, item):
    for row in database:
            print(', '.join(row))
    return 0

def main():

    if len(sys.argv) < 4:
        print("Usage: python server.py <port> <data_file> <private_key_file>")
        sys.exit(1)

    # Get port number, data file and private key from command line arguments
    PORT = int(sys.argv[1])
    DATA_FILE = sys.argv[2]
    PRIVATE_KEY_FILE = sys.argv[3]

    # Parse the key_file and data_file to objects
    # Data_csv
    data_file_name = DATA_FILE
    with open(data_file_name + '.csv', newline='') as csvfile:
        database = csv.reader(csvfile, delimiter=' ', quotechar='|')

    # Private key
    private_key_file_name = PRIVATE_KEY_FILE
    with open(private_key_file_name + '.pem', "rb") as key_file:
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
        print("Server started")
        print("Listening for client on {HOST}:{PORT}")
        print("...")
 
        # Wait for a client to connect
        conn, addr = s.accept()
        with conn:
            print("Connected by address: ", addr)

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
            
            print("Session key: ", session_key)

            while True:
                # Receive data from client
                data = conn.recv(1024)
                if not data:
                    break

                # Print received data
                print("Received from client:", {data.decode()})

                # Send data back to client
                conn.sendall(data)

if __name__ == '__main__':
	main()
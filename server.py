import socket
import sys
import csv

# Imported from cryptography library
from helper_symmetric import decrypt_symmetric, encrypt_symmetric
from helper_asymmetric import decrypt_asymmetric
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# Define host
HOST = "127.0.0.1"

# Database tags
database_dictionary = {
    "type": 0,
    "game_id": 1,
    "home_team": 2,
    "away_team": 3,
    "week": 4,
    "season": 5,
    "home_score": 6,
    "away_score": 7,
}


# Get item from csv file to form server response
def get_item_from_data_base(data_file_name, search_id, item):
    with open(data_file_name + ".csv", newline="") as csvfile:
        database = csv.reader(csvfile, delimiter=" ", quotechar="|")
        for row in database:
            list = row[0].split(",")
            if list[1] == search_id:
                if database_dictionary.get(item) != None:
                    return list[database_dictionary.get(item)]
                else:
                    return None
        return None


def main():
    if len(sys.argv) < 4:
        print("Usage: python server.py <port> <data_file> <private_key_file>")
        sys.exit(1)

    # Get port number, data file and private key from command line arguments
    PORT = int(sys.argv[1])
    DATA_FILE = sys.argv[2]
    PRIVATE_KEY_FILE = sys.argv[3]

    # Parse the key_file to object
    private_key_file_name = PRIVATE_KEY_FILE
    with open(private_key_file_name + ".txt", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(), password=None, backend=default_backend()
        )

    # Create socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Bind socket to specified host and port
        s.bind((HOST, PORT))

        # Listen for incoming connections
        s.listen()
        print("Server started")
        print("Listening for client on: ", str(HOST) + ":" + str(PORT))
        print("...")

        # Wait for a client to connect
        conn, addr = s.accept()
        with conn:
            print("Connected by address: ", addr)

            # Receive initialization message from client
            encrypted_session_key = conn.recv(1024)

            # Decrypt the session key using the server's private key
            session_key = decrypt_asymmetric(private_key, encrypted_session_key)

            while True:
                # Receive data from client
                data = conn.recv(1024)
                if not data:
                    break

                # Decrypt and print received data
                message = decrypt_symmetric(data, session_key)
                # Extract message length byte
                message_length = message[0]

                # Extract message string
                message_string = message[1 : message_length + 1].decode()
                message_words = message_string.split()
                word_count = len(message_words)

                if word_count != 2:
                    # Terminate connection if 'quit' message received
                    if message_string == "quit":
                        text = "connection terminated"
                        print(text)
                        final_response = bytes([len(text)]) + text.encode()
                        final_message = encrypt_symmetric(final_response, session_key)
                        conn.sendall(final_message)
                        return 0
                    else:
                        text = "unknown"

                else:
                    # Get item from csv
                    request_data = get_item_from_data_base(
                        DATA_FILE, message_words[0], message_words[1]
                    )
                    if request_data == None:
                        text = "unknown"
                    else:
                        text = request_data
                        if len(text) >= 256:
                            raise ValueError("message exceeding 256 bytes")

                # Respond to the client request
                response = bytes([len(text)]) + text.encode()
                message = encrypt_symmetric(response, session_key)
                conn.sendall(message)


if __name__ == "__main__":
    main()

# NFL Game Query Networked Client/Server Application in Python

This is a networked client/server application in Python that allows a client program to query a simple database managed by a server program. The database contains information about NFL games, and the client program sends a message containing a query about a game to the server, which responds with the requested information.

## Communication
To ensure secure communication between the client and server, the application uses a hybrid encryption scheme. Asymmetric encryption is used to transmit a session key at the beginning of each session, and symmetric encryption is used for the remainder of the session.

## Implementation
The application consists of two programs: the client program and the server program. Both programs should run as separate processes, which can be invoked by the user in a shell. The server must be started before the client, and it listens to a port until a client initiates communication. Once communication is initiated, the client sends a request to the server, and the server responds with the corresponding information. This process continues until the client sends a quit message to the server.

The server program requires access to a database of information about NFL games, which is stored in a comma-separated value (csv) file. The first row of the csv file contains the field names and should remain unchanged. Each row after the first line contains information about a single game, including the type of match, unique identifier for the match, short names of the home and away teams, the week number in which the match was held, the year in which the match took place, and the number of points scored by each team.

## Usage
The server program should take three command-line arguments: the server port number, the name of the file containing the database of all game information, and the name of the file containing the server's private key. The client program should take three command-line arguments: the server host name, the server port number, and the name of the file containing the server's public key.

When the server program is started, it should print "server started" and wait to receive messages from a client. When a request is received, the server program will print the game_id and field in the message on the screen on a new line. The client program will present the user with a prompt, ">," and the user can enter a query about a specific NFL game.

## Packages
The NFL Game Query Networked Client/Server Application in Python requires a Python cryptography library that contains functions for both symmetric and asymmetric encryption to function and socket library for server-client connections. 


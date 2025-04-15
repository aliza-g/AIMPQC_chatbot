# implement a text based chat application consisting of one chat server and
# one chat client using python and only built in libraries

# takes command-line argument specifying the TCP port to connect to
# connects to chat server
# displays welcome message indicating how the client can exit the chat ("exit")
# allows sending and receiving text messages to and from the server
# supports graceful disconnection using a keyword ("exit")

import socket
import sys
import threading

def handle_client(client_socket):
    # Send a welcome message to the client
    client_socket.send("Welcome to the chat server! Type 'exit' to disconnect.\n".encode())

    while True:
        try:
            # Receive message from the client
            message = client_socket.recv(1024).decode()
            if message.lower() == "exit":
                print("Client disconnected.")
                break

            # Print received message in the server's console
            print(f"Client: {message}")

            # Send the message back to the client
            reply = input("Server: ")
            client_socket.send(reply.encode())

        except ConnectionResetError:
            print("Client forcibly disconnected.")
            break

    client_socket.close()

def start_server(port):
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))  # Listen on all interfaces
    server_socket.listen(1)
    print(f"Server is listening on port {port}...")

    while True:
        # Wait for a client connection
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        # Handle the client connection in a new thread
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python chat_server.py <port>")
        sys.exit(1)

    try:
        port = int(sys.argv[1])
        if port < 1025 or port > 65535:
            print("Port must be between 1025 and 65535.")
            sys.exit(1)
    except ValueError:
        print("Invalid port number. Port must be an integer.")
        sys.exit(1)

    start_server(port)

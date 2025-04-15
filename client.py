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

def receive_messages(server_socket):
    while True:
        try:
            message = server_socket.recv(1024).decode()
            print(f"Server: {message}")
        except ConnectionResetError:
            print("Connection to the server was lost.")
            break

def start_client(server_ip, port):
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))

    # Start a thread to receive messages from the server
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    # Allow the user to send messages
    while True:
        message = input("You: ")
        if message.lower() == "exit":
            client_socket.send("exit".encode())
            print("Disconnected from the server.")
            break
        client_socket.send(message.encode())

    client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python chat_client.py <server_ip> <port>")
        sys.exit(1)

    server_ip = sys.argv[1]
    try:
        port = int(sys.argv[2])
        if port < 1025 or port > 65535:
            print("Port must be between 1025 and 65535.")
            sys.exit(1)
    except ValueError:
        print("Invalid port number. Port must be an integer.")
        sys.exit(1)

    start_client(server_ip, port)

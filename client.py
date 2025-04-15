# implement a text based chat application consisting of one chat server and
# one chat client using python and only built in libraries

# takes command-line argument specifying the TCP port to connect to
# connects to chat server
# displays welcome message indicating how the client can exit the chat ("exit")
# allows sending and receiving text messages to and from the server
# supports graceful disconnection using a keyword ("exit")

import socket

def main():
    host = 'localhost'  # or '127.0.0.1' if you're running it on the same machine

    # Ask user for port
    try:
        port = int(input("Enter the port to connect to: "))
        if not (1025 <= port <= 65535):
            raise ValueError("Port must be between 1025 and 65535.")
    except ValueError as e:
        print(f"Invalid port: {e}")
        return

    # Connect to the server
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        print(f"Connected to chat server on port {port}. Type 'exit' to disconnect.")
    except ConnectionRefusedError:
        print("Could not connect to server. Make sure it's running.")
        return

    try:
        while True:
            message = input("You: ")
            client_socket.sendall((message + '\n').encode())

            if message.strip().lower() == "exit":
                print("Disconnected from server.")
                break

            reply = client_socket.recv(1024).decode().strip()
            if not reply:
                print("Server disconnected.")
                break

            print("Server:", reply)
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()

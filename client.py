# implement a text based chat application consisting of one chat server and
# one chat client using python and only built in libraries

# takes command-line argument specifying the TCP port to connect to
# connects to chat server
# displays welcome message indicating how the client can exit the chat ("exit")
# allows sending and receiving text messages to and from the server
# supports graceful disconnection using a keyword ("exit")

import socket
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python client.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect(('localhost', port))
        welcome = client_socket.recv(1024).decode()
        print(welcome.strip())

        while True:
            msg = input("You: ")
            client_socket.sendall((msg + '\n').encode())
            if msg.strip().lower() == "exit":
                print("Disconnected from server.")
                break
            data = client_socket.recv(1024).decode()
            if not data or data.strip().lower() == "exit":
                print("Server disconnected.")
                break
            print(f"Server: {data.strip()}")
    except ConnectionRefusedError:
        print("Could not connect to server. Make sure the server is running.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()

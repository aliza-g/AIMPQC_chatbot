# implement a text based chat application consisting of one chat server and
# one chat client using python and only built in libraries

# takes command-line argument specifying the TCP port to listen on
# validates that port number is an integer between 1025 and 65535
# listens for and accepts a single client connection
# sends a welcome message to the client upon connection
# allows basic text-based chat between the connected client and the server console
# supports graceful shutdown

import socket
import sys

def validate_port(port_str):
    try:
        port = int(port_str)
        if 1025 <= port <= 65535:
            return port
        else:
            raise ValueError
    except ValueError:
        print("Port must be an integer between 1025 and 65535.")
        sys.exit(1)


def main():
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)

    port = validate_port(sys.argv[1])

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen(1)

    print(f"Server listening on port {port}...")

    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")
    conn.sendall(b"Welcome to the chat! Type 'exit' to quit.\n")

    try:
        while True:
            data = conn.recv(1024).decode()
            if not data or data.strip().lower() == "exit":
                print("Client disconnected.")
                break
            print(f"Client: {data.strip()}")
            # Automatically generate a reply (repeat last 2-3 words with a ?)
            words = data.strip().split()
            if len(words) >= 3:
                msg = " ".join(words[-3:])
            elif len(words) >= 2:
                msg = " ".join(words[-2:])
            else:
                msg = data.strip()
            msg += "?"
            
            conn.sendall((msg + '\n').encode())
            if msg.strip().lower() == "exit":
                print("Server exiting.")
                break
    finally:
        conn.close()
        server_socket.close()


if __name__ == "__main__":
    main()

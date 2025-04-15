# implement a text based chat application consisting of one chat server and
# one chat client using python and only built in libraries

# takes command-line argument specifying the TCP port to connect to
# connects to chat server
# displays welcome message indicating how the client can exit the chat ("exit")
# allows sending and receiving text messages to and from the server
# supports graceful disconnection using a keyword ("exit")

import socket  # Import socket library to use TCP/IP communication
import sys     # Import sys to access command-line arguments

def main():
    # Ensure exactly one argument is passed (the port number)
    if len(sys.argv) != 2:
        print("Usage: python client.py <port>")
        sys.exit(1) # Exit if argument count is incorrect

    port = int(sys.argv[1]) # Convert the port argument to integer
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Attempt to connect to the server running on localhost at the given port
        client_socket.connect(('localhost', port))
        # Receive and print the welcome message from server
        welcome = client_socket.recv(1024).decode()
        print(welcome.strip())

        while True:
            # Prompt user for input
            msg = input("You: ")
            # Send message to the server (add newline for consistency)
            client_socket.sendall((msg + '\n').encode())
            # Check if user wants to exit
            if msg.strip().lower() == "exit":
                print("Disconnected from server.")
                break  # Check if user wants to exit
            # Receive response from server
            data = client_socket.recv(1024).decode()
            # If server closes connection or sends "exit", exit
            if not data or data.strip().lower() == "exit":
                print("Server disconnected.")
                break
            print(f"Server: {data.strip()}")
    except ConnectionRefusedError:
        # Handle case where connection to server fails
        print("Could not connect to server. Make sure the server is running.")
    finally:
        # Ensure socket is closed properly in all cases
        client_socket.close()

if __name__ == "__main__":
    main()

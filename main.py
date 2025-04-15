# This launches both the server and the client of the chatbot
# uses subprocesses to run server.py and client.py
# waits for the client to exit,then terminates the server gracefully.


import subprocess # runs external python files as separate processes
import time # introduce delays (so server has time to start)
import sys # access command-line arguments and python executable

def main():
    # Check if a port number is passed as command-line argument
    if len(sys.argv) != 2:
        print("Usage: python main.py <port>")
        sys.exit(1) # Exit if no port provided

    port = sys.argv[1] # Read the port from the argument

    # Start the server
    print(f"Starting server on port {port}...")
    # Launch server.py as a subprocess using the same Python interpreter
    server_proc = subprocess.Popen([sys.executable, 'server.py', port])

    # Wait a moment to let the server start
    time.sleep(1)

    # Start the client
    print(f"Starting client on port {port}...")
    # Launch client.py as a subprocess (interactive chat starts)
    client_proc = subprocess.Popen([sys.executable, 'client.py', port])

    # Wait for the client process to finish
    client_proc.wait() # Block here until client.py is done

    # After client exits, stop the server
    server_proc.terminate()
    print("Chat session ended.")

if __name__ == "__main__":
    main()

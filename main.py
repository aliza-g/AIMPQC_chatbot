import subprocess
import time
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <port>")
        sys.exit(1)

    port = sys.argv[1]

    # Start the server
    print(f"Starting server on port {port}...")
    server_proc = subprocess.Popen([sys.executable, 'server.py', port])

    # Wait a moment to let the server start
    time.sleep(1)

    # Start the client
    print(f"Starting client on port {port}...")
    client_proc = subprocess.Popen([sys.executable, 'client.py', port])

    # Wait for the client process to finish
    client_proc.wait()

    # After client exits, stop the server
    server_proc.terminate()
    print("Chat session ended.")

if __name__ == "__main__":
    main()

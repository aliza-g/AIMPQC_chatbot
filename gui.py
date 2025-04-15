import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import sys
import time


class ChatClientGUI:
    def __init__(self, root, port):
        self.root = root
        self.root.title("Chat Client")
        self.port = port

        # Set background color
        self.root.configure(bg="#F3C178")

        # GUI Elements
        self.chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', height=20, bg="#ACEDFF",
                                                      fg="black", font=("Arial", 12))
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.msg_entry = tk.Entry(root, font=("Arial", 12))
        self.msg_entry.pack(padx=10, pady=(0, 10), fill=tk.X)
        self.msg_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(root, text="✈️ Send", command=self.send_message, bg="#002642", fg="white",
                                     font=("Arial", 12))
        self.send_button.pack(pady=(0, 10))

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Set up socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect(('localhost', self.port))
        except ConnectionRefusedError:
            messagebox.showerror("Connection Error", "Could not connect to server.")
            root.destroy()
            return

        welcome = self.client_socket.recv(1024).decode()
        self.append_chat(f"Server: {welcome.strip()}", "server")

        # Start thread to listen for messages
        self.running = True
        threading.Thread(target=self.receive_messages, daemon=True).start()

        # Apply custom styles for messages
        self.custom_style()

    def custom_style(self):
        # Create custom style for messages
        self.chat_display.tag_configure("user", background="#FFB8DE", justify="left", font=("Arial", 12))
        self.chat_display.tag_configure("server", background="#785964", foreground="white", justify="left",
                                        font=("Arial", 12))

    def send_message(self, event=None):
        msg = self.msg_entry.get().strip()
        if msg:
            self.append_chat(f"You: {msg}", "user")
            self.client_socket.sendall((msg + '\n').encode())
            if msg.lower() == "exit":
                self.running = False
                self.root.destroy()
        self.msg_entry.delete(0, tk.END)

    def receive_messages(self):
        while self.running:
            try:
                data = self.client_socket.recv(1024).decode()
                if not data or data.strip().lower() == "exit":
                    self.append_chat("Server disconnected.", "server")
                    self.running = False
                    break
                self.append_chat(f"Server: {data.strip()}", "server")
            except:
                break

    def append_chat(self, message, sender):
        self.chat_display.configure(state='normal')

        # Format message bubble based on sender
        if sender == "user":
            self.chat_display.insert(tk.END, f"{message}\n", "user")
        elif sender == "server":
            self.chat_display.insert(tk.END, f"{message}\n", "server")

        self.chat_display.configure(state='disabled')
        self.chat_display.yview(tk.END)

    def on_close(self):
        try:
            self.client_socket.sendall(b"exit\n")
            self.client_socket.close()
        except:
            pass
        self.running = False
        self.root.destroy()


# Launch server and GUI client together
def main():
    if len(sys.argv) != 2:
        print("Usage: python gui_client.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])

    # Start server in background
    server_proc = subprocess.Popen([sys.executable, 'server.py', str(port)])
    time.sleep(1)  # Let server start

    # Launch GUI
    root = tk.Tk()
    app = ChatClientGUI(root, port)
    root.mainloop()

    # After GUI closes
    server_proc.terminate()
    print("Chat session ended.")


if __name__ == "__main__":
    main()

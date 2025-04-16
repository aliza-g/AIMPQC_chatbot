AIM-PQC Chat Application
This project is a text only chat application with a built-in GUI. It was coded in Python and allows communication between a client and server over TCP ports. 
Libraries used:
•	socket: TCP communication
•	subprocess: Process management (server/client launching)
•	threading: Background message handling (non-blocking GUI)
•	tkinter: GUI framework for Python
•	sys, time: Utility functions and timing

Files:
1. server.py:
•	Listen for TCP connections on a user-defined port.
•	Accept exactly one client.
•	Receive and respond to messages.
•	End when "exit" is received.
•	Message Response Logic: Echoes back the last 2–3 words of a message as a question to mimic talking to someone who isn’t really engaged with the conversation.
2. client.py
•	Connect to the server and initiate communication.
•	Allow user to input messages.
•	Display responses from the server.
•	Exit on command.
3. gui.py
•	Connects to the server and handles socket communication in background threads.
•	Provides a GUI (more info in bonus feature section)
4. main.py
  •	Launcher for CLI testing.
  •	Starts both server and client subprocesses with a specified port.

How to run?
1.	Open the command prompt
2.	Navigate to the folder containing all four files (main.py, gui.py, client.py and server.py)
EX: cd Users\aliza\projects
3.	Start program with port number (1025-65535)
EX: python gui.py 12345 or python main.py 12345 (if you don’t want to use the GUI)
*You may have to install python. To do so just type python in the command prompt
  
Bonus feature:
Chat GUI 
•	Chat history (scrollable text box)
•	Message input field
•	Send button
•	Handles graceful shutdown on window close or "exit".
•	Threading: Uses a background thread to listen for server messages without freezing the UI.
Color palette used: https://coolors.co/edd4b2-d0a98f-cac2b5-ecdcc9-002642

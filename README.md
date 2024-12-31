## DESCRIPTION

This project is a gRPC-based chat application implemented in Python. It consists of a server that handles chat messages
and a client that provides a graphical user interface (GUI) for users to send and receive messages.

# FEATURES


### Server-Side:
- Maintains a log file for persistent message storage.
- Provides sendMessage and getMessages functions to handle message insertion and retrieval.
- Implements MD5 checksums to ensure data integrity.
- Supports multiple clients simultaneously, ensuring scalability.
- Automatically detects tampering in the chat_log.txt file and skips corrupted entries.
### Client-Side:
- GUI implemented using Tkinter for a more user-friendly experience.
- Polls the server to fetch new messages using getMessages.
- Sends messages to the server through an input text box.
- Automatically disconnects when the server shuts down.


## REQUIREMENTS

In a virtual environment, run the following commands.

If necessary, upgrade your version of pip:

```bash
python -m pip install --upgrade pip
```

Install the required packages in the requirements.txt file:

```bash
pip install -r requirements.txt
```

To re-generate the Python code from the protocol buffer file, run the following command:

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./messanger.proto
```
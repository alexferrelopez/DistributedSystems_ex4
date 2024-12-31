## DESCRIPTION

This project is a gRPC-based chat application implemented in Python. It consists of a server that handles chat messages
and a client that provides a graphical user interface (GUI) for users to send and receive messages.

# FEATURES

- The server can handle multiple clients at the same time.
- The server can provide context to the client by sending only the messages that the client has not yet received.
- The client can send and receive messages to/from the server through a graphical user interface (GUI) made in Tkinter.
- The clients automatically disconnect from the server once it is shut down.

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
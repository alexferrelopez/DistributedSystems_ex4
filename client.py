import logging
import sys
import threading
from time import sleep
from tkinter import *

import grpc

import messanger_pb2
import messanger_pb2_grpc

BG_COLOR = "#ffffff"
TEXT_COLOR = "#000000"

FONT = "Arial 14"

logging_level = logging.INFO
logging.basicConfig(level=logging_level, format="%(message)s")
logger = logging.getLogger(__name__)


def listen_for_messages(stub, nickname):
    last_id = -1
    while True:
        try:
            response = stub.getMessages(messanger_pb2.MessageListRequest(last_id=last_id, nickname=nickname))
            for message in response.messages:
                txt.config(state=NORMAL)
                txt.insert(END, message + "\n")
                txt.config(state=DISABLED)
                txt.see(END)

            last_id = max(last_id, response.last_id)
        except grpc.RpcError as ex:
            if ex.code() in (grpc.StatusCode.UNAVAILABLE, grpc.StatusCode.RESOURCE_EXHAUSTED):
                logger.error(f"Server unavailable: {ex}")
                root.destroy()  # Close the Tkinter window
            else:
                logger.error(f"Error: {ex}")
        sleep(1)


# Send function
def send(event):
    msg = e.get()
    if msg.strip():
        e.delete(0, END)
        try:
            response = stub.sendMessage(messanger_pb2.MessageRequest(nickname=nickname, message=msg))
            if response.status < 0:
                logger.warning(f"Failed to send message: {response.status_message}")

        except grpc.RpcError as ex:
            logger.error(f"Error: {ex}")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        logger.info("Usage: ./client.py <chatServerIP> <nickname>")
        sys.exit(1)

    chat_server_ip = sys.argv[1]
    nickname = sys.argv[2]

    # Connect to the server
    try:
        channel = grpc.insecure_channel(f"{chat_server_ip}:50051")
        stub = messanger_pb2_grpc.ChatServiceStub(channel)
        grpc.channel_ready_future(channel).result(timeout=2)
    except grpc.FutureTimeoutError:
        logger.error("Failed to connect to the server.")
        sys.exit(1)

    # GUI
    root = Tk()
    root.title("gRPC chat - " + nickname)
    txt = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=50, state=DISABLED)
    txt.grid(row=0, column=0, sticky=N + E + S + W)

    scrollbar = Scrollbar(root, command=txt.yview)
    scrollbar.grid(row=0, column=1, sticky=N + S)
    txt.config(yscrollcommand=scrollbar.set)

    e = Entry(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=1)
    e.grid(row=1, column=0, columnspan=2, sticky=E + W)
    e.focus_set()

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    root.bind("<Return>", send)

    # Start a thread to listen for incoming messages
    threading.Thread(target=listen_for_messages, args=(stub, nickname,), daemon=True).start()

    root.mainloop()

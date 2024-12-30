import logging
import os
import threading
from concurrent import futures

import grpc

import messanger_pb2
import messanger_pb2_grpc

logging_level = logging.INFO
logging.basicConfig(level=logging_level, format="%(message)s")
logger = logging.getLogger(__name__)


class ChatService(messanger_pb2_grpc.ChatServiceServicer):
    def __init__(self):
        self.chat_file = "logs/chat_log.txt"
        self.file_lock = threading.Lock()
        self.last_id = -1
        if not os.path.exists(self.chat_file):
            open(self.chat_file, 'w').close()  # Create the file if it doesn't exist
        else:
            with open(self.chat_file, 'r+b') as file:
                self.last_id = self._get_last_id(file)

    def sendMessage(self, request, context):
        try:
            with open(self.chat_file, 'a') as file:
                with self.file_lock:
                    self.last_id += 1
                    file.write(f"{self.last_id}-{request.nickname}: {request.message}\n")

            return messanger_pb2.StatusResponse(status=self.last_id, status_message="Message sent successfully")
        except Exception as e:
            return messanger_pb2.StatusResponse(status=-1, status_message=str(e))

    def getMessages(self, request, context):
        try:
            with open(self.chat_file, 'r') as file:
                trimmed_messages = self._get_lines(file, request.last_id + 1)

            return messanger_pb2.MessageListResponse(messages=trimmed_messages,
                                                     last_id=len(trimmed_messages) + request.last_id)
        except Exception as e:
            return messanger_pb2.MessageListResponse(messages=[])

    def _get_lines(self, fp, _from):
        l = []

        for i, x in enumerate(fp):
            if i >= _from:
                split = x.strip().split("-", 1)

                if len(split) == 2:
                    l.append(split[1])

        return l

    @staticmethod
    def _get_last_id(f):
        try:  # catch OSError in case of a one line file
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
        except OSError:
            f.seek(0)
        last_line: str = f.readline().decode().split("-")[0]
        if last_line.strip(' \t\n\r') != "":
            num = int(last_line)
        else:
            num = -1
        return num


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    messanger_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)
    port = 50051
    server.add_insecure_port('[::]:' + str(port))
    logger.info("Server started on port %s", port)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

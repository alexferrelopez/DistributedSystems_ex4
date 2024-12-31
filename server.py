import hashlib
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
        if not os.path.exists(self.chat_file):
            open(self.chat_file, 'w', encoding="utf-8").close()  # Create the file if it doesn't exist

    def sendMessage(self, request, context):
        try:
            with open(self.chat_file, 'a', encoding="utf-8") as file:
                with self.file_lock:
                    full_msg = f"{request.nickname}: {request.message}"
                    hashed = str(int(hashlib.md5(full_msg.encode("utf-8")).hexdigest(), 16))
                    file.write(f"{hashed}-{full_msg}\n")

            return messanger_pb2.StatusResponse(status=hashed, status_message="Message sent successfully")
        except Exception as e:
            return messanger_pb2.StatusResponse(status="-1", status_message=str(e))

    def getMessages(self, request, context):
        try:
            with open(self.chat_file, 'r', encoding="utf-8") as file:
                trimmed_messages = self._get_lines(file, request.last_id + 1)

            return messanger_pb2.MessageListResponse(messages=trimmed_messages,
                                                     last_id=len(trimmed_messages) + request.last_id)
        except Exception as e:
            return messanger_pb2.MessageListResponse(messages=[])

    @staticmethod
    def _get_lines(fp, _from):
        l = []
        i = 0
        for x in fp:
            is_valid, split = ChatService._is_valid_line(x)

            if is_valid:
                # looking for the line where we should start reading
                if i >= _from:
                    l.append(split[1])
                i += 1

        return l

    @staticmethod
    def _is_valid_line(line):
        split = line.strip(' \t\n\r').split("-", 1)
        if len(split) == 2:
            hashed_msg = str(int(hashlib.md5(split[1].encode("utf-8")).hexdigest(), 16))
            true_hash = split[0]
            return hashed_msg == true_hash, split
        else:
            return False, None


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    messanger_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)
    port = 50051
    ip = "127.0.0.1"
    server.add_insecure_port(ip + ":" + str(port))
    logger.info("Server started on port %s", port)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

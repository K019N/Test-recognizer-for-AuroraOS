import socket
import json


class Client():
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(("127.0.0.1", 8000))
    
    def recive_data():
        pass

    def send_data(self, data):
        self.client.sendall(bytes(json.dumps(data), encoding="utf-8"))
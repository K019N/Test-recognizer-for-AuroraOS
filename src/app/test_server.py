import socket


class Server():
    def __init__():
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("127.0.0.1", 8080))
        server.listen(4)

        while(True):
            (clientConnected, clientAddress) = server.accept()
            dataFromClient = clientConnected.recv(1024)
            print(dataFromClient.decode())
            clientConnected.send("Hello Client!".encode())

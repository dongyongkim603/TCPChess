import socket
import time
import pickle



HEADERSIZE = 10

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((socket.gethostname(), 8081))
sock.listen(50)

while True:
    clientsocket, address = sock.accept()
    print(f"connection {address} has established connection")

    d = {1: "hey", 2: "There"}
    message = pickle.dumps(d)

    message = bytes(f'{len(message):<10}', "utf-8") + message
    print(f'{len(message):<{HEADERSIZE}}')

    clientsocket.send(message)

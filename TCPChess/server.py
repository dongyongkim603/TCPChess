import socket
import time

HEADERSIZE = 10

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((socket.gethostname(), 8081))
sock.listen(50)

while True:
    clientsock, address = sock.accept()
    print(f"connection {address} has established connection")

    message = "Bienvinedo al la server"
    message = f'{len(message):<10}' + message
    print(f'{len(message):<{HEADERSIZE}}')

    clientsock.send(bytes(message, "utf-8"))

    while True:
        time.sleep(3)
        message = f"Local server time is {time.time()}"
        message = f'{len(message):<10}' + message
        clientsock.send(bytes(message, "utf-8"))
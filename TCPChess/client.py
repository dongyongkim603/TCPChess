import socket
import pickle

HEADERSIZE = 10

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((socket.gethostname(), 8081))

while True:

    full_msg = b''
    new_msg = True
    while True:
        message = sock.recv(16)
        if new_msg:
            print(f"new message length: {message[:HEADERSIZE]}")
            messageLen = int(message[:HEADERSIZE])
            new_msg = False

        full_msg += message

        if len(full_msg)-HEADERSIZE == messageLen:
            print("full msg recvd")
            print(full_msg[HEADERSIZE:])

            d = pickle.loads(full_msg[HEADERSIZE:])
            print(d)

            new_msg = True
            full_msg = b''

        print(full_msg)
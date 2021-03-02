import socket
import pickle
import select



HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 8081

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_sock.bind((IP, PORT))
server_sock.listen()

sockets_list = [server_sock]

client = {}

def recieve_messgae(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False
        message_length = int(message_header.decode('utf-8').strip())
        return {"header": message_header,"data": client_socket.recv(message_length)}

    except:
        return False


while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_sock:
            client_socket, client_address = server_sock.accept()

            user = recieve_messgae(client_socket)
            if user is False:
                continue

            sockets_list.append(client_socket)

            client[client_socket] = user

            print(f"new connection established from {client_address[0]}:{client_address[1]} username{user['data'].decode('utf-8')}")

        else:
            message = recieve_messgae(notified_socket)

            if message is False:
                print(f"Closed connection from {client[notified_socket]['data'].decode('utf-8')}")
                sockets_list.remove(notified_socket)
                del client[notified_socket]
                continue

            user = client[notified_socket]
            print(f"Recieved message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

            for client_socket in client:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del client[notified_socket]
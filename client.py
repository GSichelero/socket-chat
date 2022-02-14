import datetime
import select
import socket
import sys

PORT = 5050
SERVER = "192.168.0.105"
ADDR = (SERVER, PORT)

server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_connection.connect(ADDR)

user_name = input("Qual o seu nome? ")

connect = True
while connect:
    sockets_list = [sys.stdin, server_connection]
    read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])
 
    for connection_received in read_sockets:
        if connection_received == server_connection:
            message = connection_received.recv(4096).decode('utf-8')
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print(f'{current_time} {message}', flush = True)
        else:
            message = input()
            sys.stdout.write("\033[F")
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print(f'{current_time} Você: {message}')
            server_message_full_information = f'{user_name}::{current_time}::{message}'
            server_connection.send(server_message_full_information.encode('utf-8'))
            if message == '!Desconectar':
                connect = False
                break

import threading
import datetime
import socket

PORT = 5050
SERVER = "192.168.0.105"
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDR)
server.listen(10)
 
clients_connected = []

def cancel_clients_connection(connection):
    if connection in clients_connected:
        clients_connected.remove(connection)


def send_message_to_all_other_clients(message, connection):
    for clients in clients_connected:
        if clients!=connection:
            try:
                clients.send(message.encode('utf-8'))
            except:
                clients.close()
                cancel_clients_connection(clients)


def handle_client(conn, addr):
    print(f"Usuário {addr} conectou!", flush = True)
    conn.send("Bem-vindo a sala de chat!".encode('utf-8'))
    ip_address = str(addr).split("'")[1]
    port_address = str(str(addr).split(", ")[1])[:-1]
    connected = True
    while connected:
        message = conn.recv(4096).decode("utf-8")
        if not message:
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M:%S")
            connected = False
            cancel_clients_connection(conn)
            final_message = f'{addr} foi desconectado em {current_time}!'
        elif message.split("::")[2] == "!Desconectar":
            user_name = message.split("::")[0]
            message_sent_time = message.split("::")[1]
            connected = False
            cancel_clients_connection(conn)
            final_message = f'Usuário {user_name} (IP:{ip_address} Port:{port_address}) se desconectou em {message_sent_time}!'
        else:
            user_name = message.split("::")[0]
            message_sent_time = message.split("::")[1]
            message_text = message.split("::")[2]
            final_message = f'{user_name}: {message_text}\nEnviada do local: [IP:{ip_address} Port:{port_address}] as: {message_sent_time}'
        print(final_message, flush = True)
        send_message_to_all_other_clients(final_message, conn)


def start():
    print('Server Iniciado!', flush=True)
    server.listen()
    while True:
        conn, addr = server.accept()
        clients_connected.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

start()

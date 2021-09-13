from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

server_host = "0.0.0.0"
server_port = 6677
input_buffer = 1024
addr = (server_host, server_port)
server = socket(AF_INET, SOCK_STREAM)
server.bind(addr)

client_sockets = {}
addresses = {}


def incoming_connections():
    while True:
        client, client_address = server.accept()
        print(f"{client_address} has connected.")
        client.send(bytes("Now Conntect.", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).daemon = True
        Thread(target=handle_client, args=(client,)).start()


if __name__ == "__main__":
    server.listen(3)
    accept = Thread(target=incoming_connections)
    accept.start()
    accept.join()
    server.close()
    

def handle_client(client):
    name = client.recv(input_buffer).decode("utf8")
    rules = f"Welcome {name}, please type {quit} if you need to exit."
    client.send(bytes(rules, "utf8"))
    join = f"{name} has joined the chat"
    broadcast(bytes(join, "utf8"))
    client_sockets[client] = name

    while True:
        msg = client.recv(input_buffer)
        if msg != bytes("{quit}", "{utf8}"):
            broadcast(msg, name + ": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del client_sockets[client]
            broadcast(bytes(f"{name} has left the chat.", "utf8"))
            break


def broadcast(msg, prefix=""):
    for sockt in client_sockets:
        sockt.send(bytes(prefix, "utf8") + msg)

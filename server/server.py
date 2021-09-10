import socket
from threading import Thread

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 6677
BUFSIZ = 1024
separator_token = "<SEP>"

client_sockets = set()

TCP_socket = socket.socket()

TCP_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

TCP_socket.bind((SERVER_HOST, SERVER_PORT))

TCP_socket.listen(5)

print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

clients = {}
addresses = {}


def incoming_connections(cs):
    while True:
        try:
            msg = cs.recv(1024).decode
        except Exception as expt:
            print(f"***Error***: {expt}")
            client_sockets.remove(cs)

    while True:
        client_socket, client_address = TCP_socket.accept()
        print(f"{client_address} has connected.")
        client_socket.sent(bytes("You are now connected.", "utf8"))
        client_sockets.add(client_socket)
        addresses[client_socket] = client_address
        Thread(target=handle_client, args=(client_socket,)).daemon = True
        Thread(target=handle_client, args=(client_socket,)).start()


def handle_client(client_socket):
    name = client_socket.recv(BUFSIZ).decode("utf8")
    rules = f"Welcome {name}, please type {quit} if you need to exit."
    client_socket.send(bytes(rules, "utf8"))
    join = f"{name} has joined the chat"
    broadcast(bytes(join, "utf8"))
    client_sockets[client_socket] = name

    while True:
        msg = client_socket.recv(BUFSIZ)
        if msg != bytes("{quit}", "{utf8}"):
            broadcast(msg, name + ": ")
        else:
            client_socket.send(bytes("{quit}", "utf8"))
            client_socket.close()
            del client_sockets[client_socket]
            broadcast(bytes(f"{name} has left the chat.", "utf8"))
            break

def broadcast(msg, prefix=""):
    for sock in client_sockets:
        sock.send(bytes(prefix, "utf8")+msg)

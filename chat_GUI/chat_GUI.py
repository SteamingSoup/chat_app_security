from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

server_host = input('Host: ')
server_port = input('Port: ')
if not server_port:
    server_port = 5002
else:
    server_port = int(server_port)
input_buffer = 1024
addr = (server_host, server_port)
socket = socket(AF_INET, SOCK_STREAM)
socket.connect(addr)

def receive():
    while True:
        try:
            msg = socket.recv(input_buffer).decode('utf8')
            msg_list.insert(tkinter.END, msg)
        except OSError:
            break
            

def send():
    msg = my_msg.get()
    my_msg.set("")
    socket.send(bytes(msg, 'utf8'))
    if msg == '{quit}':
        socket.close()
        top.quit()


def closing():
    my_msg.set('{quit}')
    send()

top = tkinter.Tk()
top.title("chat window")

top_frame = tkinter.Frame(top)
start_button = tkinter.Button(top_frame, text="Connect", command=lambda : start_server())
start_button.pack(side=tkinter.LEFT)
stop_button = tkinter.Button(top_frame, text="Stop", command=lambda : stop_server(), state=tkinter.DISABLED)
stop_button.pack(side=tkinter.LEFT)
top_frame.pack(side=tkinter.TOP, pady=(5, 0))

middle_frame = tkinter.Frame(top)
host_label = tkinter.Label(middle_frame, text = "Host: 127.0.0.1")
host_label.pack(side=tkinter.LEFT)
port_label = tkinter.Label(middle_frame, text = "Port: 5002")
port_label.pack(side=tkinter.LEFT)
middle_frame.pack(side=tkinter.TOP, pady=(5, 0))

client_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()
my_msg.set("Type your messages here.")
scrollbar = tkinter.Scrollbar(client_frame)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list = tkinter.Listbox(client_frame, height=15, width=50, yscrollcommand=scrollbar.set)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
tkinter_display = tkinter.Text(client_frame, height=15, width=40)
tkinter_display.pack(side=tkinter.LEFT, fill=tkinter.Y, padx=(5, 0))
scrollbar.config(command=tkinter_display.yview)
tkinter_display.config(yscrollcommand=scrollbar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
client_frame.pack(side=tkinter.BOTTOM, pady=(5,10))

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

def start_server():
    start_button.config(state=tkinter.DISABLED)
    stop_button.config(state=tkinter.NORMAL)

def stop_server():
    start_button.config(state=tkinter.NORMAL)
    stop_button.config(state=tkinter.DISABLED)

top.protocol("WM_DELETE_WINDOW", closing)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()

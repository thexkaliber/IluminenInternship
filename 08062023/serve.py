from tkinter import *
from tkinter import messagebox, ttk
import _thread
import socket


def send_message():
    global connected_clients
    message = entry.get()
    try:
        message_listbox.insert(END, message)
        client_socket.sendall(message.encode())
    except (OSError, NameError):
        messagebox.showerror(message='Make sure if the socket is connected.')
    entry.delete(0, END)


def handle_client(client_socket, client_address):
    global connected_clients
    connected_clients.append(client_socket)
    clients_listbox.insert(END, client_address)
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if data:
                message_listbox.insert(END, data)
        except (ConnectionResetError, ConnectionAbortedError):
            messagebox.showerror(message='Make sure if the socket is connected.')
            break


def stop_thread():
    message_listbox.insert(END, 'Server Stopped at localhost:4210')
    client_socket.close()


def start_thread(host='127.0.0.1', port=4210):
    global client_socket, connected_clients
    connected_clients =[]
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address}")

        _thread.start_new_thread(handle_client, (client_socket, client_address))
        message_listbox.insert(END, 'Server Started at localhost:4210')
        _thread.start_new_thread(send_message, ())


def start_chat_application():
    global root, entry, clients_listbox, message_listbox, client_socket

    root = Tk()
    root.title("Chat Application Server")
    root.geometry('900x630')
    root.minsize(900, 630)

    sendto_frame = Frame(root)
    sendto_frame.pack(side=TOP, anchor=NW, pady=5)

    dropdown_label = Label(sendto_frame, text='Send to: ')
    dropdown_label.pack(side=LEFT, anchor=NW, padx=10, pady=5)

    dropdown_default = StringVar()
    dropdown_default.set('Broadcast')
    dropdown_options = ['Broadcast', 'Client 1', 'Client 2']
    dropdown_menu = OptionMenu(sendto_frame, dropdown_default, *dropdown_options)
    dropdown_menu.pack(side=LEFT, anchor=NW)

    refresh_button = Button(sendto_frame, text="Refresh")
    refresh_button.pack(side=LEFT, anchor=NW, padx=5, pady=2)

    button_frame = Frame(root)
    button_frame.pack(side=TOP, anchor=NE, pady=5)

    start_button = Button(button_frame, text="Start", command=start_thread)
    start_button.pack(side=LEFT, anchor=NW, padx=5)

    stop_button = Button(button_frame, text="Stop", command=stop_thread)
    stop_button.pack(side=LEFT, anchor=NW, padx=5)


    clients_frame = Frame(root)
    clients_frame.pack(side=LEFT, anchor=W, padx=10)
    clients_list = Label(clients_frame, text='Connected Clients: ')
    clients_list.pack(side=TOP, anchor=NW)

    clients_listbox = Listbox(clients_frame, height=31)
    clients_listbox.pack(side=LEFT, fill=Y, anchor=W, ipady=10)

    chat = Label(root, text='Chat: ')
    chat.pack(side=TOP, anchor=NW, expand=FALSE)

    message_listbox = Listbox(root)
    message_listbox.pack(fill=BOTH, expand=TRUE, padx=4)

    entry_frame = Frame(root)
    entry_frame.pack(side=BOTTOM, fill=X, padx=5)

    entry = Entry(entry_frame)
    entry.pack(side=TOP, fill=X, expand=TRUE, pady=5)

    send_button = Button(entry_frame, text="Send", command=send_message)
    send_button.pack(side=RIGHT, pady=5)

    root.protocol("WM_DELETE_WINDOW", root.destroy)

    root.mainloop()


if __name__ == "__main__":
    start_chat_application()

from tkinter import *
from tkinter import messagebox
import _thread
import socket


def send_message():
    message = entry.get()
    try:
        client_socket.sendto(message.encode('utf-8'),('127.0.0.1',4210))
        print('sent')
    except (OSError, NameError):
        messagebox.showerror(message='Make sure if the socket is connected.')
    entry.delete(0, END)


def receive_messages():
    while True:
        try:
            data = client_socket.recvfrom(1024)
            (data, address) = data
            if data:
                message_listbox.insert(END, data.decode('utf-8'))
        except (ConnectionResetError, ConnectionAbortedError):
            messagebox.showerror(message='Make sure if the socket is connected.')
            break


def stop_thread():
    client_socket.close()


def start_thread(host='localhost', port=4210):
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.bind((host, port))

    _thread.start_new_thread(receive_messages, ())


def start_chat_application():
    global root, entry, message_listbox, client_socket

    root = Tk()
    root.title("Chat Application")

    start_button = Button(root, text="Start", command=start_thread)
    start_button.pack(side=TOP, anchor=NE)

    stop_button = Button(root, text="Stop", command=stop_thread)
    stop_button.pack(side=TOP, anchor=NE)

    exit_button = Button(root, text="Exit", command=root.destroy)
    exit_button.pack(side=TOP, anchor=NE)

    message_listbox = Listbox(root)
    message_listbox.pack(fill=BOTH, expand=True)

    entry = Entry(root)
    entry.pack(side=BOTTOM, fill=X)

    send_button = Button(root, text="Send", command=send_message)
    send_button.pack(side=BOTTOM)

    root.protocol("WM_DELETE_WINDOW", stop_thread)

    root.mainloop()


if __name__ == "__main__":
    start_chat_application()

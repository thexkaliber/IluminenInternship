from tkinter import *
from tkinter import messagebox
import _thread
import socket


def send_message():
    message = entry.get()
    try:
        client_socket.sendall(message.encode())

    except (OSError, NameError):
        messagebox.showerror(message='Make sure if the socket is connected.')
        connection_status.config(text='Connection Status: Disconnected')
    message_listbox.insert(END, message)
    entry.delete(0, END)


def receive_messages():
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if data:
                message_listbox.insert(END, data)
        except (ConnectionResetError, ConnectionAbortedError, OSError):
            messagebox.showerror(message='Make sure if the socket is connected.')
            connection_status.config(text='Connection Status: Disconnected')
            break


def stop_thread():
    try:
        client_socket.close()
        root.destroy()
    except NameError:
        root.destroy()


def start_thread():
    global client_socket
    try:
        host = connectto_entry.get()
        host, port = str(host).split(':')
    except ValueError:
        messagebox.showerror(message='Enter a valid IP:Port')
    connection_status.config(text='Connection Status: Disconnected')
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, int(port)))
        _thread.start_new_thread(send_message, ())
        _thread.start_new_thread(receive_messages, ())
        connection_status.config(text='Connection Status: Connected')
    except ConnectionRefusedError:
        messagebox.showerror(message='Make sure if the server is turned on.')
        connection_status.config(text='Connection Status: Disconnected')


def gui():
    global root, entry, message_listbox, client_socket, connection_status, connectto_entry

    root = Tk()
    root.title("Chat Application Client")
    root.minsize(400,330)
    root.maxsize(root.winfo_screenwidth(),330)
    main_frame = Frame(root)
    main_frame.pack(fill=X)

    connectto_entryframe = Frame(main_frame)
    connectto_entryframe.pack(side=TOP, anchor=NW, padx=5, pady=10)

    connectto_label = Label(connectto_entryframe, text='Connect to: ')
    connectto_label.pack(side=LEFT, anchor=NW)

    connectto_entry = Entry(connectto_entryframe)
    connectto_entry.pack(side=LEFT, anchor=NW)

    connect_status = Button(main_frame, text='Connect/Refresh', command=start_thread)
    connect_status.pack(side=TOP, anchor=NE, padx=5, pady=5)

    connection_status = Label(main_frame, text='Connection Status: Unknown')
    connection_status.pack(side=TOP, anchor=NW, padx=5)



    message_listbox = Listbox(main_frame)
    message_listbox.pack(fill=BOTH, padx=5)

    entry_frame = Frame(main_frame)
    entry_frame.pack(side=BOTTOM, fill=X, padx=5)
    entry = Entry(entry_frame)
    entry.pack(side=TOP, fill=X, expand=TRUE,pady=5)
    send_button = Button(entry_frame, text="Send", command=send_message)
    send_button.pack(side=RIGHT, pady=5)
    root.protocol("WM_DELETE_WINDOW", stop_thread)

    root.mainloop()
    start_thread()


if __name__ == "__main__":
    gui()

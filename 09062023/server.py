from tkinter import *
from tkinter import messagebox, ttk
import tkinter
import _thread
import socket

server_socket = None
clients = []


def send_message():
    """
    Send Messages to the connected server by getting input from the Entry Widget and sending it to through a Socket
    Connection.


    Parameters defined/used:
    entry (widget) - Get Message Data
    message (str) - Message Data
    sendto (str) - Recipient Connection
    message_listbox (widget) - Message Listbox Widget
    response (str) - Response Data
    client_socket, client_sockets (obj) - Socket object

    """

    message = entry.get()
    sendto = dropdown_option.get()
    if str(sendto) == 'Broadcast': # Default Behaviour is to Broadcast
        try:
            for client_sockets in clients:
                response = "Server broadcast:  " + message
                client_sockets.sendall(response.encode())
            message_listbox.insert(END, message)
        except (OSError, NameError):
            messagebox.showerror(message='Make sure if the socket is connected.')
    else:
        try:
            for client_socket in clients:  # Send to specific client if sendto is not 'Broadcast'
                if str(client_socket) == str(sendto):
                    response = "Server whispered:  " + message
                    client_socket.sendall(response.encode())
                    message_listbox.insert(END, message)
                    break
        except (OSError, NameError):
            messagebox.showerror(message='Make sure if the socket is connected.')

    entry.delete(0, END)


def handle_client(client_socket):
    """
    Handle Clients and Receive Data from the different clients.


    Parameters defined/used:
    data (bytes) - Raw Message Data
    message (str) - Message Data
    message_listbox (widget) - Message Listbox Widget
    client_socket (obj) - Socket object
    clients (list) - Connected Clients List
    client_address (list) - Client Address Information

    """

    global clients

    while True:  # Receive data from any of the clients
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode()
            message_listbox.insert(END, f"Received from client {client_address[0]}:{client_address[1]}: {message}")

        except ConnectionResetError:
            break

    # Close Socket Connection if the Connection no longer exists
    client_socket.close()
    clients.remove(client_socket)


def update_client_menu():
    """
    Update GUI with the latest status of the Connected Clients available to send data to.


    Parameters defined/used:
    dropdown_menu (widget) - OptionMenu Widget
    menu (Any) - OptionMenu options
    dropdown_option (StringVar) - Default Option
    client(obj) - Socket object
    clients (list) - Connected Clients List
    client_address (list) - Client Address Information

    """

    menu = dropdown_menu['menu']
    menu.delete(0, END)
    menu.add_command(label=f"Broadcast")
    for client in clients:  # Generate Options for the OptionMenu based on connected clients.
        client_address = client.getpeername()
        menu.add_command(label=f"{client_address[0]}:{client_address[1]}",
                         command=tkinter._setit(dropdown_option, client))

    if not clients:
        dropdown_option.set("No Clients connected.")


def update_clients():
    """
    Update GUI with the latest status of the Connected Clients in a list and call update_client_menu to update the
    available connections to send to.


    Parameters defined/used:
    updater (obj) - root.after ID variable
    clients_listbox (widget) - Clients Listbox Widget
    client(obj) - Socket object
    clients (list) - Connected Clients List
    client_address (list) - Client Address Information

    """

    global updater
    clients_listbox.delete(0, END)
    for client in clients: # Generate items for the Listbox based on connected clients
        client_address = client.getpeername()
        clients_listbox.insert(END, f"{client_address[0]}:{client_address[1]}")
    update_client_menu()
    updater = root.after(1000, update_clients)  # Callback every 1 second to refresh status of connected clients.


def accept_connections():
    """
    Accept Connections from Clients and call update_clients function to update the list of available connections


    Parameters defined/used:
    server_socket, client_socket (obj) - Socket Object
    clients (list) - Connected Clients List
    client_address (list) - Client Address Information
    clients_listbox (widget) - Clients Listbox Widget

    """
    global server_socket, clients, client_address, clients_listbox

    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        message_listbox.insert(END, f"Accepted connection from {client_address[0]}:{client_address[1]}")
        clients_listbox.insert(END, f"{client_address[0]}:{client_address[1]}")
        _thread.start_new_thread(handle_client, (client_socket,))
        update_clients()


def stop_thread():
    """
    Close the connection and/or exit the application by stopping all Socket Connection Threads, kept track in the
    Connected Clients List and/or destroy the Application Mainloop.


    Parameters defined/used:
    server_socket, client_socket (obj) - Socket object
    clients (list) - Connected Clients List
    message_listbox (widget) - Message Listbox Widget
    updater (obj) - root.after ID variable

    """

    global server_socket, clients

    message_listbox.insert(END, "Stopping server...")

    for client_socket in clients: # Attempt to close threads and clear connection list
        client_socket.close()
    clients.clear()

    server_socket.close()
    root.after_cancel(updater)  # Stop Callback when all threads are closed.
    message_listbox.insert(END, "Server stopped.")


def start_thread():
    """
    Create a Socket for connection to the Client by binding to an IP & Port and attempt to initialize the Socket
    Connection by creating a Socket Connection Thread whenever a new Client is trying to connect to the Server.


    Parameters defined/used:
    client_socket (obj) - Socket object
    message_listbox (widget) - Listbox Widget

    """

    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 4210))
    server_socket.listen(5)  # Listen for a maximum of 5 connections.

    message_listbox.insert(END, "Server started. Listening for connections...")

    _thread.start_new_thread(accept_connections, ())


def gui():
    """
    Initialize Tkinter Event Mainloop, Root Window, Frames, Bindings and relevant Widgets to connect to a client,
    start/stop threads, check Connection Status and to send/receive messages.


    Parameters defined/used:
    root (func) - Root Window
    entry (widget) - Get Message Data
    clients_listbox (widget) - Clients Listbox Widget
    message_listbox (widget) - Listbox Widget
    client_socket (obj) - Socket object
    dropdown_option (StringVar) - Default Option
    dropdown_menu (widget) - OptionMenu Widget

    """

    # Global Variables and Widgets
    global root, entry, clients_listbox, message_listbox, client_socket, dropdown_option, dropdown_menu

    # Create Root Window
    root = Tk()
    root.title("Chat Application Server")
    root.geometry('950x630')
    root.minsize(980, 630)

    # Create Connection Recipient Frame
    sendto_frame = Frame(root)
    sendto_frame.pack(side=TOP, anchor=NW, pady=5)

    # Connection Recipient Frame Widgets
    dropdown_label = Label(sendto_frame, text='Send to: ')
    dropdown_label.pack(side=LEFT, anchor=NW, padx=10, pady=5)

    dropdown_option = StringVar()
    dropdown_option.set('Broadcast')
    dropdown_menu = OptionMenu(sendto_frame, dropdown_option, 'No Clients connected.')
    dropdown_menu.pack(side=LEFT, anchor=NW)

    # Create Server Control Frame
    button_frame = Frame(root)
    button_frame.pack(side=TOP, anchor=NE, pady=5)

    # Server Control Frame Buttons
    start_button = Button(button_frame, text="Start", command=start_thread)
    start_button.pack(side=LEFT, anchor=NW, padx=5)

    stop_button = Button(button_frame, text="Stop", command=stop_thread)
    stop_button.pack(side=LEFT, anchor=NW, padx=5)

    # Create Clients List Frame
    clients_frame = Frame(root)
    clients_frame.pack(side=LEFT, anchor=W, padx=10)

    # Clients List Frame Widgets
    clients_list = Label(clients_frame, text='Connected Clients: ')
    clients_list.pack(side=TOP, anchor=NW)

    clients_listbox = Listbox(clients_frame, height=31)
    clients_listbox.pack(side=LEFT, fill=Y, anchor=W, ipady=10)

    # Create Chat Frame
    chat_frame = Frame(root)
    chat_frame.pack(side=TOP, anchor=W, fill=BOTH, expand=TRUE)

    # Chat Frame Widgets
    chat = Label(chat_frame, text='Chat: ')
    chat.pack(side=TOP, anchor=NW, expand=FALSE)

    xscrollbar = ttk.Scrollbar(chat_frame, orient=HORIZONTAL)
    xscrollbar.pack(side="bottom", fill="x")

    yscrollbar = ttk.Scrollbar(chat_frame, orient=VERTICAL)
    yscrollbar.pack(side="right", fill="y")

    message_listbox = Listbox(chat_frame, xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
    message_listbox.pack(fill=BOTH, expand=TRUE, padx=4)

    # Create Chat Entry Frame
    entry_frame = Frame(root)
    entry_frame.pack(side=BOTTOM, fill=X, padx=5)

    # Chat Entry Frame Widgets
    entry = Entry(entry_frame)
    entry.pack(side=TOP, fill=X, expand=TRUE, pady=5)

    send_button = Button(entry_frame, text="Send", command=send_message)
    send_button.pack(side=RIGHT, pady=5)

    # Root Configurations
    root.bind('<Return>', (lambda event: send_message()))
    root.protocol("WM_DELETE_WINDOW", root.destroy)

    # Initialize GUI Event Loop
    root.mainloop()


if __name__ == "__main__":
    gui()

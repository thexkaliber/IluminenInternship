from tkinter import *
from tkinter import messagebox, ttk
import _thread
import socket
import re


def send_message():
    """
    Send Messages to the connected server by getting input from the Entry Widget and sending it to through a Socket
    Connection.

    Parameters defined/used:
    entry (widget) - Get Message Data
    message_listbox (widget) - Listbox Widget
    connection_status (widget) - Connection Status Label Widget
    message (str) - Message Data
    client_socket (obj) - Socket object
    """

    message = entry.get()
    try:
        client_socket.sendall(message.encode())
        message_listbox.insert(END, message)

    except (OSError, NameError):  # Change Connection Status if error occurs
        messagebox.showerror(message='Make sure if the socket is connected.')
        connection_status.config(text='Connection Status: Disconnected', foreground='red')
    entry.delete(0, END)


def receive_messages():
    """
    Receive Messages from the connected server by making the Socket Connection available to receive data.

    Parameters defined/used:
    data (str) - Received Data
    message_listbox (widget) - Listbox Widget
    connection_status (widget) - Connection Status Label Widget
    client_socket (obj) - Socket object
    """

    while True:
        try:
            data = client_socket.recv(1024).decode()
            connection_status.config(text='Connection Status: Connected', foreground='green')
            if data:
                message_listbox.insert(END, data)
        except (ConnectionResetError, ConnectionAbortedError, OSError):  # Change Connection Status if error occurs
            messagebox.showerror(message='Make sure if the socket is connected.')
            connection_status.config(text='Connection Status: Disconnected', foreground='red')
            break


def refresh():
    """
    Check if connection still exists by sending a whitespace byte to server

    Parameters defined/used:
    client_socket (obj) - Socket object
    connection_status (widget) - Connection Status Label Widget
    """

    try:
        client_socket.sendall(b' ')
        connection_status.config(text='Connection Status: Connected', foreground='green')
    except (ConnectionResetError, ConnectionAbortedError, OSError):
        connection_status.config(text='Connection Status: Disconnected', foreground='red')


def stop_thread():
    """
    Close the connection and/or exit the application by stopping all Socket Connection Threads and/or destroy the
    Application Mainloop.

    Parameters defined/used:
    client_socket (obj) - Socket object
    """

    try:  # If connections exist, close the Sockets and exit
        client_socket.close()
        root.destroy()
    except NameError:  # Else exit immediately
        root.destroy()


def start_thread():
    """
    Create a Socket for connection to the Server by accepting a Host and Port, check for invalid addresses and
    attempt to initialize the Socket Connection by creating a Socket Connection Thread.

    Parameters defined/used:
    host (str) - IP Address
    port (int) - Port
    message_listbox (widget) - Listbox Widget
    connection_status (widget) - Connection Status Label Widget
    connectto_entry (widget) - Connection Establishment Entry Widget
    client_socket (obj) - Socket object
    """

    global client_socket  # Access Global Variables
    try:  # Check if given IP is valid
        host = connectto_entry.get()
        port = 4210  # Default Port
        if re.match(r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$", host) or re.match('localhost', host):
            pass
        else:
            raise ValueError
    except ValueError:  # Throw Error if not a valid IP
        messagebox.showerror(message='Enter a valid IP to be connected to the 4210 port.')
    connection_status.config(text='Connection Status: Disconnected', foreground='red')

    # Try to Initialize the Socket and create a thread
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, int(port)))
        _thread.start_new_thread(send_message, ())
        _thread.start_new_thread(receive_messages, ())
        connection_status.config(text='Connection Status: Connected', foreground='green')
        message_listbox.insert(0, f'***Connected to Server at {host} on port {port}***')

    except ConnectionRefusedError:  # Throw Error if not connected
        messagebox.showerror(message='Make sure if the server is turned on.')
        connection_status.config(text='Connection Status: Disconnected', foreground='red')


def gui():
    """
    Initialize Tkinter Event Mainloop, Root Window, Frames, Bindings and relevant Widgets to connect to a server,
    start/stop threads, check Connection Status and to send/receive messages.


    Parameters defined/used:
    root (func) - Root Window
    entry (widget) - Get Message Data
    message_listbox (widget) - Listbox Widget
    client_socket (obj) - Socket object
    connection_status (widget) - Connection Status Label Widget
    connectto_entry (widget) - Connection Establishment Entry Widget
    """

    # Global Variables and Widgets
    global root, entry, message_listbox, client_socket, connection_status, connectto_entry

    # Create Root Window
    root = Tk()
    root.title("Chat Application Client")
    root.minsize(400, 360)
    root.maxsize(root.winfo_screenwidth(), 330)

    # Create Main Frame
    main_frame = Frame(root)
    main_frame.pack(fill=X)

    # Create Connection Entry Frame
    connectto_entryframe = Frame(main_frame)
    connectto_entryframe.pack(side=TOP, anchor=NW, padx=5, pady=10)

    # Connection Entry Frame Widgets
    connectto_label = Label(connectto_entryframe, text='Connect to: ')
    connectto_label.pack(side=LEFT, anchor=NW)

    connectto_entry = Entry(connectto_entryframe)
    connectto_entry.pack(side=LEFT, anchor=NW)

    # Create Connection Establishment Frame
    connect_frame = Frame(main_frame)
    connect_frame.pack(side=TOP, anchor=NE, padx=5, pady=5)

    # Connection Establishment Frame Widgets
    connect = Button(connect_frame, text='Connect', command=start_thread)
    connect.pack(side=LEFT, anchor=NE, padx=4, pady=5)

    refresh_status = Button(connect_frame, text='Refresh', command=refresh)
    refresh_status.pack(side=LEFT, anchor=NE, padx=4, pady=5)

    # Connection Status Indicator
    connection_status = Label(main_frame, text='Connection Status: Unknown')
    connection_status.pack(side=TOP, anchor=NW, padx=5)

    # Create Message Log Frame
    message_frame = Frame(main_frame)
    message_frame.pack(fill=BOTH, padx=5)

    # Message Log Frame Widgets
    xscrollbar = ttk.Scrollbar(message_frame, orient=HORIZONTAL)
    xscrollbar.pack(side="bottom", fill="x")

    yscrollbar = ttk.Scrollbar(message_frame, orient=VERTICAL)
    yscrollbar.pack(side="right", fill="y")

    message_listbox = Listbox(message_frame, xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
    message_listbox.pack(fill='both', expand=TRUE)
    
    xscrollbar.config(command=message_listbox.xview)
    yscrollbar.config(command=message_listbox.yview)


    # Create Message Entry Frame
    entry_frame = Frame(main_frame)
    entry_frame.pack(side=BOTTOM, fill=X, padx=5)

    # Message Entry Frame Widgets
    entry = Entry(entry_frame)
    entry.pack(side=TOP, fill=X, expand=TRUE, pady=5)

    send_button = Button(entry_frame, text="Send", command=send_message)
    send_button.pack(side=RIGHT, pady=5)

    # Root Configurations
    root.bind('<Return>', (lambda event: send_message()))
    root.protocol("WM_DELETE_WINDOW", stop_thread)

    # Initialize GUI Event Loop
    root.mainloop()


if __name__ == "__main__":
    gui()

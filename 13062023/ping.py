from tkinter import *
from tkinter import ttk, messagebox
# import pickle
import datetime
import socket
import re


def clear():

    """
    Clears the listbox.

    Parameters defined/used:
    log_listbox(widget) - Activity Log Listbox Widget
    """
    log_listbox.delete(0, END)


def send_messages():

    """
    Sends Messages to the Receiver.

    connection_status (widget) - Connection Status Label Widget
    packet_entry (widget) - Packet Data Entry Widget
    delay_entry (widget) - Delay Entry Widget
    data (str) - Data as string
    delay (int) - Delay in seconds
    response (Any) - Response as string or other data type.
    client_socket (obj) - Socket object
    log_listbox (widget) - Activity Log Listbox Widget
    pinger (obj)- root.after Object ID
    """
    global connection_status
    data = packet_entry.get()
    delay = delay_entry.get()
    if delay == '':
        delay = 1
    try:
        response = '[' + str(datetime.datetime.now().replace(microsecond=0)) + ']: ' + data
        # response = [str(datetime.datetime.now().replace(microsecond=0)),data]
        # response = pickle.dumps(response)
        client_socket.sendall(response.encode())
        log_listbox.insert(END, response)
        pinger = root.after(int(delay) * 1000, send_messages)

    except (OSError, NameError, ConnectionResetError, ConnectionAbortedError):
        # Change Connection Status if error occurs
        messagebox.showerror(message='Make sure if the socket is connected.')
        connection_status.config(text='Connection Status: Disconnected', foreground='red')
        connect_button.config(text='Connect', relief=RAISED, width=7)
        root.after_cancel(pinger)
    except UnboundLocalError:
        pass


def stop_connection():

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


def start_connection():

    """
    Create a Socket for connection to the Server by accepting a Host and Port, check for invalid addresses and
    attempt to initialize the Socket Connection by creating a Socket Connection Thread.

    Parameters defined/used:
    host (str) - IP Address
    port (int) - Port
    log_listbox (widget) - Activity Log Listbox Widget
    connection_status (widget) - Connection Status Label Widget
    connectto_entry (widget) - Connection Establishment Entry Widget
    connect_button (widget) - Connect/Disconnect Button Widget
    client_socket (obj) - Socket object
    """

    global client_socket, connection_status
    connect_button.config(relief=SUNKEN)
    try:
        host = connectto_entry.get()
        port = 4210  # Default Port
        if re.match(r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$", host) or re.match('localhost', host):
            pass
        elif re.match(r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$", socket.gethostbyname(host)):
            pass
        else:
            raise ValueError
    except ValueError:  # Throw Error if not a valid IP
        messagebox.showerror(message='Enter a valid IP to be connected to the 4210 port.')
        connection_status.config(text='Connection Status: Disconnected', foreground='red')
        connect_button.config(text='Connect', relief=RAISED, width=7)

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, int(port)))
        connection_status.config(text='Connection Status: Connected', foreground='green')
        log_listbox.insert(0, f'***Connected to Server at {host} on port {port}***')

    except (ConnectionRefusedError, ConnectionAbortedError):  # Throw Error if not connected
        messagebox.showerror(message='Make sure if the server is turned on.')
        connection_status.config(text='Connection Status: Disconnected', foreground='red')
        connect_button.config(text='Connect', relief=RAISED, width=7)


def connect_toggle():

    """
    Toggles the Connect Button between Connect and Disconnect

    Parameters used/defined:
    connect_button (widget) - Connect/Disconnect Button Widget
    client_socket (obj) - Socket object
    start_connection (func) - Function call
    """

    if connect_button.config('text')[-1] == 'Disconnect':
        client_socket.close()
        connect_button.config(text='Connect', relief=RAISED, width=7)
    else:
        connect_button.config(text='Disconnect', width=10)
        start_connection()


def gui():

    """
    Initialize Tkinter Event Mainloop, Root Window, Frames, Bindings and relevant Widgets to connect to a server,
    check Connection Status and to send messages.

    Parameters defined/used:
    root (func) - Root Window
    log_listbox (widget) - Activity Log Listbox Widget
    connectto_entry (widget) - Connection Establishment Entry Widget
    packet_entry (widget) - Packet Data Entry Widget
    delay_entry (widget) - Delay Entry Widget
    connection_status (widget) - Connection Status Label Widget
    connect_button (widget) - Connect/DisconnectButton Widget
    """

    global root, log_listbox, connect_button, connection_status, connectto_entry, packet_entry, delay_entry
    root = Tk()
    root.title('Pinger')
    root.geometry('500x400')

    main_frame = Frame(root)
    main_frame.pack(fill=X)

    # Create Connection Entry Frame
    connectto_entryframe = Frame(main_frame)
    connectto_entryframe.pack(side=TOP, anchor=NW, fill=X, padx=5, pady=10)

    # Connection Entry Frame Widgets
    connectto_label = Label(connectto_entryframe, text='Connect to: ')
    connectto_label.pack(side=LEFT, anchor=NW, pady=5)

    connectto_entry = Entry(connectto_entryframe, width=50)
    connectto_entry.pack(side=LEFT, anchor=NW, padx=5, pady=5)

    connect_button = Button(connectto_entryframe, text='Connect', width=7, command=connect_toggle)
    connect_button.pack(side=RIGHT, anchor=NE, padx=5, fill=X)

    # Create Message Entry Frame
    entries_frame = Frame(main_frame)
    entries_frame.pack(side=TOP, anchor=NW, fill=X, padx=5, pady=5)

    # Message Entry Frame Widgets
    packet_frame = Frame(entries_frame)
    packet_frame.pack(side=TOP, anchor=NW, fill=X)

    entry_label = Label(packet_frame, text='Send Packet: ')
    entry_label.pack(side=LEFT, anchor=NW, pady=5)

    packet_entry = Entry(packet_frame, width=30)
    packet_entry.pack(side=LEFT, anchor=NW, pady=5)

    # Create Delay Entry Frame
    delay_frame = Frame(entries_frame)
    delay_frame.pack(side=BOTTOM, anchor=NW, fill=X)

    # Delay Entry Frame Widgets
    delay_label = Label(delay_frame, text='Delay (s): ')
    delay_label.pack(side=LEFT, anchor=NW, pady=5)

    delay_entry = Entry(delay_frame)
    delay_entry.pack(side=LEFT, anchor=NW, padx=19, pady=5)

    send_button = Button(delay_frame, text="Send", width=7, command=send_messages)
    send_button.pack(side=RIGHT, padx=5, pady=5, fill=X)

    # Connection Status Indicator
    connection_status = Label(main_frame, text='Connection Status: Unknown')
    connection_status.pack(side=TOP, anchor=NW, padx=5)

    # Clear Activity Log
    clear_button = Button(main_frame, text="Clear", command=clear)
    clear_button.pack(side=TOP, anchor=NE, padx=5, pady=5)

    # Create Activity Log Frame
    log_labelframe = LabelFrame(main_frame, text=' Activity Log  ')
    log_labelframe.pack(side=BOTTOM, fill=BOTH, expand=TRUE, padx=5, pady=5)

    # Activity Log Widgets
    yscrollbar = ttk.Scrollbar(log_labelframe, orient=VERTICAL)
    yscrollbar.pack(side=RIGHT, fill=Y)

    log_listbox = Listbox(log_labelframe, height=30, yscrollcommand=yscrollbar.set)
    log_listbox.pack(fill=BOTH, expand=TRUE, padx=5, pady=10)

    yscrollbar.config(command=log_listbox.yview)

    # Root Configurations and Bindings
    root.protocol("WM_DELETE_WINDOW", stop_connection)
    root.mainloop()


if __name__ == '__main__':
    gui()

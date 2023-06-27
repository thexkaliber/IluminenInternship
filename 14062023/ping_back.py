# import pickle
from tkinter import END, SUNKEN, RAISED, messagebox
import datetime
import socket
import re


def clear(gui):

    """
    Clears the listbox.

    Parameters defined/used:
    log_listbox(widget) - Activity Log Listbox Widget
    """
    gui.log_listbox.delete(0, END)


def send_messages(gui):

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
    data = gui.packet_entry.get()
    delay = gui.delay_entry.get()
    if delay == '':
        delay = 1
    try:
        response = '[' + str(datetime.datetime.now().replace(microsecond=0)) + ']: ' + data
        # response = [str(datetime.datetime.now().replace(microsecond=0)),data]
        # response = pickle.dumps(response)
        client_socket.sendall(response.encode())
        gui.log_listbox.insert(END, response)
        if int(delay) > 0:
            pinger = gui.root.after(int(delay) * 1000, send_messages, gui)

    except (OSError, NameError, ConnectionResetError, ConnectionAbortedError):
        # Change Connection Status if error occurs
        messagebox.showerror(message='Make sure if the socket is connected.')
        gui.connection_status.config(text='Connection Status: Disconnected', foreground='red')
        gui.connect_button.config(text='Connect', relief=RAISED, width=7)
        gui.root.after_cancel(pinger)
    except UnboundLocalError:
        pass


def stop_connection(gui):

    """
    Close the connection and/or exit the application by stopping all Socket Connection Threads and/or destroy the
    Application Mainloop.

    Parameters defined/used:
    client_socket (obj) - Socket object
    """

    try:  # If connections exist, close the Sockets and exit
        client_socket.close()
        gui.root.destroy()
    except NameError:  # Else exit immediately
        gui.root.destroy()


def start_connection(gui):

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
    gui.connect_button.config(relief=SUNKEN)
    try:
        host = gui.connectto_entry.get()
        port = 4210  # Default Port
        if re.match(r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$", host) or re.match('localhost', host):
            pass
        elif re.match(r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$", socket.gethostbyname(host)):
            pass
        else:
            raise ValueError
    except ValueError:  # Throw Error if not a valid IP
        messagebox.showerror(message='Enter a valid IP to be connected to the 4210 port.')
        gui.connection_status.config(text='Connection Status: Disconnected', foreground='red')
        gui.connect_button.config(text='Connect', relief=RAISED, width=7)

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, int(port)))
        gui.connection_status.config(text='Connection Status: Connected', foreground='green')
        gui.log_listbox.insert(0, f'***Connected to Server at {host} on port {port}***')

    except (ConnectionRefusedError, ConnectionAbortedError):  # Throw Error if not connected
        messagebox.showerror(message='Make sure if the server is turned on.')
        gui.connection_status.config(text='Connection Status: Disconnected', foreground='red')
        gui.connect_button.config(text='Connect', relief=RAISED, width=7)


def connect_toggle(gui):

    """
    Toggles the Connect Button between Connect and Disconnect

    Parameters used/defined:
    connect_button (widget) - Connect/Disconnect Button Widget
    client_socket (obj) - Socket object
    start_connection (func) - Function call
    """

    if gui.connect_button.config('text')[-1] == 'Disconnect':
        client_socket.close()
        gui.connect_button.config(text='Connect', relief=RAISED, width=7)
    else:
        gui.connect_button.config(text='Disconnect', width=10)
        start_connection(gui)

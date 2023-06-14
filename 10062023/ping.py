from tkinter import *
from tkinter import ttk, messagebox
import socket
import re


def send_messages():
    global connection_status
    data = packet_entry.get()
    delay = delay_entry.get()
    if delay == '':
        delay = 1
    try:
        client_socket.sendall(data.encode())
        log_listbox.insert(END, data)
        pinger = root.after(int(delay)*1000, send_messages)

    except (OSError, NameError, ConnectionResetError, ConnectionAbortedError):
        # Change Connection Status if error occurs
        messagebox.showerror(message='Make sure if the socket is connected.')
        connection_status.config(text='Connection Status: Disconnected', foreground='red')
        root.after_cancel(pinger)
    except UnboundLocalError:
        pass

def clear():
    log_listbox.delete(0, END)

def start_connection():
    global client_socket, connection_status
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

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, int(port)))
        connection_status.config(text='Connection Status: Connected', foreground='green')
        log_listbox.insert(0, f'***Connected to Server at {host} on port {port}***')

    except (ConnectionRefusedError, ConnectionAbortedError):  # Throw Error if not connected
        messagebox.showerror(message='Make sure if the server is turned on.')
        connection_status.config(text='Connection Status: Disconnected', foreground='red')


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


def gui():
    global root, log_listbox, connection_status, connectto_entry, packet_entry, delay_entry
    root = Tk()
    root.title('Pinger')
    # root.minsize(500, 400)
    # root.maxsize(1600, 400)

    main_frame = Frame(root)
    main_frame.pack(fill=X)

    # Create Connection Entry Frame
    connectto_entryframe = Frame(main_frame)
    connectto_entryframe.pack(side=TOP, anchor=NW, fill=X, padx=5, pady=10)

    # Connection Entry Frame Widgets
    connectto_label = Label(connectto_entryframe, text='Connect to: ')
    connectto_label.pack(side=LEFT, anchor=NW, pady=5)

    connectto_entry = Entry(connectto_entryframe, width=50)
    connectto_entry.pack(side=LEFT, anchor=NW, pady=5)

    connect_button = Button(connectto_entryframe, text='Connect', width=7, command=start_connection)
    connect_button.pack(side=RIGHT, anchor=NE, padx=5, fill=X)

    # Create Message Entry Frame
    entry_frame = Frame(main_frame)
    entry_frame.pack(side=TOP, anchor=NW, fill=X, padx=5, pady=5)

    # Message Entry Frame Widgets

    entry_label = Label(entry_frame, text='Send Packet: ')
    entry_label.pack(side=LEFT, anchor=NW, pady=5)

    packet_entry = Entry(entry_frame, width=30)
    packet_entry.pack(side=LEFT, pady=5)

    delay_label = Label(entry_frame, text='Delay (s): ')
    delay_label.pack(side=LEFT, padx=5, pady=5)

    delay_entry = Entry(entry_frame)
    delay_entry.pack(side=LEFT, pady=5)

    send_button = Button(entry_frame, text="Send", width=7, command=send_messages)
    send_button.pack(side=RIGHT, padx=5, pady=5, fill=X)

    # Connection Status Indicator
    connection_status = Label(main_frame, text='Connection Status: Unknown')
    connection_status.pack(side=TOP, anchor=NW, padx=5)

    clear_button = Button(main_frame, text="Clear", command=clear)
    clear_button.pack(side=TOP, anchor=NE, padx=5, pady=5)

    # Create Activity Log Frame
    log_labelframe = LabelFrame(main_frame, text=' Activity Log  ')
    log_labelframe.pack(side=TOP, anchor=NW, fill=BOTH, expand=TRUE, padx=5, pady=5)

    yscrollbar = ttk.Scrollbar(log_labelframe, orient=VERTICAL)
    yscrollbar.pack(side=RIGHT, fill=Y)

    log_listbox = Listbox(log_labelframe, yscrollcommand=yscrollbar.set)
    log_listbox.pack(fill=BOTH, expand=TRUE, padx=5, pady=10)

    yscrollbar.config(command=log_listbox.yview)

    root.protocol("WM_DELETE_WINDOW", stop_connection)
    root.mainloop()


if __name__ == '__main__':
    gui()

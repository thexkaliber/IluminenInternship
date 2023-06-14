from tkinter import *
from tkinter import ttk
import socket
import _thread

# Root window
root = Tk()
root.title('Socket Tkintering')
tab_views = ttk.Notebook(root)

send_tab = ttk.Frame(tab_views)
recv_tab = ttk.Frame(tab_views)

tab_views.add(send_tab, text='Send')
tab_views.add(recv_tab, text='Receive')
tab_views.pack(expand=1, fill='both')

# Initialize Variables
setport_data = StringVar()

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = "127.0.0.1"
PORT = 69



# Create Socket Function
def send_data():
    print("123")
    data = "msg"
    soc.connect((HOST, PORT))
    soc.send(data.encode("utf-8"))


def start_thread():
    _thread.start_new_thread(send_data, ())


# Create Submit Function
def submit():
    setport = setport_data.get()
    setmsg = setmsg_input.get("1.0", END)
    print(setport, end='\n')
    print(setmsg, end='\n')
    setport_data.set("")
    setmsg_input.delete("1.0", END)
    # send_data(setport, setmsg)


# Title
title_label = Label(send_tab, text='Sockets and Tkinter')
title_label.grid(column=1, row=0, columnspan=3, padx=5, pady=5)

# Port
setport_label = Label(send_tab, text="Set Port:")
setport_label.grid(column=1, row=1, padx=5, pady=5)

setport_input = Entry(send_tab, textvariable=setport_data, width=43)
setport_input.grid(column=2, row=1, sticky=W, padx=5, pady=5)

# Message
setmsg_label = Label(send_tab, text="Enter Message:")
setmsg_label.grid(column=1, row=2, padx=5, pady=5)

setmsg_input = Text(send_tab, height=10, width=32, state="normal")
setmsg_input.grid(column=2, row=2, columnspan=2, padx=5, pady=5)

# Submit Button
submit_button = Button(send_tab, text="Submit", command=start_thread)  # submit
submit_button.grid(column=2, row=4, sticky=E, padx=5, pady=5)


# Receive tab

def receive_data():
    with soc:
        while True:
            data = soc.recv(1024).decode('utf-8')
            if not data:
                break
            print(data)
            msg_output.insert(END, "Data Received")


def start_recv_thread():
    # Create a thread to continuously listen for messages

    _thread.start_new_thread(receive_data, ())

    while True:
        msg_output.insert(END, "Data Received")


def stop_thread():
    _thread.exit()


# Title
# title_label = Label(send_tab, text='Sockets and Tkinter')
# title_label.grid(column=1, row=0, columnspan=3, padx=5, pady=5)

# Port
# setport_label = Label(recv_tab, text=f"Port set as :")
# setport_label.grid(column=1, row=1, padx=5, pady=5)

# Message
msg_label = Label(recv_tab, text="Messages Received:")
msg_label.grid(column=1, row=1, padx=5, pady=5)

msg_output = Text(recv_tab, height=10, width=32, state="normal")
msg_output.grid(column=2, row=1, columnspan=2, padx=5, pady=5)

# Submit Button
start_button = Button(recv_tab, text="Start", command=receive_data)
start_button.grid(column=3, row=0, sticky=E, padx=5, pady=5)

stop_button = Button(recv_tab, text="Stop", command=stop_thread)
stop_button.grid(column=4, row=0, sticky=E, padx=5, pady=5)

root.mainloop()
soc.close()

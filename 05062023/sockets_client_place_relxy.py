# Import Libraries
import socket
import tkinter
from tkinter import *

# Create Tkinter Window
root = Tk()
root.geometry("1980x1080")
root.minsize(1600, 300)

# Set Title
root.title('Socket Tkintering')

# Set Frame
frame = Frame(root, width=300, height=300)

# Initialize Variables
setport_data = tkinter.StringVar()

# Create Client Function
def send_data(port, msg):
    HOST = "127.0.0.1"
    PORT = int(port)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(bytes(msg, encoding='utf-8'))


# Create Submit Function
def submit():
    setport = setport_data.get()
    setmsg = setmsg_input.get("1.0", END)
    print(setport, end='\n')
    print(setmsg, end='\n')
    setport_data.set("")
    setmsg_input.delete("1.0", END)
    send_data(setport, setmsg)


# Using RelX RelY Method for the GUI

# Create Labels
title_label = Label(root, text='Sockets and Tkinter')
title_label.place(relx=0.5, rely=0, anchor=N)

setport_label = Label(root, text='Set Port: ')
setport_label.place(relx=0.1, rely=0.1, anchor=NE)

setmsg_label = Label(root, text='Enter Message: ')
setmsg_label.place(relx=0.1, rely=0.2, anchor=NE)

# Create Inputs
setport_input = Entry(root, textvariable=setport_data)
setport_input.place(relx=0.2, rely=0.1, anchor=NE)

setmsg_input = Text(root, height=10, width=32)
setmsg_input.place(relx=0.3, rely=0.2, anchor=NE)

# Submit Data
submit_data = Button(root, text='Submit', command=submit)
submit_data.place(relx=0.5, rely=0.5, anchor=CENTER)

root.mainloop()

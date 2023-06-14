import tkinter
from tkinter import *
from tkinter import ttk
import socket
import _thread

# Root window
root = Tk()
root.title('Socket Tkintering')

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def start_socket():
    HOST = '127.0.0.1'
    PORT = 4210
    soc.connect((HOST, PORT))
    print('Socket Created')
    with soc:
        while True:
            data = soc.recv(1024)
            if not data:
                break
            print(data)
            root.after(0,show_message(data))

def stop_socket():
    soc.close()


def send_socket():
    print("msg")
    data = "msg"
    soc.sendall(data.encode("utf-8"))


def start_thread():
    _thread.start_new_thread(start_socket, ())


def show_message(data):
    print(data)
    Message(text=f"{str(data)}")
    soc.close()
    root.after(0, start_socket)


start_button = Button(root, text="Start", command=start_thread)
start_button.grid(column=3, row=0, sticky=E, padx=5, pady=5)

stop_button = Button(root, text="Stop", command=stop_socket)
stop_button.grid(column=4, row=0, sticky=E, padx=5, pady=5)

send_button = Button(root, text='Send Ping!', command=send_socket)
send_button.grid(column=1, row=3, sticky=N, padx=5, pady=5)

root.mainloop()

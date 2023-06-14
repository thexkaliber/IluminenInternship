from ping_back import connect_toggle, send_messages, clear, stop_connection
from tkinter import *
from tkinter import ttk


class GUI:
    def __init__(self, root=None):
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
        global log_listbox, connect_button, connection_status, connectto_entry, packet_entry, delay_entry

        self.root = root

        self.main_frame = Frame(root)
        self.main_frame.pack(fill=X)

        # Create Connection Entry Frame
        self.connectto_entryframe = Frame(self.main_frame)
        self.connectto_entryframe.pack(side=TOP, anchor=NW, fill=X, padx=5, pady=10)

        # Connection Entry Frame Widgets
        self.connectto_label = Label(self.connectto_entryframe, text='Connect to: ')
        self.connectto_label.pack(side=LEFT, anchor=NW, pady=5)

        self.connectto_entry = Entry(self.connectto_entryframe, width=50)
        self.connectto_entry.pack(side=LEFT, anchor=NW, padx=5, pady=5)

        self.connect_button = Button(self.connectto_entryframe, text='Connect', width=7, command= lambda:connect_toggle(self))
        self.connect_button.pack(side=RIGHT, anchor=NE, padx=5, fill=X)

        # Create Message Entry Frame
        self.entries_frame = Frame(self.main_frame)
        self.entries_frame.pack(side=TOP, anchor=NW, fill=X, padx=5, pady=5)

        # Message Entry Frame Widgets
        self.packet_frame = Frame(self.entries_frame)
        self.packet_frame.pack(side=TOP, anchor=NW, fill=X)

        self.entry_label = Label(self.packet_frame, text='Send Packet: ')
        self.entry_label.pack(side=LEFT, anchor=NW, pady=5)

        self.packet_entry = Entry(self.packet_frame, width=30)
        self.packet_entry.pack(side=LEFT, anchor=NW, pady=5)

        # Create Delay Entry Frame
        self.delay_frame = Frame(self.entries_frame)
        self.delay_frame.pack(side=BOTTOM, anchor=NW, fill=X)

        # Delay Entry Frame Widgets
        self.delay_label = Label(self.delay_frame, text='Delay (s): ')
        self.delay_label.pack(side=LEFT, anchor=NW, pady=5)

        self.delay_entry = Entry(self.delay_frame)
        self.delay_entry.pack(side=LEFT, anchor=NW, padx=19, pady=5)

        self.send_button = Button(self.delay_frame, text="Send", width=7, command=lambda:send_messages(self))
        self.send_button.pack(side=RIGHT, padx=5, pady=5, fill=X)

        # Connection Status Indicator
        self.connection_status = Label(self.main_frame, text='Connection Status: Unknown')
        self.connection_status.pack(side=TOP, anchor=NW, padx=5)

        # Clear Activity Log
        self.clear_button = Button(self.main_frame, text="Clear", command=lambda:clear(self))
        self.clear_button.pack(side=TOP, anchor=NE, padx=5, pady=5)

        # Create Activity Log Frame
        self.log_labelframe = LabelFrame(self.main_frame, text=' Activity Log  ')
        self.log_labelframe.pack(side=BOTTOM, fill=BOTH, expand=TRUE, padx=5, pady=5)

        # Activity Log Widgets
        self.yscrollbar = ttk.Scrollbar(self.log_labelframe, orient=VERTICAL)
        self.yscrollbar.pack(side=RIGHT, fill=Y)

        self.log_listbox = Listbox(self.log_labelframe, height=30, yscrollcommand=self.yscrollbar.set)
        self.log_listbox.pack(fill=BOTH, expand=TRUE, padx=5, pady=10)

        self.yscrollbar.config(command=self.log_listbox.yview)

        # Root Configuration and Bindings
        # self.root.protocol("WM_DELETE_WINDOW", stop_connection(self))


root = Tk()
root.title('Pinger')
root.geometry('500x400')
GUI(root)
root.mainloop()
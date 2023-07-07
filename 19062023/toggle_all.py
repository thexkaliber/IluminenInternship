from tkinter import *
from tkinter import ttk

def connect_toggle():

    """
    Toggles the Connect Button between Connect and Disconnect.

    Parameters used/defined:
    connect_button (widget) - Connect/Disconnect Button Widget
    """

    if connect_button.config('text')[-1] == 'Disconnect':
        connect_button.config(text='Connect', relief=RAISED, width=7)
    else:
        connect_button.config(text='Disconnect',relief=SUNKEN, width=10)

    for items in root.winfo_children(): # Looks at all Widgets in the frame
        if isinstance(items, Entry): #Checks if Widget is an instance of Entry Class
            items.config(state=NORMAL) #Enable them once you hit connect


def gui():
    global connect_button, root
    root = Tk()
    root.title('Toggle')
    root.geometry('300x300')

    label_1 = Label(root,text='Label 1: ')
    label_1.grid(column=0,row=0)

    entry_1 = Entry(root)
    entry_1.grid(column=1,row=0, padx=5, pady=5)

    connect_button = Button(root, text='Connect', width=7, command=connect_toggle)
    connect_button.grid(column=2, row=0)

    label_2 = Label(root,text='Label 2: ')
    label_2.grid(column=0,row=1)

    entry_2 = Entry(root, state=DISABLED)
    entry_2.grid(column=1,row=1, padx=5, pady=5)
    
    label_3 = Label(root,text='Label 3: ')
    label_3.grid(column=0,row=2)

    entry_3 = Entry(root, state=DISABLED)
    entry_3.grid(column=1,row=2, padx=5, pady=5)
        
    label_4 = Label(root,text='Label 4: ')
    label_4.grid(column=0,row=3)

    entry_4 = Entry(root, state=DISABLED)
    entry_4.grid(column=1,row=3, padx=5, pady=5)

        
    label_5 = Label(root,text='Label 5: ')
    label_5.grid(column=0,row=4)

    entry_5 = Entry(root, state=DISABLED)
    entry_5.grid(column=1,row=4, padx=5, pady=5)
    
    root.mainloop()

if __name__ ==  '__main__':
    gui()

from tkinter import *
from tkinter import ttk

def connect_toggle():
    global entry_widgets

    """
    Toggles the Connect Button between Connect and Disconnect

    Parameters used/defined:
    connect_button (widget) - Connect/Disconnect Button Widget
    """

    if connect_button.config('text')[-1] == 'Disconnect':
        connect_button.config(text='Connect', relief=RAISED, width=7)
    else:
        connect_button.config(text='Disconnect',relief=SUNKEN, width=10)

def enable_entry(current_widget, next_widget=None):
    if current_widget.get() != '': #If current widget is not empty after hitting enter
        next_widget.config(state=NORMAL) #Enable the next widget if given.
    else:
        try:
            next_widget.config(state=DISABLED)
        except AttributeError:
            pass

def gui():
    global connect_button, root
    root = Tk()
    root.title('Toggle')
    root.geometry('300x300')

    label_1 = Label(root,text='Label 1: ')
    label_1.grid(column=0,row=0)

    var1= StringVar()
    entry_1 = Entry(root, textvariable=var1)
    entry_1.grid(column=1,row=0, padx=5, pady=5)
    var1.trace("w",lambda *args:enable_entry(entry_1, entry_2)) #After entering details, if Enter is hit, next Entry is enabled.
                                                                          #Lambda allows us to call functions while also passing arguments.
                                                                          #Tkinter by default only expects a function call with no arguments to pass
                                                                          #Lambda allows us to overcome the limitation by anonymously calling the required function with arguments


    connect_button = Button(root, text='Connect', width=7, command=connect_toggle)
    connect_button.grid(column=2, row=0)

    label_2 = Label(root,text='Label 2: ')
    label_2.grid(column=0,row=1)

    var2= StringVar()
    entry_2 = Entry(root, state=DISABLED, textvariable=var2)
    entry_2.grid(column=1,row=1, padx=5, pady=5)
    var2.trace("w",lambda *args:enable_entry(entry_2, entry_3))

    
    label_3 = Label(root,text='Label 3: ')
    label_3.grid(column=0,row=2)

    var3= StringVar()
    entry_3 = Entry(root, state=DISABLED, textvariable=var3)
    entry_3.grid(column=1,row=2, padx=5, pady=5)
    var3.trace("w",lambda *args:enable_entry(entry_3, entry_4))
        
    label_4 = Label(root,text='Label 4: ')
    label_4.grid(column=0,row=3)

    var4= StringVar()
    entry_4 = Entry(root, state=DISABLED, textvariable=var4)
    entry_4.grid(column=1,row=3, padx=5, pady=5)
    var4.trace("w",lambda *args:enable_entry(entry_4, entry_5))
    
    label_5 = Label(root,text='Label 5: ')
    label_5.grid(column=0,row=4)

    var5= StringVar()
    entry_5 = Entry(root, state=DISABLED, textvariable=var5)
    entry_5.grid(column=1,row=4, padx=5, pady=5)
    var5.trace("w",lambda *args:enable_entry(entry_5))
    
    root.mainloop()

if __name__ ==  '__main__':
    gui()
from tkinter import *
import tkinter.scrolledtext as tkst
import os.path
from tkinter import filedialog
import tkinter.font as tkFont


class Application:
    def __init__(self,master): #master means root or main window
        self.master = master
        self.initUI()

    def initUI(self):
        root.title("Simple Text Editor")  # changes the main window title
        scrollBar = Scrollbar(root)
        self.font=tkFont.Font(family="Calibri", size=12)
        self.textPad = Text(root, width=100, height=100, wrap='word',
                       yscrollcommand=scrollBar.set,
                       borderwidth=0, highlightthickness=0) #font=self.font) #creates a 100x100 text area
        scrollBar.config(command=self.textPad.yview)
        scrollBar.pack(side='right', fill='y')
        #self.textPad.pack(side='left', fill='both', expand=True)

        mainMenu = Menu(self.master)
        root.config(menu=mainMenu)
        fileMenu = Menu(mainMenu)
        mainMenu.add_cascade(label="File", menu=fileMenu)
        #fileMenu.add_command(label="New...", command=self.new)
        fileMenu.add_command(label="Open...", accelerator = 'Ctrl+O', command=self.open_command)
        fileMenu.add_separator()
        fileMenu.add_command(label="Save", command=self.save, accelerator='Ctrl+S')
        fileMenu.add_command(label="Save As...", command=self.save_as)
        fileMenu.add_command(label="Exit", accelerator = 'Ctrl+Q', command=self.kill)

        editMenu = Menu(mainMenu)
        mainMenu.add_cascade(label="Edit", menu=editMenu)
        #editMenu.add_command(label="Undo", accelerator='Ctrl+Z', command=self.undo)
        #editMenu.add_command(label="Redo", accelerator='Ctrl+Shift+Z', command=text.edit_redo)
        editMenu.add_command(label="Undo", accelerator='Ctrl+Z', command=self.undo)
        editMenu.add_command(label="Redo", accelerator='Ctrl+Shift+Z', command=self.redo)
        editMenu.add_separator()
        editMenu.add_command(label="Cut", accelerator='Ctrl+X',
                             command=lambda: self.textPad.event_generate('<Control-x>')) #The easiest way to make the edit commands is to just generate them
        editMenu.add_command(label="Copy", accelerator='Ctrl+C',
                             command=lambda: self.textPad.event_generate('<Control-c>'))
        editMenu.add_command(label="Paste", accelerator='Ctrl+V',
                             command=lambda: self.textPad.event_generate('<Control-v>'))
        editMenu.add_command(label="Select All", accelerator='Ctrl+/',
                             command=lambda: self.textPad.event_generate('<Control-0x002f>'))  #0x002f is the '/' key
        #editMenu.add_command(label="Find...", accelerator='Ctrl+F', command=self.find)


        #fontMenu = Menu(mainMenu)
        #mainMenu.add_cascade(label="Font", menu=fontMenu)
        #fontMenu.add_command(label="Bold", command=self.bold_font)


#  ***** Toolbar Creation *****  on second thought, this looks terrible in a text editor
        '''toolbar = Frame(self.master)

        self.saveImage = PhotoImage(file='savepic.gif')
        saveButton = Button(toolbar, command=self.save)
        saveButton.config(image=self.saveImage, width='20', height='20')

        self.openImage = PhotoImage(file='open_folder.gif')
        openButton = Button(toolbar, command=self.open_command)
        openButton.config(image=self.openImage, width='20', height='20')

        #fontIncreaseButton=Button(toolbar, text="Font Up", command=self.bigger_font)

        openButton.pack(side='left', padx=2, pady=2)
        saveButton.pack(side='left', padx=2, pady=2)
        #fontIncreaseButton.pack(side='left', padx=2, pady=2)

        toolbar.pack(side='top', fill='x')'''
        self.textPad.bind_all("<Control-o>", self.open_command)  #binds the hotkey to the main window
        self.textPad.bind_all("<Control-q>", self.kill)
        self.textPad.pack(side='left', fill='both', expand=True)




    '''def new(self):
        root = Tk()
        app = Application(root)
        popupMenu = PopupMenu(root)
        root.mainloop()''' #doesn't work

    def open_command(self, *args):  #try/except block
        global file_path
        file_path = filedialog.askopenfilename(initialdir="/", title="Select a file",
                                               filetypes=[("text files", "*.txt"), ("csv files", "*.csv")])
        #filetypes either requires a trailing comma or []; the above command opens a dialog box for opening a file
        if file_path != ():
            global file
            file = open(file_path)
            if file != None:
                contents = file.read()
                self.textPad.insert(1.0, contents)
                file.close()

    def save_as(self):
        try:
            fileName = open(
                filedialog.asksaveasfilename(initialdir="/", title="Select a file",
                                             filetypes=[("text files", "*.txt"), ("csv files", "*.csv")]),
                                                        mode='w')
            if fileName != None:
                data = self.textPad.get(1.0, END)
                fileName.write(data)
                fileName.close()

        except FileNotFoundError:
            pass

        except NameError:
            pass

    def save(self):
        try:
            os.path.isfile(file_path)
            # file2 = open(file)
            file2 = open(file_path, mode='w')
            contents2 = self.textPad.get(1.0, END)
            file2.write(contents2)
            file2.close()
        except NameError:
            try:
                fileName = open(
                    filedialog.asksaveasfilename(initialdir="/", title="Select a file",
                                                 filetypes=[("text files", "*.txt"), ("csv files", "*.csv")]),
                                                            mode='w')
                if fileName != None:
                    data = self.textPad.get(1.0, END)
                    fileName.write(data)
                    fileName.close()

            except TypeError:
                pass

            except FileNotFoundError:
                pass

    def kill(self, *args):
        root.destroy()

    def dummy_command(self):
        pass

    def undo(self, *args):
        """Undo function"""
        try:
            self.textPad.edit_undo()
        except TclError:
            pass

    def redo(self, *args):
        """Redo function"""
        try:
            self.textPad.edit_redo()
        except TclError:
            pass

    '''def bigger_font(self):
        size = int(self.font.cget("size"))
        size += 2
        self.font.configure(size=size)'''  #changes the font size, but also grows the root window

    '''def bold_font(self):
        #font = tkFont.Font(family="Times", size="10", weight="bold")
        self.font.configure(weight="bold")''' #does nothing

    '''def find(self, *args):
        find_UI = Toplevel()
        find_UI.title("Find")
        find_label = Label(find_UI, text="Find:")
        find_label.pack(side="left")
        user_entry = Entry(find_UI)
        user_entry.pack(side="left")  
        find_button = Button(find_UI, text="Find", command=self.textPad.find_text)
        find_button.pack(side="right")

    def find_text(self, *args):
        countVar = tk.StringVar()
        findtext = str(find.get(1.0, END))
        pos = self.textPad.search("1.0", findtext, stopindex="end", count=countVar)
        self.textPad.tag_configure("search", background="green")
        self.textPad.tag_add("search", pos, "%s + %sc" (pos, countVar.get()))'''  #also does nothing...



class PopupMenu:
    def __init__(self, master, *args, **kwargs):
        self.popup_menu = Menu(root, tearoff=0)
        self.popup_menu.add_command(label="Cut",
                                    command=lambda: app.textPad.event_generate('<<Cut>>'))
        self.popup_menu.add_command(label="Copy",
                                    command=lambda: app.textPad.event_generate('<<Copy>>'))
        self.popup_menu.add_command(label="Paste",
                                    command=lambda: app.textPad.event_generate('<<Paste>>'))
        self.popup_menu.add_separator()
        self.popup_menu.add_command(label="Undo", command=app.textPad.edit_undo)
        self.popup_menu.add_command(label="Redo", command=app.textPad.edit_redo)
        app.textPad.bind("<Button-3>", self.popup)
        self.popup_menu.bind("<FocusOut>",self.popupFocusOut)

    '''def copy_command(self):
        app.textPad.focus()
        app.textPad.event_generate('<Control-c>')   #This is another way to do these

    def paste_command(self):
        app.textPad.focus()
        app.textPad.event_generate('<Control-v>')'''

    def popup(self, event):
        self.popup_menu.post(event.x_root, event.y_root)
        self.popup_menu.focus_set()

    def popupFocusOut(self, event=None):
        self.popup_menu.unpost()

if __name__ =="__main__":
    root = Tk()
    app = Application(root)
    popupMenu = PopupMenu(root)
    root.mainloop()

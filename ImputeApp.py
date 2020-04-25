import tkinter as tk
from tkinter import filedialog


def load_file():
    filename = filedialog.askopenfilename(
        initialdir="/", title="Select file",
        filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    print(filename)


def print_test():
    print("test")


class ImputeApp(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.winfo_toplevel().title("ImputeApp")
        self.winfo_toplevel().geometry("500x500")
        self.winfo_toplevel().config(menu=self.make_menu())
        self.make_widgets()

    def make_widgets(self):
        quit_button = tk.Button(self, text='QUIT', fg='red', command=self.quit)
        quit_button.pack({"side": "left"})

        hi_there = tk.Button(self, text='Hello', command=print_test)
        hi_there.pack({"side": "left"})

    def make_menu(self):
        menubar = tk.Menu(self.master)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Import", command=load_file)
        menubar.add_cascade(label="File", menu=filemenu)

        return menubar


class Menu(tk.Frame):
    def __init__(self, master=None):
        menubar = tk.Menu(master)
        datamenu = tk.Menu(self, tearoff=0)
        datamenu.add_command(label="Salir", command=root.quit)
        menubar.add_cascade(label="Datos", menu=datamenu)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImputeApp(master=root)
    app.mainloop()

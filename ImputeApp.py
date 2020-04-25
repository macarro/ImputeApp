import tkinter as tk
from tkinter import filedialog

import pandas as pd


def print_test():
    print("test")


class ImputeApp:
    def __init__(self):
        self.root = tk.Tk()

        self.root.title("ImputeApp")
        self.root.geometry("500x500")
        self.root.config(menu=self.make_menu())

        self.data = None

        self.data_msg = tk.StringVar(self.root)
        self.data_msg.set("No file loaded.")

        self.data_info = tk.StringVar(self.root)
        self.data_info.set("")

        self.make_widgets()

        self.root.mainloop()

    def make_widgets(self):

        data_frame = tk.Frame(self.root, bg='red', height=50, width=300)
        data_frame.grid(row=1, column=1, padx=10, pady=10)

        data_label = tk.Label(data_frame, textvariable=self.data_msg)
        data_label.grid(row=1, column=1, padx=5, pady=50)

        info_frame = tk.Frame(self.root, bg='blue', height=50, width=300)
        info_frame.grid(row=2, column=1, padx=10, pady=10)

        info_label = tk.Label(info_frame, textvariable=self.data_info)
        info_label.grid(row=1, column=1, padx=5, pady=50)

        hi_there = tk.Button(self.root, text='Hello', command=print_test)
        hi_there.grid(row=3, column=1)

    def make_menu(self):
        menubar = tk.Menu(self.root)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Import", command=self.load_file)
        menubar.add_cascade(label="File", menu=filemenu)

        return menubar

    def load_file(self):
        filename = filedialog.askopenfilename(
            initialdir="/", title="Select file",
            filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
        self.data = pd.read_table(filename)
        self.data_msg.set('File: ' + filename)
        self.data_info.set(str(self.data))


if __name__ == "__main__":
    app = ImputeApp()


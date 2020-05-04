import tkinter as tk
from tkinter import filedialog

import pandas as pd
import imputena as ina


class HorizontallyScrollableFrame(tk.Frame):
    def __init__(self, container, width, height, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self, width=width, height=height)
        scrollbar = tk.Scrollbar(
            self, orient='horizontal', command=canvas.xview)
        self.scrollable_frame = tk.Frame(canvas)
        self.scrollable_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(
                scrollregion=canvas.bbox('all')
            )
        )
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        canvas.configure(xscrollcommand=scrollbar.set)
        canvas.pack(fill='both', expand=True)
        scrollbar.pack(fill='x')


class ImputeApp:
    def __init__(self):
        # Create and configure window:
        self.root = tk.Tk()
        self.root.title("ImputeApp")
        self.root.geometry("450x620")
        self.root.minsize(450, 620)
        self.root.config(menu=self.make_menu())
        # Initialize class attributes:
        self.imputation_methods = [
            'Listwise deletion',
            'Drop variables'
        ]
        self.imputation_method = tk.StringVar(self.root)
        self.imputation_method.set(self.imputation_methods[0])
        self.data = None
        self.data_characteristics = {}
        self.data_characteristics_str = tk.StringVar(self.root)
        self.data_characteristics_str.set('')
        self.outdata_characteristics = {}
        self.outdata_characteristics_str = tk.StringVar(self.root)
        self.outdata_characteristics_str.set('')
        self.indata_selection_frame_fileloc_entry = None
        self.indata_preview = None
        self.outdata = None
        # Make widgets:
        self.show_initial_view()

        #TODO del
        self.load_test_data()

        # Mainloop:
        self.root.mainloop()

    def show_initial_view(self):
        # --------------------------
        # Input data selection frame
        # --------------------------
        indata_selection_frame = tk.Frame(
            self.root, height=100, width=230)
        indata_selection_frame.grid(
            row=1, column=1, padx=10, pady=10)
        # Label:
        indata_selection_frame_l1 = tk.Label(
            indata_selection_frame, text='Input file:')
        indata_selection_frame_l1.grid(
            row=1, column=1, sticky='W', padx=2, pady=2)
        # Container
        indata_selection_cont = tk.Frame(
            indata_selection_frame,
            highlightbackground='black', highlightthickness=1)
        indata_selection_cont.grid(
            row=2, column=1, padx=2, pady=2)
        # Entry:
        self.indata_selection_frame_fileloc_entry = tk.Entry(
            indata_selection_cont, width=20)
        self.indata_selection_frame_fileloc_entry.grid(
            row=1, column=1, sticky='W', padx=2, pady=2)
        # Button:
        indata_selection_frame_b1 = tk.Button(
            indata_selection_cont, text='Import',
            command=self.load_input_from_entry)
        indata_selection_frame_b1.grid(
            row=2, column=1, sticky='W', padx=2, pady=2)

    def show_data_and_imputation(self):
        # --------------------------------
        # Input data characteristics frame
        # --------------------------------
        indata_characteristics_frame = tk.Frame(
            self.root, height=100, width=230)
        indata_characteristics_frame.grid(row=1, column=2, padx=10, pady=10)
        # Label:
        indata_characteristics_frame_l1 = tk.Label(
            indata_characteristics_frame,
            text='Input characteristics:', justify=tk.LEFT)
        indata_characteristics_frame_l1.grid(
            row=1, column=1, sticky='W', padx=2, pady=2)
        # Container
        indata_characteristics_cont = tk.Frame(
            indata_characteristics_frame,
            highlightbackground='black', highlightthickness=1)
        indata_characteristics_cont.grid(
            row=2, column=1, padx=2, pady=2)
        # Label with info:
        indata_characteristics_frame_l2 = tk.Label(
            indata_characteristics_cont,
            textvariable=self.data_characteristics_str,  justify=tk.LEFT)
        indata_characteristics_frame_l2.grid(
            row=1, column=1, sticky='W', padx=2, pady=2)
        # ------------------------
        # Input data preview frame
        # ------------------------
        indata_preview_frame = tk.Frame(
            self.root, height=100, width=250)
        indata_preview_frame.grid(
            row=2, column=1, columnspan=2, padx=10, pady=10)
        # Label:
        indata_preview_frame_l1 = tk.Label(
            indata_preview_frame,
            text='Input data preview:', justify=tk.LEFT)
        indata_preview_frame_l1.grid(
            row=1, column=1, sticky='W', padx=2, pady=2)
        # Scroll container:
        indata_preview_scroll_cont = HorizontallyScrollableFrame(
            indata_preview_frame, width=400, height=130,
            highlightbackground='black',
            highlightthickness=1)
        indata_preview_scroll_cont.grid(
            row=2, column=1, sticky='W', padx=2, pady=2)
        # Preview container:
        self.indata_preview = tk.Frame(
            indata_preview_scroll_cont.scrollable_frame
        )
        self.indata_preview.grid(row=1, column=1)
        # ----------------
        # Imputation frame
        # ----------------
        imputation_frame = tk.Frame(self.root)
        imputation_frame.grid(
            row=3, column=1, columnspan=2, padx=10, pady=10)
        # Label
        imputation_frame_l1 = tk.Label(
            imputation_frame, text='Method:')
        imputation_frame_l1.grid(
            row=1, column=1, sticky='W', padx=2, pady=2)
        # Dropdown
        imputation_frame_dropdown = tk.OptionMenu(
            imputation_frame, self.imputation_method, *self.imputation_methods)
        imputation_frame_dropdown.grid(
            row=1, column=2, sticky='W', padx=2, pady=2)
        # Button
        imputation_frame_b1 = tk.Button(
            imputation_frame, text='Apply',
            command=self.apply_imputation)
        imputation_frame_b1.grid(
            row=1, column=3, sticky='W', padx=2, pady=2)

    def show_output(self):
        # ------------------------
        # Output data export frame
        # ------------------------
        outdata_export_frame = tk.Frame(
            self.root, height=100, width=230)
        outdata_export_frame.grid(
            row=4, column=1, padx=10, pady=10)
        # Label:
        outdata_export_frame_l1 = tk.Label(
            outdata_export_frame, text='Save output file:')
        outdata_export_frame_l1.grid(
            row=1, column=1, sticky='W', padx=2, pady=2)
        # Button:
        outdata_export_frame_b1 = tk.Button(
            outdata_export_frame, text='Save',
            command=self.save_file)
        outdata_export_frame_b1.grid(
            row=2, column=1, sticky='W', padx=2, pady=2)
        # ---------------------------------
        # Output data characteristics frame
        # ---------------------------------
        outdata_characteristics_frame = tk.Frame(
            self.root, height=100, width=230)
        outdata_characteristics_frame.grid(row=4, column=2, padx=10, pady=10)
        # Label:
        outdata_characteristics_frame_l1 = tk.Label(
            outdata_characteristics_frame,
            text='Output characteristics:', justify=tk.LEFT)
        outdata_characteristics_frame_l1.grid(
            row=1, column=1, sticky='W', padx=2, pady=2)
        # Container
        outdata_characteristics_cont = tk.Frame(
            outdata_characteristics_frame,
            highlightbackground='black', highlightthickness=1)
        outdata_characteristics_cont.grid(
            row=2, column=1, padx=2, pady=2)
        # Label with info:
        outdata_characteristics_frame_l2 = tk.Label(
            outdata_characteristics_cont,
            textvariable=self.outdata_characteristics_str, justify=tk.LEFT)
        outdata_characteristics_frame_l2.grid(
            row=1, column=1, sticky='W', padx=2, pady=2)

    def make_menu(self):
        # Create menubar:
        menubar = tk.Menu(self.root)
        # Create filemenu
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Import", command=self.load_file)
        menubar.add_cascade(label="File", menu=filemenu)
        # Return menubar:
        return menubar

    def load_file(self):
        # Open file dialog:
        filename = filedialog.askopenfilename(
            initialdir="/", title="Select file",
            filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
        # Update fileloc_entry:
        self.indata_selection_frame_fileloc_entry.delete(0, tk.END)
        self.indata_selection_frame_fileloc_entry.insert(0, filename)
        self.indata_selection_frame_fileloc_entry.xview_moveto(1)
        # Load table and update info:
        self.load_and_update_input(filename)

    def save_file(self):
        f = filedialog.asksaveasfile(mode='w', defaultextension=".csv")
        if f is None:
            return
        else:
            f.write(self.outdata.to_csv(index=False))
            f.close()

    def load_input_from_entry(self):
        # Retrieve text written in entry:
        filename = self.indata_selection_frame_fileloc_entry.get()
        # Load table and update info:
        self.load_and_update_input(filename)

    def load_and_update_input(self, filename):
        # Read csv:
        self.data = pd.read_csv(filename)
        # Show data and imputation:
        self.show_data_and_imputation()
        # Update data_characteristics and data_characteristics_str:
        self.data_characteristics['num-columns'] = len(self.data.columns)
        self.data_characteristics['num-rows'] = len(self.data.index)
        self.data_characteristics['num-observable'] = \
            self.data.notna().sum().sum()
        self.data_characteristics['num-missing'] = \
            self.data.isna().sum().sum()
        self.data_characteristics['num-total'] = \
            self.data_characteristics['num-columns'] * \
            self.data_characteristics['num-rows']
        self.data_characteristics_str.set(
            'Input characteristics:\n'
            f'Variables: {self.data_characteristics["num-columns"]}\n'
            f'Subjects: {self.data_characteristics["num-rows"]}\n'
            f'Observations: {self.data_characteristics["num-observable"]}\n'
            f'Missing values: {self.data_characteristics["num-missing"]}\n'
            f'Total values: {self.data_characteristics["num-total"]}\n')
        # Populate input preview:
        tk.Label(self.indata_preview, text='Index',
                 borderwidth=1).grid(row=0, column=0)
        for row_idx, row_name in enumerate(self.data.head(5).index):
            tk.Label(
                self.indata_preview, text=row_name,
                borderwidth=1).grid(row=row_idx + 1, column=0)
        for col_idx, col_name in enumerate(self.data.columns):
            tk.Label(self.indata_preview, text=col_name,
                     borderwidth=1).grid(row=0, column=col_idx+1)
            for row_idx, row_name in enumerate(self.data.head(5).index):
                tk.Label(
                    self.indata_preview, text=self.data[col_name][row_name],
                    borderwidth=1).grid(row=row_idx+1, column=col_idx+1)

    def apply_imputation(self):
        if self.imputation_method.get() == 'Listwise deletion':
            self.outdata = ina.delete_listwise(self.data)
        if self.imputation_method.get() == 'Drop variables':
            self.outdata = ina.delete_columns(self.data)
        # Show output:
        self.show_output()
        # Update data_characteristics and data_characteristics_str:
        self.outdata_characteristics['num-columns'] = len(self.outdata.columns)
        self.outdata_characteristics['num-rows'] = len(self.outdata.index)
        self.outdata_characteristics['num-observable'] = \
            self.outdata.notna().sum().sum()
        self.outdata_characteristics['num-missing'] = \
            self.outdata.isna().sum().sum()
        self.outdata_characteristics['num-total'] = \
            self.outdata_characteristics['num-columns'] * \
            self.outdata_characteristics['num-rows']
        self.outdata_characteristics_str.set(
            'Output characteristics:\n'
            f'Variables: {self.outdata_characteristics["num-columns"]}\n'
            f'Subjects: {self.outdata_characteristics["num-rows"]}\n'
            f'Observations: {self.outdata_characteristics["num-observable"]}\n'
            f'Missing values: {self.outdata_characteristics["num-missing"]}\n'
            f'Total values: {self.outdata_characteristics["num-total"]}\n')

    # TODO del
    def load_test_data(self):
        self.indata_selection_frame_fileloc_entry.insert(0,
            '/Users/miguelmacarro/Downloads/calles.csv')
        self.indata_selection_frame_fileloc_entry.xview_moveto(1)
        # Load table and update info:
        self.load_and_update_input('/Users/miguelmacarro/Downloads/calles.csv')

if __name__ == "__main__":
    imputeApp = ImputeApp()




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
        # Configure language
        self.language = 'ES'  # TODO change
        self.msgs_ES = {
            'Language': 'Idioma',
            'English': 'Inglés',
            'Spanish': 'Español',
            'Input file:': 'Archivo de entrada:',
            'Import': 'Importar',
            'Input characteristics:': 'Características de entrada:',
            'Variables': 'Variables',
            'Subjects': 'Sujetos',
            'Observations': 'Observaciones',
            'Missing values': 'Ausencias',
            'Total values': 'Valores totales',
            'Percentage missing': 'Proporción de ausencias',
            'Input data preview:': 'Vista previa de entrada:',
            'Imputation:': 'Imputación:',
            'Method:': 'Método:',
            'Apply': 'Aplicar',
            'Applied': 'Aplicado',
            'Save output file:': 'Guardar salida',
            'Save': 'Guardar',
            'Output characteristics:': 'Características de salida:',
            'File': 'Archivo',
            'Select file': 'Seleccionar archivo',
            'File not found.': 'Archivo no encontrado.',
            'File could not be read.': 'No se puede interpretar.',
            'Index': 'Índice',
            'Listwise deletion': 'Análisis de casos completos',
            'Drop variables': 'Eliminar variables'
        }
        self.languages = {
            'ES': self.msgs_ES
        }
        self.imputation_methods = [
            'Listwise deletion',
            'Drop variables'
        ]
        # Create and configure window:
        self.root = tk.Tk()
        self.root.title("ImputeApp")
        self.root.geometry("450x620")
        self.root.minsize(450, 620)
        self.make_menu()
        # Initialize class attributes:
        self.initialize_inputation_methods()
        self.data_characteristics_str = tk.StringVar(self.root)
        self.data_characteristics_str.set('')
        self.outdata_characteristics_str = tk.StringVar(self.root)
        self.outdata_characteristics_str.set('')
        self.data = None
        self.input_fileloc = ''
        # Initialize widgets:
        self.indata_selection_frame = None
        self.indata_selection_frame_fileloc_entry = None
        self.indata_preview = None
        self.outdata = None
        self.indata_selection_cont = None
        self.indata_characteristics_frame = None
        self.indata_preview_frame = None
        self.imputation_frame = None
        self.input_error_label = None
        self.imputation_cont = None
        self.imputation_log = None
        self.outdata_export_frame = None
        self.outdata_characteristics_frame = None
        # Make widgets:
        self.show_initial_view()

        #TODO del
        self.load_test_data()

        # Mainloop:
        self.root.mainloop()

    # Initial view ------------------------------------------------------------

    def show_initial_view(self):
        # --------------------------
        # Input data selection frame
        # --------------------------
        self.indata_selection_frame = tk.Frame(
            self.root, height=100, width=230)
        self.indata_selection_frame.grid(
            row=1, column=1, padx=10, pady=10)
        # Label:
        indata_selection_frame_l1 = tk.Label(
            self.indata_selection_frame, text=self.msg('Input file:'))
        indata_selection_frame_l1.grid(
            row=1, column=1, sticky='W', padx=2, pady=2)
        # Container
        self.indata_selection_cont = tk.Frame(
            self.indata_selection_frame,
            highlightbackground='black', highlightthickness=1)
        self.indata_selection_cont.grid(
            row=2, column=1, padx=2, pady=2)
        # Entry:
        self.indata_selection_frame_fileloc_entry = tk.Entry(
            self.indata_selection_cont, width=20)
        self.indata_selection_frame_fileloc_entry.grid(
            row=1, column=1, sticky='W', padx=2, pady=2)
        # Button:
        indata_selection_frame_b1 = tk.Button(
            self.indata_selection_cont, text=self.msg('Import'),
            command=self.load_input_from_entry)
        indata_selection_frame_b1.grid(
            row=2, column=1, sticky='W', padx=2, pady=2)

    def hide_initial_view(self):
        shown = self.indata_selection_frame is not None
        if shown:
            self.indata_selection_frame.grid_remove
        return shown

    # Data and imputation view ------------------------------------------------

    def show_data_and_imputation(self):
        # --------------------------------
        # Input data characteristics frame
        # --------------------------------
        self.indata_characteristics_frame = tk.Frame(
            self.root, height=100, width=230)
        self.indata_characteristics_frame.grid(
            row=1, column=2, padx=10, pady=10)
        # Label:
        indata_characteristics_frame_l1 = tk.Label(
            self.indata_characteristics_frame,
            text=self.msg('Input characteristics:'), justify=tk.LEFT)
        indata_characteristics_frame_l1.grid(
            row=1, column=1, sticky='W', padx=2, pady=2)
        # Container
        indata_characteristics_cont = tk.Frame(
            self.indata_characteristics_frame,
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
        self.indata_preview_frame = tk.Frame(
            self.root, height=100, width=250)
        self.indata_preview_frame.grid(
            row=2, column=1, columnspan=2, padx=10, pady=10)
        # Label:
        indata_preview_frame_l1 = tk.Label(
            self.indata_preview_frame,
            text=self.msg('Input data preview:'), justify=tk.LEFT)
        indata_preview_frame_l1.grid(
            row=1, column=1, sticky='W', padx=2, pady=2)
        # Scroll container:
        indata_preview_scroll_cont = HorizontallyScrollableFrame(
            self.indata_preview_frame, width=400, height=130,
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
        self.imputation_frame = tk.Frame(self.root)
        self.imputation_frame.grid(
            row=3, column=1, columnspan=2, padx=10, pady=10, sticky='W')
        # Label:
        imputation_frame_l1 = tk.Label(
            self.imputation_frame,
            text=self.msg('Imputation:'), justify=tk.LEFT)
        imputation_frame_l1.grid(
            row=1, column=1, sticky='W', padx=2, pady=2)
        # Container:
        self.imputation_cont = tk.Frame(
            self.imputation_frame,
            highlightbackground='black', highlightthickness=1)
        self.imputation_cont.grid(
            row=2, column=1, padx=2, pady=2)
        # Label for method:
        imputation_frame_l2 = tk.Label(
            self.imputation_cont, text=self.msg('Method:'))
        imputation_frame_l2.grid(
            row=1, column=1, sticky='W', padx=2, pady=2)
        # Dropdown:
        imputation_frame_dropdown = tk.OptionMenu(
            self.imputation_cont, self.imputation_method_loc,
            *self.imputation_methods_loc.keys())
        imputation_frame_dropdown.grid(
            row=1, column=2, sticky='W', padx=2, pady=2)
        # Button:
        imputation_frame_b1 = tk.Button(
            self.imputation_cont, text=self.msg('Apply'),
            command=self.apply_imputation)
        imputation_frame_b1.grid(
            row=1, column=3, sticky='W', padx=2, pady=2)

    def hide_data_and_imputation(self):
        shown = self.indata_characteristics_frame is not None and \
                self.indata_preview_frame is not None and \
                self.imputation_frame is not None
        if shown:
            self.indata_characteristics_frame.grid_remove()
            self.indata_preview_frame.grid_remove()
            self.imputation_frame.grid_remove()
        return shown

    # Output view -------------------------------------------------------------

    def show_output(self):
        # ------------------------
        # Output data export frame
        # ------------------------
        self.outdata_export_frame = tk.Frame(
            self.root, height=100, width=230)
        self.outdata_export_frame.grid(
            row=4, column=1, padx=10, pady=10)
        # Label:
        outdata_export_frame_l1 = tk.Label(
            self.outdata_export_frame, text=self.msg('Save output file:'))
        outdata_export_frame_l1.grid(
            row=1, column=1, sticky='W', padx=2, pady=2)
        # Button:
        outdata_export_frame_b1 = tk.Button(
            self.outdata_export_frame, text=self.msg('Save'),
            command=self.save_file)
        outdata_export_frame_b1.grid(
            row=2, column=1, sticky='W', padx=2, pady=2)
        # ---------------------------------
        # Output data characteristics frame
        # ---------------------------------
        self.outdata_characteristics_frame = tk.Frame(
            self.root, height=100, width=230)
        self.outdata_characteristics_frame.grid(row=4, column=2, padx=10,
                                              pady=10)
        # Label:
        outdata_characteristics_frame_l1 = tk.Label(
            self.outdata_characteristics_frame,
            text=self.msg('Output characteristics:'), justify=tk.LEFT)
        outdata_characteristics_frame_l1.grid(
            row=1, column=1, sticky='W', padx=2, pady=2)
        # Container
        outdata_characteristics_cont = tk.Frame(
            self.outdata_characteristics_frame,
            highlightbackground='black', highlightthickness=1)
        outdata_characteristics_cont.grid(
            row=2, column=1, padx=2, pady=2)
        # Label with info:
        outdata_characteristics_frame_l2 = tk.Label(
            outdata_characteristics_cont,
            textvariable=self.outdata_characteristics_str, justify=tk.LEFT)
        outdata_characteristics_frame_l2.grid(
            row=1, column=1, sticky='W', padx=2, pady=2)

    def hide_output(self):
        shown = self.outdata_export_frame is not None and \
                self.outdata_characteristics_frame is not None
        if shown:
            self.outdata_export_frame.grid_remove()
            self.outdata_characteristics_frame.grid_remove()
        return shown

    # Menu --------------------------------------------------------------------

    def make_menu(self):
        # Create menubar:
        menubar = tk.Menu(self.root)
        # Create filemenu:
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label=self.msg('Import'), command=self.load_file)
        menubar.add_cascade(label=self.msg('File'), menu=filemenu)
        # Create language menu:
        languagemenu = tk.Menu(menubar, tearoff=0)
        languagemenu.add_command(
            label=self.msg('English'),
            command=lambda: self.change_language('EN'))
        languagemenu.add_command(
            label=self.msg('Spanish'),
            command=lambda: self.change_language('ES'))
        menubar.add_cascade(label=self.msg('Language'), menu=languagemenu)
        # Add menubar to root:
        self.root.config(menu=menubar)

    # Controller functions ----------------------------------------------------

    def msg(self, code):
        res = code
        if self.language in self.languages and \
                code in self.languages[self.language]:
            res = self.languages[self.language][code]
        return res

    def change_language(self, languagecode):
        # Change language:
        self.language = languagecode
        # Redraw interface:
        self.hide_initial_view()
        self.show_initial_view()
        self.indata_selection_frame_fileloc_entry.insert(0, self.input_fileloc)
        self.indata_selection_frame_fileloc_entry.xview_moveto(1)
        if self.hide_data_and_imputation():
            self.show_data_and_imputation()
            # Reload input to draw preview, characteristics:
            self.load_and_update_input(self.input_fileloc)
            # Reload imputation methods:
            self.initialize_inputation_methods()
        if self.hide_output():
            self.show_output()
            # Update outdata_characteristics_str:
            self.outdata_characteristics_str.set(
                self.create_characteristics_string(self.outdata))
        self.make_menu()

    def initialize_inputation_methods(self):
        self.imputation_methods_loc = {
            self.msg(v): v for v in self.imputation_methods}
        self.imputation_method_loc = tk.StringVar(self.root)
        self.imputation_method_loc.set(self.msg(self.imputation_methods[0]))

    def load_file(self):
        # Open file dialog:
        filename = filedialog.askopenfilename(
            initialdir="/", title=self.msg('Select file'),
            filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
        # Update fileloc_entry:
        self.indata_selection_frame_fileloc_entry.delete(0, tk.END)
        self.indata_selection_frame_fileloc_entry.insert(0, filename)
        self.indata_selection_frame_fileloc_entry.xview_moveto(1)
        self.input_fileloc = filename
        # Load table and update info:
        self.load_and_update_input(filename)

    def load_input_from_entry(self):
        # Retrieve text written in entry:
        filename = self.indata_selection_frame_fileloc_entry.get()
        self.input_fileloc = filename
        # Load table and update info:
        self.load_and_update_input(filename)

    def load_and_update_input(self, filename):
        # Hide data, imputation and output and error labels:
        self.hide_data_and_imputation()
        if self.input_error_label is not None:
            self.input_error_label.grid_remove()
        # Read csv:
        try:
            self.data = pd.read_csv(filename)
        except FileNotFoundError:
            self.input_error_label = tk.Label(
                self.indata_selection_cont, text=self.msg('File not found.'))
            self.input_error_label.grid(
                row=3, column=1, sticky='W')
            return
        except Exception:
            self.input_error_label = tk.Label(
                self.indata_selection_cont,
                text=self.msg('File could not be read.'))
            self.input_error_label.grid(
                row=3, column=1, sticky='W')
            return
        # Show data and imputation:
        self.show_data_and_imputation()
        # Update data_characteristics_str:
        self.data_characteristics_str.set(
            self.create_characteristics_string(self.data))
        # Populate input preview:
        tk.Label(self.indata_preview, text=self.msg('Index'),
                 borderwidth=1).grid(row=0, column=0)
        for row_idx, row_name in enumerate(self.data.head(5).index):
            tk.Label(
                self.indata_preview, text=row_name,
                borderwidth=1).grid(row=row_idx + 1, column=0)
        for col_idx, col_name in enumerate(self.data.columns):
            tk.Label(self.indata_preview, text=col_name,
                     borderwidth=1).grid(row=0, column=col_idx+1)
            for row_idx, row_name in enumerate(self.data.head(5).index):
                if pd.isna(self.data[col_name][row_name]):
                    tk.Label(
                        self.indata_preview,
                        text='NA',
                        fg='red',
                        borderwidth=1
                    ).grid(row=row_idx + 1, column=col_idx + 1)
                else:
                    tk.Label(
                        self.indata_preview,
                        text=self.data[col_name][row_name],
                        borderwidth=1
                    ).grid(
                        row=row_idx+1, column=col_idx+1)

    def apply_imputation(self):
        if self.imputation_method_loc.get() == self.msg('Listwise deletion'):
            self.outdata = ina.delete_listwise(self.data)
        if self.imputation_method_loc.get() == self.msg('Drop variables'):
            self.outdata = ina.delete_columns(self.data)
        # Add log:
        if self.imputation_log is not None:
            self.imputation_log.grid_remove()
        self.imputation_log = tk.Label(
            self.imputation_cont,
            text=self.msg('Applied') + ' ' + self.imputation_method_loc.get()
                 + '.'
        )
        self.imputation_log.grid(row=2, column=1, columnspan=2, sticky='W')
        # Show output:
        self.show_output()
        # Update outdata_characteristics_str:
        self.outdata_characteristics_str.set(
            self.create_characteristics_string(self.outdata))

    def create_characteristics_string(self, data):
        # Compute values:
        num_columns = len(data.columns)
        num_rows = len(data.index)
        num_observable = data.notna().sum().sum()
        num_missing = data.isna().sum().sum()
        num_total = num_columns * num_rows
        if num_total == 0:
            missing_percentage = 'NA'
        else:
            missing_percentage = str(
                int((num_missing / num_total) * 100)) + '%'
        # Format and return string:
        res = \
            self.msg('Variables') + ': ' + str(num_columns) + '\n' + \
            self.msg('Subjects') + ': ' + str(num_rows) + '\n' + \
            self.msg('Observations') + ': ' + str(num_observable) + '\n' + \
            self.msg('Missing values') + ': ' + str(num_missing) + '\n' + \
            self.msg('Total values') + ': ' + str(num_total) + '\n' + \
            self.msg('Percentage missing') + ': ' + str(missing_percentage)
        return res

    def save_file(self):
        f = filedialog.asksaveasfile(mode='w', defaultextension=".csv")
        if f is None:
            return
        else:
            f.write(self.outdata.to_csv(index=False))
            f.close()

    # TODO del
    def load_test_data(self):
        self.indata_selection_frame_fileloc_entry.insert(
            0, '/Users/miguelmacarro/Downloads/0-sales.csv')
        self.indata_selection_frame_fileloc_entry.xview_moveto(1)
        self.input_fileloc = '/Users/miguelmacarro/Downloads/0-sales.csv'
        # Load table and update info:
        self.load_and_update_input(
            '/Users/miguelmacarro/Downloads/0-sales.csv')


if __name__ == "__main__":
    imputeApp = ImputeApp()

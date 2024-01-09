import numpy as np
import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo


# Find all positions of a substring
def find_all_str(main_string, substring):
    positions = []
    index = main_string.find(substring)
    while index != -1:
        positions.append(index)
        index = main_string.find(substring, index + 1)
    return positions


# Root window class
class root_window:
    def __init__(self, root):
        # Main window geometry
        root.title("Raith Dose Assignment")
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        width = 480
        height = 200
        alignstr = '%dx%d+%d+%d' % (width, 
                                    height, 
                                    (screenwidth - width) / 2, 
                                    (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(False, False)

        # File path inputboxes
        GDS_label = tk.Label(root, text="GDSII file")
        GDS_label.place(x=20, y=20)
        self.GDS_inputbox=tk.Entry(root)
        self.GDS_inputbox.place(x=20, y=40, width=360, height=25)
        self.GDS_path = ''
        self.GDS_data = np.zeros(1)

        ldt_label = tk.Label(root, text="LDT file")
        ldt_label.place(x=20, y=80)
        self.ldt_inputbox=tk.Entry(root)
        self.ldt_inputbox.place(x=20, y=100, width=360, height=25)
        self.ldt_data = np.zeros(1)

        # Button open GDSII file
        open_button_GDS = tk.Button(
            root,
            text="Load...",
            command=self.select_GDS_file)
        open_button_GDS.place(x=390, y=40, width=70, height=25)

        # Button open ldt file
        open_button_ldt = tk.Button(
            root,
            text="Load...",
            command=self.select_ldt_file)
        open_button_ldt.place(x=390, y=100, width=70, height=25)

        # Button write dose info into GDSII file
        run_button = tk.Button(
            root,
            text="Write")
        run_button["command"] = self.dose_assign
        run_button.place(x=390, y=160, width=70, height=25)
    
    
    # Function to select one single GDSII file
    def select_GDS_file(self):
        filetypes = (
            ('GDSII Files', '*.gds'),
            ('All files', '*.*'))

        GDS_path = fd.askopenfilename(
            title="Select the GDSII File",
            initialdir="/",
            filetypes=filetypes)
        
        self.GDS_inputbox.delete(0, tk.END)
        self.GDS_inputbox.insert(0, GDS_path)
        self.GDS_hex_string(GDS_path)
    

    # Function read GDSII file and convert to hex string
    def GDS_hex_string(self, GDS_path):
        try:
            with open(GDS_path, 'rb') as GDS_file:                                          # open file by read-only binary
                # GDS_data = np.fromfile(GDS_file, dtype=np.uint8)
                GDS_data = np.frombuffer(GDS_file.read(), dtype=np.uint8)                   # read as unit8
                GDS_data_hex = np.vectorize(lambda x: format(x, '02X'))(GDS_data)           # convert dec to hex
                GDS_data_hex = ''.join(GDS_data_hex.flatten('F'))                           # convert to a single string
                self.GDS_path = GDS_path
                self.GDS_data = GDS_data_hex
                # TO BE DONE: There should be some simple way to do this
                # ...

        except FileNotFoundError:
            print(f"File {GDS_path} not found.")

        except Exception as err:
            print(f"An error occurred: {err}")
    

    # Function to select one single ldt file
    def select_ldt_file(self):
        filetypes = (
            ('Dose Mapping Files', '*.ldt'),
            ('All files', '*.*'))

        ldt_path = fd.askopenfilename(
            title='Select the LDT File',
            initialdir='/',
            filetypes=filetypes)

        self.ldt_inputbox.delete(0, tk.END)                                                 # update the file path to Entry
        self.ldt_inputbox.insert(0, ldt_path)
        self.dose_map(ldt_path)
    

    # Function to obtain dose mapping from ldt file
    def dose_map(self, ldt_path):
        dose_table = np.loadtxt(ldt_path,                                                   # read text directly from its path
                                dtype=float,
                                delimiter=',',
                                skiprows=2,                                                 # skip first 2 rows
                                converters={0: lambda s: s[1:], -1: lambda s: s[:-1]})      # remove the first and last char in each row
        # TO BE DONE: convert the first column to interger
        # ...
        dose_dict = dict(zip(dose_table[:, 0], dose_table[:, 1]))                           # convert to dose dict by datatype
        self.ldt_data = dose_dict


    # Function to assign dose to the GDSII by datatype
    def dose_assign(self):
        datatype_pos = find_all_str(self.GDS_data, "00060E02")
        datatype_pos = np.asarray(datatype_pos, dtype="int") + 8

        for position in datatype_pos:
            datatype_hex = self.GDS_data[position:position+4]
            datatype_dec = int(datatype_hex, 16)
            
            try:
                dose = int(self.ldt_data.get(datatype_dec)*1000)
                dose = format(dose, '04X')
            except KeyError:
                showinfo("Mapping Error", f"Datatype '{datatype_dec}' not found in the dose map.")

            self.GDS_data = self.GDS_data[:position] + dose + self.GDS_data[(position+4):]
        
        # Write to file
        binary_GDS_data = bytes.fromhex(self.GDS_data)
        output_path = self.GDS_path[:-4] + "_mapped.GDS"
        with open(output_path, 'wb') as file:
            file.write(binary_GDS_data)





# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = root_window(root)
    root.mainloop()
import numpy as np
import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

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
        #run_button["command"] = 
        run_button.place(x=390, y=160, width=70, height=25)

    # Function of select one single GDSII file
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
        try:
            with open(GDS_path, 'rb') as GDS_file:
                GDS_data = np.frombuffer(GDS_file.read(), dtype=np.uint8)
                print(GDS_data)

        except FileNotFoundError:
            print(f"File not found: {GDS_path}")

        #except Exception as e:
        #    print(f"An error occurred: {e}")


    # Function of select one single ldt file
    def select_ldt_file(self):
        filetypes = (
            ('Dose Mapping Files', '*.ldt'),
            ('All files', '*.*')
        )

        ldt_path = fd.askopenfilename(
            title='Select the LDT File',
            initialdir='/',
            filetypes=filetypes)

        self.ldt_inputbox.delete(0, tk.END)
        self.ldt_inputbox.insert(0, ldt_path)





# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = root_window(root)
    root.mainloop()
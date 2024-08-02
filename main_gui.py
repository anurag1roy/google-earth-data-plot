import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pandas as pd
import os
from pathlib import Path
import importlib
import shutil
import sys

# Ensure paths are included only once
path_to_add = os.path.dirname(os.path.abspath(__file__))
if path_to_add not in sys.path:
    sys.path.append(path_to_add)

# Conditional imports to avoid re-import issues
if 'gpr_plot_gui' in sys.modules:
    gpr_plot_gui = importlib.reload(sys.modules['gpr_plot_gui']).gpr_plot_gui
else:
    from gpr_plot_gui import gpr_plot_gui

if 'fwd_plot_gui' in sys.modules:
    fwd_plot_gui = importlib.reload(sys.modules['fwd_plot_gui']).fwd_plot_gui
else:
    from fwd_plot_gui import fwd_plot_gui

if 'core_plot_gui' in sys.modules:
    core_plot_gui = importlib.reload(sys.modules['core_plot_gui']).core_plot_gui
else:
    from core_plot_gui import core_plot_gui

def select_input_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        process_input_file(file_path)

def process_input_file(input_file):
    try:
        input_data = pd.read_csv(input_file)
        output_dir = os.path.join(os.path.dirname(input_file), 'output_kmz')
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir)

        # Function to process data for a given folder name and plot function
        def process_data(folder_name, plot_function):
            data_row = input_data[input_data['Folder Name'] == folder_name]
            if data_row.empty:
                raise ValueError(f"{folder_name} not found in the input file.")

            data_folder = data_row['Folder Location'].values[0]

            # Check if the folder exists
            if not os.path.exists(data_folder):
                raise ValueError(f"The folder {data_folder} does not exist.")

            # List all files in the folder
            files = list(Path(data_folder).glob("*.csv"))
            if not files:
                print(f"No CSV files found in {data_folder}")
            else:
                print(f"CSV files found in {data_folder}: {[str(f) for f in files]}")

            # Process each CSV file in the folder
            for csv_file in files:
                print(f"Processing file: {csv_file}")
                plot_function(csv_file, output_dir)

            print(f"All CSV files in {folder_name} have been processed.")

        # Process GPR DATA
        process_data('GPR DATA', gpr_plot_gui)

        # Process FWD DATA
        process_data('FWD DATA', fwd_plot_gui)

        # Process CORE DATA
        process_data('CORE DATA', core_plot_gui)

        messagebox.showinfo("Success", "KML files created successfully!")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Initialize the GUI
root = tk.Tk()
root.title("Pavement Data File Processor")

# Configure style
style = ttk.Style()
style.theme_use('clam')
style.configure('TFrame', background='#f0f0f0')
style.configure('TButton', font=('Helvetica', 12), background='#4CAF50', foreground='white')
style.configure('TLabel', font=('Helvetica', 14), background='#f0f0f0')

frame = ttk.Frame(root, padding="20 20 20 20")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)

title_label = ttk.Label(frame, text="Pavement Data File Processor", anchor="center")
title_label.grid(row=0, column=0, pady=(0, 10))

summary_label = ttk.Label(frame, text="Easily process and visualize pavement data into KML files with a single click.", anchor="center")
summary_label.grid(row=1, column=0, pady=(0, 20))

select_button = ttk.Button(frame, text="Select Input File", command=select_input_file)
select_button.grid(row=2, column=0)

root.mainloop()

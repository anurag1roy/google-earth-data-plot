import sys
import importlib
import pandas as pd
import os
from pathlib import Path

# Ensure paths are included only once
path_to_add = r"C:\Users\anurag.TRANSTEC\OneDrive - The Transtec Group\Desktop\PythonProjects\google earth data plot"
if path_to_add not in sys.path:
    sys.path.append(path_to_add)

# Conditional imports to avoid re-import issues
if 'gpr_plot' in sys.modules:
    plot_gpr = importlib.reload(sys.modules['gpr_plot']).plot_gpr
else:
    from gpr_plot import plot_gpr

if 'fwd_plot' in sys.modules:
    plot_fwd = importlib.reload(sys.modules['fwd_plot']).plot_fwd
else:
    from fwd_plot import plot_fwd

if 'core_plot' in sys.modules:
    plot_core = importlib.reload(sys.modules['core_plot']).plot_core
else:
    from core_plot import plot_core

# Specify the full path to your input file
input_file = r"C:\Users\anurag.TRANSTEC\OneDrive - The Transtec Group\Desktop\PythonProjects\google earth data plot\input file.csv"

# Read the input file as CSV
input_data = pd.read_csv(input_file)

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
        plot_function(csv_file)

    print(f"All CSV files in {folder_name} have been processed.")

# Process GPR DATA
process_data('GPR DATA', plot_gpr)

# Process FWD DATA
process_data('FWD DATA', plot_fwd)

# Process CORE DATA
process_data('CORE DATA', plot_core)

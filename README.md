# Google Earth Data Plotter

This project plots GPR (Ground Penetrating Radar), FWD (Falling Weight Deflectometer), and Core data into a 3D KML file using Python. The generated KML file can be viewed in Google Earth to visualize the data in 3D.

## Features

- Plots GPR data
- Plots FWD data
- Plots Core data
- Generates a 3D KML file

## Requirements

- Python
- Python packages: pandas, simplekml, PyQt5 (for GUI)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/anurag1roy/google-earth-data-plot.git
    ```

2. Navigate to the project directory:

    ```bash
    cd google-earth-data-plot
    ```

3. Install the required Python packages:

    ```bash
    pip install pandas simplekml PyQt5
    ```

## Usage

1. Run the main script to start the application:

    ```bash
    python main.py
    ```

2. Use the GUI to load your data and generate the KML file.

## Code Overview

- **core_plot.py**: Script for processing and plotting core data.
- **core_plot_gui.py**: GUI script for core data plotting.
- **fwd_plot.py**: Script for processing and plotting FWD data.
- **fwd_plot_gui.py**: GUI script for FWD data plotting.
- **gpr_plot.py**: Script for processing and plotting GPR data.
- **gpr_plot_gui.py**: GUI script for GPR data plotting.
- **main.py**: Main script to start the application.
- **main_gui.py**: GUI script for the main application.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the Roy License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, feel free to contact the project maintainer.

import pandas as pd
from simplekml import Kml, AltitudeMode
import os

def create_polygon_placemark(kml, coords, name, description, color='7f0000ff', line_color='ff0000ff'):
    pol = kml.newpolygon(name=name, description=description)
    pol.outerboundaryis = coords
    pol.extrude = 1
    pol.altitudemode = AltitudeMode.relativetoground
    pol.style.polystyle.color = color  # Blue color with 50% opacity by default
    pol.style.linestyle.color = line_color  # Blue color by default
    pol.style.linestyle.width = 5
    return pol

def fwd_plot_gui(csv_file, output_dir):
    try:
        kml = Kml()

        # Read CSV file
        data = pd.read_csv(csv_file)

        # Print column names for debugging
        print("CSV Columns:", data.columns)

        # Ensure necessary columns are present
        if 'Longitude' not in data.columns or 'Latitude' not in data.columns or 'N1' not in data.columns:
            raise ValueError("Required columns ('Longitude', 'Latitude', 'N1') not found in CSV file.")

        # Convert necessary columns to numeric
        data['Longitude'] = pd.to_numeric(data['Longitude'], errors='coerce')
        data['Latitude'] = pd.to_numeric(data['Latitude'], errors='coerce')
        data['N1'] = pd.to_numeric(data['N1'], errors='coerce')

        # Loop through the data and create individual polygons for each section
        for i in range(len(data) - 1):
            lon1 = data['Longitude'][i]
            lat1 = data['Latitude'][i]
            deflection1 = data['N1'][i] * 10  # Scale the deflection for better visualization

            lon2 = data['Longitude'][i + 1]
            lat2 = data['Latitude'][i + 1]
            deflection2 = data['N1'][i + 1] * 10  # Scale the deflection for better visualization

            coords = [
                (lon1, lat1, 0),  # Ground point of the first location
                (lon1, lat1, deflection1),  # Top of the first vertical line
                (lon2, lat2, deflection2),  # Top of the second vertical line
                (lon2, lat2, 0),  # Ground point of the second location
                (lon1, lat1, 0)  # Return to ground point of the first location
            ]

            description = f"Deflection: {data['N1'][i]:.2f} to {data['N1'][i + 1]:.2f} mils"
            create_polygon_placemark(kml, coords, name=f"Section {i + 1}", description=description)

        kml_file = os.path.join(output_dir, os.path.basename(csv_file).replace('.csv', '_fwd_plot.kml'))
        kml.save(kml_file)
        return kml_file

    except Exception as e:
        print(f"An error occurred: {e}")
        raise

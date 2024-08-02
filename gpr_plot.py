import pandas as pd
from simplekml import Kml, AltitudeMode
from pathlib import Path

def create_polygon_placemark(kml, coords):
    pol = kml.newpolygon(name="Connected Polygon")
    pol.outerboundaryis = coords  # Pass the list of tuples directly
    pol.extrude = 1
    pol.altitudemode = AltitudeMode.relativetoground
    pol.style.polystyle.color = '7f0000ff'  # Blue color with 50% opacity
    pol.style.linestyle.color = 'ff0000ff'  # Blue color
    pol.style.linestyle.width = 5
    return pol

def plot_gpr(csv_file):
    # Read CSV file
    data = pd.read_csv(csv_file)

    # Print column names for debugging
    print("Columns in the CSV file:", data.columns)

    # Convert necessary columns to numeric
    data['Long'] = pd.to_numeric(data['Long'], errors='coerce')
    data['lat'] = pd.to_numeric(data['lat'], errors='coerce')
    data['T1 (in.)'] = pd.to_numeric(data['T1 (in.)'], errors='coerce')

    # Generate coordinates for the polygon
    coords = []

    # First, add ground points and vertical lines
    for i in range(len(data)):
        lon = data['Long'][i]
        lat = data['lat'][i]
        height = data['T1 (in.)'][i] * 10  # Scale the height for better visualization

        # Add ground point
        coords.append((lon, lat, 0))

        # Add top of vertical line
        coords.append((lon, lat, height))

        # Return to ground point
        coords.append((lon, lat, 0))

    # Then, add top points of vertical lines in reverse order to close the polygon
    for i in range(len(data) - 1, -1, -1):
        lon = data['Long'][i]
        lat = data['lat'][i]
        height = data['T1 (in.)'][i] * 10  # Scale the height for better visualization

        # Add top of vertical line
        coords.append((lon, lat, height))

    # Print some coordinates for debugging
    print("Sample coordinates:", coords[:10])

    # Create output file name based on the CSV file name
    base_name = Path(csv_file).stem
    kml_file = Path(csv_file).parent / f"{base_name}_gpr_plot.kml"

    # Start KML content
    kml = Kml()

    # Add the polygon placemark to the KML content
    create_polygon_placemark(kml, coords)

    # Save KML file
    kml.save(str(kml_file))

    print(f"KML file '{kml_file}' generated successfully.")

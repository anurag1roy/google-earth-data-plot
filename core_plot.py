import pandas as pd
from simplekml import Kml, AltitudeMode
from pathlib import Path

def create_layer_placemark(kml, tag, lat, lon, height, base_height, color, label):
    width = 0.000045  # Approx. 5 feet wide in latitude/longitude degrees
    coordinates = [
        (lon - width / 2, lat, base_height),
        (lon - width / 2, lat, height),
        (lon + width / 2, lat, height),
        (lon + width / 2, lat, base_height),
        (lon - width / 2, lat, base_height)
    ]
    placemark = kml.newpolygon(name=tag, description=f"Thickness: {label} in")
    placemark.outerboundaryis = coordinates
    placemark.altitudemode = AltitudeMode.relativetoground
    placemark.extrude = 1
    placemark.style.polystyle.color = color
    return placemark

def plot_core(csv_file):
    # Read CSV file
    data = pd.read_csv(csv_file)

    # Ensure column names match expected names
    data.columns = ["Tag", "Latitude", "Longitude", "HMA_Thickness_1", "Concrete_Thickness", "HMA_Thickness_2", "Base_Thickness"]

    # Convert necessary columns to numeric
    data["Longitude"] = pd.to_numeric(data["Longitude"], errors="coerce")
    data["Latitude"] = pd.to_numeric(data["Latitude"], errors="coerce")
    data["HMA_Thickness_1"] = pd.to_numeric(data["HMA_Thickness_1"], errors="coerce")
    data["Concrete_Thickness"] = pd.to_numeric(data["Concrete_Thickness"], errors="coerce")
    data["HMA_Thickness_2"] = pd.to_numeric(data["HMA_Thickness_2"], errors="coerce")
    data["Base_Thickness"] = pd.to_numeric(data["Base_Thickness"], errors="coerce")

    # Create output file name based on the CSV file name
    base_name = Path(csv_file).stem
    kml_file = Path(csv_file).parent / f"{base_name}_core_plot.kml"

    # Start KML content
    kml = Kml()

    # Create folders for each layer type
    hma1_folder = kml.newfolder(name="HMA 1")
    concrete_folder = kml.newfolder(name="Concrete")
    hma2_folder = kml.newfolder(name="HMA 2")
    base_folder = kml.newfolder(name="Base")

    # Add the stacked column placemarks to the respective folders
    for _, row in data.iterrows():
        tag = row["Tag"]
        lat = row["Latitude"]
        lon = row["Longitude"]
        hma1_thickness = row["HMA_Thickness_1"]
        concrete_thickness = row["Concrete_Thickness"]
        hma2_thickness = row["HMA_Thickness_2"]
        base_thickness = row["Base_Thickness"]

        current_height = 0

        if not pd.isna(hma1_thickness) and hma1_thickness > 0:
            create_layer_placemark(hma1_folder, tag, lat, lon, current_height + hma1_thickness * 10, current_height, 'ff000000', f"HMA 1 - {hma1_thickness}")
            current_height += hma1_thickness * 10

        if not pd.isna(concrete_thickness) and concrete_thickness > 0:
            create_layer_placemark(concrete_folder, tag, lat, lon, current_height + concrete_thickness * 10, current_height, 'ff808080', f"Concrete - {concrete_thickness}")
            current_height += concrete_thickness * 10

        if not pd.isna(hma2_thickness) and hma2_thickness > 0:
            create_layer_placemark(hma2_folder, tag, lat, lon, current_height + hma2_thickness * 10, current_height, 'ff000000', f"HMA 2 - {hma2_thickness}")
            current_height += hma2_thickness * 10

        if not pd.isna(base_thickness) and base_thickness > 0:
            create_layer_placemark(base_folder, tag, lat, lon, current_height + base_thickness * 10, current_height, 'ff00a5ff', f"Base - {base_thickness}")

    # Save KML file
    kml.save(str(kml_file))

    print(f"KML file '{kml_file}' generated successfully.")

import pandas as pd
from simplekml import Kml, AltitudeMode
import os

def create_polygon_placemark(kml, coords, name, description, color, line_color):
    pol = kml.newpolygon(name=name, description=description)
    pol.outerboundaryis = coords
    pol.extrude = 1
    pol.altitudemode = AltitudeMode.relativetoground
    pol.style.polystyle.color = color
    pol.style.linestyle.color = line_color
    pol.style.linestyle.width = 5
    return pol

def html_to_kml_color(html_color):
    # Convert HTML color (#rrggbb) to KML color (aabbggrr)
    rr = html_color[1:3]
    gg = html_color[3:5]
    bb = html_color[5:7]
    aa = '7f'  # Default opacity
    return aa + bb + gg + rr

def get_color_for_thickness(thickness):
    # Define HTML colors for each range of thickness
    if thickness < 2:
        return html_to_kml_color('#b3d9ff')  # Light Blue
    elif thickness < 4:
        return html_to_kml_color('#99ff99')  # Light Green
    elif thickness < 6:
        return html_to_kml_color('#ffffcc')  # Light Yellow
    elif thickness < 8:
        return html_to_kml_color('#ffcc99')  # Light Orange
    elif thickness < 10:
        return html_to_kml_color('#ff9999')  # Light Red
    else:
        return html_to_kml_color('#8b0000')  # Dark Red

def gpr_plot_gui(csv_file, output_dir):
    try:
        kml = Kml()

        # Read CSV file
        data = pd.read_csv(csv_file)

        # Print column names for debugging
        print("CSV Columns:", data.columns)

        # Ensure necessary columns are present
        if 'Long' not in data.columns or 'lat' not in data.columns or 'T1 (in.)' not in data.columns:
            raise ValueError("Required columns ('Long', 'lat', 'T1 (in.)') not found in CSV file.")

        # Convert necessary columns to numeric
        data['Long'] = pd.to_numeric(data['Long'], errors='coerce')
        data['lat'] = pd.to_numeric(data['lat'], errors='coerce')
        data['T1 (in.)'] = pd.to_numeric(data['T1 (in.)'], errors='coerce')

        i = 0
        while i < len(data) - 1:
            start_index = i
            thickness = data['T1 (in.)'][i]

            # Find the end of the segment with the same thickness
            while i < len(data) - 1 and data['T1 (in.)'][i] == data['T1 (in.)'][i + 1]:
                i += 1

            end_index = i
            i += 1

            # Generate coordinates for the polygon
            coords = []

            for j in range(start_index, end_index + 1):
                lon = data['Long'][j]
                lat = data['lat'][j]
                height = thickness * 10  # Scale the height for better visualization

                # Add ground point
                coords.append((lon, lat, 0))

                # Add top of vertical line
                coords.append((lon, lat, height))

                # Return to ground point
                coords.append((lon, lat, 0))

            # Add top points of vertical lines in reverse order to close the polygon
            for j in range(end_index, start_index - 1, -1):
                lon = data['Long'][j]
                lat = data['lat'][j]
                height = thickness * 10  # Scale the height for better visualization

                # Add top of vertical line
                coords.append((lon, lat, height))

            # Calculate average thickness (although they are all the same in this case)
            description = f"Average thickness = {thickness:.2f} in"
            color = get_color_for_thickness(thickness)
            create_polygon_placemark(kml, coords, name=f"Section {start_index + 1} to {end_index + 1}", description=description, color=color, line_color=color)

        kml_file = os.path.join(output_dir, os.path.basename(csv_file).replace('.csv', '_gpr_plot.kml'))
        kml.save(kml_file)
        return kml_file

    except Exception as e:
        print(f"An error occurred: {e}")
        raise

# mapping_dataDXF to SHP File Conversion and Visualization 📐🌍
This folder contains tools and scripts for converting DXF files (commonly used in CAD software) into SHP files (a popular GIS format), as well as for symbolizing and visualizing spatial data in QGIS.

# 🚀 Features
1. DXF to SHP Conversion

  -  Transform CAD files into shapefiles for GIS analysis.
2. Automated Symbolization in QGIS

  - Python scripts to automate styling and symbolization for easy visualization.
3. Interactive Mapping

  - Jupyter Notebook showcasing mapping workflows and visualizations.
# 📂 Folder Structure
- code_symbolisation_qgis.py

  Python script for automating the symbolization of shapefiles in QGIS.

- mapping.ipynb

  Jupyter Notebook demonstrating the conversion process and mapping workflows, including data visualization techniques.

- data/

  (Optional) Placeholder for input DXF files and output SHP files.

  
# 💻 Technologies Used
- GIS Software: QGIS
- Programming: Python (PyQGIS, Geopandas)
- Visualization: Jupyter Notebook

# 🌟 Future Improvements
- Add functionality for batch DXF to SHP conversion.
- Enhance symbolization scripts to support more geometry types.
- Integrate real-time updates from external databases.

#

# Convert LST GeoID Grid to TIFF Format 🗺️

This notebook, geoide_groupe3.ipynb, demonstrates how to process LST GeoID grid data and convert it into a TIFF format for spatial analysis and visualization in GIS software.

# 🚀 Features

1. Grid Data to TIFF Conversion

- Transform GeoID grid data into GeoTIFF format for compatibility with GIS tools.
2. Geospatial Visualization

- Preview GeoTIFF outputs using Python libraries.
3. Customizable Workflow

- Adjust parameters to fit specific GeoID datasets and coordinate reference systems (CRS).
# 📂 Folder Structure
- geoide_groupe3.ipynb

Jupyter Notebook for processing and converting GeoID grid files.

- data/

(Optional) Folder for input GeoID grid files and output GeoTIFF files.

- docs/screenshots/

(Optional) Contains example outputs and visualizations.

# 📋 How to Use
1. Prepare the Environment

Ensure you have the required dependencies installed:

    pip install numpy pandas matplotlib rasterio geopandas
2. Run the Notebook

Open the notebook in Jupyter or JupyterLab:

    jupyter notebook geoide_groupe3.ipynb
3. Provide Input Data

Place your GeoID grid file in the data/ folder and modify the input file path in the notebook.

4. Generate TIFF

Execute the notebook cells to process the grid file and output a GeoTIFF file in the desired location.

# 🖼️ Examples

1. Input GeoID Grid

A sample grid file used as input for processing.

2. Generated GeoTIFF

# 💻 Technologies Used
- Programming: Python
- Libraries: Rasterio, GeoPandas, NumPy, Matplotlib
# 🌟 Future Improvements
- Add support for batch conversion of multiple grid files.
- Implement error handling for missing or incompatible grid data.
- Integrate interactive visualization for the resulting GeoTIFFs.

# 📞 Contact
Feel free to reach out for questions or suggestions!

Walid

GitHub: @waliddev23

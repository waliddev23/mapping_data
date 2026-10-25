# Convert LST GeoID Grid to TIFF Format 🗺️

The notebook `geoide_groupe3.ipynb` demonstrates how to process geoid undulation grid data from an ASCII `.lst` file (columns: `id`, `phi` (latitude), `lambda` (longitude), `ondulation` (geoid undulation)) and convert it into a GeoTIFF for spatial analysis and visualization in GIS software.

# 🚀 Features

1. Grid Data to TIFF Conversion

- Transform GeoID grid data into GeoTIFF format for compatibility with GIS tools.
2. Geospatial Visualization

- Preview GeoTIFF outputs using Python libraries (seaborn heatmap + rasterio preview).
3. Customizable Workflow

- Adjust parameters to fit specific GeoID datasets and coordinate reference systems (CRS).

# 📂 Folder Structure
- `geoide_groupe3.ipynb`

  Jupyter Notebook: reads the `.lst` text file, parses the columns, rebuilds the 17 × 18 lat/lon grid, and writes `output.tiff`.

- `geoide.csv` / `geoide_raw.csv`

  Exported grid values (with / without header & index), for use in external software.

- `output.tiff`

  The generated GeoTIFF (`+proj=latlong`, pixel step = grid spacing).

# 💻 Technologies Used
- Programming: Python
- Libraries: Rasterio, GeoPandas, NumPy, Matplotlib / Seaborn

# 🌟 Future Improvements
- Add support for batch conversion of multiple grid files.
- Implement error handling for missing or incompatible grid data.
- Integrate interactive visualization for the resulting GeoTIFFs.

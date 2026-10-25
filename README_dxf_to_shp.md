# mapping_data – DXF to SHP File Conversion and Visualization 📐🌍

This folder contains tools and scripts for converting DXF files (commonly used in CAD software) into SHP files (a popular GIS format), as well as for symbolizing and visualizing spatial data in QGIS.

> 📘 **Full step-by-step usage guide (installation, commands, QGIS styling, troubleshooting): see [USAGE.md](dxf_to_shp_file/USAGE.md).**

# 🚀 Features
1. DXF to SHP Conversion

  - Transform CAD files into shapefiles for GIS analysis.

2. Command-line converter with batch mode (`dxf_to_shp.py`)

  - Convert a single DXF or every `.dxf` in a folder in one go.
  - `--split-layers` : one shapefile per CAD layer (`bois`, `puits`, ...).
  - `--to-polygon`   : turn closed LineStrings into Polygons.

```bash
python dxf_to_shp.py "dxf_inputs/Tp_Tech_Imp.dxf" -o shapefile_output/site --split-layers --to-polygon
python dxf_to_shp.py dxf_inputs -o shapefile_output --batch
```

3. Automated Symbolization in QGIS

  - Python scripts to automate styling and symbolization for easy visualization.
4. Interactive Mapping

  - Jupyter Notebook showcasing mapping workflows and visualizations.

# 📂 Folder Structure
- `dxf_to_shp.py`

  Command-line DXF ➜ Shapefile converter (single file / per-layer split / polygon mode / batch).

- `code_symbolisation_qgis.py`

  Python script for automating the symbolization of shapefiles in QGIS.

- `mapping.ipynb`

  Jupyter Notebook demonstrating the conversion process and mapping workflows, including data visualization techniques.

- `dxf_inputs/`
  Sample AutoCAD DXF files used by the examples (site plan: buildings, olive trees, wells, pump track, ...).

- `shapefile_input/` and `shapefile_output/`

  Intermediate and converted shapefiles, one folder per CAD layer.

- `svg/` and `hab.svg`

  SVG marker symbols used by the QGIS symbolization script.

- `result.pdf`

  Example of the final rendered map.

  
# 💻 Technologies Used
- GIS Software: QGIS
- Programming: Python (PyQGIS, Geopandas, GDAL/OGR)
- Visualization: Jupyter Notebook

# 🌟 Future Improvements
- [x] Add functionality for batch DXF to SHP conversion. *(done — `dxf_to_shp.py --batch`)*
- [ ] Enhance symbolization scripts to support more geometry types.
- [ ] Integrate real-time updates from external databases.

# 📞 Contact
Feel free to reach out for questions or suggestions!

Walid

GitHub: @waliddev23

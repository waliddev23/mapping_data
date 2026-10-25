# mapping_data 🗺️📐

A collection of geospatial data-format conversion tools. Two sub-projects, each for a specific use:

| Tool | Folder | What it does |
|---|---|---|
| **DXF ➜ SHP** | `dxf_to_shp_file/` | Convert AutoCAD **DXF** drawings (CAD) into ESRI **Shapefiles** (GIS), then symbolize/visualize them in **QGIS** |
| **GeoID grid ➜ TIFF** | `lst_geoid_grid_to_tiff/` | Parse a geoid undulation grid from an ASCII **`.lst`** file and export it as a **GeoTIFF** raster + CSV |

---

## 1) DXF ➜ SHP File Conversion and Visualization 📐

Converts CAD drawings (site plans, cadastral data, ...) into shapefiles for GIS analysis. The sample data shows a rural site plan: buildings (`bois`, `faubourg`), temporary stream, farm track, wells, olive trees, mosque.

### Quick start

```bash
# install once:  conda install -c conda-forge gdal geopandas
# (on Windows, alternatively use the QGIS "OSGeo4W Shell")

# single file, one shapefile per CAD layer
python dxf_to_shp.py "dxf_inputs/Tp_Tech_Imp.dxf" -o shapefile_output/site --split-layers

# closed CAD outlines become polygons
python dxf_to_shp.py "dxf_inputs/Tp_Tech_Imp.dxf" -o shapefile_output/site --to-polygon

# batch: convert every .dxf in a folder
python dxf_to_shp.py dxf_inputs -o shapefile_output --batch
```

Then open the output shapefiles in **QGIS** and run `code_symbolisation_qgis.py`
from the QGIS Python console to apply the styling (fills, hatch patterns, dashed
lines and the SVG symbols for the mosque / olive trees / wells layers).

### 📘 More details
- **Full step-by-step guide:** [`dxf_to_shp_file/USAGE.md`](dxf_to_shp_file/USAGE.md)
  (installation options, SHX vs SHX-font clarification, notebook walkthrough, troubleshooting)
- **Interactive workflow:** [`dxf_to_shp_file/mapping.ipynb`](dxf_to_shp_file/mapping.ipynb)
- **Example result:** [`dxf_to_shp_file/result.pdf`](dxf_to_shp_file/result.pdf)

### > About ".shx"
The `.shx` that sits next to a `.shp` (`.shp .shx .dbf`) is only the shapefile's
**index file** — GDAL/QGIS create it automatically. An AutoCAD **SHX *font***
file (e.g. `simplex.shx`) is a font, not geometry: convert it to TTF instead if
you need it as a label font in QGIS.

---

## 2) GeoID Grid ➜ TIFF 🗺️

`lst_geoid_grid_to_tiff/geoide_groupe3.ipynb` reads an ASCII `.lst` geoid file
(columns: `id`, `phi` (latitude), `lambda` (longitude), `ondulation` (geoid
undulation)), rebuilds the 17 × 18 lat/lon grid, and writes:

- `output.tiff` — the GeoTIFF (`+proj=latlong`, pixel step = grid spacing)
- `geoide.csv` / `geoide_raw.csv` — grid values for external software
- a seaborn **heatmap preview** in the notebook

Requires: `pandas`, `numpy`, `rasterio`, `seaborn`.

---

## 📂 Repository structure

```
mapping_data/
├── dxf_to_shp_file/           # DXF ➜ SHP tool
│   ├── dxf_to_shp.py          #   CLI converter (batch / per-layer / polygon modes)
│   ├── mapping.ipynb          #   notebook workflow
│   ├── code_symbolisation_qgis.py  # QGIS styling automation
│   ├── USAGE.md               #   full usage guide
│   ├── dxf_inputs/            #   sample CAD files
│   ├── shapefile_input/  shapefile_output/  svg/  result.pdf
└── lst_geoid_grid_to_tiff/    # GeoID grid ➜ TIFF tool
    ├── geoide_groupe3.ipynb
    ├── geoide.csv  geoide_raw.csv
    └── output.tiff
```

## 💻 Technologies
- GIS software: **QGIS** (PyQGIS)
- Python: **GDAL/OGR**, **GeoPandas**, **Rasterio**, **Pandas / NumPy**
- Visualization: **Jupyter Notebook**

## 🌟 Roadmap
- [x] Batch DXF ➜ SHP conversion (`dxf_to_shp.py --batch`)
- [ ] More geometry types in the symbolization script
- [ ] Batch GeoID grid conversion with error handling



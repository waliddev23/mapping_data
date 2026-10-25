# How to use the mapping_data tools (DXF ➜ SHP)

This guide answers the GitHub issue
*"dxf to shp or shx font file could you help me — how to use your mapping data tools?"*.

---

## 1. What these tools do — and one important clarification

The `dxf_to_shp_file/` tool converts **CAD drawings (`.dxf`)** into **ESRI Shapefiles (`.shp`)**
so you can open, style, and analyse them in a GIS such as **QGIS**.

> ⚠️ **About ".shx"**: there are two different things called SHX — don't confuse them!
>
> | File | What it is |
> |---|---|
> | `.shx` in a shapefile folder | the tiny **index file** that travels with `.shp` and `.dbf`. You never touch it — GDAL/QGIS creates it automatically (see `shapefile_output/` in this repo: every `.shp` has one). |
> | AutoCAD **SHX font** file | a compiled AutoCAD **font/shape** file (e.g. `simplex.shx`). This is **not convertible to a shapefile** — it is a font, not geometry. To use those fonts outside AutoCAD you convert them to **TTF** (e.g. with AutoCAD's `COMPILE` / a font converter), or re-save the drawing as DXF with text exploded to geometry. |
>
> If your goal is to convert a drawing → use DXF ➜ SHP (this repo). If your goal is to
> display SHX fonts inside the GIS text labels → install a TTF version of the font on your
> system and pick it in QGIS layer styling.

---

## 2. Installation

The converter needs **Python with GDAL/OGR bindings**, plus **GeoPandas** for the
notebook workflow (`mapping.ipynb`). The easiest setups:

**Option A — conda (recommended, all platforms):**
```bash
conda create -n mapping -c conda-forge python gdal geopandas pandas jupyter
conda activate mapping
```

**Option B — QGIS on Windows:** install QGIS, then run the scripts from the
built-in **OSGeo4W Shell** (GDAL, Python and PyQGIS are already there).

**Option C — plain Windows:** install GDAL wheels from
[CGohlke's geospatial-wheels](https://github.com/cgohlke/geospatial-wheels/) with
`pip install <GDAL wheel file>` then `pip install geopandas`.

---

## 3. Quick start — command line (easiest)

Repo files were extracted next to this guide; from the `dxf_to_shp_file/` folder:

```bash
# 1) Convert one DXF into a merged shapefile
python dxf_to_shp.py "dxf_inputs/mosquée.dxf" -o shapefile_output/mosquee

# 2) Same, but ALSO split into one shapefile per CAD layer (bois, puits, ...)
python dxf_to_shp.py "dxf_inputs/mosquée.dxf" -o shapefile_output/mosquee --split-layers

# 3) Convert closed lines into polygons (useful for parcel/building outlines)
python dxf_to_shp.py "dxf_inputs/Tp_Tech_Imp.dxf" -o shapefile_output/site --to-polygon

# 4) BATCH: convert EVERY .dxf found in a folder at once
python dxf_to_shp.py dxf_inputs -o shapefile_output --batch --split-layers
```

Each DXF layer becomes its own shapefile in `shapefile_output/<layer>/<layer>.shp`,
exactly mirroring the example outputs already committed in this repo
(`bois`, `faubourg`, `mosquee`, `oliviers`, `puits`, ...).

---

## 4. Quick start — the notebook (step by step, what actually happens)

Open `mapping.ipynb` in Jupyter. The workflow is:

1. **Inspect the DXF** (`dxf_to_dataframe`) — lists every entity with its CAD
   `Layer`, `Text`, `Linetype`, etc. Useful to see which CAD layers exist.
2. **Convert** (`dxf_to_shapefile`) — opens the DXF with the GDAL **DXF driver**
   and copies every feature/attribute into the **ESRI Shapefile** driver output.
   *The `.shx` and `.dbf` companions are generated automatically.*
3. **Verify** with GeoPandas (`gpd.read_file(...)`) and `value_counts()` on the
   `Layer` column to see the CAD layer names.
4. **Filter / convert geometry** — keep only wanted CAD layers
   (`~autre['Layer'].isin([...])`), optionally turn closed **LineStrings into Polygons**.
5. **Split** the merged file into one shapefile per CAD layer (cell 16/17).
6. **Point layers** — if a CAD line actually represents a location (olive trees, wells),
   take its first vertex as a `Point` and export that (cell 19).

---

## 5. Visualising / symbolising in QGIS

1. Open QGIS → `Layer ▸ Add Layer ▸ Add Vector Layer` → select `shapefile_output/<name>/<name>.shp`.
2. Manual styling is possible, but the repo ships an automation script:
   open **QGIS ▸ Plugins ▸ Python Console** (or open the layer properties,
   or paste the script in `Plugins ▸ Python Console ▸ Show Editor`) and run
   `code_symbolisation_qgis.py`.
   It adds each layer (fills, hatch patterns, dashed lines) and—when your SVG files
   are present—shows symbols for **mosquee**, **oliviers**, **puits**.
3. Optionally edit the fonts/colors directly in the layer's `Symbology` tab.

---

## 6. Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: osgeo` | GDAL not installed — see §2. |
| `Layer ... is not a valid layer` in GeoPandas | convert to absolute paths; also make sure the whole trio `.*shp .shx .dbf` stays together when copying. |
| Missing fills / empty polygons | your CAD outlines are open LineStrings — re-run with `--to-polygon` or notebook cell 13. |
| Chinese/special characters garbled | ensure a `.cpg` file (e.g. `UTF-8`) sits next to the shapefiles. |
| Nothing visible after load | check `Layer properties ▸ Source ▸ CRS`; DXF files convert in CAD units—assign the right coordinate system. |

---

## 7. The other tool in this repository

`lst_geoid_grid_to_tiff/` converts a **GeoID grid (CSV)** into a **GeoTIFF** raster —
see the accompanying root README for that workflow.

---

*Contact: Walid (@waliddev23).*

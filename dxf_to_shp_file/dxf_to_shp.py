"""
dxf_to_shp.py -- DXF (CAD) to ESRI Shapefile converter, based on GDAL/OGR.

This script turns the notebook workflow (mapping.ipynb) into a reusable,
command-line friendly tool. It supports:

  1. Single DXF conversion          -> one merged shapefile
  2. Per-DXF-layer splitting        -> one shapefile folder per DXF layer
  3. LineString -> Polygon mode     -> closed CAD outlines become polygons
  4. Batch mode                     -> convert every *.dxf in a folder

Requirements
------------
Python 3.8+ with GDAL/OGR bindings (`from osgeo import ogr`).

Easy installing options:
  - conda:   conda install -c conda-forge gdal
  - pip:     pip install GDAL        (version must match your GDAL install)
  - Windows: install QGIS / OSGeo4W and run the script from the "OSGeo4W shell"

Usage
-----
# single file, merged output
python dxf_to_shp.py "dxf_inputs/mosquée.dxf" -o shapefile_output/mosquee

# single file, one shapefile per DXF layer
python dxf_to_shp.py "dxf_inputs/mosquée.dxf" -o shapefile_output/mosquee --split-layers

# convert closed LineStrings to Polygons (like the notebook does)
python dxf_to_shp.py "dxf_inputs/Tp_Tech_Imp.dxf" -o shapefile_output/site --to-polygon

# batch: convert every DXF inside a folder (recursively)
python dxf_to_shp.py dxf_inputs -o shapefile_output --batch
"""

import argparse
import os
import re
import sys

try:
    from osgeo import ogr, osr
except ImportError:
    sys.exit(
        "GDAL/OGR Python bindings are required.\n"
        "Install one of the following ways:\n"
        "  conda install -c conda-forge gdal\n"
        "  pip install GDAL   (match your GDAL version)\n"
        "  or run inside the QGIS 'OSGeo4W shell' on Windows."
    )

SHP_DRIVER = ogr.GetDriverByName("ESRI Shapefile")
DXF_DRIVER = ogr.GetDriverByName("DXF")

if SHP_DRIVER is None:
    sys.exit("ESRI Shapefile driver not available in this GDAL build.")
if DXF_DRIVER is None:
    sys.exit("DXF driver not available in this GDAL build.")


def safe_name(name):
    """Make a DXF layer/file name safe to use as a folder/file name."""
    name = re.sub(r'[\\/:*?"<>|]', "_", str(name)).strip()
    return name or "layer"


def dxf_to_shapefile(dxf_file, output_shapefile):
    """Copy every feature of a DXF into a single ESRI shapefile (like the notebook)."""
    dxf_ds = DXF_DRIVER.Open(dxf_file, 0)
    if dxf_ds is None:
        raise RuntimeError(f"Could not open {dxf_file}")

    # The GDAL DXF driver exposes one 'entities' layer holding every DXF entity.
    src_layer = dxf_ds.GetLayerByIndex(0)
    src_defn = src_layer.GetLayerDefn()

    out_path = os.fspath(output_shapefile)
    if os.path.exists(out_path):
        SHP_DRIVER.DeleteDataSource(out_path)

    out_ds = SHP_DRIVER.CreateDataSource(out_path)
    if out_ds is None:
        raise RuntimeError(f"Could not create {out_path}")

    out_layer = out_ds.CreateLayer(
        os.path.splitext(os.path.basename(out_path))[0],
        geom_type=src_layer.GetGeomType(),
    )

    # Copy attribute fields (Layer, Text, Linetype, SubClasses, ...)
    for i in range(src_defn.GetFieldCount()):
        out_layer.CreateField(src_defn.GetFieldDefn(i))

    out_layer.StartTransaction()
    for feature in src_layer:
        new_feature = ogr.Feature(out_layer.GetLayerDefn())
        new_feature.SetFrom(feature)
        out_layer.CreateFeature(new_feature)
        new_feature = None
    out_layer.CommitTransaction()

    count = out_layer.GetFeatureCount()
    out_ds = None  # close
    dxf_ds = None
    return count


def split_by_dxf_layer(shapefile_path, output_folder):
    """Split a merged shapefile into one folder/<layer>/<layer>.shp per DXF layer
    (mirrors cell 16 of mapping.ipynb)."""
    src_ds = SHP_DRIVER.Open(shapefile_path, 0)
    if src_ds is None:
        raise RuntimeError(f"Could not reopen {shapefile_path}")
    src_layer = src_ds.GetLayerByIndex(0)
    src_defn = src_layer.GetLayerDefn()

    # Collect the distinct DXF layer names first
    layer_names = set()
    src_layer.ResetReading()
    for feature in src_layer:
        val = feature.GetField("Layer") if feature.IsFieldSet("Layer") else "unknown"
        layer_names.add(str(val))

    # Create one shapefile per name
    targets = {}
    for name in layer_names:
        folder = os.path.join(output_folder, safe_name(name))
        os.makedirs(folder, exist_ok=True)
        shp_path = os.path.join(folder, f"{safe_name(name)}.shp")
        if os.path.exists(shp_path):
            SHP_DRIVER.DeleteDataSource(shp_path)
        out_ds = SHP_DRIVER.CreateDataSource(shp_path)
        out_layer = out_ds.CreateLayer(
            safe_name(name), geom_type=src_layer.GetGeomType()
        )
        for i in range(src_defn.GetFieldCount()):
            out_layer.CreateField(src_defn.GetFieldDefn(i))
        targets[name] = (out_ds, out_layer)

    # Second pass: route each feature into its shapefile
    src_layer.ResetReading()
    for feature in src_layer:
        val = feature.GetField("Layer") if feature.IsFieldSet("Layer") else "unknown"
        out_ds, out_layer = targets[str(val)]
        new_feature = ogr.Feature(out_layer.GetLayerDefn())
        new_feature.SetFrom(feature)
        out_layer.CreateFeature(new_feature)
        new_feature = None

    for out_ds, _ in targets.values():
        out_ds = None  # close all
    src_ds = None


def to_polygons(shapefile_path):
    """In-place style helper: convert closed LineStrings to Polygons
    (mirrors cell 13 of mapping.ipynb)."""
    ds = SHP_DRIVER.Open(shapefile_path, 1)
    if ds is None:
        raise RuntimeError(f"Could not open {shapefile_path} for update")
    layer = ds.GetLayerByIndex(0)

    for feature in layer:
        geom = feature.GetGeometryRef()
        if geom is None:
            continue
        if geom.GetGeometryType() == ogr.wkbLineString:
            line = ogr.ForceToLineString(geom)
            if line and line.GetPointCount() > 2:
                poly = ogr.Geometry(ogr.wkbPolygon)
                poly.AddGeometry(line)
                feature.SetGeometry(poly)
                layer.SetFeature(feature)
        geom = None
    ds = None


def convert_one(dxf_file, output_path, split_layers=False, to_polygon=False):
    print(f"[dxfs2shp] {dxf_file} -> {output_path}")
    n = dxf_to_shapefile(dxf_file, output_path)
    print(f"           wrote {n} features")

    if split_layers:
        folder = os.path.dirname(output_path) or "."
        print(f"           splitting by DXF layer into {folder}/<layer>/ ...")
        split_by_dxf_layer(output_path, folder)

    if to_polygon:
        print("           converting closed LineStrings to Polygons ...")
        # Apply polygon conversion to every per-layer shapefile we just created
        if split_layers:
            folder = os.path.dirname(output_path) or "."
            for sub in os.listdir(folder):
                shp = os.path.join(folder, sub, f"{sub}.shp")
                if os.path.exists(shp):
                    to_polygons(shp)
        else:
            to_polygons(output_path)


def batch_convert(input_folder, output_folder, split_layers=False, to_polygon=False):
    dxf_files = []
    for root, _dirs, files in os.walk(input_folder):
        for f in files:
            if f.lower().endswith(".dxf"):
                dxf_files.append(os.path.join(root, f))

    if not dxf_files:
        sys.exit(f"No DXF files found under {input_folder}")

    os.makedirs(output_folder, exist_ok=True)
    for dxf_file in sorted(dxf_files):
        base = safe_name(os.path.splitext(os.path.basename(dxf_file))[0])
        out_dir = os.path.join(output_folder, base)
        os.makedirs(out_dir, exist_ok=True)
        out_shp = os.path.join(out_dir, f"{base}.shp")
        try:
            convert_one(dxf_file, out_shp, split_layers=split_layers, to_polygon=to_polygon)
        except Exception as e:  # keep converting the rest
            print(f"           FAILED: {e}", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description="Convert DXF (CAD) files to ESRI Shapefiles.")
    ap.add_argument("input", help="a .dxf file, or a folder for --batch mode")
    ap.add_argument("-o", "--output", required=True,
                    help="output .shp path (single file) or folder (batch mode)")
    ap.add_argument("--batch", action="store_true",
                    help="treat INPUT as a folder and convert every DXF inside it")
    ap.add_argument("--split-layers", action="store_true",
                    help="also write one shapefile per DXF layer")
    ap.add_argument("--to-polygon", action="store_true",
                    help="convert closed LineStrings into Polygons")
    args = ap.parse_args()

    if args.batch:
        batch_convert(args.input, args.output,
                      split_layers=args.split_layers, to_polygon=args.to_polygon)
    else:
        if os.path.isdir(args.input):
            sys.exit("Input is a folder -- did you forget --batch ?")
        convert_one(args.input, args.output,
                    split_layers=args.split_layers, to_polygon=args.to_polygon)
    print("done.")


if __name__ == "__main__":
    main()

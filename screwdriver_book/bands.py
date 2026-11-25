"""Colour separations for the cap in its face-down print coordinates, in mm."""
from decimal import Decimal
from pathlib import Path
import xml.etree.ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

import yaml

TEAL = "#00B1B7"
BLACK = "#000000"
REFERENCE = Path(__file__).resolve().parents[1] / "source_file/oomp_drive_type_colours.yaml"
CORE = "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"


def colour_bands(family, size):
    entries = yaml.safe_load(REFERENCE.read_text(encoding="utf-8"))["entries"]
    drive = "hex_socket" if family == "hex" else family
    entry = next(row for row in entries if row["value"] == drive)
    bands = []
    band = {}
    band["role"] = "Drive"
    band["from_mm"] = 1.4
    band["to_mm"] = 3.0
    band["colour"] = entry["color"]
    band["hex"] = entry["hex"]
    bands.append(band)

    # Store metric widths in tenths, always with two digits (0.7 -> 07).
    # The literal Phillips string preserves the distinction between 0, 00 and 000.
    digits = size.removeprefix("T")
    if family in ("hex", "slotted"):
        tenths = Decimal(size) * 10
        if tenths != int(tenths) or not 0 <= tenths < 100:
            raise ValueError(f"Size {size} needs a new metric encoding")
        digits = f"{int(tenths):02d}"
    if not digits.isascii() or not digits.isdigit() or len(digits) > 3:
        raise ValueError(f"Unsupported cap marking {size}")
    # Five 0.2 mm layers per digit and four teal layers between digits.
    digit_width_mm = 1.0
    teal_gap_mm = 0.8
    for index, digit in enumerate(digits):
        row = next(row for row in entries if row["resistor_digit"] == int(digit))
        band = {}
        band["role"] = f"Digit {digit}"
        band["from_mm"] = round(4.0 + index * (digit_width_mm + teal_gap_mm), 1)
        band["to_mm"] = round(band["from_mm"] + digit_width_mm, 1)
        band["colour"] = row["color"]
        band["hex"] = row["hex"]
        bands.append(band)
    return bands


def write_cap(folder, part):
    import manifold3d
    import numpy as np
    import trimesh

    base = trimesh.load_mesh(folder / "3dpr_color_main.stl")
    ink = trimesh.load_mesh(folder / "3dpr_color_support.stl")
    remainder = manifold3d.Manifold(manifold3d.Mesh64(
        np.ascontiguousarray(base.vertices, dtype=np.float64),
        np.ascontiguousarray(base.faces, dtype=np.uint64)))
    if remainder.is_empty() or not ink.is_volume:
        raise ValueError(f"Invalid cap source in {folder}")

    sections = []
    for band in part["colour_bands"]:
        remainder, teal = remainder.split_by_plane((0, 0, 1), band["from_mm"])
        remainder, stripe = remainder.split_by_plane((0, 0, 1), band["to_mm"])
        sections.append(("Teal shell", TEAL, teal))
        sections.append((band["role"] + " - " + band["colour"], band["hex"], stripe))
    sections.append(("Teal skirt", TEAL, remainder))
    if abs(sum(s.volume() for _, _, s in sections) - base.volume) > .001:
        raise ValueError("Cap separations changed the shell volume")

    meshes = []
    for name, colour, solid in sections:
        mesh = solid.to_mesh64()
        meshes.append((name, colour, mesh.vert_properties[:, :3], mesh.tri_verts))
    meshes.append(("Black face marking", BLACK, ink.vertices, ink.faces))
    title = f'{part["shape"].title()} {part["siz"]}'
    colours = [("OOBB teal", TEAL), ("Black", BLACK)]
    for band in part["colour_bands"]:
        colours.append((band["colour"].title(), band["hex"]))
    return write_material_package(folder / "3dpr_banded.3mf", part["id"], title + " cap", title, colours, meshes)


def write_handle(folder, part):
    import trimesh

    plate = trimesh.load_mesh(folder / "3dpr.stl")
    bodies = sorted(plate.split(), key=lambda body: body.bounds[0, 0])
    names = ["Handle", "Slotted lock key", "Nut cradle", "Bearing lifter", "Countersunk insert"]
    meshes = []
    for name, body in zip(names, bodies, strict=True):
        if not body.is_volume:
            raise ValueError(f"Invalid {name} in {folder}")
        meshes.append((name, TEAL, body.vertices, body.faces))
    title = f'{part["diameter_bit_main"]} mm shaft handle'
    return write_material_package(folder / "3dpr_teal.3mf", part["id"], title, title, [("OOBB teal", TEAL)], meshes)


def write_material_package(target, part_id, title, slicer_name, colours, meshes):
    model = ET.Element("model", xmlns=CORE, unit="millimeter")
    model.set("xmlns:slic3rpe", "http://schemas.slic3r.org/3mf/2017/06")
    ET.SubElement(model, "metadata", name="slic3rpe:Version3mf").text = "1"
    ET.SubElement(model, "metadata", name="Title").text = title
    resources = ET.SubElement(model, "resources")
    palette = ET.SubElement(resources, "basematerials", id="1")
    materials = {}
    # A single build object keeps the stripes at their installed Z on import.
    # Core 3MF carries face materials; Prusa's optional metadata names the
    # corresponding closed volumes and assigns each to a filament slot.
    obj = ET.SubElement(resources, "object", id="2", type="model", name=part_id, pid="1", pindex="0")
    mesh = ET.SubElement(obj, "mesh")
    coords = ET.SubElement(mesh, "vertices")
    triangles = ET.SubElement(mesh, "triangles")
    config = ET.Element("config")
    volume_config = ET.SubElement(config, "object", id="2", instances_count="1")
    ET.SubElement(volume_config, "metadata", type="object", key="name", value=slicer_name)
    for name, colour in colours:
        if colour not in materials:
            materials[colour] = len(materials)
            ET.SubElement(palette, "base", name=name, displaycolor=colour + "FF")
    for name, colour, vertices, faces in meshes:
        offset = len(coords)
        first = len(triangles)
        for x, y, z in vertices:
            ET.SubElement(coords, "vertex", x=f"{x:.10g}", y=f"{y:.10g}", z=f"{z:.10g}")
        for a, b, c in faces:
            ET.SubElement(triangles, "triangle", v1=str(offset+int(a)), v2=str(offset+int(b)),
                          v3=str(offset+int(c)), pid="1", p1=str(materials[colour]))
        volume = ET.SubElement(volume_config, "volume", firstid=str(first), lastid=str(len(triangles)-1))
        ET.SubElement(volume, "metadata", type="volume", key="name", value=name)
        ET.SubElement(volume, "metadata", type="volume", key="volume_type", value="ModelPart")
        ET.SubElement(volume, "metadata", type="volume", key="extruder", value=str(materials[colour]+1))
    ET.SubElement(ET.SubElement(model, "build"), "item", objectid="2")
    files = {
        "[Content_Types].xml": '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="config" ContentType="application/xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>',
        "_rels/.rels": '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="model" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>',
        "Metadata/Slic3r_PE_model.config": ET.tostring(config, encoding="utf-8", xml_declaration=True),
        "3D/3dmodel.model": ET.tostring(model, encoding="utf-8", xml_declaration=True),
    }
    temp = target.with_suffix(".building.3mf")
    with ZipFile(temp, "w") as package:
        for path, data in files.items():
            package.writestr(ZipInfo(path), data, compress_type=ZIP_DEFLATED)
    temp.replace(target)
    return target


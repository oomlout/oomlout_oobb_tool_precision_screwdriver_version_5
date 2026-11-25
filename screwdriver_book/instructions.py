"""Stage the parts from the two print files in assembly coordinates (millimetres)."""
import csv
import hashlib
import json
import math
from pathlib import Path
import subprocess

import numpy as np
import trimesh

from . import assembly_booklet, assembly_viewer

ROOT = Path(__file__).resolve().parents[1]


def panel_geometry(style):
    return tuple((side - 2 * style["margin_mm"] - (n - 1) * style["gutter_mm"]) / n
                 for side, n in zip(style["page_mm"], (style["columns"], style["rows"])))


def rotate(mesh, degrees, axis):
    mesh.apply_transform(trimesh.transformations.rotation_matrix(math.radians(degrees), axis))


def shaft(radius, height, sides=64):
    mesh = trimesh.creation.cylinder(radius=radius, height=height, sections=sides)
    mesh.apply_translation([0, 0, height / 2])
    return mesh


def ring(radius, bore, height, sides=64):
    cut = shaft(bore, height + .2)
    cut.apply_translation([0, 0, -.1])
    return trimesh.boolean.difference([shaft(radius, height, sides), cut], engine="manifold")


def screw(length):
    # External envelope, including a recess for the 2 mm hex key.
    stem = shaft(1.5, length - 1.65)
    rim = shaft(3.3, .12)
    rim.apply_translation([0, 0, length - .12])
    cone = trimesh.creation.cone(radius=3.3, height=3.3, sections=64)
    rotate(cone, 180, [1, 0, 0])
    cone.apply_translation([0, 0, length - .1])
    solid = trimesh.boolean.union([stem, cone, rim], engine="manifold")
    tool = shaft(2 / math.sqrt(3), 1.3, 6)
    tool.apply_translation([0, 0, length - 1.2])
    return trimesh.boolean.difference([solid, tool], engine="manifold")


def assembly_meshes(handle_stl, cap_main, cap_ink):
    body, key, cradle, lifter, insert = sorted(trimesh.load_mesh(handle_stl).split(), key=lambda m: m.bounds[0, 0])
    rotate(body, 180, [1, 0, 0])
    body.apply_translation([0, 0, 91.5])
    key.apply_translation([-17, 7, -1.5])
    rotate(key, 90, [1, 0, 0])
    rotate(key, 90, [0, 0, 1])
    key.apply_translation([0, 0, 49])
    cradle.apply_translation([-25.7, 0, -3.6])
    rotate(cradle, -90, [0, 1, 0])
    cradle.apply_translation([0, 0, 83.75])
    for piece, x, z in [(lifter, 42, 92.9), (insert, 55, 99.9)]:
        piece.apply_translation([-x, 0, 0])
        rotate(piece, 180, [1, 0, 0])
        piece.apply_translation([0, 0, z])
    cap, ink = [trimesh.load_mesh(p) for p in (cap_main, cap_ink)]
    for piece in (cap, ink):
        rotate(piece, 180, [1, 0, 0])
        piece.apply_translation([0, 0, 101.6])
    # This is an illustration of the purchased bit. Show its narrow drive end
    # and full-size hex shank so the insertion direction is visible in print.
    stem = trimesh.creation.revolve([[0, -45], [.7, -45], [.7, -44],
                                     [1.75, -41], [1.75, 25], [0, 25]])
    angles = np.linspace(0, 2 * math.pi, 72, endpoint=False)
    radii = .59 + .11 * np.cos(6 * angles)
    outline = np.column_stack((radii * np.cos(angles), radii * np.sin(angles)))
    centre = len(outline)
    tip_faces = [[centre, i, (i+1) % len(outline)] for i in range(len(outline))]
    tip = trimesh.creation.extrude_triangulation(np.vstack([outline, [0, 0]]), tip_faces, height=2)
    tip.apply_translation([0, 0, -47])
    shank = shaft(6.35 / math.sqrt(3), 28, 6)
    shank.apply_translation([0, 0, 25])
    bit = trimesh.util.concatenate([tip, stem, shank])
    bearing = trimesh.util.concatenate([ring(8.5, 7.35, 6), ring(7.34, 4.11, 5.6), ring(4.1, 3, 6)])
    bearing.apply_translation([0, 0, 92.9])
    top_nut = ring(5.5 / math.sqrt(3), 1.3, 2.4, 6)
    rotate(top_nut, 30, [0, 0, 1])
    side_nut = top_nut.copy()
    top_nut.apply_translation([0, 0, 86.25])
    rotate(side_nut, 90, [0, 1, 0])
    side_nut.apply_translation([-1.5, 0, 58])
    top_screw = screw(16)
    top_screw.apply_translation([0, 0, 83.85])
    side_screw = screw(6)
    rotate(side_screw, 90, [0, 1, 0])
    side_screw.apply_translation([.5, 0, 58])
    return dict(body=body, key=key, cradle=cradle, lifter=lifter, insert=insert, cap=cap, ink=ink,
                bit=bit, top_nut=top_nut, side_nut=side_nut, top_screw=top_screw,
                side_screw=side_screw, bearing=bearing)


def publish(cfg):
    from render_parts import find_blender
    output = ROOT / cfg["assembly_folder"]
    render = output / "render"
    raw = render / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    handle = ROOT / "parts" / cfg["example_id"] / "3dpr.stl"
    cap = ROOT / "parts" / cfg["example_cap"]
    sources = [handle, cap / "3dpr_color_main.stl", cap / "3dpr_color_support.stl"]
    package = cap / "3dpr_banded.3mf"
    hashes = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in [*sources, package, ROOT / cfg["book"]["logo_svg"]]}
    meshes = assembly_meshes(*sources)
    labels = cfg["part_labels"]
    parts = {}
    printed = []
    for key, label in labels.items():
        part = dict(key=key, name=label["name"], quantity=1)
        if "id" in label:
            part.update(label)
            digest = hashlib.md5(label["id"].encode()).hexdigest()
            code = np.base_repr(int(digest[:6], 16), 36).lower()
            part.update(md5=digest, md5_6_alpha=code, short_url="https://oom.lt/a/" + code)
        else:
            printed.append(key)
            part["id"] = cfg["example_cap"] if key == "cap" else cfg["example_id"]
            part["identity_source"] = "printed plate"
        parts[key] = part
    views = {}
    consumed = []
    steps = []
    for index, definition in enumerate(cfg["steps"], 1):
        step = dict(definition, key=f"step_{index:02d}")
        if set(consumed).intersection(step["add"]):
            raise ValueError("Assembly inventory counted twice")
        consumed.extend(step["add"])
        step["loose_parts"] = dict.fromkeys(step["add"], 1)
        steps.append(step)
        views[step["key"]] = {
            name: [distance * cfg["style"]["explosion_scale"] for distance in step["move"].get(name, [0, 0, 0])]
            for name in consumed
        }
        if "detail_from_z" in step:
            views[step["key"] + "_detail"] = views[step["key"]]
    if set(consumed) != set(parts):
        raise ValueError("Assembly inventory does not match steps")
    views["book_cover"] = dict.fromkeys(consumed, [0, 0, 0])
    for name in consumed:
        views["part_" + name] = {name: [0, 0, 0]}
    stage = ROOT / "build" / "screwdriver_assembly"
    stage.mkdir(parents=True, exist_ok=True)
    for key, mesh in meshes.items():
        mesh.export(stage / (key + ".stl"))
    details = {step["key"] + "_detail": step["detail_from_z"] for step in steps if "detail_from_z" in step}
    scene = dict(views=views, detail_from_z=details, output=str(raw), stage=str(stage), banded=str(package))
    job = stage / "views.json"
    job.write_text(json.dumps(scene))
    worker = Path(__file__).with_name("render_assembly.py")
    studio = ROOT / "presentation/scripts/render_catalogue.py"
    signature = hashlib.sha256(worker.read_bytes() + studio.read_bytes() + Path(__file__).read_bytes() + json.dumps([hashes, views, details]).encode()).hexdigest()
    stamp = stage / "render.sha256"
    if not stamp.exists() or stamp.read_text() != signature or any(not (raw / (name + ".png")).exists() for name in views):
        with (stage / "blender.log").open("w") as log:
            subprocess.run([find_blender(), "-b", "--python-exit-code", "1", "-P", str(worker), "--", str(job)],
                           stdout=log, stderr=subprocess.STDOUT, check=True)
        stamp.write_text(signature)
    data = dict(configuration_title=cfg["version_title"], book=cfg["book"], style=cfg["style"],
                parts=parts, printed_keys=printed, steps=steps, physical_item_count=len(parts), source_sha256=hashes)
    with (output / "parts.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["key","name","quantity","id","identity_source","md5","md5_6_alpha","short_url"])
        writer.writeheader()
        writer.writerows(parts.values())
    assembly_booklet.publish(output=output, data=data)
    assembly_booklet.review_outputs(output=output, data=data)
    assembly_viewer.publish(output=output, data=data)


"""Check generated version 1 meshes against every archived printable part.

Run after action_make_scad.py. Add --initial-version-2 to also compare the
unedited version 2 starting drawings. Run the default check after v2 edits.
"""
import argparse
from pathlib import Path

import trimesh
import yaml
from shapely.geometry import MultiLineString

PROJECT = Path(__file__).resolve().parent


def section_outline(mesh, z):
    section = mesh.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
    return MultiLineString([loop[:, :2] for loop in section.discrete])


def main(compare_initial_copy=False):
    archive = PROJECT / "old_version" / "parts"
    expected = {p.parent.name for p in archive.glob("*/3dpr.stl")}
    seen = set()
    max_bounds = max_volume = max_outline = 0
    for metadata in sorted((PROJECT / "parts_source").glob("*_version_1_*/working.yaml")):
        part = yaml.safe_load(metadata.read_text(encoding="utf-8"))
        legacy_id = part["legacy_id"]
        if legacy_id in seen:
            raise ValueError(f"Duplicate archived part {legacy_id}")
        seen.add(legacy_id)
        directory = PROJECT / "parts" / metadata.parent.name
        reference = trimesh.load_mesh(archive / legacy_id / "3dpr.stl")
        mesh = trimesh.load_mesh(directory / "3dpr.stl")
        if not mesh.is_volume or mesh.body_count != 1:
            raise ValueError(f"{directory.name} is not one closed solid")
        bounds = abs(reference.bounds - mesh.bounds).max()
        volume = abs(mesh.volume / reference.volume - 1) * 100

        # Cross the bit passage, shoulder, transverse lock, grip and cap.
        # On the labels, cross both the engraving and the hex plug.
        name = part["oobb_name"]
        if name == "precision_screwdriver":
            heights = [3, 10, 24, 26, 32, 55, 58.1, 62, 89, 102, 106]
        elif name == "bit_lock":
            heights = [1, 8, 9.3, 12]
        else:
            heights = [-5.5, -2, 0.25, 1.0]
        outline = max(section_outline(reference, z).hausdorff_distance(section_outline(mesh, z))
                      for z in heights)
        if bounds > 0.001 or volume > 0.01 or outline > 0.25:
            raise ValueError(f"{directory.name}: bounds {bounds} mm, volume {volume}%, outline {outline} mm")
        max_bounds = max(max_bounds, bounds)
        max_volume = max(max_volume, volume)
        max_outline = max(max_outline, outline)

        if compare_initial_copy:
            sibling = directory.with_name(directory.name.replace("_version_1_", "_version_2_", 1))
            if (directory / "3dpr.scad").read_bytes() != (sibling / "3dpr.scad").read_bytes():
                raise ValueError(f"Initial version 2 drawing differs for {directory.name}")
            other = trimesh.load_mesh(sibling / "3dpr.stl")
            if mesh.identifier_hash != other.identifier_hash or not other.is_volume or other.body_count != 1:
                raise ValueError(f"Initial version 2 mesh differs for {directory.name}")
    if not expected or expected != seen:
        raise ValueError(f"Catalogue differs from archive: {expected ^ seen}")
    print(f"{len(seen)} archived meshes checked. Maximum bounds delta {max_bounds:.6f} mm, "
          f"volume delta {max_volume:.6f}%, section outline delta {max_outline:.4f} mm.")
    if compare_initial_copy:
        print(f"Matched {len(seen)} initial version 2 SCAD files and mesh fingerprints.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--initial-version-2", action="store_true")
    main(parser.parse_args().initial_version_2)

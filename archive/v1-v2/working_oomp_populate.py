"""Catalogue for the precision screwdriver. Run from the project directory."""
import copy
from pathlib import Path

import yaml
from oomp_populate_helper import build_oomp_id, write_extras


def main(**kwargs):
    extras = []

    for version in ["version_1", "version_2"]:
        options = []

        # These are the round shaft diameters of the bits, in millimetres.
        # All handles take the same quarter-inch hex shank.
        for diameter in [2, 2.25, 2.5, 2.75, 3, 3.25, 3.5, 3.75, 4, 4.25, 4.5, 4.75, 5]:
            option = {}
            option["oobb_name"] = "precision_screwdriver"
            option["diameter_bit_main"] = diameter
            option["radius_bit_main"] = diameter / 2
            option["thickness"] = 3
            option["extra"] = f"{diameter}_mm_diameter_bit_main"
            option["taxonomy_4"] = option["extra"].replace(".", "_")
            options.append(option)

        option = {}
        option["oobb_name"] = "bit_lock"
        option["thickness"] = 3
        options.append(option)

        # Keep the label text as strings so PH0, PH00 and PH000 stay distinct.
        label_sizes = {}
        label_sizes["hex"] = ["5", "4", "3.5", "3", "2.5", "2", "1.5", "0.9", "0.7", "1.3"]
        label_sizes["slotted"] = ["0.8", "1", "1.2", "1.5", "1.8", "2", "2.5", "3", "4"]
        label_sizes["phillips"] = ["0", "00", "000", "1", "2"]

        for shape, sizes in label_sizes.items():
            for siz in sizes:
                option = {}
                option["oobb_name"] = "label_top"
                option["shape"] = shape
                option["siz"] = siz
                option["thickness"] = 1.5 if version == "version_1" else 11.25
                option["extra"] = f"{shape}_shape_{siz}_size"
                option["taxonomy_4"] = shape
                option["taxonomy_5"] = f"{siz}_size".replace(".", "_")
                options.append(option)

        if version == "version_2":
            for name, height in [("bearing_mount", 6.75), ("fit_coupons", 21)]:
                option = {}
                option["oobb_name"] = name
                option["thickness"] = height
                options.append(option)

        for option in options:
            name = option["oobb_name"]
            thickness = option["thickness"]
            extra = option.get("extra", "")
            option["taxonomy_1"] = "tool_precision_screwdriver"
            option["taxonomy_2"] = version
            option["taxonomy_3"] = name
            option["project_name"] = "oomlout_oobb_tool_precision_screwdriver"
            option["classification"] = "project"
            option["type"] = "github"
            option["size"] = "oomlout"
            option["color"] = "oomlout_oobb_tool_precision_screwdriver"
            option["description_main"] = f"{name}_1_width_1_height_{thickness}_mm_depth"
            option["description_extra"] = f"{extra}_extra" if extra else ""
            legacy_id = f'project_github_oomlout_{option["color"]}_{option["description_main"]}'
            if extra:
                legacy_id += f"_{extra}_extra"
            if name == "label_top":
                legacy_id = legacy_id.replace(f"_{thickness}_mm_depth", "_1.5_mm_depth")
            if name not in ["bearing_mount", "fit_coupons"]:
                option["legacy_id"] = legacy_id.replace(".", "_")
            if name == "label_top" and version == "version_2":
                option["color_parts"] = ["main", "support"]

            p3 = {}
            p3["oobb_name"] = name
            p3["oobb_type"] = f"{name}_{version}"
            p3["run_scad"] = True
            p3["run_solidcraft"] = False
            p3["width"] = 1
            p3["height"] = 1
            p3["thickness"] = thickness
            p3["extra"] = extra
            if name == "precision_screwdriver":
                p3["diameter_bit_main"] = option["diameter_bit_main"]
                p3["radius_bit_main"] = option["radius_bit_main"]
            if name == "label_top":
                p3["shape"] = option["shape"]
                p3["siz"] = option["siz"]
            option["oobb_details"] = p3
            extras.append(copy.deepcopy(option))

    # Purchased hardware is shared by both revisions. Keep its supplier record,
    # drawings and diagrams with it when materializing a fresh parts directory.
    hardware_folder = Path("source_file/hardware_screw_countersunk_m3_black_6_mm_length_hex_head")
    option = yaml.safe_load((hardware_folder / "working.yaml").read_text(encoding="utf-8"))
    option["taxonomy_1"] = "hardware"
    option["taxonomy_2"] = "screw_countersunk"
    option["taxonomy_3"] = "m3"
    option["taxonomy_4"] = "black"
    option["taxonomy_5"] = "6_mm_length"
    option["taxonomy_6"] = "hex_head"
    option["file_copy"] = []
    for asset in sorted(hardware_folder.iterdir()):
        if asset.name != "working.yaml":
            file_copy = {}
            file_copy["file_source"] = asset.as_posix()
            file_copy["file_destination"] = asset.name
            option["file_copy"].append(file_copy)
    extras.append(option)

    import working_oomp_populate_extra_detail
    working_oomp_populate_extra_detail.main(extras=extras)
    write_extras(extras)


if __name__ == "__main__":
    main()

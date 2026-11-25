"""Catalogue for the precision screwdriver. Run from the project directory."""
import copy
from pathlib import Path

import yaml
from oomp_populate_helper import build_oomp_id, write_extras


def main(**kwargs):
    extras = []

    version = "version_3"
    options = []

    # These are the round shaft diameters of the bits, in millimetres.
    # All handles take the same quarter-inch hex shank.
    for diameter in [2, 2.25, 2.5, 2.75, 3, 3.25, 3.5, 3.75, 4, 4.25, 4.5, 4.75, 5]:
        option = {}
        option["oobb_name"] = "precision_screwdriver"
        option["diameter_bit_main"] = diameter
        option["radius_bit_main"] = diameter / 2
        option["thickness"] = 91.5
        option["extra"] = f"{diameter}_mm_diameter_bit_main"
        option["taxonomy_4"] = option["extra"].replace(".", "_")
        options.append(option)

    # Keep the label text as strings so PH0, PH00 and PH000 stay distinct.
    label_sizes = {}
    label_sizes["hex"] = ["5", "4", "3.5", "3", "2.5", "2", "1.5", "0.9", "0.7", "1.3"]
    label_sizes["slotted"] = ["0.8", "1", "1.2", "1.5", "1.8", "2", "2.5", "3", "4"]
    label_sizes["phillips"] = ["0", "00", "000", "1", "2"]

    label_sizes["torx"] = ["T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10", "T15", "T20", "T25"]

    from screwdriver_book.bands import colour_bands
    for shape, sizes in label_sizes.items():
        for siz in sizes:
            option = {}
            option["oobb_name"] = "label_top"
            option["shape"] = shape
            option["siz"] = siz
            option["colour_bands"] = colour_bands(shape, siz)
            option["thickness"] = 11.25
            option["extra"] = f"{shape}_shape_{siz}_size"
            option["taxonomy_4"] = shape
            option["taxonomy_5"] = f"{siz.lower()}_size".replace(".", "_")
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
        if name == "label_top":
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
    import json
    Path("catalogue.json").write_text(json.dumps(define_project(), indent=2) + "\n", encoding="utf-8")


def define_assembly_card_style(**kwargs):
    """Four largely pictorial panels on landscape A4; dimensions in mm."""
    kwargs = copy.deepcopy(kwargs)
    kwargs.setdefault("page_mm", [297, 210])
    kwargs.setdefault("columns", 2)
    kwargs.setdefault("rows", 2)
    kwargs.setdefault("caption_background", "#00B1B7")
    kwargs.setdefault("caption_text", "#000000")
    return kwargs


def define_project():
    project = {}
    project["title"] = "OOBB precision screwdriver"
    project["summary"] = "A printable, bearing-capped handle for long quarter-inch hex bits. Choose the handle by the round shaft diameter and the cap by the drive marking."
    project["parts"] = "Print one handle plate and one cap. Each handle plate contains the body, slotted key, side-loading nut cradle, bearing lifter and countersunk insert."
    project["assembly"] = "Load the bit and lock before fitting the cradle, lifter and bearing. The cap presses onto the outer ring."
    project["credit"] = "The Oomlout precision screwdriver is the starting design. Wera Kraftform Micro and the iFixit Precision Bit Driver informed the fingertip waist and grip texture."
    project["credits"] = [
        ["Original screwdriver by Oomlout", "https://github.com/oomlout/oomlout_oobb_tool_precision_screwdriver"],
        ["Oomlout", "https://github.com/oomlout"],
    ]
    project["study"] = [
        {
            "driver": "Wera Kraftform Micro",
            "observation": "Wera divides the handle into a precision zone near the tip, a wider torque grip and a fast-turning zone near the cap.",
            "decision": "Give the fingertips a 10.3 mm waist, increase the thumb pad to 12.7 mm, and keep the rear taper smooth for spinning.",
            "source": "https://www.wera.de/en/tools/highlights-great-tools/kraftform-micro/",
        },
        {
            "driver": "iFixit Precision Bit Driver",
            "observation": "The 115 mm aluminium driver combines a knurled grip with a swivel cap.",
            "decision": "Use eight broad axial flutes on the thumb pad. Their tapered ends follow the print direction and leave the adjacent spanner flats accessible.",
            "source": "https://www.ifixit.com/products/ifixit-precision-bit-driver-aluminum",
        },
        {
            "driver": "Wiha PicoFinish",
            "observation": "Wiha puts the drive symbol on its rotating end cap so a driver can be identified in the rack.",
            "decision": "Pair the printed drive symbol with its size on the closed cap face. Torx caps carry a T prefix and a rounded six-lobe mark.",
            "source": "https://digicat.wiha.com/int/en/tools/screwdrivers/precision-screwdrivers/picofinish/sets/fine-screwdriver-set-picofinish/42996",
        },
    ]
    project["archive_versions"] = [
        {"title": "Version 2", "description": "First 606 bearing assembly, 111.6 mm nose to palm", "page": "archive/v1-v2/VERSION_2_BUILD.md", "image": "archive/v1-v2/assembly_version_2.png"},
        {"title": "Version 1", "description": "Original plug-style topper and handle", "page": "archive/v1-v2/navigation_oobb/tool_precision_screwdriver/version_1/README.md", "image": "archive/v1-v2/parts/tool_precision_screwdriver_version_1_precision_screwdriver_3_5_mm_diameter_bit_main/3dpr_presentation.png"},
    ]
    project["example_id"] = "tool_precision_screwdriver_version_3_precision_screwdriver_3_5_mm_diameter_bit_main"
    project["example_cap"] = "tool_precision_screwdriver_version_3_label_top_torx_t5_size"
    project["modes"] = ["3dpr", "true"]
    project["assembly_folder"] = "assembly"
    project["version_folder"] = "parts/version_3"
    project["version_name"] = "Version 3"
    project["version_title"] = "Version 3 · compact bearing handle"
    project["version_description"] = "101.6 mm capped, waisted grip and Torx labels"
    project["part_labels"] = {
        "body": {"name": "Handle, 3.5 mm shaft"},
        "key": {"name": "Slotted lock key"},
        "cradle": {"name": "Side-loading cradle"},
        "lifter": {"name": "Bearing lifter"},
        "insert": {"name": "Countersunk insert"},
        "cap": {"name": "T5 palm cap"},
        "bit": {
            "name": "100 mm bit, 1/4 inch shank",
            "id": "precision_screwdriver_bit_100_mm_quarter_inch_3_5_mm_shaft_t5",
            "identity_source": "project-local representative bit",
        },
        "bearing": {
            "name": "606 bearing, 6 x 17 x 6",
            "id": "hardware_bearing_600_series_606_size_6_mm_id_17_mm_od_6_mm_depth",
            "identity_source": "OOMP bearing catalogue",
        },
        "side_screw": {
            "name": "M3 x 6 countersunk hex",
            "id": "hardware_screw_countersunk_m3_black_6_mm_length_hex_head",
            "identity_source": "project purchased hardware record",
        },
        "top_screw": {
            "name": "M3 x 16 countersunk hex",
            "id": "hardware_screw_countersunk_hex_head_black_m3_diameter_16_mm_length",
            "identity_source": "OOMP screw catalogue",
        },
        "top_nut": {
            "name": "M3 hex nut",
            "id": "hardware_nut_m3",
            "identity_source": "OOMP bolt catalogue",
        },
    }
    project["part_labels"]["side_nut"] = copy.deepcopy(project["part_labels"]["top_nut"])
    book = {}
    book["cover_title"] = "Precision screwdriver"
    book["cover_subtitle"] = "Version 3 / 606 bearing / quarter-inch drive"
    book["project_name"] = "oomlout_oobb_tool_precision_screwdriver_version_5"
    book["project_url"] = "https://github.com/oomlout/" + book["project_name"]
    book["viewer_layout"] = "a4-landscape-four-step"
    book["viewer_start"] = "page-01"
    book["materials"] = "One handle plate, one cap, one 100 mm quarter-inch bit, one 606 bearing (6 × 17 × 6 mm), two M3 nuts, and M3 × 6 mm and M3 × 16 mm countersunk screws."
    project["book"] = book
    project["style"] = define_assembly_card_style()
    project["steps"] = [
        {
            "title": "Lock the bit",
            "action": "Feed the bit tip-first from the rear. Slide in the key, align its slot, and secure it with the side nut and M3 × 6 mm screw.",
            "add": ["body", "bit", "key", "side_screw", "side_nut"],
            "move": {"key": [0, 0, 45], "side_screw": [10, 0, 0], "side_nut": [-10, 0, 0]},
        },
        {
            "title": "Load the cradle",
            "action": "Slide the second M3 nut edge-first into the cradle, thread facing up. Push the cradle into the side slot until its curved face is flush.",
            "add": ["cradle", "top_nut"],
            "move": {"cradle": [0, 13, 0], "top_nut": [0, 9, -0.65]},
        },
        {
            "title": "Seat the bearing",
            "action": "Seat the lifter in the handle. Place the 606 on its raised centre, then fit the insert into the bearing bore, countersink facing up.",
            "add": ["lifter", "bearing", "insert"],
            "move": {"lifter": [0, 0, 5], "bearing": [0, 0, 13], "insert": [0, 0, 24]},
        },
        {
            "title": "Fit the cap",
            "action": "Tighten the M3 × 16 mm screw into the captive nut. Check the outer ring spins, press the cap onto it, and spin again under light pressure.",
            "add": ["top_screw", "cap"],
            "move": {"top_screw": [0, 0, 8], "cap": [0, 0, 23]},
        },
    ]
    return project


if __name__ == "__main__":
    main()

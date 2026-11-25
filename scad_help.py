import copy
import oobb
import yaml
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
import working_scad
###### utilities


def cleanup_raw_scad_artifacts(folder):
    if not folder or not os.path.isdir(folder):
        return

    hex_pattern = re.compile(r"^(?P<stem>.+)_[0-9a-f]{16}\.scad$")
    referenced_helpers = {}

    for entry in os.listdir(folder):
        if not entry.endswith(".scad"):
            continue

        scad_path = os.path.join(folder, entry)
        try:
            with open(scad_path, "r", encoding="utf-8") as handle:
                contents = handle.read()
        except OSError:
            continue

        for match in re.finditer(r"use <([^>]+/(?P<stem_abs>[^/>]+)_[0-9a-f]{16}\.scad|(?P<stem_rel>[^/>]+)_[0-9a-f]{16}\.scad)>", contents):
            stem = match.group("stem_abs") or match.group("stem_rel")
            hashed_name = os.path.basename(match.group(1))
            referenced_helpers[stem] = hashed_name

        updated = re.sub(
            r"use <([^>]+/)?(?P<stem>[^/>]+)_[0-9a-f]{16}\.scad>",
            lambda m: f"use <{m.group('stem')}.scad>",
            contents,
        )
        if updated != contents:
            with open(scad_path, "w", encoding="utf-8") as handle:
                handle.write(updated)

    for stem, hashed_name in referenced_helpers.items():
        friendly_path = os.path.join(folder, f"{stem}.scad")
        hashed_path = os.path.join(folder, hashed_name)
        if not os.path.exists(friendly_path) and os.path.exists(hashed_path):
            with open(hashed_path, "r", encoding="utf-8") as src:
                contents = src.read()
            with open(friendly_path, "w", encoding="utf-8") as dst:
                dst.write(contents)

    for entry in os.listdir(folder):
        match = hex_pattern.match(entry)
        if not match:
            continue

        friendly_name = f"{match.group('stem')}.scad"
        friendly_path = os.path.join(folder, friendly_name)
        hashed_path = os.path.join(folder, entry)

        if os.path.exists(friendly_path):
            try:
                os.remove(hashed_path)
            except OSError:
                pass

def get_typ(**kwargs):
    typ = kwargs.get("typ", "")

    if typ == "":
        #setup
        #typ = "all"
        typ = "fast"
        #typ = "manual"

    return typ


def get_build_variables(typ, filter=""):
    if typ == "all":
        return {
            "filter": filter,
            "save_type": "all",
            "navigation": True,
            "overwrite": True,
            "modes": ["3dpr"],
            "oomp_run": True,
        }

    if typ == "fast":
        return {
            "filter": filter,
            "save_type": "none",
            "navigation": True,
            "overwrite": True,
            "modes": ["3dpr"],
            "oomp_run": False,
        }

    if typ == "manual":
        return {
            "filter": filter,
            #"filter": "test"
            "save_type": "none",
            #"save_type": "all"
            "navigation": True,
            #"navigation": False
            "overwrite": True,
            "modes": ["3dpr"],
            #"modes": ["3dpr", "laser", "true"]
            #"modes": ["laser"]
            "oomp_run": True,
            #"oomp_run": False
        }

    raise ValueError(f"Unknown typ: {typ}")


def get_navigation_sort(oobb_style=False):
    sort = []
    if oobb_style:
        #sort.append("extra")
        sort.append("oobb_name")
        sort.append("width")
        sort.append("height")
        sort.append("thickness")
    else:
        for i in range(1, 10):
            sort.append(f"taxonomy_{i}")
    return sort


def prepare_base_for_print(thing, pos, **kwargs):
    #put into a rotation object
    components_second = copy.deepcopy(thing["components"])
    return_value_2 = {}
    return_value_2["type"]  = "rotation"
    return_value_2["typetype"]  = "p"
    pos1 = copy.deepcopy(pos)
    pos1[0] += 50
    return_value_2["pos"] = pos1
    return_value_2["rot"] = [180,0,0]
    return_value_2["objects"] = components_second

    thing["components"].append(return_value_2)

    #add slice # top
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_slice"
    pos1 = copy.deepcopy(pos)
    pos1[0] += -500/2
    pos1[1] += 0
    pos1[2] += -500/2
    p3["pos"] = pos1
    #p3["m"] = "#"
    oobb.append_full(thing,**p3)

def make_parts(**kwargs):
    parts = kwargs.get("parts", [])
    filter = kwargs.get("filter", "")
    #make the parts
    if True:
        for part in parts:
            oobb_name = part.get("oobb_name", "default")
            extra = part["kwargs"].get("extra", "")
            if filter in oobb_name or filter in extra or filter in part.get("id", "") or filter in part.get("oobb_details", {}).get("oobb_type", ""):
                print(f"making {part['oobb_name']}")
                make_scad_generic(part)

            else:
                print(f"skipping {part['oobb_name']}")


def make_scad_generic(part):
    import working_cad
    if not working_cad.enabled(part.get("oobb_details", {}), "scad"):
        return


    # fetching variables
    oobb_name = part.get("oobb_name", "default")
    project_name = part.get("project_name", "default")

    kwargs = working_cad.geometry_parameters(part.get("kwargs", {}))

    modes = kwargs.get("modes", ["3dpr", "laser", "true"])
    save_type = kwargs.get("save_type", "all")
    overwrite = kwargs.get("overwrite", True)

    kwargs["type"] = f"{project_name}_{oobb_name}"

    thing = oobb.get_default_thing(**kwargs)
    thing.update(part)
    kwargs.pop("size","")

    # An explicit oobb_type selects get_<type> in this backend's recipe module.
    func = working_cad.resolve_builder(working_scad, part, legacy_fallback=True)
    func(thing, **kwargs)

    oomp_mode = kwargs.get("oomp_mode", "project")

    if oomp_mode == "project":
        descmain = ""
        current_description_main = thing.get("description_main", "default")
        current_size = thing.get("size", "default")
        new_size = current_size.replace(f"{project_name}_", "")
        descmain = f"{new_size}_{current_description_main}"
        kwargs["oomp_description_main"] = f"{descmain}"
        descextra = ""
        current_description_extra = thing.get("description_extra", "")
        descextra = f"{current_description_extra}"
        kwargs["oomp_description_extra"] = f"{descextra}"
    elif oomp_mode == "oobb":
        current_description_main = thing.get("description_main", "default")
        descmain = f"{current_description_main}"

        descextra = thing.get("extra", "")
        if descextra != "":
            descextra = f"{descextra}_extra"
        kwargs["oomp_description_main"] = f"{current_description_main}"
        kwargs["oomp_description_extra"] = f"{descextra}"
        kwargs["oomp_size"] = f"{part['oobb_name']}"

    #id = thing.get("oobb_id", "default")


    #kwargs["description_main"] = id

    oomp_keys = ["classification", "type", "size", "color", "description_main", "description_extra", "manufacturer", "part_number"]
    oomp_id = part.get("id", "")
    if oomp_id == "":
        for key in oomp_keys:
            deet = part.get(key, "")
            deet = deet.replace(".","_")
            if deet != "":
                oomp_id += f"{deet}_"
        oomp_id = oomp_id[:-1]
    part["id"] = oomp_id
    folder = f"parts/{oomp_id}"

    for mode in modes:
        depth = thing.get(
            "depth_mm", thing.get("thickness_mm", 3))
        height = thing.get("height_mm", 100)
        layers = depth / 3
        tilediff = height + 10
        start = 1.5
        if layers != 1:
            start = 1.5 - (layers / 2)*3
        if "bunting" in thing:
            start = 0.5


        scad_path = Path(folder) / f"{mode}.scad"
        printable = mode == "3dpr" and save_type == "all"
        # The shared "all" exporter also requests 2-D formats. These parts
        # are solids. Export the mesh and preview with checked exit codes.
        oobb.opsc_make_object(str(scad_path), thing["components"], mode=mode,
                              save_type="none" if printable else save_type,
                              overwrite=overwrite, layers=layers, tilediff=tilediff, start=start)
        if printable:
            from PIL import Image
            openscad = shutil.which("openscad.com") or shutil.which("openscad")
            if not openscad:
                raise FileNotFoundError("OpenSCAD is required for STL and PNG export")
            mesh = scad_path.with_suffix(".stl")
            preview = scad_path.with_suffix(".png")
            if overwrite or not mesh.exists():
                subprocess.run([openscad, "--export-format", "binstl", "-o", str(mesh), str(scad_path)], check=True)
        if mode == "3dpr":
            for color_part in part.get("color_parts", []):
                color_path = scad_path.with_stem(f"3dpr_color_{color_part}")
                color_kwargs = copy.deepcopy(kwargs)
                color_kwargs["color_part"] = color_part
                color_thing = oobb.get_default_thing(**color_kwargs)
                func(color_thing, **color_kwargs)
                oobb.opsc_make_object(str(color_path), color_thing["components"], mode=mode,
                                      save_type="none", overwrite=overwrite)
                color_mesh = color_path.with_suffix(".stl")
                if printable and (overwrite or not color_mesh.exists()):
                    subprocess.run([openscad, "--export-format", "binstl", "-o",
                                    str(color_mesh), str(color_path)], check=True)
        if printable:
            if overwrite or not preview.exists():
                if part.get("color_parts") == ["main", "support"]:
                    # Show the readable palm face while preserving bed coordinates
                    # in both printable meshes. F5 preview preserves material colours.
                    with tempfile.TemporaryDirectory() as temporary_directory:
                        display = Path(temporary_directory) / "label.scad"
                        main_mesh = scad_path.with_stem("3dpr_color_main").with_suffix(".stl").resolve()
                        ink_mesh = scad_path.with_stem("3dpr_color_support").with_suffix(".stl").resolve()
                        display.write_text(
                            f'rotate([180,0,0]) {{\n'
                            f'  color("#00B1B7") import("{main_mesh.as_posix()}");\n'
                            f'  color("#000000") import("{ink_mesh.as_posix()}");\n}}\n',
                            encoding="utf-8",
                        )
                        subprocess.run([openscad, "--preview", "--camera", "0,-10,35,0,0,-3",
                                        "--viewall", "--autocenter", "--imgsize", "1000,1000",
                                        "-o", str(preview), str(display)], check=True)
                else:
                    subprocess.run([openscad, "--render", "--viewall", "--autocenter",
                                "--imgsize", "1000,1000", "-o", str(preview), str(scad_path)], check=True)
            with Image.open(preview) as image:
                for width in [1000, 600, 300, 140]:
                    thumbnail = image.copy()
                    thumbnail.thumbnail((width, width), Image.Resampling.LANCZOS)
                    thumbnail.save(preview.with_name(f"{mode}_{width}.png"))
        cleanup_raw_scad_artifacts(folder)



    yaml_file = f"{folder}/working.yaml"
    #partial dump
    with open(yaml_file, 'w') as file:
        part_new = copy.deepcopy(part)
        kwargs_new = part_new.get("kwargs", {})
        kwargs_new.pop("save_type","")
        part_new["kwargs"] = kwargs_new
        part_new["project_name"] = project_name
        part_new["id_oobb"] = thing["id"]
        #part_new["thing"] = thing
        part_new.pop("thing", "")
        yaml.dump(part_new, file)

    #full dump
    yaml_file = f"{folder}/thing.yaml"
    with open(yaml_file, 'w') as file:
        part_new = copy.deepcopy(part)
        kwargs_new = part_new.get("kwargs", {})
        kwargs_new.pop("save_type","")
        part_new["kwargs"] = kwargs_new
        part_new["project_name"] = project_name
        part_new["id_oobb"] = thing["id"]
        part_new["thing"] = thing
        yaml.dump(part_new, file)


    print(f"done {oomp_id}")

def generate_navigation(folder="parts", sort=None, **kwargs):
    from working_navigation import generate_navigation as generate
    return generate(folder=folder, sort=sort)

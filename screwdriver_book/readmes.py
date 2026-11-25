"""Version index and build notes from populate metadata and current part records."""
NOTICE = "AI-generated CAD images and instructions. Errors possible."
ORIGIN = ("This is an entirely AI-generated coding project. The source code is largely unreadable by humans, "
          "but usable generated files are included. It is published so others can use their own AI tools "
          "to understand, modify and regenerate the design.")


def version_pages(root, cfg, records):
    version = cfg["version_folder"]
    index = version + "/README.md"
    manual = cfg["assembly_folder"]
    photo = manual + "/render/raw/book_cover.png"
    credits = " · ".join(f"[{name}]({url})" for name, url in cfg["credits"])
    lines = ["# " + cfg["title"], "", cfg["summary"] + " Each printable part includes STL and OpenSCAD files.",
             "", cfg["credit"] + " " + credits, "",
             f'[![Assembled teal precision driver with a banded cap]({photo})]({index})', "",
             f'[Choose a handle and cap]({index}#choose-the-two-print-files) · [Four-step assembly]({manual}/README.md)', "", ORIGIN, "", NOTICE, "",
             "The dimensions and assembly clearances have been checked in CAD. The compact grip and the bearing press fit still need a physical trial.", "",
             "| Image | Version and description | Main README | HTML assembly instructions | PDF download |",
             "| --- | --- | --- | --- | --- |",
             f'| [<img src="{photo}" width="150" alt="Compact screwdriver">]({index}) | [{cfg["version_name"]}]({index}) · {cfg["version_description"]} | [Design and print files]({index}) | [Standalone viewer]({manual}/assembly_instructions.html) | [Landscape A4 PDF]({manual}/assembly_instructions.pdf) |']
    for old in cfg["archive_versions"]:
        lines.append(f'| [<img src="{old["image"]}" width="150" alt="{old["title"]}">]({old["page"]}) | [{old["title"]}]({old["page"]}) · {old["description"]} | [Archived design]({old["page"]}) | — | — |')
    lines.extend(["", "[Browse handles and caps](navigation_oobb/tool_precision_screwdriver/version_3/) · "
                  "[CAD build and maintenance](CATALOGUE_BUILD.md) · [Archive](archive/README.md)"])
    landing = "\n".join(lines)

    handles = sorted((p for _,p in records if p.get("oobb_name") == "precision_screwdriver"),
                     key=lambda p: p["diameter_bit_main"])
    caps = [p for _,p in records if p.get("oobb_name") == "label_top"]
    lines = ["# " + cfg["version_title"], "", "[Project and previous versions](../../README.md)", "",
             "The handle is 91.5 mm from nose to rear face. The fitted cap adds 10.1 mm. The 10 mm and 13 mm spanner lands and the quarter-inch bit lock remain at their original positions.", "",
             "![Assembled driver](../../assembly/render/raw/book_cover.png)", "", "## Choose the two print files", "",
             cfg["parts"], "", "Measure the round shaft immediately above the bit tip. The quarter-inch hex shank is common to every handle.", "",
             "**Handle shaft diameter (mm)**  "]
    lines.append(" · ".join(f'[{p["diameter_bit_main"]}](../{p["id"]}/)' for p in handles))
    lines += ["", "| Cap marking | Sizes |", "| --- | --- |"]
    for family in ("hex", "slotted", "phillips", "torx"):
        members = [p for p in caps if p["shape"] == family]
        def order(part):
            value = part["siz"].lstrip("T")
            return float(value), -len(value)
        links = " · ".join(f'[{p["siz"]}](../{p["id"]}/)' for p in sorted(members, key=order))
        lines.append(f"| {family.title()} | {links} |")
    lines += ["", "Open the cap’s **banded 3MF** as a single assembly. Keep the registered parts together and assign filament by colour. Use the supplied face-down orientation. For a two-colour print, load the main and support STLs together at their original coordinates and assign teal to the shell and black to the marking.", "",
              "## Read the cap bands", "",
              "Read from the labelled palm face towards the handle. The wide ring identifies the drive. Narrow rings give the size, with a teal gap between digits. The face always spells out the size in black on teal.", "",
              "| Wide drive band | Narrow size bands | Example |", "| --- | --- | --- |",
              "| Slotted · brown | Millimetres in tenths, two digits | 1.5 mm → 15 → brown, green |",
              "| Hex · green | Millimetres in tenths, two digits | 0.7 mm → 07 → black, violet |",
              "| Phillips · red | Read the marking literally | PH00 → two black rings |",
              "| Torx · yellow | Read the number after T | T5 → one green ring |", "",
              "Digits from 0 to 9 are black, brown, red, orange, yellow, green, blue, violet, grey and white. Drive colours come from OOMP Band 5. The size convention is specific to this screwdriver. [Source palette](../../source_file/oomp_drive_type_colours.yaml)", "",
              "## Profile study", "", "| Driver | Manufacturer’s design | Decision for this print |", "| --- | --- | --- |"]
    for item in cfg["study"]:
        lines.append(f'| [{item["driver"]}]({item["source"]}) | {item["observation"]} | {item["decision"]} |')
    lines += ["", "The 10 mm reduction comes from the taper between the 13 mm hex and the flare. The cradle follows the revised taper so its outer face sits flush. The 17.07 mm bearing socket, recessed screw insert and 0.65 mm radial skirt clearance carry over from version 2.", "",
              "## Assembly", "", "[One shared four-step guide for every handle and cap](../../assembly/README.md) · [One-page PDF](../../assembly/assembly_instructions.pdf)", ""]
    lines += ["", "## Bench trial", "",
              "Compare this handle with version 2 using the same bit and bearing. Check whether your thumb and forefinger can spin the waist with your palm on the cap, then move to the fluted pad for the final turn. Check that the key holds, the cradle sits flush and the cap clears the flare under light pressure.", "",
              NOTICE, "", "[Editable drawing](../../working_scad_version_3.py) · [Part definitions and assembly sequence](../../working_oomp_populate.py) · [Build and verification](../../CATALOGUE_BUILD.md)"]
    shared = ["# Assemble the precision screwdriver", "",
              cfg["book"]["materials"], "",
              "[Open the illustrated sheet](assembly_instructions.html) · [Print the single-page PDF](assembly_instructions.pdf) · [Parts list](parts.csv)", "",
              "## Assembly", ""]
    for number, step in enumerate(cfg["steps"], 1):
        shared.append(f'{number}. **[{step["title"]}](render/raw/step_{number:02d}.png).** {step["action"]}')
    shared.extend(["", "![Four illustrated assembly steps](pages/page_01.png)", "", NOTICE, "",
                   "[Choose print files](../parts/version_3/README.md) · [Project](../README.md)"])
    return {root / "README.md": landing, root / index: "\n".join(lines),
            root / manual / "README.md": "\n".join(shared)}

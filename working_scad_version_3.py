"""Editable precision screwdriver drawings, version 3."""
import copy
import math

import oobb

# Shared by the stationary handle and the rotating cap skirt.
HANDLE_FLARE_RADIUS = 8.35


def get_label_top_version_3(thing, **kwargs):
    """Face-down palm cover. The coloured glyphs occupy the first three 0.2 mm layers."""
    pos = kwargs.get("pos", [0, 0, 0])
    shape = kwargs["shape"]
    siz = kwargs["siz"]
    color_part = kwargs.get("color_part", "engraved")
    ink_depth = 0.60

    if color_part != "support":
        # The whole skirt slides over the 606. Adjust the diametral
        # allowance for the printer and filament. Negative is interference.
        bearing_diameter = 17.0
        bearing_fit_allowance = kwargs.get("bearing_fit_allowance", 0.07)
        # 3dpr uses 50 facets. Specify the bore across the flats of the
        # polygon, where a round steel bearing first contacts the socket.
        socket_radius = (bearing_diameter + bearing_fit_allowance) / (2 * math.cos(math.pi / 50))

        # A single straight side between two rounded edges. The flat
        # centre of the face goes on the bed, with the lettering in it.
        cap_radius = 10.4
        # Extend the open end only; the bearing shoulder and label face
        # keep their assembled heights.
        cap_height = 11.25
        edge_radius = 0.65
        for bottom, top, radius in [
            (0, cap_height, cap_radius - edge_radius),
            (edge_radius, cap_height - edge_radius, cap_radius),
        ]:
            p3 = copy.deepcopy(kwargs)
            p3["type"] = "positive"
            p3["shape"] = "oobb_cylinder"
            p3["depth"] = top - bottom
            p3["radius"] = radius
            p3["pos"] = [pos[0], pos[1], pos[2] + (top + bottom) / 2]
            oobb.append_full(thing, **p3)

        for height in [edge_radius, cap_height - edge_radius]:
            p3 = copy.deepcopy(kwargs)
            p3["type"] = "positive"
            p3["shape"] = "oring"
            p3["id"] = cap_radius - 2 * edge_radius
            p3["depth"] = 2 * edge_radius
            p3["pos"] = [pos[0], pos[1], pos[2] + height]
            oobb.append_full(thing, **p3)

        # Eighteen shallow scallops with tapered ends give a fingertip
        # purchase in either direction. Leave both rounded edges smooth.
        for flute in range(18):
            angle = math.radians(flute * 20)
            x = pos[0] + (cap_radius + 0.55) * math.cos(angle)
            y = pos[1] + (cap_radius + 0.55) * math.sin(angle)
            for bottom, top, r1, r2 in [
                (0.9, 1.9, 0.4, 1.15),
                (1.88, 8.57, 1.15, 1.15),
                (8.55, 9.55, 1.15, 0.4),
            ]:
                p3 = copy.deepcopy(kwargs)
                p3["type"] = "negative"
                p3["shape"] = "oobb_cylinder"
                p3["depth"] = top - bottom
                p3["r1"] = r1
                p3["r2"] = r2
                p3["pos"] = [x, y, pos[2] + (top + bottom) / 2]
                oobb.append_full(thing, **p3)

        # Closed palm face, printed against the bed. Cut the underside
        # only. The 15 mm relief leaves a full annular press shoulder
        # at Z=2.70 for the 606 outer ring. The hidden screw and flange
        # turn clear of the pocket roof, even under the engraved markings.
        # The skirt clears the stationary R8.35 flare. The relief is
        # R9.00 at the polygon flats, giving 0.65 mm per side even as
        # the cap facets rotate past the tips of the handle facets.
        skirt_running_clearance = 0.65
        skirt_bore_radius = (HANDLE_FLARE_RADIUS + skirt_running_clearance) / math.cos(math.pi / 50)
        for bottom, top, lower_radius, upper_radius in [
            (1.25, 2.72, 7.50, 7.50),
            (2.70, 8.64, socket_radius, socket_radius),
            (8.62, 9.32, socket_radius, skirt_bore_radius),
            (9.30, cap_height + 0.05, skirt_bore_radius, skirt_bore_radius),
        ]:
            p3 = copy.deepcopy(kwargs)
            p3["type"] = "negative"
            p3["shape"] = "oobb_cylinder"
            p3["depth"] = top - bottom
            p3["r1"] = lower_radius
            p3["r2"] = upper_radius
            p3["pos"] = [pos[0], pos[1], pos[2] + (top + bottom) / 2]
            oobb.append_full(thing, **p3)

    # The same outlines cut the main plastic and fill the accent plastic.
    # The default single-colour STL keeps the recesses so it reads on its own.
    ink_type = "positive" if color_part == "support" else "negative"
    # Give each digit its own position. A 1.1 mm round decimal remains
    # visible on a 0.4 mm nozzle, and PH000 has daylight between the zeros.
    # Centre the original size-above-symbol layout on the full face.
    text_y = 4.0 if len(siz) == 1 else 3.5
    text_size = 4.5 if len(siz) == 1 else 4.0
    digit_pitch = 3.65
    if "." in siz:
        digit_pitch = 2.85
    for index, character in enumerate(siz):
        x = pos[0] + (index - (len(siz) - 1) / 2) * digit_pitch
        if character == ".":
            p3 = copy.deepcopy(kwargs)
            p3["type"] = ink_type
            p3["shape"] = "oobb_cylinder"
            p3["radius"] = 0.55
            p3["depth"] = ink_depth
            p3["pos"] = [x, pos[1] - text_y + 1.3, pos[2] + ink_depth / 2]
            oobb.append_full(thing, **p3)
        else:
            p3 = copy.deepcopy(kwargs)
            p3["type"] = ink_type
            p3["shape"] = "oobb_text"
            p3["text"] = character
            p3["font"] = "Liberation Sans:style=Bold"
            p3["size"] = text_size
            p3["depth"] = ink_depth
            p3["rot"] = [180, 0, 0]
            p3["pos"] = [x, pos[1] - text_y, pos[2] + ink_depth]
            oobb.append_full(thing, **p3)

    if shape == "hex":
        p3 = copy.deepcopy(kwargs)
        p3["type"] = ink_type
        p3["shape"] = "polyg"
        p3["sides"] = 6
        p3["radius"] = 3.0
        p3["height"] = ink_depth
        p3["pos"] = [pos[0], pos[1] + 3, pos[2]]
        oobb.append_full(thing, **p3)
    elif shape == "torx":
        # Six rounded lobes. This is a face marking, not a bit socket.
        points = []
        for step in range(96):
            angle = 2 * math.pi * step / 96
            radius = 2.45 + 0.65 * math.cos(6 * angle)
            points.append([radius * math.cos(angle), radius * math.sin(angle)])
        p3 = copy.deepcopy(kwargs)
        p3["type"] = ink_type
        p3["shape"] = "polygon"
        p3["points"] = points
        p3["height"] = ink_depth
        p3["pos"] = [pos[0], pos[1] + 3, pos[2]]
        oobb.append_full(thing, **p3)
    else:
        symbol_y = 2 if shape == "slotted" else 3
        strokes = [[6, 1.5]]
        if shape == "phillips":
            strokes.append([1.5, 6])
        for width, height in strokes:
            p3 = copy.deepcopy(kwargs)
            p3["type"] = ink_type
            p3["shape"] = "oobb_cube"
            p3["size"] = [width, height, ink_depth]
            p3["pos"] = [pos[0], pos[1] + symbol_y, pos[2]]
            oobb.append_full(thing, **p3)


def draw_handle_body_version_3(thing, **kwargs):

    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("thickness", 3)
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")

    #variables
    hex_side_ratio = 1.1547
    radius_main = 11 / 2

    #1_driver_bit
    driver_bit_lift = 25
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "negative"
        #p3["m"] = "#"
        p3["clearance"] = 0.2
        p3["clearance_top"] = True
        p3["length"] = 100
        pos1 = copy.deepcopy(pos)
        pos1[0] += 0 #+ 45
        pos1[2] += driver_bit_lift
        p3["pos"] = pos1
        get_tool_screwdriver_bit_quarter_inch_drive_100_mm_depth_version_3(thing, **p3)

    current_z = 0
    #2_indent_bottom
    indent_bottom_depth = 6
    current_depth = indent_bottom_depth
    indent_bottom_radius_bottom = kwargs.get("radius_bit_main", 1.75) + 0.125 + 0.95
    indent_bottom_radius_top = radius_main
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "positive"
        p3["shape"] = f"oobb_cylinder"
        p3["depth"] = indent_bottom_depth
        p3["r1"] = indent_bottom_radius_bottom
        p3["r2"] = indent_bottom_radius_top
        pos1 = copy.deepcopy(pos)
        pos1[2] += indent_bottom_depth/2
        p3["pos"] = pos1
        #p3["m"] = "#"
        oobb.append_full(thing, **p3)
    current_z += current_depth

    #3_hex_bottom
    hex_bottom_depth = 6
    current_depth = hex_bottom_depth
    hex_bottom_radius = 10/2 * hex_side_ratio
    hex_bottom_joiner_donut_bottom_radius = 25/2
    hex_bottom_joiner_donut_top_radius = 25/2
    hex_bottom_joiner_donut_id = hex_bottom_radius / hex_side_ratio
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "positive"
        p3["shape"] = f"polyg"
        p3["sides"] = 6
        p3["height"] = hex_bottom_depth
        p3["radius"] = hex_bottom_radius
        pos1 = copy.deepcopy(pos)
        pos1[2] += current_z
        p3["pos"] = pos1
        #p3["m"] = "#"
        oobb.append_full(thing, **p3)

        #joiners
        #shaft top joiner
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "negative"
        p3["shape"] = f"oring"
        dep = hex_bottom_joiner_donut_bottom_radius
        p3["depth"] = dep
        p3["id"] = hex_bottom_joiner_donut_id
        pos1 = copy.deepcopy(pos)
        pos1[2] += current_z #+ dep/2


        p3["pos"] = pos1
        #p3["m"] = "#"
        oobb.append_full(thing, **p3)

        p4 = copy.deepcopy(p3)
        dep = hex_bottom_joiner_donut_top_radius
        p4["depth"] = dep
        pos1 = copy.deepcopy(p4["pos"])
        pos1[2] += hex_bottom_depth
        p4["pos"] = pos1
        #p4["m"] = "#"
        oobb.append_full(thing, **p4)


    current_z += current_depth

    #4_shaft_bottom
    shaft_bottom_depth = 40
    # Smooth fingertip waist behind the nose, then a fluted thumb pad.
    # Stations are measured from the end of the 10 mm wrench land.
    for bottom, top, lower_radius, upper_radius in [
        (0, 6, 5.5, 5.15),
        (6, 12, 5.15, 5.15),
        (12, 21, 5.15, 6.35),
        (21, 33, 6.35, 6.35),
        (33, 40, 6.35, 5.5),
    ]:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "positive"
        p3["shape"] = "oobb_cylinder"
        p3["depth"] = top - bottom
        p3["r1"] = lower_radius
        p3["r2"] = upper_radius
        p3["pos"] = [pos[0], pos[1], pos[2] + current_z + (top + bottom) / 2]
        oobb.append_full(thing, **p3)
    current_z += shaft_bottom_depth

    #5 hex_top
    hex_top_depth = 12
    current_depth = hex_top_depth
    hex_top_radius = 13/2 * hex_side_ratio
    hex_top_joiner_donut_radius = 10/2
    hex_top_joiner_donut_id = radius_main
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "positive"
        p3["shape"] = f"polyg"
        p3["sides"] = 6
        p3["height"] = hex_top_depth
        p3["radius"] = hex_top_radius
        pos1 = copy.deepcopy(pos)
        pos1[2] += current_z
        p3["pos"] = pos1
        rot1 = copy.deepcopy(rot)
        rot1[2] = 360/12
        p3["rot"] = rot1
        #p3["m"] = "#"
        oobb.append_full(thing, **p3)

        #joiners
        #shaft top joiner
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "negative"
        p3["shape"] = f"oring"
        dep = hex_top_joiner_donut_radius
        p3["depth"] = dep
        p3["id"] = hex_top_joiner_donut_id
        pos1 = copy.deepcopy(pos)
        pos1[2] += current_z #+ dep/2
        pos2 = copy.deepcopy(pos)
        pos2[2] += current_z + hex_top_depth
        p3["pos"] = pos2

        poss = []
        poss.append(copy.deepcopy(pos1))
        poss.append(copy.deepcopy(pos2))
        p3["pos"] = poss
        #p3["m"] = "#"
        oobb.append_full(thing, **p3)

    current_z += current_depth

    #6_shaft_top
    shaft_top_depth = 25
    shaft_top_flair = 1
    shaft_top_radius_bottom = radius_main
    shaft_top_radius_top = shaft_top_radius_bottom + shaft_top_flair



    current_depth = shaft_top_depth

    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "positive"
        p3["shape"] = f"oobb_cylinder"
        dep = shaft_top_depth
        p3["depth"] = dep
        p3["r1"] = shaft_top_radius_bottom
        p3["r2"] = shaft_top_radius_top
        pos1 = copy.deepcopy(pos)
        pos1[2] += current_z + dep/2
        p3["pos"] = pos1
        #p3["m"] = "#"
        oobb.append_full(thing, **p3)




    current_z += current_depth

    # Eight round-ended axial flutes on the lower grip. Smooth bands beside
    # the 10 and 13 mm spanner lands leave both wrench approaches open.
    for index in range(8):
        angle = math.radians(index * 45)
        x = pos[0] + 7.20 * math.cos(angle)
        y = pos[1] + 7.20 * math.sin(angle)
        for bottom, top, lower_radius, upper_radius in [
            (29, 33, 0.35, 1.50),
            (33, 45, 1.50, 1.50),
            (45, 49, 1.50, 0.35),
        ]:
            p3 = copy.deepcopy(kwargs)
            p3["type"] = "negative"
            p3["shape"] = "oobb_cylinder"
            p3["depth"] = top - bottom
            p3["r1"] = lower_radius
            p3["r2"] = upper_radius
            p3["pos"] = [x, y, pos[2] + (top + bottom) / 2]
            oobb.append_full(thing, **p3)

    # The rear face is a flat annulus all the way from the bit-loading
    # mouth to the flare. All bearing lift is on the loose spacer.
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "positive"
    p3["shape"] = "oobb_cylinder"
    p3["depth"] = 2.5
    p3["r1"] = 6.5
    p3["r2"] = HANDLE_FLARE_RADIUS
    p3["pos"] = [pos[0], pos[1], pos[2] + 90.25]
    oobb.append_full(thing, **p3)

    # Continue the round rear mouth through the top of the cradle slot.
    # The former hex ledge between Z=88.35 and Z=89 obstructed this opening.
    mouth_bottom = 88.30
    mouth_top = 91.60
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "negative"
    p3["shape"] = "oobb_cylinder"
    p3["depth"] = mouth_top - mouth_bottom
    p3["radius"] = 4.4
    p3["pos"] = [pos[0], pos[1], pos[2] + (mouth_bottom + mouth_top) / 2]
    oobb.append_full(thing, **p3)

    # The cradle enters from +Y. Its full-width shoulders clear the far
    # wall by 0.10 mm when the narrower nose reaches its blind stop.
    for width, back, front in [(7.5, -3.70, 8.4), (4.7, -4.95, -3.50)]:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "negative"
        p3["shape"] = "oobb_cube"
        p3["size"] = [width, front - back, 4.9]
        p3["pos"] = [pos[0], pos[1] + (front + back) / 2, pos[2] + 83.45]
        oobb.append_full(thing, **p3)

    #8_screw_lock
    screw_lock_depth = 8
    screw_lock_lift =  indent_bottom_depth + hex_bottom_depth + shaft_bottom_depth + hex_top_depth/2#driver_bit_lift + 30 + 5
    width_bit_locker = 7
    height_bit_locker = 3
    depth_bit_locker = 14
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "negative"
        p3["shape"] = f"oobb_screw_countersunk"
        dep = screw_lock_depth
        p3["depth"] = dep
        p3["nut"] = True
        p3["clearance"] = ["top","bottom"]
        p3["radius_name"] = "m3"
        p3["clearance_tightness"] = -0.2
        pos1 = copy.deepcopy(pos)
        y_shift = (shaft_top_radius_bottom - screw_lock_depth)
        pos1[0] += 0 + dep/2 - y_shift#+ 45

        pos1[2] += screw_lock_lift
        p3["pos"] = pos1
        rot1 = copy.deepcopy(rot)
        rot1[1] += 90
        #rot1[0] += 360/12
        rot1[2] = 0  # transverse to the key, along the original screw axis
        p3["rot"] = rot1
        #p3["m"] = "#"
        oobb.append_full(thing, **p3)

        #add screw locker clearance

        shift_y = 0
        #shift_y = 30
        extra = 10
        bot = screw_lock_lift - extra
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "negative"
        p3["shape"] = f"oobb_cube"
        clear = kwargs.get("key_allowance", 0.5)
        hei = width_bit_locker + clear
        wid = height_bit_locker + clear
        dep = 120 - bot
        size = [wid, hei, dep]
        p3["size"] = size
        pos1 = copy.deepcopy(pos)
        pos1[0] += 0 #+ 45
        pos1[1] += shift_y
        pos1[2] += bot
        p3["pos"] = pos1
        #p3["m"] = "#"
        #p3["zz"] = "mi"
        oobb.append_full(thing, **p3)

    pass

def get_bit_lock_version_3(thing, **kwargs):

    width_bit_locker = 7
    height_bit_locker = 3
    depth_bit_locker = 14

    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("thickness", 3)
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")

    dep = depth_bit_locker

    #add cube
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "positive"
    p3["shape"] = f"oobb_cube"
    wid = width_bit_locker
    hei = height_bit_locker
    dep = dep
    size = [wid, hei, dep]
    p3["size"] = size
    #p3["holes"] = True         uncomment to include default holes
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)
    p3["pos"] = pos1
    oobb.append_full(thing, **p3)

    #add slot
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "negative"
    p3["shape"] = f"oobb_slot"
    p3["m"] = "#"
    wid = 5
    p3["width"] = wid
    p3["depth"] = height_bit_locker
    pos1 = copy.deepcopy(pos)
    pos1[2] += depth_bit_locker - wid + 1.5
    pos1[1] += -height_bit_locker/2
    p3["pos"] = pos1
    rot1 = copy.deepcopy(rot)
    rot1[1] = 90
    rot1[2] = 90
    p3["rot"] = rot1
    # Resolve the standard M3 end radius separately for each output mode.
    for mode in ["laser", "3dpr", "true"]:
        radius = oobb.gv("hole_radius_m3", mode)
        # Explicit end cylinders preserve the slot while avoiding the legacy
        # slot exporter emitting redundant r, r1 and r2 arguments together.
        thing["components"].append({
            "type": "hull", "typetype": "negative", "inclusion": mode,
            "pos": [pos1[0], pos1[1], pos1[2] - height_bit_locker / 2],
            "rot": copy.deepcopy(rot1),
            "objects": [{"type": "positive", "shape": "cylinder",
                         "r": radius, "h": height_bit_locker,
                         "pos": [x, 0, 0]} for x in (-wid / 2, wid / 2)],
        })

    if prepare_print:
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
        oobb.append_full(thing, **p3)

def get_tool_screwdriver_bit_quarter_inch_drive_100_mm_depth_version_3(thing, **kwargs):
    clearance = kwargs.get("clearance", 0)
    include_bit = kwargs.get("include_bit", True)
    clearance_top = kwargs.get("clearance_top", False)
    radius_bit_main = kwargs.get("radius_bit_main", 3.5/2)
    pos = kwargs.get("pos", [0, 0, 0])
    rot = kwargs.get("rot", [0, 0, 0])

    length = kwargs.get("length", 150)

    # setting up for rotation object
    typ = kwargs.get("type", "p")
    kwargs["type"] = "positive" #needs to be positive for the difference to work
    rot_original = rot
    kwargs.pop("rot", None)
    kwargs.pop("rot_x", None)
    kwargs.pop("rot_y", None)
    kwargs.pop("rot_z", None)

    # storing pos and popping it out to add it in rotation element
    pos_original = copy.deepcopy(copy.deepcopy(kwargs.get("pos", [0, 0, 0])))
    pos_original_original = copy.deepcopy(pos_original)
    kwargs.pop("pos", None)
    pos = [0,0,0]



    return_value = []

    #hex shank
    if True:
        #hex bit is 0.25 inch6.35 mm
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "p"
        p3["shape"] = f"polyg"
        p3["sides"] = 6
        rad = (0.25 * 25.4) / 2  * 1.1546 + clearance# 7.32 hopefully
        p3["radius"] = rad
        height_total = 28 + clearance
        height_total_local = height_total
        if clearance_top:
            height_total_local += 200
        else:
            height_total_local = height_total
        p3["height"] = height_total_local
        #p3["depth"] = 4
        pos1 = copy.deepcopy(pos)
        pos1[0] += clearance /2
        p3["pos"] = pos1
        #p3["m"] = "#"
        return_value.append(oobb.oobb_easy(**p3))

    #cutout at bottom
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"tube_new"
        p3["height"] = 2
        p3["r2"]= 7.35/2 + clearance/2
        #p3["r1"]= 3.5/2
        p3["r1"]= radius_bit_main #+ clearance/2
        p3["wall_thickness"] = 8
        pos1 = copy.deepcopy(pos)
        p3["pos"] = pos1
        #p3["m"] = "#"
        # Use the OPSC tapered annulus directly (bottom-anchored, 2 mm high).
        return_value.append(oobb.opsc_easy(**p3))

    if include_bit:
        #add bit
        p3 = copy.deepcopy(kwargs)
        #p3["type"] = "n"
        p3["shape"] = f"oobb_cylinder"
        dep = length
        p3["depth"] = dep

        p3["radius"] = radius_bit_main + 0.25 / 2
        pos1 = copy.deepcopy(pos)
        pos1[2] += -dep/2 + height_total
        p3["pos"] = pos1
        p3["m"] = "#"
        return_value.append(oobb.oobb_easy(**p3))


    # packaging as a rotation object
    return_value_2 = {}
    return_value_2["type"]  = "rotation"
    return_value_2["typetype"]  = typ
    return_value_2["pos"] = pos_original
    return_value_2["rot"] = rot_original
    return_value_2["objects"] = return_value
    return_value_2 = [return_value_2]


    thing["components"].append(return_value_2)
def get_precision_screwdriver_version_3(thing, **kwargs):
    # Flip the body as a whole onto its broad rear ring. Keep the key's
    # subtractive slot local to the key, then lay it on a 7 x 14 mm face.
    pos = kwargs.get("pos", [0, 0, 0])
    p3 = copy.deepcopy(kwargs)
    p3["pos"] = [0, 0, 0]
    body = oobb.get_default_thing(**p3)
    draw_handle_body_version_3(body, **p3)
    placement = {}
    placement["type"] = "rotation"
    placement["typetype"] = "positive"
    placement["rot"] = [180, 0, 0]
    placement["pos"] = [pos[0], pos[1], pos[2] + 91.5]
    placement["objects"] = body["components"]
    thing["components"].append(placement)

    key = oobb.get_default_thing(**p3)
    get_bit_lock_version_3(key, **p3)
    placement = {}
    placement["type"] = "rotation"
    placement["typetype"] = "positive"
    placement["rot"] = [-90, 0, 0]
    placement["pos"] = [pos[0] + 17, pos[1] - 7, pos[2] + 1.5]
    placement["objects"] = key["components"]
    thing["components"].append(placement)

    cradle = oobb.get_default_thing(**p3)
    draw_nut_cradle_version_3(cradle, **p3)
    placement = {}
    placement["type"] = "rotation"
    placement["typetype"] = "positive"
    # Put the flat side on the bed so the nut slot prints on edge.
    placement["rot"] = [0, 90, 0]
    placement["pos"] = [pos[0] + 28 - 2.3, pos[1], pos[2] + 3.6]
    placement["objects"] = cradle["components"]
    thing["components"].append(placement)

    # The flat-footed bearing spacer prints to the right of the cradle.
    p3 = copy.deepcopy(kwargs)
    p3["pos"] = [pos[0] + 42, pos[1], pos[2]]
    draw_bearing_spacer_version_3(thing, **p3)

    p3 = copy.deepcopy(kwargs)
    p3["pos"] = [pos[0] + 55, pos[1], pos[2]]
    draw_screw_insert_version_3(thing, **p3)

def draw_nut_cradle_version_3(thing, **kwargs):
    """Load the M3 nut edge first, then pull it up into the closed hex seat."""
    pos = kwargs.get("pos", [0, 0, 0])
    cradle_base_z = 83.75
    cradle_height = 4.6

    # Use the shaft taper for the plain, flush outside face. Trim only the
    # sides and back. The 7.2 mm wide carrier fits the 7.5 mm shaft opening.
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "positive"
    p3["shape"] = "oobb_cylinder"
    p3["depth"] = cradle_height
    p3["r1"] = 5.5 + (cradle_base_z - 64) / 25
    p3["r2"] = 5.5 + (cradle_base_z + cradle_height - 64) / 25
    p3["pos"] = [pos[0], pos[1], pos[2] + cradle_height / 2]
    oobb.append_full(thing, **p3)

    for x in [-8.6, 8.6]:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "negative"
        p3["shape"] = "oobb_cube"
        p3["size"] = [10, 18, 5]
        p3["pos"] = [pos[0] + x, pos[1], pos[2] - 0.2]
        oobb.append_full(thing, **p3)

    p3 = copy.deepcopy(kwargs)
    p3["type"] = "negative"
    p3["shape"] = "oobb_cube"
    p3["size"] = [16, 10, 5]
    p3["pos"] = [pos[0], pos[1] - 9.95, pos[2] - 0.2]
    oobb.append_full(thing, **p3)

    # Keep a 4.4 mm wide tongue from Y=-3.60 to Y=-4.95. Its upper
    # and lower rails straddle the nut loading slot.
    for x in [-5.2, 5.2]:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "negative"
        p3["shape"] = "oobb_cube"
        p3["size"] = [6, 10, 5]
        p3["pos"] = [pos[0] + x, pos[1] - 8.6, pos[2] - 0.2]
        oobb.append_full(thing, **p3)

    # Open the 2.55 mm high loading slot through both flat sides for its
    # entire length, including the nut position. Stop inside the smooth
    # front face so that solid material still joins the two rails.
    slot_back = -5.15
    slot_front = 3.35
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "negative"
    p3["shape"] = "oobb_cube"
    p3["size"] = [7.6, slot_front - slot_back, 2.55]
    p3["pos"] = [pos[0], pos[1] + (slot_front + slot_back) / 2, pos[2] + 0.60]
    oobb.append_full(thing, **p3)

    # Tightening lifts the nut behind the 0.55 mm high retaining step.
    # Six flats resist rotation and the shaft closes the loading end.
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "negative"
    p3["shape"] = "polyg"
    p3["sides"] = 6
    p3["radius"] = 5.70 / math.sqrt(3)
    p3["height"] = 3.12
    p3["rot"] = [0, 0, 30]
    p3["pos"] = [pos[0], pos[1], pos[2] + 0.58]
    oobb.append_full(thing, **p3)

    p3 = copy.deepcopy(kwargs)
    p3["type"] = "negative"
    p3["shape"] = "oobb_cylinder"
    p3["radius"] = 1.7
    p3["depth"] = cradle_height + 0.4
    p3["pos"] = [pos[0], pos[1], pos[2] + cradle_height / 2]
    oobb.append_full(thing, **p3)


def draw_bearing_spacer_version_3(thing, **kwargs):
    pos = kwargs.get("pos", [0, 0, 0])
    # Print the bearing contact face down; flip it to assemble. The
    # 8 mm land supports the inner race, then widens gradually to a
    # 10.5 mm foot. Its underside sits on the flat 8.8 mm handle mouth.
    # The chamfered 8.45 mm spigot points down into that mouth when fitted.
    for bottom, top, lower_radius, upper_radius in [
        (0, 0.22, 4.0, 4.0),
        (0.20, 1.40, 4.0, 5.25),
        (1.38, 2.55, 4.225, 4.225),
        (2.53, 2.90, 4.225, 3.95),
    ]:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "positive"
        p3["shape"] = "oobb_cylinder"
        p3["r1"] = lower_radius
        p3["r2"] = upper_radius
        p3["depth"] = top - bottom
        p3["pos"] = [pos[0], pos[1], pos[2] + (bottom + top) / 2]
        oobb.append_full(thing, **p3)

    p3 = copy.deepcopy(kwargs)
    p3["type"] = "negative"
    p3["shape"] = "oobb_cylinder"
    p3["radius"] = 1.7
    p3["depth"] = 3.3
    p3["pos"] = [pos[0], pos[1], pos[2] + 1.45]
    oobb.append_full(thing, **p3)


def draw_screw_insert_version_3(thing, **kwargs):
    pos = kwargs.get("pos", [0, 0, 0])

    # One top-hat insert carries the whole countersink and bore pilot.
    # Its 5.75 mm stem leaves 0.25 mm below it in the 6 mm bearing.
    # At the base of the 1 mm flange the 90-degree countersink still
    # leaves 0.48 mm of radial wall inside the 5.8 mm diameter stem.
    insert_x = pos[0]
    for bottom, top, radius in [(0, 1.0, 4), (0.98, 6.75, 2.9)]:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "positive"
        p3["shape"] = "oobb_cylinder"
        p3["radius"] = radius
        p3["depth"] = top - bottom
        p3["pos"] = [insert_x, pos[1], pos[2] + (top + bottom) / 2]
        oobb.append_full(thing, **p3)

    for bottom, top, lower_radius, upper_radius in [
        (-0.05, 1.72, 3.47, 1.7),
        (1.70, 6.80, 1.7, 1.7),
    ]:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "negative"
        p3["shape"] = "oobb_cylinder"
        p3["r1"] = lower_radius
        p3["r2"] = upper_radius
        p3["depth"] = top - bottom
        p3["pos"] = [insert_x, pos[1], pos[2] + (bottom + top) / 2]
        oobb.append_full(thing, **p3)



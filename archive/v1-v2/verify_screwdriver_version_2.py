"""Check version 2 print plates, mounting clearances and registered material splits."""
import math
from pathlib import Path

import numpy as np
import trimesh
from shapely.geometry import LineString, Point

PARTS = Path(__file__).resolve().parent / "parts"
PREFIX = "tool_precision_screwdriver_version_2_"


def move(mesh, offset, angle=0):
    result = mesh.copy()
    if angle:
        result.apply_transform(trimesh.transformations.rotation_matrix(math.radians(angle), [1, 0, 0]))
    result.apply_translation(offset)
    return result


def solids(folder, count):
    mesh = trimesh.load_mesh(folder / "3dpr.stl")
    assert mesh.is_volume and mesh.body_count == count, folder.name
    bodies = mesh.split()
    assert len(bodies) == count and all(p.is_volume for p in bodies), folder.name
    assert all(abs(p.bounds[0, 2]) < 0.001 for p in bodies), folder.name
    return sorted(bodies, key=lambda p: p.bounds[0, 0])


def cylinder(radius, bottom, top):
    mesh = trimesh.creation.cylinder(radius=radius, height=top-bottom, sections=100)
    return move(mesh, [0, 0, (bottom+top)/2])


def clear(a, b, label):
    intersection = trimesh.boolean.intersection([a, b], engine="manifold")
    # Contact faces can have zero enclosed volume. Evaluate the signed
    # tetrahedral volumes directly without computing their centres of mass.
    triangles = intersection.triangles
    overlap = abs(np.einsum("ij,ij->", triangles[:, 0],
                            np.cross(triangles[:, 1], triangles[:, 2]))) / 6
    assert overlap < 0.001, f"{label}: {overlap:.6f} mm3 interference"


def compare_printed_copy(packed, reference, offset):
    restored = move(packed, -np.array(offset))
    assert np.allclose(restored.bounds, reference.bounds, atol=0.001)
    for a, b in [(restored, reference), (reference, restored)]:
        assert trimesh.boolean.difference([a, b], engine="manifold").volume < 0.001


def main():
    shuttle, sleeve, insert = solids(PARTS / (PREFIX + "bearing_mount"), 3)
    cradle_reference, sleeve_reference, insert_reference = shuttle, sleeve, insert
    # The tightened shuttle bears against the roof of its transverse channel.
    # Reverse the edge-down print placement for the assembled fit checks.
    shuttle = move(shuttle, [2.3, 0, -3.6])
    shuttle.apply_transform(trimesh.transformations.rotation_matrix(-math.pi/2, [0, 1, 0]))
    shuttle = move(shuttle, [0, 0, 93.75])
    # A gauge spanning both sides must clear from the tongue all the way
    # past the nut axis. The front web keeps the cradle one printable solid.
    slot_gauge = trimesh.creation.box(extents=[7.6, 8.25, 2.53])
    slot_gauge.apply_translation([0, -0.825, 93.75 + 1.875])
    clear(shuttle, slot_gauge, 'full-width loading slot')
    sleeve = move(move(sleeve, [-18, 0, 0]), [0, 0, 102.9], 180)
    insert = move(move(insert, [-32, 0, 0]), [0, 0, 109.9], 180)
    bearing = trimesh.boolean.difference([cylinder(8.5, 102.9, 108.9),
                                          cylinder(3, 102.8, 109.0)], engine="manifold")
    screw = cylinder(1.5, 93.85, 108.05)
    head = trimesh.creation.cone(radius=3.36, height=3.36, sections=80)
    head = move(head, [0, 0, 109.85], 180)
    nut = trimesh.creation.cylinder(radius=5.5/math.sqrt(3), height=2.4, sections=6)
    nut.apply_transform(trimesh.transformations.rotation_matrix(math.pi/6, [0, 0, 1]))
    nut = move(nut, [0, 0, 96.25])
    for name, part in [('sleeve', sleeve), ('insert', insert), ('shuttle', shuttle)]:
        clear(screw, part, 'screw/' + name)
        clear(head, part, 'countersink/' + name)
        clear(nut, part, 'nut/' + name)
        clear(bearing, part, 'bearing/' + name)

    # Test the whole straight nut insertion path into the loose cradle.
    for y in np.linspace(-10, 0, 21):
        clear(shuttle, move(nut, [0, y, -0.65]), 'edge-first entry of hex nut')
    for lift in np.linspace(-0.65, 0, 8):
        clear(shuttle, move(nut, [0, 0, lift]), 'nut lifting into seat')
    for escape in [move(nut, [0, -1, 0]), move(nut, [0, 1, 0])]:
        assert trimesh.boolean.intersection([escape, shuttle], engine="manifold").volume > 0.1
    turned_nut = nut.copy()
    turned_nut.apply_transform(trimesh.transformations.rotation_matrix(math.pi/6, [0, 0, 1]))
    assert trimesh.boolean.intersection([turned_nut, shuttle], engine="manifold").volume > 0.1
    assert np.allclose(cradle_reference.extents[[0, 2]], [4.6, 7.2], atol=0.001)
    # Tighten the hidden M3 into the single insert before pressing on the cap.
    # Driving the head a further 0.1 mm must seat against the countersink.
    seated = trimesh.boolean.intersection([insert, move(head, [0, 0, -0.1])], engine="manifold")
    assert seated.volume > 0.1
    assert np.allclose(insert.bounds[:, 2], [103.15, 109.9], atol=0.001)
    assert abs(insert.bounds[0, 2] - bearing.bounds[0, 2] - 0.25) < 0.001
    # The insert enters 5.75 mm of the 6 mm bore, with the lower spacer
    # located in the handle instead. The two printed parts cannot bottom.
    clear(insert, sleeve, 'insert/spacer')
    assert np.allclose(sleeve.bounds[:, 2], [100, 102.9], atol=0.001)
    for z, radius in [(100.8, 4.225), (101.45, 4.225), (102.8, 4.0)]:
        plane = sleeve.section([0, 0, 1], [0, 0, z])
        measured = max(np.linalg.norm(loop[:, :2], axis=1).max() for loop in plane.discrete)
        assert abs(measured - radius) < 0.005
    assert screw.bounds[0, 2] < nut.bounds[0, 2], "M3 screw must engage the full nut"

    handles = sorted(PARTS.glob(PREFIX + 'precision_screwdriver_*'))
    assert len(handles) == 13
    key_reference = trimesh.load_mesh(PARTS / (PREFIX + 'bit_lock') / '3dpr.stl')
    for folder in handles:
        body, key, packed_cradle, packed_spacer = solids(folder, 4)
        compare_printed_copy(packed_spacer, sleeve_reference, [24, 0, 0])
        # The whole flared annulus is one flat first layer around the
        # bit-loading mouth. A recessed middle or integral lift loses area.
        bed = body.section([0, 0, 1], [0, 0, 0.01])
        rings = sorted(max(np.linalg.norm(loop[:, :2], axis=1)) for loop in bed.discrete)
        assert np.allclose(rings, [4.4, 8.35], atol=0.025), folder.name
        compare_printed_copy(packed_cradle, cradle_reference, [28, 0, 0])
        body = move(body, [0, 0, 101.5], 180)
        key = move(move(key, [-17, 7, -1.5]), [0, 0, 0], 90)
        assert abs(key.volume - key_reference.volume) < 0.001
        assert np.allclose(key.bounds, key_reference.bounds, atol=0.001)
        key.apply_transform(trimesh.transformations.rotation_matrix(math.pi/2, [0, 0, 1]))
        key = move(key, [0, 0, 49])
        for item in [key, shuttle, sleeve, screw, nut]:
            clear(body, item, folder.name)
        # The 8.8 mm round passage reaches the cradle roof, with no hex
        # shelf above it. Sample immediately above the slot and the old step.
        for height in [98.36, 98.68, 98.99, 99.01]:
            plane = body.section([0, 0, 1], [0, 0, height])
            loops = sorted(plane.discrete, key=lambda pts: np.linalg.norm(pts[:, :2], axis=1).max())
            assert len(loops) == 2
            radii = np.linalg.norm(loops[0][:, :2], axis=1)
            assert radii.min() > 4.389 and abs(radii.max() - 4.4) < 0.001, folder.name
        for height, axis, width in [(9, 1, 10), (57, 0, 13)]:
            section = body.section([0, 0, 1], [0, 0, height])
            assert abs(np.ptp(section.vertices[:, axis]) - width) < 0.01, folder.name

    # The curved face continues the shaft's original R5.5..R6.5 taper.
    # Compare mesh sections at multiple heights. The whole exposed arc must follow the shaft.
    assert shuttle.bounds[1, 2] < 99
    for z in [94.0, 95.8, 98.1]:
        points = shuttle.section([0, 0, 1], [0, 0, z]).vertices
        radii = np.linalg.norm(points[:, :2], axis=1)
        shaft_radius = 5.5 + (z - 64) / 35
        assert shaft_radius - 0.015 < max(radii) < shaft_radius + 0.001
        outline = shuttle.section([0, 0, 1], [0, 0, z])
        front = [LineString(loop[:, :2]) for loop in outline.discrete]
        for angle in np.linspace(-30, 30, 25):
            r = math.radians(angle)
            point = Point(shaft_radius * math.sin(r), shaft_radius * math.cos(r))
            assert min(loop.distance(point) for loop in front) < 0.015, "groove in outside face"
    assert abs(body.bounds[1, 2] - 101.5) < 0.001

    # The cylindrical spigot can enter axially and is centred by the
    # existing loading hole. A sideways offset beyond the fit interferes.
    for dz in [1.5, 1.0, 0.5]:
        clear(body, move(sleeve, [0, 0, dz]), 'spacer entering handle mouth')
    for dx, dy in [(0.30, 0), (-0.30, 0), (0, 0.30), (0, -0.30)]:
        wall = trimesh.boolean.intersection([body, move(sleeve, [dx, dy, 0])], engine="manifold")
        assert wall.volume > 0.01
    shoulder = trimesh.boolean.intersection([body, move(sleeve, [0, 0, -0.05])], engine="manifold")
    assert shoulder.volume > 0.5, "lifter must stop at the handle face"

    for y in np.linspace(20, 0, 21):
        clear(body, move(shuttle, [0, y, 0]), 'side entry of loaded cradle')
        clear(body, move(nut, [0, y, 0]), 'side entry of loaded cradle nut')

    # Both rails enter the far wall. Only the nose should meet material
    # on slight overtravel, before the wider shoulders can bottom out.
    assert abs(shuttle.bounds[0, 1] + 4.95) < 0.001
    # Leave 0.02 mm below the roof to isolate the radial stop contact.
    contact = trimesh.boolean.intersection([body, move(shuttle, [0, -0.06, -0.02])], engine="manifold")
    assert contact.volume > 0.30 and contact.bounds[1, 1] < -4.949
    assert contact.bounds[0, 2] < 94 and contact.bounds[1, 2] > 98
    # Confirm an unbroken backing behind the full width of the blind pocket.
    backing = trimesh.creation.box(extents=[4.7, 0.75, 4.60])
    backing.apply_translation([0, -5.335, 96])
    assert trimesh.boolean.difference([backing, body], engine="manifold").volume < 0.001

    coupons = solids(PARTS / (PREFIX + "fit_coupons"), 7)
    assert sorted(round(p.extents[2]) for p in coupons) == [3, 12, 12, 12, 21, 21, 21]
    covers = sorted(PARTS.glob(PREFIX + "label_top_*"))
    assert len(covers) == 24
    for folder in covers:
        base = trimesh.load_mesh(folder / "3dpr_color_main.stl")
        ink = trimesh.load_mesh(folder / "3dpr_color_support.stl")
        mono, mono_sleeve, mono_insert = solids(folder, 3)
        assert base.is_volume and base.body_count == 3
        base, main_sleeve, main_insert = sorted(base.split(), key=lambda part: part.bounds[0, 0])
        for piece in [mono_sleeve, main_sleeve]:
            compare_printed_copy(piece, sleeve_reference, [4, 0, 0])
        for piece in [mono_insert, main_insert]:
            compare_printed_copy(piece, insert_reference, [4, 0, 0])
        assert base.is_volume and ink.is_volume and abs(mono.volume - base.volume) < 0.001
        assert np.allclose(ink.bounds[:, 2], [0, 0.6], atol=0.001)
        clear(base, ink, folder.name + ' material volumes')
        flush = trimesh.boolean.union([base, ink], engine="manifold")
        assert flush.is_volume and flush.body_count == 1, folder.name
        if folder == covers[0]:
            blank_volume = flush.volume
        assert abs(flush.volume - blank_volume) < 0.005, folder.name
        cap = move(flush, [0, 0, 111.6], 180)
        # Solid material remains below the deepest 0.60 mm engraving:
        # every single-colour face must span the screw and the entire relief.
        roof = cylinder(7.48, 110.40, 110.96)
        missing = trimesh.boolean.difference([roof, move(mono, [0, 0, 111.6], 180)], engine="manifold")
        assert missing.volume < 0.001, folder.name + ' open palm face'
        clear(cap, move(insert, [0, 0, 0.40]), 'closed cap/insert clearance')
        # Measure all exported sockets across their polygon flats. Check
        # the straight seat at three heights and the wider lead-in below it.
        for z in [103.1, 106.0, 108.7, 102.5]:
            outline = cap.section([0, 0, 1], [0, 0, z])
            diameters = sorted(2 * LineString(loop[:, :2]).distance(Point(0, 0))
                               for loop in outline.discrete)
            assert len(diameters) == 2, folder.name
            inside, outside = diameters
            if z == 102.5:
                assert inside > 17.4, "lead-in chamfer"
            else:
                assert abs(inside - 17.07) < 0.01, (folder.name, z, inside)
            assert 19.5 < outside <= 20.8
        if folder == covers[0]:
            # Across the rounded edges the diameter grows smoothly to the
            # barrel. Its central section has eighteen distinct scallops.
            for local_height in [0.05, 0.30, 0.60, 0.85, 10.40, 10.65, 10.95, 11.20]:
                plane = flush.section([0, 0, 1], [0, 0, local_height])
                radius = max(np.linalg.norm(loop[:, :2], axis=1).max() for loop in plane.discrete)
                edge_distance = min(local_height, 11.25 - local_height, 0.65)
                rounded = 9.75 + math.sqrt(0.65**2 - (0.65-edge_distance)**2)
                assert abs(radius - rounded) < 0.025
            plane = flush.section([0, 0, 1], [0, 0, 4.0])
            outer_loop = max(plane.discrete, key=lambda p: np.abs(p[:, 0]).max())
            boundary = LineString(outer_loop[:, :2])
            for index in range(36):
                angle = math.radians(index * 10)
                r = 9.8 if index % 2 == 0 else 10.4
                point = Point(r * math.cos(angle), r * math.sin(angle))
                assert boundary.distance(point) < 0.03, "missing flute or ridge"
            assert abs(body.bounds[1, 2] - cap.bounds[0, 2] - 1.15) < 0.001
            assert abs(bearing.bounds[0, 2] - cap.bounds[0, 2] - 2.55) < 0.001
            # The flare tapers from R6.5 to R8.35. This cylinder encloses
            # every angular position of the flare, plus 0.64 mm on all
            # sides. Extend it 0.5 mm above the flare to check axial margin.
            sweep_gauge = cylinder(8.99 / math.cos(math.pi / 100), 99.0, 102.0)
            clear(cap, sweep_gauge, 'continuous skirt clearance')
            for height in [100.36, 100.8, 101.49, 102.0]:
                plane = cap.section([0, 0, 1], [0, 0, height])
                contours = [LineString(loop[:, :2]) for loop in plane.discrete]
                assert len(contours) == 2
                assert abs(min(c.distance(Point(0, 0)) for c in contours) - 9.0) < 0.002

            # At the seating plane the internal annular lip touches only
            # the outer runner. Probe the axial stop below the socket wall.
            gauge = cylinder(8.47, 108.88, 109.00)
            stop = trimesh.boolean.intersection([cap, gauge], engine="manifold")
            assert stop.volume > 4
            radii = np.linalg.norm(stop.vertices[:, :2], axis=1)
            assert radii.min() > 7.47 and radii.max() <= 8.471
            # Load is carried only by the inner-ring shoulders on these parts.
            for seat, offset in [(sleeve, -0.1), (insert, 0.1)]:
                contact = trimesh.boolean.intersection([seat, move(bearing, [0, 0, offset])],
                                                       engine="manifold")
                assert contact.volume > 1 and np.max(np.linalg.norm(contact.vertices[:, :2], axis=1)) < 4.01
            # Check the palm face register and clearance around the 606
            # through a full turn about the fixed sleeve.
            for angle in range(0, 360, 30):
                turned = cap.copy()
                turned.apply_transform(trimesh.transformations.rotation_matrix(math.radians(angle), [0, 0, 1]))
                for fixed in [body, sleeve, insert, head]:
                    clear(turned, fixed, 'rotating label')
        for item in [bearing, sleeve, insert, screw, head, body]:
            clear(cap, item, folder.name + ' installed')
    print("13 handle/key/cradle/spacer plates, 10 and 13 mm flats, three mount pieces, six fit sections and a coupon key,")
    print("24 sheath/sleeve/insert plates and 24 complementary colour pairs passed the geometry checks.")


if __name__ == "__main__":
    main()

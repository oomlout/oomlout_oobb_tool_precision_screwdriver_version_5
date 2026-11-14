# OOBB precision screwdriver

A printable handle for long quarter-inch hex bits, a sliding bit lock and interchangeable labelled top covers. The catalogue includes the archived M3 Ã— 6 mm black countersunk socket screw as purchased hardware.

[Browse version 2 by part family](navigation_oobb/tool_precision_screwdriver/version_2) Â· [Version 1 baseline](navigation_oobb/tool_precision_screwdriver/version_1) Â· [606 assembly, hardware and two-colour printing](VERSION_2_BUILD.md) · [Original prototype plan](VERSION_2_PLAN.md)

| Family | Variants | Selector |
| --- | ---: | --- |
| Precision screwdriver | 13 | Version 2 includes the lock key, nut cradle and bearing-lift spacer. Round bit shaft diameter, 2â€“5 mm in 0.25 mm steps |
| Bit lock | 1 | 7 Ã— 3 Ã— 14 mm slider with an M3 slot |
| Label top | 24 | Version 2 includes the closed bearing cap, self-centring lifter and recessed insert. 10 hex, 9 slotted, 5 Phillips. The size is engraved text, including 0, 00 and 000. |
| Bearing mount | 1 plate in version 2 | Side-loading nut cradle, self-centring lifter and one-piece countersunk insert |
| Fit coupons | 1 plate in version 2 | Three nose sections, three lock sections and a flat key |

## Edit and build

Edit the long drawing routines in [working_scad_version_2.py](working_scad_version_2.py). Each feature begins with its own copy of the drawing arguments and individual `p3` assignments. The version 2 handle calls its own version 2 bit cavity routine. The base drawing and the bit cavity are also available individually as helpers. [Version 1](working_scad_version_1.py) is the migration reference.

Run from this project directory with the OOBB v5, OOMP v5 and Roboclick Python modules on the import path. Full export also uses OpenSCAD on PATH, Pillow and the Liberation Sans Bold font. This migration was rendered using OpenSCAD 2026.04.16.

```powershell
python action_make_scad_no_stl.py
python action_make_scad.py
```

The first action writes SCAD. The second also renders STL meshes and PNG previews. Both run [population](working_oomp_populate.py), wait for [OOMP materialization](working_oomp.py), and then call [working_scad](working_scad.py). Population writes the editable catalogue definitions to `parts_source`. OOMP and SCAD publish into `parts`, and the same outputs appear under `navigation_oobb` grouped by revision, family and size. Individual records carry the archived `legacy_id`. The purchased screw is shared across revisions and has its own [record and drawings](parts/hardware_screw_countersunk_m3_black_6_mm_length_hex_head).

After editing geometry, redraw just one populated variant with its part ID as the filter.

```powershell
python -c "import working_scad; working_scad.main(typ='all', filter='version_2_precision_screwdriver_3_5_mm_diameter_bit_main')"
```

## Migration checks

```powershell
python -m unittest discover -s tests
python verify_screwdriver.py
python verify_screwdriver_version_2.py
```

The version 1 mesh verifier requires trimesh, NumPy, SciPy, Shapely and PyYAML. The default check compares version 1 with all 38 archived STLs. The separate version 2 verifier uses manifold3d to check the bearing assembly, key, spanner lands and both colour volumes.

At migration, all 76 meshes were single watertight solids. Across version 1 and the archive, the largest bounding-coordinate difference was 0.000005 mm and the largest relative volume difference was 0.000266%. Sampled cross-sections through the bit passage, lock, grip, label plug and engraving differed by up to 0.1175 mm in outline. The archived font name was misspelled. Explicit Liberation Sans Bold closely reproduces the engraved area, with a small difference in glyph placement. Corresponding starting SCAD files for versions 1 and 2 were byte-identical. Physical fit is the first bench test in the prototype plan.

The project photographs, Corel drawing, manual project description, configuration and supplier data are available at the project root. The original source, historical exports and legacy build tooling remain in [old_version](old_version).

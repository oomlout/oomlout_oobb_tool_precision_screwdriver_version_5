# Build the precision screwdriver catalogue

The version 3 catalogue has one handle plate per round bit shaft diameter and one cap per drive and size. Purchased hardware has its own record. The retired [catalogues, drawings and source YAMLs](archive/README.md) are outside the active scanners.

## Rebuild

Install the OOBB and OOMP version 5 Python libraries used by this project, OpenSCAD, Blender, and the packages in `requirements-catalogue.txt`. Use `OPENSCAD_EXE` or `BLENDER_EXE` when needed.

```powershell
python catalogue.py build --populate --workers 4
python verify_screwdriver_version_3.py
python -m unittest discover -s tests -q
```

The build runs `working_oomp_populate`, synchronous `working_oomp` source materialisation, and `working_scad`. It exports the production and nominal meshes, a teal five-piece handle 3MF per shaft diameter, registered label STLs and a material-assigned banded 3MF per cap, studio sheets, cap face previews, illustrated assembly instructions, and Markdown navigation. `python working.py` also performs a populated build. Without `--populate`, the source YAMLs and catalogue definition already on disk control the build.

For a single variant, use e.g. `python catalogue.py build --filter version_3_label_top_torx_t5_size`. Use `python catalogue.py render` after exporting meshes independently, `python catalogue.py docs` for Markdown alone, and `python catalogue.py verify` to check navigation, local links, renders, and the manual. Published models live under `parts`, and each printable navigation leaf carries a byte-verified production STL. The shared instructions live under `assembly`.

## Edit the design or instructions

- [Drawing routines](working_scad_version_3.py) use the existing multiline `p3` style. Grip stations and wrench lands are in `draw_handle_body_version_3`. The cap socket uses a 0.07 mm allowance on **diameter**.
- [Populate definitions](working_oomp_populate.py) own the diameters, style–size pairs, project description, source credits, design study, version rows, book style, inventory and numbered assembly sequence. Run with `--populate` after changing these.
- [Colour separations](screwdriver_book/bands.py) use a local copy of the [OOMP Band 5 definitions](source_file/oomp_drive_type_colours.yaml) from `oomp_hardware_color_code/source_files/band_definition_band_5/working.yaml`. The 3MF writer splits the production cap at printable layer heights and preserves the registered face inlay.
- [README generation](screwdriver_book/readmes.py) links every active part to the [communal assembly guide](assembly/README.md). Five operations in populate supply the shared Markdown, the OOBB style-v4 landscape A4 booklet and its offline HTML viewer. The viewer opens on steps 1–4; the next page shows the cap installation. The booklet also includes the finished assembly and hardware inventory. The images use the production cap’s 3MF material assignments. The version README contains the print selector, colour key and design study.
- The studio and face renders reside in the canonical part folders. The shared illustrations, PDF, viewer, hardware inventory and source hashes live under [assembly](assembly/). Hardware codes identify specifications; redirect registration and website publication are separate operations.
- [OOBB README guidelines](https://github.com/oomlout/oomlout_oobb_version_5/blob/main/README_GUIDELINES.md) · [Assembly instructions guide](https://github.com/oomlout/oomlout_oobb_version_5/blob/main/ASSEMBLY_INSTRUCTIONS_GUIDE.md)

## Storage and Git history

The initial refresh was explicitly authorised to replace history after verification.
Verified worktree archives, hash manifests and original Git bundles are retained
outside this checkout under `C:/gh/_repository_recovery/catalogue_refresh_2026-11-14/`.
They preserve old navigation-only material and uncommitted work. Ignored build and
dependency caches are local and excluded from the published tree.

Normal future updates use ordinary commits. Do not reset history on each build.
Any future reset must preserve current files, all relevant refs, dirty/index changes
and remote-only work, then validate the final tree. Create a parentless commit from
that reviewed tree and publish only with an explicit old-remote-SHA lease. Verify an
independent full clone before expiring old local reflogs or collecting objects.
Do not claim GitHub server storage is reclaimed simply because its branch changed.

[Refresh record](MAINTENANCE.md)

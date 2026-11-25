# Precision screwdriver version 2 prototype plan

The bearing-based first prototypes and print files are now available. See the [build and fit guide](VERSION_2_BUILD.md) for the implemented geometry and outstanding bench trials.

## 1. Print the nose and lock before a full handle

The 2 mm shaft version starts at Z = 0. The 3.5 mm and 5 mm versions start at Z = 0.882 and 1.941 mm respectively. The outer taper starts at a 1.25 mm radius for every handle, while the bore is the shaft radius plus 0.125 mm. As the shaft gets larger the bore consumes the end of the taper. The 2 mm handle itself starts with only 0.125 mm of nominal wall. A watertight STL can still have a tip the slicer cannot lay down.

Print short nose sections for 2, 3.5 and 5 mm shafts. Compare the existing taper with a nose radius calculated from shaft radius, radial clearance and a separate minimum wall. For a 0.45 mm extrusion width, try 0.90 mm of wall as the first candidate. Inspect the first layers in the slicer and keep the narrowest candidate that shows two continuous perimeter paths, admits the measured bit by hand and reaches the intended recessed screw. Prusa documents how extrusion width limits thin walls and how orientation and material affect mating clearances. [Prusa design guidance](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135)

Print a second short section through the quarter-inch shank seat and transverse M3 lock. Keep the baseline slider at 7 × 3 × 14 mm. Compare its existing 0.50 mm total pocket allowance with 0.30 and 0.70 mm, changing this dimension independently of bit clearance. Use the same bit, M3 × 6 mm fastener, nut, filament and orientation for each comparison. Record whether the screw seats, the slider releases by hand, and the bit develops lash or witness-mark movement under the same applied load. Repeat after 30 lock/release cycles. Retain a candidate only if it improves assembly or play and holds at least as well as the baseline on the same bench test.

## 2. Try a rotating labelled cap on one handle

The current label has a 6 mm hex plug. The plug keys it to the handle, so fingers turning the shaft also turn the surface beneath the palm. Keep that plug as a fixed carrier and prototype a separate, captive labelled disc on a short journal. That preserves the existing drive and lets the palm maintain axial pressure while the fingertips turn the shaft. Commercial precision drivers use a free-turning cap for this purpose. [Wiha PicoFinish](https://wiha.com/tools/screwdrivers/precision-screwdrivers/picofinish/sets/fine-screwdriver-set-picofinish/42996)

Start with the 3.5 mm handle and one label. Compare the fixed cap and two journal clearances on the same run of ten small screws. Record time, regrips, cap binding and accidental separation. Choose the rotating design only if it lowers regrips or completion time and stays captured through 100 loaded hand turns. A removable plug must still allow bit and lock servicing.

## 3. Test grip and label recognition separately

The handle already has an 11 mm main shaft, a central hex and a grooved top. Leave those dimensions in the cap trial. Then compare one smooth fingertip band against one shallow-fluted band on otherwise identical handles. Wera describes separate fast-turning, precision and torque zones on its Micro drivers. The experiment here is to find which existing surface the user actually holds for each task. Mark finger contact positions and count regrips on the same screw-starting and final-tightening tasks. Keep the current central hex if the alternative offers no measurable benefit. [Wera Kraftform Micro catalogue](https://www-de.wera.de/fileadmin/pdf/catalog-toolrebels/EN-Tools-for-Rebels-2023.pdf)

Print a small label set containing PH0, PH00, PH000, hex 0.7 and slotted 0.8. Compare the existing symbol-and-size layout with a wider zero string and a more prominent decimal point. Shuffle the labels in a tray, ask for each size twice, and log wrong picks and selection time under ordinary bench lighting. Keep a layout that produces ten correct picks and survives the slicer preview at the chosen nozzle size.

## 4. Promote the winners through the catalogue

Keep each trial confined to version 2. Record the printer, nozzle, extrusion width, layer height, material, orientation, measured bit, CAD revision and measurements alongside the chosen sample. Run one assembled handle at each diameter extreme and at 3.5 mm before regenerating all 13 handles and 24 labels. Check the meshes and taxonomy again, then repeat the version 1 archive check. The proposed cycle counts and acceptance criteria above are project test targets. Physical testing is still to come.

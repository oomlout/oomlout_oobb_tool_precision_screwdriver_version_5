$fn = 50;

difference() {
	union() {
		translate(v = [-2.85, -3.5, 0.6]) {
			rotate(a = [180, 0, 0]) {
				linear_extrude(height = 0.6) {
					text(font = "Liberation Sans:style=Bold", halign = "center", size = 4.0, text = "2", valign = "center");
				}
			}
		}
		translate(v = [0.0, -2.2, 0.0]) {
			cylinder(h = 0.6, r = 0.55);
		}
		translate(v = [2.85, -3.5, 0.6]) {
			rotate(a = [180, 0, 0]) {
				linear_extrude(height = 0.6) {
					text(font = "Liberation Sans:style=Bold", halign = "center", size = 4.0, text = "5", valign = "center");
				}
			}
		}
		translate(v = [-3.0, 1.25, 0]) {
			cube(size = [6, 1.5, 0.6]);
		}
	}
	union();
}

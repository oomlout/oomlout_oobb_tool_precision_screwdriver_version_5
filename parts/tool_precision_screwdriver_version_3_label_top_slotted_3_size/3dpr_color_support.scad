$fn = 50;

difference() {
	union() {
		translate(v = [0.0, -4.0, 0.6]) {
			rotate(a = [180, 0, 0]) {
				linear_extrude(height = 0.6) {
					text(font = "Liberation Sans:style=Bold", halign = "center", size = 4.5, text = "3", valign = "center");
				}
			}
		}
		translate(v = [-3.0, 1.25, 0]) {
			cube(size = [6, 1.5, 0.6]);
		}
	}
	union();
}

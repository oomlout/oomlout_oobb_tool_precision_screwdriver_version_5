$fn = 50;

difference() {
	union() {
		translate(v = [-3.65, -3.5, 0.6]) {
			rotate(a = [180, 0, 0]) {
				linear_extrude(height = 0.6) {
					text(font = "Liberation Sans:style=Bold", halign = "center", size = 4.0, text = "0", valign = "center");
				}
			}
		}
		translate(v = [0.0, -3.5, 0.6]) {
			rotate(a = [180, 0, 0]) {
				linear_extrude(height = 0.6) {
					text(font = "Liberation Sans:style=Bold", halign = "center", size = 4.0, text = "0", valign = "center");
				}
			}
		}
		translate(v = [3.65, -3.5, 0.6]) {
			rotate(a = [180, 0, 0]) {
				linear_extrude(height = 0.6) {
					text(font = "Liberation Sans:style=Bold", halign = "center", size = 4.0, text = "0", valign = "center");
				}
			}
		}
		translate(v = [-3.0, 2.25, 0]) {
			cube(size = [6, 1.5, 0.6]);
		}
		translate(v = [-0.75, 0.0, 0]) {
			cube(size = [1.5, 6, 0.6]);
		}
	}
	union();
}

$fn = 50;

difference() {
	union() {
		translate(v = [0.0, -4.0, 0.6]) {
			rotate(a = [180, 0, 0]) {
				linear_extrude(height = 0.6) {
					text(font = "Liberation Sans:style=Bold", halign = "center", size = 4.5, text = "4", valign = "center");
				}
			}
		}
		translate(v = [0, 3, 0]) {
			linear_extrude(height = 0.6) {
				polygon(points = [[3.0, 0.0], [1.5000000000000004, 2.598076211353316], [-1.4999999999999993, 2.598076211353316], [-3.0, 3.6739403974420594e-16], [-1.5000000000000013, -2.5980762113533156], [1.499999999999998, -2.598076211353317]]);
			}
		}
	}
	union();
}

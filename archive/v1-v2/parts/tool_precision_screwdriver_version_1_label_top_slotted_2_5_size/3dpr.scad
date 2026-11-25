$fn = 50;

difference() {
	union() {
		difference() {
			union() {
				cylinder(h = 1.5, r = 6.5);
				rotate_extrude(angle = 360) {
					translate(v = [6.5, 0, 0]) {
						circle(r = 1.5);
					}
				}
			}
			union() {
				translate(v = [-25.0, -25.0, -50]) {
					cube(size = [50, 50, 50]);
				}
				#translate(v = [-3.0, -2.75, 0.5]) {
					cube(size = [6, 1.5, 1]);
				}
				#translate(v = [0, 3.5, 0.5]) {
					linear_extrude(height = 1) {
						text(font = "Liberation Sans:style=Bold", halign = "center", size = 4, text = "2.5", valign = "center");
					}
				}
			}
		}
		union() {
			translate(v = [0, 0, -6]) {
				linear_extrude(height = 6) {
					polygon(points = [[3.8658550000000003, 0.0], [1.9329275000000006, 3.347928637347091], [-1.9329274999999992, 3.3479286373470916], [-3.8658550000000003, 4.734306951717792e-16], [-1.932927500000002, -3.3479286373470907], [1.9329274999999975, -3.347928637347093]]);
				}
			}
		}
	}
	union() {
		#translate(v = [0, 0, -6]) {
			#rotate_extrude(angle = 360) {
				translate(v = [4.5, 0, 0]) {
					circle(r = 1.5);
				}
			}
		}
	}
}

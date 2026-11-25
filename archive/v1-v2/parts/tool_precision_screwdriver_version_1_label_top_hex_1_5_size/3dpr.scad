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
				#translate(v = [0, -3, 0.5]) {
					#linear_extrude(height = 1) {
						polygon(points = [[3.0, 0.0], [1.5000000000000004, 2.598076211353316], [-1.4999999999999993, 2.598076211353316], [-3.0, 3.6739403974420594e-16], [-1.5000000000000013, -2.5980762113533156], [1.499999999999998, -2.598076211353317]]);
					}
				}
				#translate(v = [0, 3.5, 0.5]) {
					linear_extrude(height = 1) {
						text(font = "Liberation Sans:style=Bold", halign = "center", size = 4, text = "1.5", valign = "center");
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

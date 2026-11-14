$fn = 50;

difference() {
	union() {
		translate(v = [-3.5, -1.5, 0]) {
			cube(size = [7, 3, 14]);
		}
	}
	union() {
		translate(v = [0, -1.5, 9.0]) {
			rotate(a = [0, 90, 90]) {
				hull() {
					difference() {
						union() {
							translate(v = [-2.5, 0, 0]) {
								cylinder(h = 3, r = 1.8);
							}
							translate(v = [2.5, 0, 0]) {
								cylinder(h = 3, r = 1.8);
							}
						}
						union();
					}
				}
			}
		}
	}
}

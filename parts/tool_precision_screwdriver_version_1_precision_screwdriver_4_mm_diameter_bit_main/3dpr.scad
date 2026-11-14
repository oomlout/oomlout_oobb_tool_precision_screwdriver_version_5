$fn = 50;

difference() {
	union() {
		cylinder(h = 6, r1 = 1.25, r2 = 5.5);
		translate(v = [0, 0, 6]) {
			linear_extrude(height = 6) {
				polygon(points = [[5.7735, 0.0], [2.8867500000000006, 4.999997668749456], [-2.886749999999999, 4.999997668749457], [-5.7735, 7.070498294877244e-16], [-2.886750000000003, -4.999997668749456], [2.886749999999996, -4.999997668749459]]);
			}
		}
		translate(v = [0, 0, 12.0]) {
			cylinder(h = 40, r = 5.5);
		}
		translate(v = [0, 0, 52]) {
			rotate(a = [0, 0, 30.0]) {
				linear_extrude(height = 12) {
					polygon(points = [[7.50555, 0.0], [3.752775000000001, 6.499996969374293], [-3.7527749999999984, 6.499996969374294], [-7.50555, 9.191647783340418e-16], [-3.7527750000000037, -6.499996969374292], [3.7527749999999953, -6.499996969374297]]);
				}
			}
		}
		translate(v = [0, 0, 64.0]) {
			cylinder(h = 35, r1 = 5.5, r2 = 6.5);
		}
		translate(v = [0, 0, 101.5]) {
			cylinder(h = 6.5, r = 6.5);
		}
		translate(v = [0, 0, 101.5]) {
			cylinder(h = 4.0, r = 9.0);
		}
		#translate(v = [0, 0, 105.5]) {
			#rotate_extrude(angle = 360) {
				translate(v = [6.5, 0, 0]) {
					circle(r = 2.5);
				}
			}
		}
		#translate(v = [0, 0, 101.5]) {
			#rotate_extrude(angle = 360) {
				translate(v = [7.75, 0, 0]) {
					circle(r = 1.25);
				}
			}
		}
		translate(v = [0, 0, 99.0]) {
			cylinder(h = 3.75, r = 7.75);
		}
	}
	union() {
		translate(v = [0, 0, 25]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0.1, 0, 0]) {
							linear_extrude(height = 228.2) {
								polygon(points = [[3.8658550000000003, 0.0], [1.9329275000000006, 3.347928637347091], [-1.9329274999999992, 3.3479286373470916], [-3.8658550000000003, 4.734306951717792e-16], [-1.932927500000002, -3.3479286373470907], [1.9329274999999975, -3.347928637347093]]);
							}
						}
						#translate(v = [0, 0, -71.8]) {
							cylinder(h = 100, r = 2.125);
						}
					}
					union() {
						difference() {
							cylinder(h = 2, r1 = 10.0, r2 = 11.775);
							cylinder(h = 2, r1 = 2.0, r2 = 3.775);
						}
					}
				}
			}
		}
		translate(v = [6.5, 0, 58.0]) {
			rotate(a = [0, 90, 360.0]) {
				difference() {
					union() {
						translate(v = [0, 0, -5.5]) {
							rotate(a = [0, 0, 0]) {
								difference() {
									union() {
										translate(v = [-1.75, -3.25, -250.3]) {
											cube(size = [3.5, 6.5, 0.3]);
										}
										translate(v = [-1.75, -1.75, -250.60000000000002]) {
											cube(size = [3.5, 3.5, 0.3]);
										}
										translate(v = [-1.75, -3.25, 0]) {
											cube(size = [3.5, 6.5, 0.3]);
										}
										translate(v = [-1.75, -1.75, 0.3]) {
											cube(size = [3.5, 3.5, 0.3]);
										}
										translate(v = [0, 0, -250]) {
											linear_extrude(height = 250) {
												polygon(points = [[3.2619999999999996, 0.0], [1.6310000000000002, 2.8249748671448383], [-1.6309999999999991, 2.8249748671448387], [-3.2619999999999996, 3.9947978588186655e-16], [-1.6310000000000013, -2.824974867144838], [1.6309999999999976, -2.8249748671448396]]);
											}
										}
										translate(v = [-1.75, -3.25, -250.3]) {
											cube(size = [3.5, 6.5, 0.3]);
										}
										translate(v = [-1.75, -1.75, -250.60000000000002]) {
											cube(size = [3.5, 3.5, 0.3]);
										}
										translate(v = [-1.75, -3.25, 0]) {
											cube(size = [3.5, 6.5, 0.3]);
										}
										translate(v = [-1.75, -1.75, 0.3]) {
											cube(size = [3.5, 3.5, 0.3]);
										}
										translate(v = [-1.75, -3.25, -250.3]) {
											cube(size = [3.5, 6.5, 0.3]);
										}
										translate(v = [-1.75, -1.75, -250.60000000000002]) {
											cube(size = [3.5, 3.5, 0.3]);
										}
										translate(v = [-1.75, -3.25, 0]) {
											cube(size = [3.5, 6.5, 0.3]);
										}
										translate(v = [-1.75, -1.75, 0.3]) {
											cube(size = [3.5, 3.5, 0.3]);
										}
									}
									union();
								}
							}
						}
						translate(v = [0, 0, -5.0]) {
							rotate(a = [0, 0, 0]) {
								difference() {
									union() {
										translate(v = [-1.75, -3.25, -250.3]) {
											cube(size = [3.5, 6.5, 0.3]);
										}
										translate(v = [-1.75, -1.75, -250.60000000000002]) {
											cube(size = [3.5, 3.5, 0.3]);
										}
										translate(v = [-1.75, -3.25, 0]) {
											cube(size = [3.5, 6.5, 0.3]);
										}
										translate(v = [-1.75, -1.75, 0.3]) {
											cube(size = [3.5, 3.5, 0.3]);
										}
										translate(v = [0, 0, -250]) {
											linear_extrude(height = 250) {
												polygon(points = [[3.2619999999999996, 0.0], [1.6310000000000002, 2.8249748671448383], [-1.6309999999999991, 2.8249748671448387], [-3.2619999999999996, 3.9947978588186655e-16], [-1.6310000000000013, -2.824974867144838], [1.6309999999999976, -2.8249748671448396]]);
											}
										}
										translate(v = [-1.75, -3.25, -250.3]) {
											cube(size = [3.5, 6.5, 0.3]);
										}
										translate(v = [-1.75, -1.75, -250.60000000000002]) {
											cube(size = [3.5, 3.5, 0.3]);
										}
										translate(v = [-1.75, -3.25, 0]) {
											cube(size = [3.5, 6.5, 0.3]);
										}
										translate(v = [-1.75, -1.75, 0.3]) {
											cube(size = [3.5, 3.5, 0.3]);
										}
										translate(v = [-1.75, -3.25, -250.3]) {
											cube(size = [3.5, 6.5, 0.3]);
										}
										translate(v = [-1.75, -1.75, -250.60000000000002]) {
											cube(size = [3.5, 3.5, 0.3]);
										}
										translate(v = [-1.75, -3.25, 0]) {
											cube(size = [3.5, 6.5, 0.3]);
										}
										translate(v = [-1.75, -1.75, 0.3]) {
											cube(size = [3.5, 3.5, 0.3]);
										}
									}
									union();
								}
							}
						}
						translate(v = [0, 0, -5.5]) {
							rotate(a = [0, 0, 0]) {
								difference() {
									union() {
										translate(v = [-1.75, -3.25, -250.3]) {
											cube(size = [3.5, 6.5, 0.3]);
										}
										translate(v = [-1.75, -1.75, -250.60000000000002]) {
											cube(size = [3.5, 3.5, 0.3]);
										}
										translate(v = [-1.75, -3.25, 0]) {
											cube(size = [3.5, 6.5, 0.3]);
										}
										translate(v = [-1.75, -1.75, 0.3]) {
											cube(size = [3.5, 3.5, 0.3]);
										}
										translate(v = [0, 0, -250]) {
											linear_extrude(height = 250) {
												polygon(points = [[3.2619999999999996, 0.0], [1.6310000000000002, 2.8249748671448383], [-1.6309999999999991, 2.8249748671448387], [-3.2619999999999996, 3.9947978588186655e-16], [-1.6310000000000013, -2.824974867144838], [1.6309999999999976, -2.8249748671448396]]);
											}
										}
										translate(v = [-1.75, -3.25, -250.3]) {
											cube(size = [3.5, 6.5, 0.3]);
										}
										translate(v = [-1.75, -1.75, -250.60000000000002]) {
											cube(size = [3.5, 3.5, 0.3]);
										}
										translate(v = [-1.75, -3.25, 0]) {
											cube(size = [3.5, 6.5, 0.3]);
										}
										translate(v = [-1.75, -1.75, 0.3]) {
											cube(size = [3.5, 3.5, 0.3]);
										}
										translate(v = [-1.75, -3.25, -250.3]) {
											cube(size = [3.5, 6.5, 0.3]);
										}
										translate(v = [-1.75, -1.75, -250.60000000000002]) {
											cube(size = [3.5, 3.5, 0.3]);
										}
										translate(v = [-1.75, -3.25, 0]) {
											cube(size = [3.5, 6.5, 0.3]);
										}
										translate(v = [-1.75, -1.75, 0.3]) {
											cube(size = [3.5, 3.5, 0.3]);
										}
									}
									union();
								}
							}
						}
						translate(v = [0, 0, -8.0]) {
							cylinder(h = 8, r = 1.5);
						}
						translate(v = [0, 0, -1.9]) {
							cylinder(h = 1.9, r1 = 1.8, r2 = 3.6);
						}
						cylinder(h = 250, r = 3.6);
						translate(v = [0, 0, -8.0]) {
							cylinder(h = 8, r = 1.8);
						}
						translate(v = [0, 0, -8.0]) {
							cylinder(h = 8, r = 1.5);
						}
					}
					union();
				}
			}
		}
		translate(v = [0, 0, 6]) {
			rotate_extrude(angle = 360) {
				translate(v = [11.25, 0, 0]) {
					circle(r = 6.25);
				}
			}
		}
		translate(v = [0, 0, 12]) {
			rotate_extrude(angle = 360) {
				translate(v = [11.25, 0, 0]) {
					circle(r = 6.25);
				}
			}
		}
		translate(v = [0, 0, 52]) {
			rotate_extrude(angle = 360) {
				translate(v = [8.0, 0, 0]) {
					circle(r = 2.5);
				}
			}
		}
		translate(v = [0, 0, 64]) {
			rotate_extrude(angle = 360) {
				translate(v = [8.0, 0, 0]) {
					circle(r = 2.5);
				}
			}
		}
		translate(v = [0, 0, 99]) {
			rotate_extrude(angle = 360) {
				translate(v = [7.75, 0, 0]) {
					circle(r = 1.25);
				}
			}
		}
		rotate(a = [0, 0, 0.0]) {
			translate(v = [9.7, 0, 0]) {
				translate(v = [-0.5, -0.5, 99.0]) {
					rotate(a = [0, 0, 45]) {
						cube(size = [1, 1, 9]);
					}
				}
			}
		}
		rotate(a = [0, 0, 10.0]) {
			translate(v = [9.7, 0, 0]) {
				translate(v = [-0.5, -0.5, 99.0]) {
					rotate(a = [0, 0, 45]) {
						cube(size = [1, 1, 9]);
					}
				}
			}
		}
		rotate(a = [0, 0, 20.0]) {
			translate(v = [9.7, 0, 0]) {
				translate(v = [-0.5, -0.5, 99.0]) {
					rotate(a = [0, 0, 45]) {
						cube(size = [1, 1, 9]);
					}
				}
			}
		}
		rotate(a = [0, 0, 30.0]) {
			translate(v = [9.7, 0, 0]) {
				translate(v = [-0.5, -0.5, 99.0]) {
					rotate(a = [0, 0, 45]) {
						cube(size = [1, 1, 9]);
					}
				}
			}
		}
		rotate(a = [0, 0, 40.0]) {
			translate(v = [9.7, 0, 0]) {
				translate(v = [-0.5, -0.5, 99.0]) {
					rotate(a = [0, 0, 45]) {
						cube(size = [1, 1, 9]);
					}
				}
			}
		}
		rotate(a = [0, 0, 50.0]) {
			translate(v = [9.7, 0, 0]) {
				translate(v = [-0.5, -0.5, 99.0]) {
					rotate(a = [0, 0, 45]) {
						cube(size = [1, 1, 9]);
					}
				}
			}
		}
		rotate(a = [0, 0, 60.0]) {
			translate(v = [9.7, 0, 0]) {
				translate(v = [-0.5, -0.5, 99.0]) {
					rotate(a = [0, 0, 45]) {
						cube(size = [1, 1, 9]);
					}
				}
			}
		}
		rotate(a = [0, 0, 70.0]) {
			translate(v = [9.7, 0, 0]) {
				translate(v = [-0.5, -0.5, 99.0]) {
					rotate(a = [0, 0, 45]) {
						cube(size = [1, 1, 9]);
					}
				}
			}
		}
		rotate(a = [0, 0, 80.0]) {
			translate(v = [9.7, 0, 0]) {
				translate(v = [-0.5, -0.5, 99.0]) {
					rotate(a = [0, 0, 45]) {
						cube(size = [1, 1, 9]);
					}
				}
			}
		}
		rotate(a = [0, 0, 90.0]) {
			translate(v = [9.7, 0, 0]) {
				translate(v = [-0.5, -0.5, 99.0]) {
					rotate(a = [0, 0, 45]) {
						cube(size = [1, 1, 9]);
					}
				}
			}
		}
		rotate(a = [0, 0, 100.0]) {
			translate(v = [9.7, 0, 0]) {
				translate(v = [-0.5, -0.5, 99.0]) {
					rotate(a = [0, 0, 45]) {
						cube(size = [1, 1, 9]);
					}
				}
			}
		}
		rotate(a = [0, 0, 110.0]) {
			translate(v = [9.7, 0, 0]) {
				translate(v = [-0.5, -0.5, 99.0]) {
					rotate(a = [0, 0, 45]) {
						cube(size = [1, 1, 9]);
					}
				}
			}
		}
		rotate(a = [0, 0, 120.0]) {
			translate(v = [9.7, 0, 0]) {
				translate(v = [-0.5, -0.5, 99.0]) {
					rotate(a = [0, 0, 45]) {
						cube(size = [1, 1, 9]);
					}
				}
			}
		}
		rotate(a = [0, 0, 130.0]) {
			translate(v = [9.7, 0, 0]) {
				translate(v = [-0.5, -0.5, 99.0]) {
					rotate(a = [0, 0, 45]) {
						cube(size = [1, 1, 9]);
					}
				}
			}
		}
		rotate(a = [0, 0, 140.0]) {
			translate(v = [9.7, 0, 0]) {
				translate(v = [-0.5, -0.5, 99.0]) {
					rotate(a = [0, 0, 45]) {
						cube(size = [1, 1, 9]);
					}
				}
			}
		}
		rotate(a = [0, 0, 150.0]) {
			translate(v = [9.7, 0, 0]) {
				translate(v = [-0.5, -0.5, 99.0]) {
					rotate(a = [0, 0, 45]) {
						cube(size = [1, 1, 9]);
					}
				}
			}
		}
		rotate(a = [0, 0, 160.0]) {
			translate(v = [9.7, 0, 0]) {
				translate(v = [-0.5, -0.5, 99.0]) {
					rotate(a = [0, 0, 45]) {
						cube(size = [1, 1, 9]);
					}
				}
			}
		}
		rotate(a = [0, 0, 170.0]) {
			translate(v = [9.7, 0, 0]) {
				translate(v = [-0.5, -0.5, 99.0]) {
					rotate(a = [0, 0, 45]) {
						cube(size = [1, 1, 9]);
					}
				}
			}
		}
		rotate(a = [0, 0, 180.0]) {
			translate(v = [9.7, 0, 0]) {
				translate(v = [-0.5, -0.5, 99.0]) {
					rotate(a = [0, 0, 45]) {
						cube(size = [1, 1, 9]);
					}
				}
			}
		}
		rotate(a = [0, 0, 190.0]) {
			translate(v = [9.7, 0, 0]) {
				translate(v = [-0.5, -0.5, 99.0]) {
					rotate(a = [0, 0, 45]) {
						cube(size = [1, 1, 9]);
					}
				}
			}
		}
		rotate(a = [0, 0, 200.0]) {
			translate(v = [9.7, 0, 0]) {
				translate(v = [-0.5, -0.5, 99.0]) {
					rotate(a = [0, 0, 45]) {
						cube(size = [1, 1, 9]);
					}
				}
			}
		}
		rotate(a = [0, 0, 210.0]) {
			translate(v = [9.7, 0, 0]) {
				translate(v = [-0.5, -0.5, 99.0]) {
					rotate(a = [0, 0, 45]) {
						cube(size = [1, 1, 9]);
					}
				}
			}
		}
		rotate(a = [0, 0, 220.0]) {
			translate(v = [9.7, 0, 0]) {
				translate(v = [-0.5, -0.5, 99.0]) {
					rotate(a = [0, 0, 45]) {
						cube(size = [1, 1, 9]);
					}
				}
			}
		}
		rotate(a = [0, 0, 230.0]) {
			translate(v = [9.7, 0, 0]) {
				translate(v = [-0.5, -0.5, 99.0]) {
					rotate(a = [0, 0, 45]) {
						cube(size = [1, 1, 9]);
					}
				}
			}
		}
		rotate(a = [0, 0, 240.0]) {
			translate(v = [9.7, 0, 0]) {
				translate(v = [-0.5, -0.5, 99.0]) {
					rotate(a = [0, 0, 45]) {
						cube(size = [1, 1, 9]);
					}
				}
			}
		}
		rotate(a = [0, 0, 250.0]) {
			translate(v = [9.7, 0, 0]) {
				translate(v = [-0.5, -0.5, 99.0]) {
					rotate(a = [0, 0, 45]) {
						cube(size = [1, 1, 9]);
					}
				}
			}
		}
		rotate(a = [0, 0, 260.0]) {
			translate(v = [9.7, 0, 0]) {
				translate(v = [-0.5, -0.5, 99.0]) {
					rotate(a = [0, 0, 45]) {
						cube(size = [1, 1, 9]);
					}
				}
			}
		}
		rotate(a = [0, 0, 270.0]) {
			translate(v = [9.7, 0, 0]) {
				translate(v = [-0.5, -0.5, 99.0]) {
					rotate(a = [0, 0, 45]) {
						cube(size = [1, 1, 9]);
					}
				}
			}
		}
		rotate(a = [0, 0, 280.0]) {
			translate(v = [9.7, 0, 0]) {
				translate(v = [-0.5, -0.5, 99.0]) {
					rotate(a = [0, 0, 45]) {
						cube(size = [1, 1, 9]);
					}
				}
			}
		}
		rotate(a = [0, 0, 290.0]) {
			translate(v = [9.7, 0, 0]) {
				translate(v = [-0.5, -0.5, 99.0]) {
					rotate(a = [0, 0, 45]) {
						cube(size = [1, 1, 9]);
					}
				}
			}
		}
		rotate(a = [0, 0, 300.0]) {
			translate(v = [9.7, 0, 0]) {
				translate(v = [-0.5, -0.5, 99.0]) {
					rotate(a = [0, 0, 45]) {
						cube(size = [1, 1, 9]);
					}
				}
			}
		}
		rotate(a = [0, 0, 310.0]) {
			translate(v = [9.7, 0, 0]) {
				translate(v = [-0.5, -0.5, 99.0]) {
					rotate(a = [0, 0, 45]) {
						cube(size = [1, 1, 9]);
					}
				}
			}
		}
		rotate(a = [0, 0, 320.0]) {
			translate(v = [9.7, 0, 0]) {
				translate(v = [-0.5, -0.5, 99.0]) {
					rotate(a = [0, 0, 45]) {
						cube(size = [1, 1, 9]);
					}
				}
			}
		}
		rotate(a = [0, 0, 330.0]) {
			translate(v = [9.7, 0, 0]) {
				translate(v = [-0.5, -0.5, 99.0]) {
					rotate(a = [0, 0, 45]) {
						cube(size = [1, 1, 9]);
					}
				}
			}
		}
		rotate(a = [0, 0, 340.0]) {
			translate(v = [9.7, 0, 0]) {
				translate(v = [-0.5, -0.5, 99.0]) {
					rotate(a = [0, 0, 45]) {
						cube(size = [1, 1, 9]);
					}
				}
			}
		}
		rotate(a = [0, 0, 350.0]) {
			translate(v = [9.7, 0, 0]) {
				translate(v = [-0.5, -0.5, 99.0]) {
					rotate(a = [0, 0, 45]) {
						cube(size = [1, 1, 9]);
					}
				}
			}
		}
		translate(v = [-1.75, -3.75, 48.0]) {
			cube(size = [3.5, 7.5, 72.0]);
		}
	}
}

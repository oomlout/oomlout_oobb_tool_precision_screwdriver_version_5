/* 606 palm cap assembly, version 2. Set exploded to 0 for installed positions.
   Dimensions are mm. The grey bearing and screws are bought-in envelopes.
   Enable section to see both races, the M3 seat and the captive nut shuttle. */
exploded = 0;
section = false;
show_full_handle = false;
$fn = 80;

handle_file = "parts/tool_precision_screwdriver_version_2_precision_screwdriver_3_5_mm_diameter_bit_main/3dpr.stl";
mount_file = "parts/tool_precision_screwdriver_version_2_bearing_mount/3dpr.stl";
label_folder = "parts/tool_precision_screwdriver_version_2_label_top_phillips_000_size/";

module show_section() {
    if (section) render() difference() {
        children();
        translate([0,-50,-5]) cube([50,100,250]);
    } else children();
}

module handle() {
    render() intersection() {
        translate([0,0,101.5]) rotate([180,0,0]) import(handle_file);
        translate([-11,-11,show_full_handle ? -1 : 82]) cube([22,22,120]);
    }
}

module mount_piece(x, width) {
    render() intersection() {
        translate([-x,0,0]) import(mount_file);
        translate([-width/2,-10,-1]) cube([width,23,13]);
    }
}

module ring(outer, inner, height) {
    render() difference() {
        cylinder(d=outer,h=height);
        translate([0,0,-0.1]) cylinder(d=inner,h=height+0.2);
    }
}

// In the installed position the nut slides into the short end of the shuttle.
color("#52848a") show_section() handle();
color("#f4b056") show_section() translate([0,exploded*14,93.75])
    rotate([0,-90,0]) translate([2.3,0,-3.6]) mount_piece(0,12.2);
color("#999fa6") show_section() translate([0,exploded*6,95.05-exploded*0.65]) rotate([0,0,30])
    difference() {
        cylinder(r=5.5/sqrt(3),h=2.4,$fn=6);
        translate([0,0,-0.1]) cylinder(d=2.6,h=2.6);
    }
color("#e8ab55") show_section() translate([0,0,102.9+exploded*7]) rotate([180,0,0]) mount_piece(18,14.2);
color("#999fa6") show_section() translate([0,0,102.9+exploded*18]) ring(17,14.7,6);
color("#384356") show_section() translate([0,0,103.15+exploded*18]) ring(14.7,8.2,5.5);
color("#bfc5c8") show_section() translate([0,0,102.9+exploded*18]) ring(8.2,6,6);
color("#f2e4ce") show_section() translate([0,0,111.6+exploded*72]) rotate([180,0,0])
    render() intersection() {
        import(str(label_folder,"3dpr_color_main.stl"));
        translate([-12,-12,-1]) cube([24,24,11]);
    }
color("#35335e") show_section() translate([0,0,111.6+exploded*72]) rotate([180,0,0])
    import(str(label_folder,"3dpr_color_support.stl"));
color("#e8ab55") show_section() translate([0,0,109.9+exploded*30]) rotate([180,0,0])
    mount_piece(32,8.2);
color("#666e76") show_section() translate([0,0,93.85+exploded*51]) union() {
    cylinder(d=3,h=14.2);
    translate([0,0,14.2]) difference() {
        cylinder(d1=3.12,d2=6.72,h=1.8);
        translate([0,0,0.5]) cylinder(r=2/sqrt(3),h=1.4,$fn=6);
    }
}

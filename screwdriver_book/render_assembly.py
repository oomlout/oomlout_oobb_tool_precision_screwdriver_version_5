"""Blender worker for the views defined by the screwdriver assembly sequence."""
import json
import math
from pathlib import Path
import sys

import bpy
from mathutils import Quaternion, Vector

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "presentation" / "scripts"))
from render_catalogue import aim, material, import_banded_cap

job = json.loads(Path(sys.argv[-1]).read_text())
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.samples = 12
scene.cycles.use_denoising = True
scene.render.threads_mode = "FIXED"
scene.render.threads = 6
scene.render.resolution_x = 850
scene.render.resolution_y = 700
scene.render.resolution_percentage = 100
scene.render.film_transparent = True
scene.world = bpy.data.worlds.new("Studio")
scene.world.use_nodes = True
scene.world.node_tree.nodes["Background"].inputs[1].default_value = .8
colours = dict(body=(0,177,183), key=(30,30,30), cradle=(30,30,30), insert=(30,30,30),
               lifter=(30,30,30), bearing=(125,139,150))
palette = {name: material(name, rgb) for name, rgb in colours.items()}
metal = material("Steel", (145,151,160))
objects = {}
for name in job["views"]["book_cover"]:
    if name == "cap":
        from mathutils import Matrix
        obj = import_banded_cap(job["banded"])
        obj.data.transform(Matrix.Translation((0, 0, 101.6)) @ Matrix.Rotation(math.pi, 4, "X"))
    else:
        bpy.ops.wm.stl_import(filepath=str(Path(job["stage"]) / (name + ".stl")))
        obj = bpy.context.object
        obj.data.materials.append(palette.get(name, metal))
    objects[name] = obj

camera = bpy.data.objects.new("Assembly camera", bpy.data.cameras.new("Orthographic"))
scene.collection.objects.link(camera)
scene.camera = camera
camera.data.type = "ORTHO"
camera.data.clip_end = 5000
camera.location = (280,350,165)
aim(camera, (0,0,0))
camera.rotation_mode = "QUATERNION"
camera.rotation_quaternion @= Quaternion((0,0,1), math.radians(-50))
for name, direction, strength in [("Key", (2,3,5), 3.4), ("Fill", (-3,1,2), 1.6)]:
    light = bpy.data.objects.new(name, bpy.data.lights.new(name, "SUN"))
    scene.collection.objects.link(light)
    light.location = direction
    aim(light, (0,0,0))
    light.data.energy = strength
    light.data.angle = math.radians(28)

for view, pieces in job["views"].items():
    for key, obj in objects.items():
        obj.hide_render = key not in pieces
        obj.location = pieces.get(key, [0,0,0])
    bpy.context.view_layer.update()
    inv = camera.rotation_quaternion.inverted()
    # Frame real vertices to keep thin, diagonal assemblies readable.
    coords = [inv @ (v.co + objects[k].location) for k in pieces for v in objects[k].data.vertices]
    if view in ("step_02", "step_03", "step_04"):
        # Detail the receiving slot and bearing seat at the palm end.
        coords = [inv @ (v.co + objects[k].location) for k in pieces for v in objects[k].data.vertices
                  if (v.co + objects[k].location).z >= 73]
    low = Vector([min(v[i] for v in coords) for i in range(3)])
    high = Vector([max(v[i] for v in coords) for i in range(3)])
    centre = (low + high) * .5
    centre.z += 400
    camera.location = camera.rotation_quaternion @ centre
    camera.data.ortho_scale = 1.09 * max(high.x-low.x, (high.y-low.y)*850/700)
    scene.render.filepath = str(Path(job["output"]) / (view + ".png"))
    bpy.ops.render.render(write_still=True)


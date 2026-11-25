"""Draw the palm face from the actual first-layer outlines in the colour STLs."""
from PIL import Image, ImageDraw
from shapely.geometry import Polygon
import trimesh


def draw(folder):
    size = 600
    scale = size / 24
    centre = size // 2
    paper, palm, ink = "#f6f4ef", "#00B1B7", "#000000"
    image = Image.new("RGB", (size, size), paper)
    paint = ImageDraw.Draw(image)
    body = trimesh.load_mesh(folder / "3dpr_color_main.stl")
    contour = body.section([0, 0, 1], [0, 0, .10])
    outline = max(contour.discrete, key=lambda path: Polygon(path[:, :2]).area)
    # Flip about the X axis to view the face in its installed orientation.
    def pixels(loop):
        return [(centre + scale*x, centre + scale*y) for x,y in loop[:, :2]]
    paint.polygon(pixels(outline), fill=palm)
    accent = trimesh.load_mesh(folder / "3dpr_color_support.stl")
    contours = accent.section([0, 0, 1], [0, 0, .10])
    loops = sorted(contours.discrete, key=lambda path: -Polygon(path[:, :2]).area)
    polygons = []
    for path in loops:
        poly = Polygon(path[:, :2])
        depth = sum(parent.contains(poly) for parent in polygons)
        paint.polygon(pixels(path), fill=palm if depth % 2 else ink)
        polygons.append(poly)
    image.resize((300, 300), Image.Resampling.LANCZOS).save(folder / "palm_face.png")


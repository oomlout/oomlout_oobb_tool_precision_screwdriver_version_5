"""One shared four-step A4 sheet from the populate recipe and production CAD views."""
import hashlib
import json
from pathlib import Path

import fitz
from reportlab import rl_config
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas


def publish(output, data):
    output = Path(output)
    steps = data["steps"]
    if len(steps) != 4:
        raise ValueError("The shared assembly sheet has four panels")
    data["book_pages"] = [{"kind": "instructions", "group": 0}]
    (output / "assembly_manifest.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    pdf = output / "assembly_instructions.pdf"
    rl_config.useA85 = False
    page = canvas.Canvas(str(pdf), pagesize=landscape(A4), invariant=1, pageCompression=1)
    page.setTitle("Precision screwdriver · Version 3 assembly")
    width, height = landscape(A4)
    teal = HexColor(data["style"]["caption_background"])
    ink = HexColor(data["style"]["caption_text"])
    page.setFillColor(teal)
    page.rect(0, height - 28*mm, width, 28*mm, stroke=0, fill=1)
    page.setFillColor(ink)
    page.setFont("Helvetica-Bold", 21)
    page.drawString(8*mm, height - 12*mm, "Precision screwdriver  /  Version 3")
    page.setFont("Helvetica", 10)
    page.drawString(8*mm, height - 20*mm, data["book"]["materials"])
    for index, step in enumerate(steps):
        x = (7 + (index % 2)*143)*mm
        y = (97 - (index // 2)*84)*mm
        w, h = 137*mm, 80*mm
        page.setFillColor(white)
        page.setStrokeColor(black)
        page.setLineWidth(.8)
        page.roundRect(x, y, w, h, 2*mm, stroke=1, fill=1)
        image = output / "render/raw" / (step["key"] + ".png")
        page.drawImage(str(image), x+2*mm, y+24*mm, w-4*mm, h-26*mm,
                       preserveAspectRatio=True, anchor="c", mask="auto")
        page.setFillColor(teal)
        page.rect(x+.5, y+.5, w-1, 24*mm, fill=1, stroke=0)
        page.setFillColor(ink)
        page.setFont("Helvetica-Bold", 13)
        page.drawString(x+4*mm, y+17.4*mm, f"{index+1}   {step['title']}")
        page.setFont("Helvetica", 10)
        lines = simpleSplit(step["action"], "Helvetica", 10, w-8*mm)
        if len(lines) > 3:
            raise ValueError(f"Step {index+1} overflows the caption")
        for line_index, line in enumerate(lines):
            page.drawString(x+4*mm, y+(12.2-line_index*4.0)*mm, line)
    page.setFillColor(teal)
    page.rect(0, 0, width, 8*mm, fill=1, stroke=0)
    page.setFillColor(ink)
    page.setFont("Helvetica", 8)
    page.drawString(7*mm, 2.8*mm, "AI-generated CAD images and instructions. Errors possible. Check fit on your first print.")
    page.showPage()
    page.save()
    pages = output / "pages"
    pages.mkdir(exist_ok=True)
    with fitz.open(pdf) as document:
        assert len(document) == 1
        for step in steps:
            assert step["title"] in document[0].get_text()
        document[0].get_pixmap(matrix=fitz.Matrix(1.75, 1.75)).save(pages / "page_01.png")
    report = {"page_count": 1, "steps": 4, "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest()}
    (output / "validation.json").write_text(json.dumps(report, indent=2))

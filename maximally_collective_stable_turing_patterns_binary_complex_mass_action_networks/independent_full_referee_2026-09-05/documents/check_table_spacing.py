"""Reproduce a specific PDF-layout witness; this is not a general PDF validator.

Run from this directory with Python 3 and Poppler pdftotext installed.
The preserved PDF is unmodified. Bounding-box overlap is accompanied by
direct raster inspection in DOCUMENT_REVIEW.md, since font boxes alone need
not imply that visible glyph ink overlaps.
"""
from pathlib import Path
import json
import subprocess
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[1]
pdf = root / "source_snapshot/submission/journal/supplement.pdf"
raw = subprocess.check_output([
    "pdftotext", "-f", "15", "-l", "15", "-bbox-layout", str(pdf), "-"
])
tree = ET.fromstring(raw)
words = list(tree.iter("{http://www.w3.org/1999/xhtml}word"))

def locate(text):
    matches = [w for w in words if w.text == text]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one {text}, found {len(matches)}")
    return {k: float(matches[0].attrib[k]) for k in ("xMin", "xMax", "yMin", "yMax")}

denominator, next_numerator = locate("91125"), locate("4420871")
x_overlap = min(denominator["xMax"], next_numerator["xMax"]) - max(denominator["xMin"], next_numerator["xMin"])
y_overlap = min(denominator["yMax"], next_numerator["yMax"]) - max(denominator["yMin"], next_numerator["yMin"])
if x_overlap <= 0 or y_overlap <= 0:
    raise RuntimeError("The recorded source-PDF overlap is absent; inspect the PDF version")
result = dict(pdf=str(pdf.relative_to(root)), page=15,
              denominator_91125=denominator, next_numerator_4420871=next_numerator,
              x_overlap_points=x_overlap, y_overlap_points=y_overlap,
              interpretation="Specific bounding-box witness corroborated by raster inspection")
Path(__file__).with_name("TABLE_SPACING_WITNESS.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))

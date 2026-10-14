"""Compare the actual revised rebuild with the visually inspected frozen PDF."""
from pathlib import Path
import datetime
import hashlib
import json
import re
import subprocess

out = Path(__file__).resolve().parent
root = out.parents[1]
original = root / "publication/preprint.pdf"
rebuilt = root / "receipts/clean_reproduction_revised/pdf/preprint.pdf"
assert rebuilt.is_file()
render = out / "revised_rebuilt_pdf"
render.mkdir(exist_ok=True)
subprocess.run(["pdftoppm", "-png", "-r", "105", str(rebuilt), str(render / "page")], check=True, capture_output=True)
sha = lambda b: hashlib.sha256(b).hexdigest()
texts = []
counts = []
for p in (original, rebuilt):
    result = subprocess.run(["pdftotext", "-layout", str(p), "-"], check=True, capture_output=True)
    texts.append(re.sub(rb"\s+", b" ", result.stdout).strip())
    info = subprocess.run(["pdfinfo", str(p)], check=True, capture_output=True).stdout
    counts.append(int(re.search(rb"Pages:\s*(\d+)", info).group(1)))
assert texts[0] == texts[1] and counts == [8, 8]
pages = []
for i in range(1, 9):
    a, b = out / f"page-{i}.png", render / f"page-{i}.png"
    assert a.read_bytes() == b.read_bytes(), i
    pages.append({"page": i, "identical_png_sha256": sha(a.read_bytes())})
record = {"timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "status": "PASS_ALL_EIGHT_REBUILT_PAGE_RENDERS_IDENTICAL_TO_VISUALLY_INSPECTED_FROZEN_PAGES", "packaged_pdf_sha256": sha(original.read_bytes()), "rebuilt_pdf_sha256": sha(rebuilt.read_bytes()), "page_counts": counts, "normalized_all_page_text_equal": True, "render_dpi": 105, "pages": pages, "script_sha256": sha(Path(__file__).read_bytes())}
(out / "rebuilt_pdf_render_comparison.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps(record, indent=2))

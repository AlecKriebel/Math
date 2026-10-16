#!/usr/bin/env python3
"""Private OCR access to an authenticated original Stanford technical report."""
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
import subprocess
import hashlib
import json

A = Path(__file__).resolve().parent
P = A / 'priority_sources_private'
O = P / 'lamperti_pages'
O.mkdir(exist_ok=False)
utc = lambda: datetime.now(timezone.utc).isoformat()
sha = lambda b: hashlib.sha256(b).hexdigest()

def call(argv):
    t = utc()
    r = subprocess.run(argv, capture_output=True, timeout=60)
    e = dict(argv=argv, started_utc=t, ended_utc=utc(), exit_code=r.returncode,
             stdout=r.stdout.decode(errors='replace'), stderr=r.stderr.decode(errors='replace'))
    if r.returncode:
        (O / 'FAILED_EXECUTION.json').write_text(json.dumps(e, indent=2) + '\n')
        raise RuntimeError(e)
    return e

pdf = P / 'lamperti_stanford.pdf'
if sha(pdf.read_bytes()) != '885c8270cd29f5aca134f76aa9ea05bf76dc0865d4bf793a4ad150c7e01e908e':
    raise RuntimeError('original scan pin')
render = call(['/opt/homebrew/bin/pdftoppm', '-r', '150', '-png', str(pdf), str(O / 'page')])
pages = sorted(O.glob('page-*.png'))
if len(pages) != 19:
    raise RuntimeError('nineteen report pages')

def ocr(page):
    e = call(['/opt/homebrew/bin/tesseract', str(page), str(page.with_suffix('')), '--psm', '6'])
    e['image'] = dict(path=str(page), bytes=page.stat().st_size, sha256=sha(page.read_bytes()))
    text = page.with_suffix('.txt')
    e['text'] = dict(path=str(text), bytes=text.stat().st_size, sha256=sha(text.read_bytes()))
    return e

with ThreadPoolExecutor(max_workers=5) as pool:
    results = list(pool.map(ocr, pages))
receipt = dict(utc=utc(), render=render, pages=results,
               limitation='OCR is an aid; crucial mathematical formulas must be checked visually against the scan.')
(P / 'lamperti_ocr_receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(dict(utc=receipt['utc'], status='PASS_PRIVATE_NINETEEN_PAGE_RENDER_AND_OCR',
                     pages=len(results), all_exit_zero=True), indent=2))

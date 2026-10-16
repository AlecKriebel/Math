#!/usr/bin/env python3
"""Read-only source fetch/render receipts; source bodies remain private scratch."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import subprocess
from urllib.request import Request, urlopen

BASE = Path(__file__).resolve().parent
SCRATCH = BASE / 'tmp' / 'pdfs'
SCRATCH.mkdir(parents=True, exist_ok=True)
urls = [
    ('owr.pdf', 'https://ems.press/content/serial-article-files/47008', 407470,
     '320d7e903924249d1f57536cdf67491b3b5f89de8401c9a7c07800b09ee750c7', [16, 17]),
    ('couzinie_hirsch_v2.pdf', 'https://arxiv.org/pdf/2010.03347v2', 193301,
     '49959f145120d52d101dabfd520b7d6b88da804ca2e36d3e0f5a3bcb31bfe983', [3]),
]
receipt = []
for name, url, size, sha, pages in urls:
    with urlopen(Request(url, headers={'User-Agent': 'Independent-mathematical-audit/1.0'}), timeout=45) as response:
        data = response.read()
        status = response.status
    digest = hashlib.sha256(data).hexdigest()
    if status != 200 or len(data) != size or digest != sha:
        raise RuntimeError('Source bytes changed or retrieval failed: ' + url)
    path = SCRATCH / name
    path.write_bytes(data)
    images = []
    for page in pages:
        prefix = SCRATCH / (path.stem + '_p' + str(page))
        result = subprocess.run(['/opt/homebrew/bin/pdftoppm', '-f', str(page), '-l', str(page), '-scale-to', '1600', '-png', str(path), str(prefix)], capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError(result.stderr)
        for img in sorted(SCRATCH.glob(prefix.name + '-*.png')):
            images.append({'path_relative_to_review': str(img.relative_to(BASE)), 'bytes': img.stat().st_size, 'sha256': hashlib.sha256(img.read_bytes()).hexdigest()})
    receipt.append({'url': url, 'http_status': status, 'bytes': len(data), 'sha256': digest, 'rendered_pdf_pages_one_based': pages, 'images': images})
out = {'retrieved_utc': datetime.now(timezone.utc).isoformat(), 'sources': receipt, 'third_party_bodies_public': False, 'visual_inspection_complete': False}
(BASE / 'SOURCE_RETRIEVAL.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2))

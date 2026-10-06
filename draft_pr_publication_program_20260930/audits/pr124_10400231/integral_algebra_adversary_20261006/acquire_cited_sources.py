"""Read-only acquisition of precisely the three citations in the submitted proof."""
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import urllib.request

ROOT = Path(__file__).resolve().parent
PRIVATE = ROOT / 'private'
PRIVATE.mkdir(exist_ok=True)
SOURCES = [
    ('ohtsuki', 'https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf', [170]),
    ('massuyeau', 'https://webhomes.maths.ed.ac.uk/~v1ranick/papers/massu.pdf', [12, 13, 14]),
    ('alcaraz', 'https://arxiv.org/pdf/1406.2042v1', [11, 12, 13, 14, 15, 16]),
]
records = []
for name, url, pages in SOURCES:
    request = urllib.request.Request(url, headers={'User-Agent': 'Independent mathematical citation audit'})
    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read()
    pdf = PRIVATE / (name + '.pdf')
    pdf.write_bytes(data)
    text_path = PRIVATE / (name + '.txt')
    process = subprocess.Popen(['pdftotext', '-layout', str(pdf), str(text_path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        raise RuntimeError((name, process.returncode, stderr.decode(errors='replace')))
    renders = []
    for page in pages:
        prefix = PRIVATE / f'{name}-page-{page}'
        process2 = subprocess.Popen(['pdftoppm', '-f', str(page), '-l', str(page), '-scale-to', '1500', '-singlefile', '-png', str(pdf), str(prefix)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out2, err2 = process2.communicate()
        if process2.returncode != 0:
            raise RuntimeError((name, page, process2.returncode, err2.decode(errors='replace')))
        image = prefix.with_suffix('.png')
        renders.append({'page_one_based': page, 'sha256': sha256(image.read_bytes()).hexdigest(), 'bytes': image.stat().st_size, 'PID': process2.pid, 'exit': process2.returncode, 'stdout_sha256': sha256(out2).hexdigest(), 'stderr_sha256': sha256(err2).hexdigest()})
    records.append({'citation': name, 'url': url, 'pdf_sha256': sha256(data).hexdigest(), 'pdf_bytes': len(data), 'text_sha256': sha256(text_path.read_bytes()).hexdigest(), 'text_bytes': text_path.stat().st_size, 'pdftotext_PID': process.pid, 'pdftotext_exit': process.returncode, 'stdout_sha256': sha256(stdout).hexdigest(), 'stderr_sha256': sha256(stderr).hexdigest(), 'renders': renders})
result = {'schema': 'cited-source-acquisition/v1', 'UTC': datetime.now(timezone.utc).isoformat(), 'operator_PID': os.getpid(), 'scope': 'Only original cited sources; no new theorem or literature-status search.', 'private_source_material_ignored': True, 'sources': records}
(ROOT / 'SOURCE_ACQUISITION.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, sort_keys=True))

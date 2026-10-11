#!/usr/bin/env python3
"""Capture bounded primary-source access, including complete failed streams."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess

A = Path(__file__).resolve().parent
O = A / 'priority_sources_private'
O.mkdir(exist_ok=False)
utc = lambda: datetime.now(timezone.utc).isoformat()
sha = lambda b: hashlib.sha256(b).hexdigest()
sources = [
    ('blanchet_glynn_thorisson', 'https://arxiv.org/pdf/1503.08374'),
    ('kevei_terhesiu', 'https://arxiv.org/pdf/2005.11121'),
    ('rauwolf', 'https://publications.rwth-aachen.de/record/1018053/files/1018053.pdf'),
    ('lamperti_stanford_record', 'https://purl.stanford.edu/nn078xw6398'),
    ('lamperti_publisher_pdf', 'https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-33/issue-2/An-Invariance-Principle-in-Renewal-Theory/10.1214/aoms/1177704590.pdf'),
    ('thorisson_publisher_pdf', 'https://link.springer.com/content/pdf/10.1007/s11134-011-9241-2.pdf'),
]

def get(item):
    name, url = item
    argv = ['/usr/bin/curl', '--fail', '--location', '--silent', '--show-error', '--max-time', '30', url]
    started = utc()
    r = subprocess.run(argv, capture_output=True, timeout=35)
    body = O / (name + ('.pdf' if r.stdout.startswith(b'%PDF-') else '.body'))
    body.write_bytes(r.stdout)
    (O / (name + '.stderr')).write_bytes(r.stderr)
    e = dict(name=name, url=url, argv=argv, started_utc=started, ended_utc=utc(),
             exit_code=r.returncode, body_file=str(body), bytes=len(r.stdout), sha256=sha(r.stdout),
             stderr=r.stderr.decode(errors='replace'), stderr_sha256=sha(r.stderr), pdf=r.stdout.startswith(b'%PDF-'))
    if e['pdf'] and r.returncode == 0:
        textfile = O / (name + '.txt')
        ta = ['/opt/homebrew/bin/pdftotext', '-layout', str(body), str(textfile)]
        ts = utc()
        tr = subprocess.run(ta, capture_output=True, timeout=15)
        e['text_extraction'] = dict(argv=ta, started_utc=ts, ended_utc=utc(), exit_code=tr.returncode,
            stdout=tr.stdout.decode(errors='replace'), stderr=tr.stderr.decode(errors='replace'))
        if tr.returncode == 0:
            tb = textfile.read_bytes()
            e['text_file'] = str(textfile)
            e['text_bytes'] = len(tb)
            e['text_sha256'] = sha(tb)
    (O / (name + '_receipt.json')).write_text(json.dumps(e, indent=2) + '\n')
    return e

started = utc()
with ThreadPoolExecutor(max_workers=6) as pool:
    results = list(pool.map(get, sources))
receipt = dict(started_utc=started, ended_utc=utc(), sources=results,
               limitations='Download success authenticates captured bytes; semantic and visual read scope is recorded separately.')
(A / 'ROOT_PRIORITY_SOURCE_ACCESS.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))

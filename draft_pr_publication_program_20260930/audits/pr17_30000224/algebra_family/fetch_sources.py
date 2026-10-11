#!/usr/bin/env python3
"""Read-only retrieval of bounded, version-pinned primary-source PDFs."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import urllib.request

HERE = Path(__file__).resolve().parent
PDFS = HERE / 'tmp' / 'pdfs'
PDFS.mkdir(parents=True, exist_ok=True)
SOURCES = [
    ('hassanzadeh_v2', 'https://arxiv.org/pdf/2409.05705v2'),
    ('ma_schwede_shimomoto_v3', 'https://arxiv.org/pdf/1605.02755v3'),
    ('singh_walther_v2', 'https://arxiv.org/pdf/math/0701524v2'),
    ('eisenbud_sturmfels_author', 'https://eisenbud.github.io/papers/pdfs/1996-002.pdf'),
    ('owr_2005_19', 'https://ems.press/content/serial-article-files/45993?nt=1'),
]
records = []
for name, url in SOURCES:
    item = {'name': name, 'requested_url': url}
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'Independent mathematical source audit'})
        with urllib.request.urlopen(request, timeout=30) as response:
            data = response.read()
            item['final_url'] = response.url
            item['content_type'] = response.headers.get('Content-Type')
        if not data.startswith(b'%PDF-'):
            raise ValueError('Retrieved document is not a PDF')
        pdf = PDFS / (name + '.pdf')
        pdf.write_bytes(data)
        txt = pdf.with_suffix('.txt')
        conversion = subprocess.run(['pdftotext', '-layout', str(pdf), str(txt)], capture_output=True, text=True)
        if conversion.returncode:
            raise RuntimeError(conversion.stderr)
        item.update(status='retrieved', pdf_sha256=hashlib.sha256(data).hexdigest(),
                    bytes=len(data), text_sha256=hashlib.sha256(txt.read_bytes()).hexdigest(),
                    pdf=str(pdf.relative_to(HERE)), text=str(txt.relative_to(HERE)))
    except Exception as error:
        item.update(status='failed', error=repr(error))
    item['checked_at_utc'] = datetime.now(timezone.utc).isoformat()
    records.append(item)
    print(name, item['status'], flush=True)
out = {'scope': 'bounded cited-machinery check; no worldwide openness certification', 'records': records}
(HERE / 'evidence' / 'primary_source_receipts.json').write_text(json.dumps(out, indent=2) + '\n')

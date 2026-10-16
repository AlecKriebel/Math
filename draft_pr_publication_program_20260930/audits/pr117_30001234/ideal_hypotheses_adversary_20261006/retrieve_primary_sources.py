#!/usr/bin/env python3
import hashlib
import json
import urllib.request
from pathlib import Path

root = Path(__file__).resolve().parent
private = root / 'private_sources'
private.mkdir(exist_ok=True)
sources = [
    ('owr.pdf', 'https://ems.press/content/serial-article-files/46224'),
    ('shibuta_takagi_v3.pdf', 'https://arxiv.org/pdf/0810.1278v3'),
]
pins = []
for filename, url in sources:
    with urllib.request.urlopen(url, timeout=30) as response:
        body = response.read()
        effective_url = response.geturl()
    if not body.startswith(b'%PDF-'):
        raise RuntimeError('Retrieved source is not a PDF: ' + url)
    path = private / filename
    path.write_bytes(body)
    pins.append({'filename':filename,'url':url,'effective_url':effective_url,
                 'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest(),
                 'private_full_body_excluded_from_public_manifest':True})
(root / 'PRIMARY_SOURCE_RETRIEVAL_PINS.json').write_text(json.dumps(pins,indent=2)+'\n')
print(json.dumps(pins,indent=2))

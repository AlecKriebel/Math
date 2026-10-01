#!/usr/bin/env python3
"""Refresh only ignored foreign primary PDF bytes, verifying this gate's hashes."""
from pathlib import Path
from urllib.request import urlopen
import hashlib, json, subprocess, sys
HERE=Path(__file__).resolve().parent
receipt=json.loads((HERE/'SOURCE_RECEIPT.json').read_text())
for item in receipt['primary_retrievals']:
    if 'sha256' not in item:continue
    b=urlopen(item['url'],timeout=30).read()
    assert len(b)==item['bytes'] and hashlib.sha256(b).hexdigest()==item['sha256'],item['file']
    p=HERE/'foreign'/item['file'];p.parent.mkdir(exist_ok=True);p.write_bytes(b)
    subprocess.run(['pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],check=True)
print('Four current primary PDF byte hashes match the gate; ignored copies refreshed.')

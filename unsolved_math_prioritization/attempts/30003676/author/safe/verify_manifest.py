#!/usr/bin/env python3
"""Verify the closed safe payload and exercise two integrity negative controls."""
import hashlib
import json
from pathlib import Path
import shutil
import tempfile

ROOT=Path(__file__).resolve().parent

def verify(root):
    manifest=json.loads((root/'MANIFEST.json').read_text())
    expected={x['path']:x for x in manifest['files']}
    entries=list(root.iterdir())
    assert all(p.is_file() and not p.is_symlink() for p in entries), 'nonregular entry'
    actual={p.name for p in entries if p.name!='MANIFEST.json'}
    assert actual==set(expected), 'payload allowlist mismatch'
    for name,item in expected.items():
        assert Path(name).name==name, 'nonlocal payload name'
        b=(root/name).read_bytes()
        assert len(b)==item['bytes'], 'byte count mismatch: '+name
        assert hashlib.sha256(b).hexdigest()==item['sha256'], 'hash mismatch: '+name
    return len(expected)

count=verify(ROOT)
for mutation in ['content_tamper','unexpected_file']:
    with tempfile.TemporaryDirectory(prefix='sis-manifest-') as td:
        dst=Path(td)/'safe';shutil.copytree(ROOT,dst)
        if mutation=='content_tamper':
            with (dst/'REPORT.md').open('ab') as f:f.write(b'\nMUTATION\n')
        else:
            (dst/'unexpected_source_extract.txt').write_text('deliberate synthetic negative control')
        rejected=False
        try:verify(dst)
        except AssertionError:rejected=True
        assert rejected, 'negative control escaped: '+mutation
print(json.dumps({'status':'PASS','payload_files':count,'integrity_negative_controls_rejected':2,'manifest_self_hash':'recorded outside the manifest to avoid circular hashing'},sort_keys=True))

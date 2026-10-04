#!/usr/bin/env python3
"""Portable frozen-packet verification. Python3 and SymPy required."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile
P=Path(__file__).resolve().parent
for f in json.loads((P/'PUBLICATION_MANIFEST.json').read_text())['files']:
 b=(P/f['path']).read_bytes()
 assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256'],f['path']
R=P/'independent_review'
for f in json.loads((R/'REVIEW_MANIFEST.json').read_text())['files']:
 b=(R/f['path']).read_bytes();assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256']
assert hashlib.sha256((P/'FINAL_AUTHOR_MANIFEST.json').read_bytes()).hexdigest()=='e594f4629756fbf1a8b372d677de4f174f01f3886d3fa8c58c9dcc87c86fb2fa'
with tempfile.TemporaryDirectory(prefix='c4-frozen-author-') as t:
 A=Path(t)
 for f in json.loads((P/'FINAL_AUTHOR_MANIFEST.json').read_text())['files']:
  d=A/f['path'];d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(P/f['path'],d)
 shutil.copyfile(P/'FINAL_AUTHOR_MANIFEST.json',A/'FINAL_AUTHOR_MANIFEST.json')
 out=subprocess.check_output([sys.executable,str(R/'replay_author.py'),str(A)],cwd=A)
 assert out==(R/'AUTHOR_REPLAY.json').read_bytes()
assert subprocess.check_output([sys.executable,str(R/'independent_check.py')],cwd=R)==(R/'INDEPENDENT_CHECKS.json').read_bytes()
print('PASS: immutable publication hashes, exact author replay and independent SymPy-backed replay')

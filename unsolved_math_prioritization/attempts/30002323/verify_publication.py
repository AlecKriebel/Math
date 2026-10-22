#!/usr/bin/env python3
"""Verify source-status evidence bindings; no counterexample proof is claimed."""
from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent
checks=0
for name in ['PUBLIC_MANIFEST.json','independent_review/REVIEW_MANIFEST.json','PUBLICATION_MANIFEST.json']:
 m=p/name; entries=json.loads(m.read_text())['files']
 if isinstance(entries,dict): entries=[dict(path=k,**v) for k,v in entries.items()]
 for f in entries:
  b=(m.parent/f['path']).read_bytes()
  assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256'],(name,f['path'])
  checks+=1
assert hashlib.sha256((p/'PUBLIC_MANIFEST.json').read_bytes()).hexdigest()=='f7607db8448f3af07ab48c4ae301d6bffeff7fdf204c75520b8cd8918dfdd43b'
assert hashlib.sha256((p/'independent_review/REVIEW_MANIFEST.json').read_bytes()).hexdigest()=='e88a2a46c4fdc0daa1b52c1e05e4af3fdb7d9649fd81db8033f82d5d677b5409'
print(json.dumps(dict(status='PASS_SOURCE_STATUS_BINDINGS',digest_checks=checks,author_turns=0,construction_independently_verified=False),sort_keys=True))

#!/usr/bin/env python3
"""Verify and replay the reviewed frozen scoped research packet."""
from pathlib import Path
import json,hashlib,subprocess,sys
p=Path(__file__).resolve().parent;checks=0
for name in ['FINAL_AUTHOR_MANIFEST.json','independent_review/REVIEW_MANIFEST.json','PUBLICATION_MANIFEST.json']:
 m=p/name
 for f in json.loads(m.read_text())['files']:
  d=(m.parent/f['path']).read_bytes()
  assert len(d)==f['bytes'] and hashlib.sha256(d).hexdigest()==f['sha256'],(name,f['path'])
  checks+=1
assert hashlib.sha256((p/'FINAL_AUTHOR_MANIFEST.json').read_bytes()).hexdigest()=='ee8ac91b0fca253669b27b774c9fbd16bed4acda4d6a8fbfb0cc629b15adf221'
assert hashlib.sha256((p/'independent_review/REVIEW_MANIFEST.json').read_bytes()).hexdigest()=='30b76efd479b203f2653d49d7bb8d35bb0177eb4505d2350e5f69eb89ef28306'
a=subprocess.check_output([sys.executable,str(p/'replay_packet.py')],cwd=p);assert a==(p/'FINAL_REPLAY.json').read_bytes()
b=subprocess.check_output([sys.executable,str(p/'independent_review'/'independent_checks.py')],cwd=p);assert b==(p/'independent_review'/'INDEPENDENT_CHECKS.json').read_bytes()
print(json.dumps(dict(status='PASS_REVIEWED_SCOPED_PACKET',digest_checks=checks,author_assertions=459698,independent_assertions=1913,original_status='unsolved',author_turns=5),indent=2,sort_keys=True))

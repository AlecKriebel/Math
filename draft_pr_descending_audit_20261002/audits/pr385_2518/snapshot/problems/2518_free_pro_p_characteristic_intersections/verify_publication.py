#!/usr/bin/env python3
"""Verify frozen public research/review bytes and exact standard-library replays."""
from pathlib import Path
import hashlib,json,subprocess,sys
P=Path(__file__).resolve().parent;R=P/'independent_review'
for e in json.loads((P/'PUBLICATION_MANIFEST.json').read_text())['files']:
 b=(P/e['path']).read_bytes();assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],e['path']
assert hashlib.sha256((P/'FINAL_AUTHOR_MANIFEST.json').read_bytes()).hexdigest()=='d498046adc568031857dc5b93d7e8049a591f4f128f73666208fd8de0e4f0d8a'
assert hashlib.sha256((R/'REVIEW_MANIFEST.json').read_bytes()).hexdigest()=='6ca9abdd890d5cead8ca8c5019396080121473b61867bb3654bf7ac4ea05b4a4'
for e in json.loads((R/'REVIEW_MANIFEST.json').read_text())['files']:
 b=(R/e['path']).read_bytes();assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256']
actual=json.loads(subprocess.check_output([sys.executable,str(P/'REPLAY_ALL.py')],cwd=P))
for path in [P/'FINAL_REPLAY.json',R/'AUTHOR_REPLAY.json']:
 expected=json.loads(path.read_text());assert expected['local_source_bindings']==12
 expected['local_source_bindings']=0
 assert actual==expected
assert subprocess.check_output([sys.executable,str(R/'independent_check.py')],cwd=R)==(R/'INDEPENDENT_CHECKS.json').read_bytes()
print('PASS: frozen public hashes; 139300 author and 153807 independent exact controls; raw source replay omitted (0/12 local-only bindings)')

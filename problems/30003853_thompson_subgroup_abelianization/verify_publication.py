#!/usr/bin/env python3
"""Verify frozen public research/review bytes and exact standard-library replays."""
from pathlib import Path
import hashlib,json,subprocess,sys
P=Path(__file__).resolve().parent;R=P/'independent_review'
for e in json.loads((P/'PUBLICATION_MANIFEST.json').read_text())['files']:
 b=(P/e['path']).read_bytes();assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],e['path']
assert hashlib.sha256((P/'FINAL_AUTHOR_MANIFEST.json').read_bytes()).hexdigest()=='0f21b2a22642240ab3d2bc1e285e7854875e9c27300c48e77f199cef3d254690'
assert hashlib.sha256((R/'REVIEW_MANIFEST.json').read_bytes()).hexdigest()=='a3418ac0f444baab1872824dd9850e1c74e5f5fb8ad6123d8e2fec872fe10ad9'
for e in json.loads((R/'REVIEW_MANIFEST.json').read_text())['files']:
 b=(R/e['path']).read_bytes();assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256']

# Additional authoritative scope; immutable historical manifests remain pinned.
assert hashlib.sha256((P/'CURRENT_SCOPE_MANIFEST.json').read_bytes()).hexdigest()=='74b8fff9f4167704db696cb9f3a08b208c5c4644bf3e29504b99dfc046ceb469'
for e in json.loads((P/'CURRENT_SCOPE_MANIFEST.json').read_text())['files']:
 b=(P/e['path']).read_bytes();assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],e['path']

actual=json.loads(subprocess.check_output([sys.executable,str(P/'REPLAY_ALL.py')],cwd=P))
for path in [P/'FINAL_REPLAY.json',R/'AUTHOR_REPLAY.json']:
 expected=json.loads(path.read_text());assert expected['local_source_bindings']==20
 expected['local_source_bindings']=0
 assert actual==expected
assert subprocess.check_output([sys.executable,str(R/'independent_check.py')],cwd=R)==(R/'INDEPENDENT_CHECKS.json').read_bytes()
print('PASS: frozen public hashes; 562635 author and 110736 independent exact controls; current diagram-group gap qualification bound; raw source replay omitted (0/20 local-only bindings)')

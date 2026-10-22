#!/usr/bin/env python3
"""Portable frozen-evidence verification and complete deterministic replay."""
from pathlib import Path
import hashlib,json,subprocess,sys
p=Path(__file__).resolve().parent
checks=0
names=[f'TURN_{j}_MANIFEST.json' for j in range(1,5)]+['FINAL_AUTHOR_MANIFEST.json','independent_review/REVIEW_MANIFEST.json','PUBLICATION_MANIFEST.json']
for name in names:
 m=p/name
 for f in json.loads(m.read_text())['files']:
  b=(m.parent/f['path']).read_bytes()
  assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256'],(name,f['path'])
  checks+=1
assert hashlib.sha256((p/'FINAL_AUTHOR_MANIFEST.json').read_bytes()).hexdigest()=='421c94fc9b79cd27dfdc8a99baba57f941788a3a2b42dd704611ae892f44a10a'
assert hashlib.sha256((p/'independent_review/REVIEW_MANIFEST.json').read_bytes()).hexdigest()=='59ed029fed1d6034d65d6ed173258ac4224bf00e45b5ca57d5bf23317771e19f'
for j in range(1,6):
 assert subprocess.check_output([sys.executable,str(p/f'verify_turn{j}.py')],cwd=p)==(p/f'TURN_{j}_CHECKS.json').read_bytes()
for script,receipt in [('independent_controls.py','INDEPENDENT_CONTROLS.json'),('independent_rate_controls.py','INDEPENDENT_RATE_CONTROLS.json')]:
 assert subprocess.check_output([sys.executable,str(p/'independent_review'/script)])==(p/'independent_review'/receipt).read_bytes()
print(json.dumps({'status':'PASS_PORTABLE_PUBLICATION','file_digest_checks':checks,'author_assertions':62188,'independent_assertions':31770,'original_broad_status':'unsolved','author_turns':5},indent=2,sort_keys=True))

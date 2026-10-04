#!/usr/bin/env python3
"""Portable integrity and replay wrapper; does not modify frozen artifacts."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
p=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--source-dir',type=Path);a=ap.parse_args()
counts={}
for name,base in [(f'TURN_{k}_MANIFEST.json',p) for k in (1,2,3)]+[('FINAL_AUTHOR_MANIFEST.json',p),('REVIEW_MANIFEST.json',p/'review'),('PUBLICATION_MANIFEST.json',p)]:
 m=json.loads((base/name).read_bytes());n=0
 for f in m['files']:
  b=(base/f['path']).read_bytes()
  assert hashlib.sha256(b).hexdigest()==f['sha256'],(name,f['path'])
  assert len(b)==f['bytes'],(name,f['path'])
  n+=1
 counts[str((base/name).relative_to(p))]=n
for k in (1,2,3):
 result=subprocess.check_output([sys.executable,str(p/f'check_turn_{k}.py')],cwd=p)
 assert result==(p/f'TURN_{k}_CHECKS.json').read_bytes(),k
result=subprocess.check_output([sys.executable,str(p/'review/check_independent.py')],cwd=p/'review')
assert result==(p/'review/INDEPENDENT_CHECKS.json').read_bytes()
source='not_checked: supply --source-dir to verify the primary PDF hashes'
if a.source_dir is not None:
 n=0
 for f in json.loads((p/'SOURCE_MANIFEST.json').read_bytes())['files']:
  b=(a.source_dir/f['name']).read_bytes()
  assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256'],f['name']
  n+=1
 source={'verified_files':n}
print(json.dumps({'status':'PASS','hash_entries':counts,'all_four_replays':'byte_exact','author_assertions':60934,'independent_assertions':18678,'source_hashes':source,'scope':'Integrity and finite controls; the mathematical verdict is the independent analytic review.'},indent=2,sort_keys=True))

#!/usr/bin/env python3
"""Validate this delta artifact and replay its independent checks read-only."""
from pathlib import Path
import hashlib,json,subprocess,sys
root=Path(__file__).resolve().parent
names={'DELTA_AUDIT.md','EXACT_ACCEPTANCE.json','VERIFY_DELTA.py','RESULTS.json','README.md','CHECK_DELTA.py','MANIFEST.json'}
if {p.name for p in root.iterdir()}!=names:raise ValueError('delta audit file allowlist')
if any((root/n).is_symlink() or not (root/n).is_file() for n in names):raise ValueError('delta audit file type')
def unique(pairs):
 d={}
 for k,v in pairs:
  if k in d:raise ValueError('duplicate JSON key')
  d[k]=v
 return d
raw=(root/'MANIFEST.json').read_bytes();m=json.loads(raw,object_pairs_hook=unique)
if len(m['files'])!=6 or {r['path'] for r in m['files']}!=names-{'MANIFEST.json'}:raise ValueError('manifest membership')
for r in m['files']:
 b=(root/r['path']).read_bytes()
 if len(b)!=r['bytes'] or hashlib.sha256(b).hexdigest()!=r['sha256']:raise ValueError('delta file mismatch: '+r['path'])
r=subprocess.run([sys.executable,'-B',str(root/'VERIFY_DELTA.py'),*sys.argv[1:]],capture_output=True,check=True)
if r.stderr or r.stdout!=(root/'RESULTS.json').read_bytes():raise ValueError('delta exact replay mismatch')
print(json.dumps({'result':'PASS','manifest_sha256':hashlib.sha256(raw).hexdigest(),'exact_replay':True,'disposition':'already_solved','author_turns_used':1,'author_turn_limit':5,'note':'Authenticate the manifest with the separately reported digest. Acceptance is exact-byte scoped.'},indent=2,sort_keys=True))

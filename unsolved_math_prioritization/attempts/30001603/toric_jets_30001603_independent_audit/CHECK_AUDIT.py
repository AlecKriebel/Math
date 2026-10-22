#!/usr/bin/env python3
"""Read-only audit integrity and exact replay. Pass the frozen author packet path."""
from pathlib import Path
import hashlib,json,subprocess,sys
root=Path(__file__).resolve().parent
names={'AUDIT.md','CORRECTIONS.md','EXACT_BINDING.json','SOURCES.json','INDEPENDENT_VERIFY.py','RESULTS.json','README.md','CHECK_AUDIT.py','MANIFEST.json'}
if {p.name for p in root.iterdir()}!=names:raise ValueError('audit allowlist mismatch')
if any((root/n).is_symlink() or not (root/n).is_file() for n in names):raise ValueError('nonregular audit member')
def unique(pairs):
 d={}
 for k,v in pairs:
  if k in d:raise ValueError('duplicate JSON key')
  d[k]=v
 return d
raw=(root/'MANIFEST.json').read_bytes();m=json.loads(raw,object_pairs_hook=unique)
if len(m['files'])!=len(names)-1 or {r['path'] for r in m['files']}!=names-{'MANIFEST.json'}:raise ValueError('manifest membership')
for r in m['files']:
 data=(root/r['path']).read_bytes()
 if len(data)!=r['bytes'] or hashlib.sha256(data).hexdigest()!=r['sha256']:raise ValueError('content mismatch: '+r['path'])
packet=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else root.parent/'toric_jets_30001603'
p=subprocess.run([sys.executable,'-B',str(root/'INDEPENDENT_VERIFY.py'),str(packet)],capture_output=True,check=True)
if p.stderr or p.stdout!=(root/'RESULTS.json').read_bytes():raise ValueError('exact independent replay mismatch')
print(json.dumps({'result':'PASS','manifest_sha256':hashlib.sha256(raw).hexdigest(),'files_bound':len(names)-1,'exact_results_replay':True,'mathematical_verdict':'PASS','source_description_verdict':'CORRECTION_REQUIRED','scope':'Authenticate this manifest using the separately reported digest. No revised author packet is accepted here.'},indent=2,sort_keys=True))

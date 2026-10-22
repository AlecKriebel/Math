#!/usr/bin/env python3
from pathlib import Path
import json,hashlib,subprocess,sys
p=Path(__file__).resolve().parent;bindings=0
for name,sha in [('FINAL_AUTHOR_MANIFEST.json','d4cfe6349a6288b59ba4615778a7a6a92394f0a10999925fe1d1ce7f88547f60'),('review/REVIEW_MANIFEST.json','b635c81461d22739a60c66c8cf992767ab7c332e4ed9c1a8d20ce94c4a12f1db')]:assert hashlib.sha256((p/name).read_bytes()).hexdigest()==sha
for m in sorted(p.rglob('*MANIFEST.json')):
 files=json.loads(m.read_text()).get('files',[])
 if isinstance(files,dict):files=[dict(path=name,**v) for name,v in files.items()]
 for f in files:
  q=m.parent/f['path'];assert hashlib.sha256(q.read_bytes()).hexdigest()==f['sha256'],q
  if 'bytes' in f:assert q.stat().st_size==f['bytes']
  bindings+=1
total=0
for i in range(1,6):
 r=subprocess.check_output([sys.executable,str(p/f'verify_turn{i}.py')]);assert r==(p/f'TURN_{i}_CHECKS.json').read_bytes();total+=json.loads(r)['assertions']
r=subprocess.check_output([sys.executable,str(p/'review/independent_controls.py')]);assert r==(p/'review/INDEPENDENT_CHECKS.json').read_bytes()
s=json.loads((p/'CURRENT_STATE_T5.json').read_text());assert s['author_turns']==5 and s['original_status']=='unresolved'
print(json.dumps(dict(status='PASS',bindings=bindings,author_assertions=total,independent_assertions=json.loads(r)['assertions'],original='both reductions unsolved 5/5'),indent=2,sort_keys=True))

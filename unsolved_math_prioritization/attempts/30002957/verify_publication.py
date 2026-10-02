#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,subprocess,sys
p=Path(__file__).resolve().parent
checks=0
for name,sha in [('FINAL_AUTHOR_MANIFEST.json','4775dfe5338320da27f132013ab5627455ebadc9ed8fe9265cf71d3c78fce4b5'),('review/REVIEW_MANIFEST.json','99d845ab129a36afbcad4673b830ade6192b88529ccd88217ab776f4913ed64a')]:
 assert hashlib.sha256((p/name).read_bytes()).hexdigest()==sha
for m in sorted(p.rglob('*MANIFEST.json')):
 for f in json.loads(m.read_text()).get('files',[]):
  q=m.parent/f['path'];assert q.is_file(),q
  assert hashlib.sha256(q.read_bytes()).hexdigest()==f['sha256'],q
  if 'bytes' in f:assert q.stat().st_size==f['bytes'],q
  checks+=1
total=0
for i in range(1,6):
 r=subprocess.check_output([sys.executable,str(p/f'verify_turn{i}.py')]);assert r==(p/f'TURN_{i}_CHECKS.json').read_bytes();total+=json.loads(r)['assertions']
r=subprocess.check_output([sys.executable,str(p/'review/independent_checks.py')]);assert r==(p/'review/INDEPENDENT_CHECKS.json').read_bytes()
s=json.loads((p/'CURRENT_STATE_T5.json').read_text());assert s['author_turns']==5 and s['original_status']=='unresolved'
print(json.dumps(dict(status='PASS',bindings=checks,author_assertions=total,independent_assertions=json.loads(r)['independent_exact_assertions'],original='unsolved 5/5'),indent=2,sort_keys=True))

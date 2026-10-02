#!/usr/bin/env python3
"""Replay frozen controls and historical bindings; no general-resolution claim."""
from pathlib import Path
import json,hashlib,subprocess,sys
p=Path(__file__).resolve().parent;entries=0;total=0
for name in ['SOURCE_GATE_MANIFEST.json']+[f'TURN_{i}_MANIFEST.json' for i in range(1,6)]:
 for f in json.loads((p/name).read_text())['files']:
  d=(p/f['path']).read_bytes()
  assert len(d)==f['bytes'] and hashlib.sha256(d).hexdigest()==f['sha256'],(name,f['path'])
  entries+=1
for i in range(1,6):
 out=subprocess.check_output([sys.executable,str(p/f'verify_turn{i}.py')],cwd=p)
 assert out==(p/f'TURN_{i}_CHECKS.json').read_bytes(),i
 total+=json.loads(out)['assertions']
print(json.dumps(dict(status='PASS_FIVE_TURN_REPLAY',historical_digest_entries=entries,exact_assertions=total,author_turns=5,original_status='unresolved'),indent=2,sort_keys=True))

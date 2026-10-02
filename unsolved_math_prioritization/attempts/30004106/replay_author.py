#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,subprocess,sys
p=Path(__file__).resolve().parent
replays=[]
for n in range(1,6):
 out=subprocess.check_output([sys.executable,str(p/f'verify_turn{n}.py')],cwd=p)
 assert out==(p/f'TURN_{n}_CHECKS.json').read_bytes(),f'turn {n} receipt mismatch'
 data=json.loads(out)
 replays.append({'turn':n,'exact_assertions':data['exact_assertions'],'receipt_sha256':hashlib.sha256(out).hexdigest()})
entries=0
for name in ['SOURCE_GATE_MANIFEST.json']+[f'TURN_{n}_MANIFEST.json' for n in range(1,6)]:
 m=json.loads((p/name).read_text())
 for x in m['files']:
  b=(p/x['path']).read_bytes()
  assert len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'],(name,x['path'])
  entries+=1
print(json.dumps({'problem_id':30004106,'author_turns':5,'original_status':'unsolved','replays':replays,'total_exact_assertions':sum(x['exact_assertions'] for x in replays),'historical_manifest_entries_verified':entries},indent=2))

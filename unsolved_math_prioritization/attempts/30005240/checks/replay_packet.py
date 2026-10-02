#!/usr/bin/env python3
"""Replay all author checks and verify frozen historical manifests without mutation."""
from pathlib import Path
import hashlib,json,subprocess,sys
p=Path(__file__).resolve().parents[1]
entries=0
for name in ['SOURCE_GATE_FROZEN.json']+[f'TURN_{j}_MANIFEST.json' for j in range(1,6)]:
 m=json.loads((p/name).read_text());fs=m['files']
 if isinstance(fs,dict):fs=[{'path':k,'sha256':v} for k,v in fs.items()]
 for f in fs:
  data=(p/f['path']).read_bytes()
  assert hashlib.sha256(data).hexdigest()==f['sha256'],(name,f['path'])
  if 'bytes' in f:assert len(data)==f['bytes']
  entries+=1
receipts=[]
for j in range(1,6):
 out=subprocess.check_output([sys.executable,str(p/f'checks/verify_turn{j}.py')])
 assert out==(p/f'checks/turn{j}_output.json').read_bytes(),j
 d=json.loads(out)
 receipts.append({'turn':j,'assertions':d.get('assertions',d.get('exact_assertions')),'output_sha256':hashlib.sha256(out).hexdigest()})
print(json.dumps({'status':'PASS_ALL_FIVE_AUTHOR_CHECKS','historical_manifest_entries_verified':entries,'turns':receipts,'total_exact_assertions':sum(r['assertions'] for r in receipts),'scope':'Deterministic controls and frozen-byte integrity, not a proof of unresolved PDE hypotheses.'},indent=2,sort_keys=True))

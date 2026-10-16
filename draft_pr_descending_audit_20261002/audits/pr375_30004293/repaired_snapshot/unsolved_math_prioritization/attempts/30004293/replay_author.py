#!/usr/bin/env python3
"""Replay the frozen exact controls and byte bindings."""
from pathlib import Path
import hashlib,json,subprocess,sys
p=Path(__file__).resolve().parent
turns=[];total=0
for t in range(1,6):
 out=subprocess.check_output([sys.executable,str(p/f'verify_turn{t}.py')])
 want=(p/f'TURN_{t}_CHECKS.json').read_bytes()
 assert out==want,f'turn {t} receipt differs'
 obj=json.loads(out);total+=obj['exact_assertions']
 turns.append({'turn':t,'receipt_byte_exact':True,'exact_assertions':obj['exact_assertions']})
entries=0
for m in sorted(p.glob('*MANIFEST.json')):
 if m.name in ['SOURCE_MANIFEST.json','FINAL_AUTHOR_MANIFEST.json']:continue
 for f in json.loads(m.read_text()).get('files',[]):
  b=(p/f['path']).read_bytes()
  assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256'],(m.name,f['path'])
  entries+=1
sources=[];root=p.parent/'source'
for s in json.loads((p/'SOURCE_MANIFEST.json').read_text())['sources']:
 f=root/s['file']
 if f.exists():
  b=f.read_bytes();assert len(b)==s['bytes'] and hashlib.sha256(b).hexdigest()==s['sha256'],s['file']
  sources.append({'file':s['file'],'byte_exact':True})
 else:sources.append({'file':s['file'],'local_source_unavailable':True})
print(json.dumps({'turns':turns,'total_exact_assertions':total,'historical_manifest_entries':entries,'sources':sources},indent=2))

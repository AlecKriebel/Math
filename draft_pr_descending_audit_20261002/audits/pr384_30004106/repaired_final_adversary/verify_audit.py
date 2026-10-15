#!/usr/bin/env python3
"""Read-only verification of bound audit artifacts and fresh control output."""
from pathlib import Path
import hashlib,json,subprocess,sys
P=Path(__file__).resolve().parent
for name in ['INPUT_MANIFEST.json','OUTPUT_MANIFEST.json']:
 m=json.loads((P/name).read_text())
 for e in m['files']:
  f=Path(e['path']) if name=='INPUT_MANIFEST.json' else P/e['path']
  b=f.read_bytes()
  assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],(name,e['path'])
for seal,name in [('PRECOMPARISON_SEAL.json','PRECOMPARISON_RECONSTRUCTION.md')]:
 d=json.loads((P/seal).read_text());assert hashlib.sha256((P/name).read_bytes()).hexdigest()==d['sha256']
s=json.loads((P/'FRESH_CONTROL_SEAL.json').read_text())
assert hashlib.sha256((P/'fresh_controls.py').read_bytes()).hexdigest()==s['code_sha256']
assert hashlib.sha256((P/'FRESH_CONTROLS.json').read_bytes()).hexdigest()==s['output_sha256']
r=subprocess.run([sys.executable,'-B',str(P/'fresh_controls.py')],capture_output=True,cwd=P)
assert r.returncode==0 and not r.stderr and r.stdout==(P/'FRESH_CONTROLS.json').read_bytes()
v=json.loads((P/'VERDICT.json').read_text());assert v['mandatory_repairs']==[] and v['original_status']=='unsolved' and v['author_turns']==5
print(json.dumps({'status':'PASS','repaired_head':v['head'],'fresh_exact_assertions':json.loads(r.stdout)['exact_assertions'],'input_output_bindings_and_seals_verified':True,'full_fresh_control_stdout_byte_exact':True},indent=2))

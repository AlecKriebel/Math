#!/usr/bin/env python3
"""Check every frozen public byte and replay finite diagnostics; sources optional."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--source-dir',type=Path);a=p.parse_args();D=Path(__file__).resolve().parent
bindings=0
for name in ['FINAL_AUTHOR_MANIFEST.json']+[f'TURN_{i}_MANIFEST.json' for i in range(1,6)]:
 m=json.loads((D/name).read_bytes())
 for f in m['files']:
  b=(D/f['path']).read_bytes();assert len(b)==f['bytes'],f['path'];assert hashlib.sha256(b).hexdigest()==f['sha256'],f['path'];bindings+=1
 if name.startswith('TURN_') and int(name.split('_')[1])>1:
  i=int(name.split('_')[1]);assert m['previous_manifest_sha256']==hashlib.sha256((D/f'TURN_{i-1}_MANIFEST.json').read_bytes()).hexdigest()
r=[]
for i in range(1,6):
 b=subprocess.check_output([sys.executable,str(D/f'check_turn_{i}.py')],cwd=D)
 assert b==(D/f'TURN_{i}_CHECKS.json').read_bytes(),('receipt mismatch',i)
 r.append({'turn':i,'exact_assertions':json.loads(b)['exact_assertions'],'stdout_byte_exact':True})
ns=0
if a.source_dir:
 for f in json.loads((D/'SOURCE_MANIFEST.json').read_bytes())['files']:
  b=(a.source_dir/f['name']).read_bytes();assert len(b)==f['bytes'];assert hashlib.sha256(b).hexdigest()==f['sha256'];ns+=1
print(json.dumps({'status':'PASS','public_bindings_checked':bindings,'replays':r,'total_exact_assertions':sum(x['exact_assertions'] for x in r),'source_files_checked':ns,'source_check':'verified' if a.source_dir else 'not requested; raw sources are not distributed'},indent=2,sort_keys=True))

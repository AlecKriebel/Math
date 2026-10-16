#!/usr/bin/env python3
"""Verify public hashes and exact author replays; optionally check private source PDFs."""
from pathlib import Path
import argparse, hashlib, json, subprocess, sys
p=argparse.ArgumentParser();p.add_argument('--source-dir',type=Path);a=p.parse_args()
D=Path(__file__).resolve().parent
count=0
for name in ['FINAL_AUTHOR_MANIFEST.json']+[f'TURN_{i}_MANIFEST.json' for i in range(1,6)]:
 data=json.loads((D/name).read_bytes())
 for row in data['files']:
  b=(D/row['path']).read_bytes()
  assert len(b)==row['bytes'],(name,row['path'],'bytes')
  assert hashlib.sha256(b).hexdigest()==row['sha256'],(name,row['path'],'sha256')
  count+=1
 if name.startswith('TURN_') and int(name.split('_')[1])>1:
  i=int(name.split('_')[1]);prev=(D/f'TURN_{i-1}_MANIFEST.json').read_bytes()
  assert hashlib.sha256(prev).hexdigest()==data['previous_manifest_sha256'],name
replays=[]
for i in range(1,6):
 out=subprocess.check_output([sys.executable,str(D/f'check_turn_{i}.py')],cwd=D)
 assert out==(D/f'TURN_{i}_CHECKS.json').read_bytes(),('replay',i)
 j=json.loads(out);replays.append({'turn':i,'exact_assertions':j['exact_assertions'],'stdout_byte_exact':True})
ns=0
if a.source_dir:
 for name in ['SOURCE_MANIFEST.json','SOURCE_ADDITION_T1.json','SOURCE_ADDITION_T4.json','SOURCE_ADDITION_T5.json']:
  for row in json.loads((D/name).read_bytes())['files']:
   b=(a.source_dir/row['name']).read_bytes()
   assert len(b)==row['bytes'],row['name']
   assert hashlib.sha256(b).hexdigest()==row['sha256'],row['name']
   ns+=1
print(json.dumps({'status':'PASS','public_file_bindings_checked':count,'replays':replays,'total_exact_assertions':sum(x['exact_assertions'] for x in replays),'source_pdfs_checked':ns,'source_check':'verified' if a.source_dir else 'not requested; raw sources are not distributed'},indent=2,sort_keys=True))

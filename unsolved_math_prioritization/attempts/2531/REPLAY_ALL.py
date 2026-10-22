#!/usr/bin/env python3
"""Replay all five immutable receipts and check historical/source bindings."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--sources',type=Path);args=ap.parse_args()
p=Path(__file__).resolve().parent
turns=[];bindings=0
for i in range(1,6):
    got=subprocess.check_output([sys.executable,str(p/f'check_turn_{i}.py')])
    expected=(p/f'TURN_{i}_CHECKS.json').read_bytes()
    assert got==expected,('receipt',i)
    r=json.loads(got);assert r['status']=='PASS';turns.append({'turn':i,'assertions':r.get('assertions',r.get('exact_assertions'))})
    m=json.loads((p/f'TURN_{i}_MANIFEST.json').read_bytes())
    if i>1:assert m['previous_manifest_sha256']==hashlib.sha256((p/f'TURN_{i-1}_MANIFEST.json').read_bytes()).hexdigest()
    for f in m['files']:
        b=(p/f['path']).read_bytes();assert len(b)==f['bytes'];assert hashlib.sha256(b).hexdigest()==f['sha256'];bindings+=1
source_count=0
if args.sources:
    for f in json.loads((p/'SOURCE_MANIFEST.json').read_bytes())['files']:
        b=(args.sources/f['name']).read_bytes();assert len(b)==f['bytes'];assert hashlib.sha256(b).hexdigest()==f['sha256'];source_count+=1
print(json.dumps({'status':'PASS','author_assertions':sum(x['assertions'] for x in turns),'turns':turns,'historical_file_bindings':bindings,'historical_chain_links':4,'source_files_verified':source_count,'original_target':'unresolved','author_turns_used':5},indent=2,sort_keys=True))

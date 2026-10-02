#!/usr/bin/env python3
from pathlib import Path
import json,hashlib,subprocess,sys
p=Path(__file__).resolve().parents[1]
entries=0
for name in ['SOURCE_GATE_FROZEN.json']+[f'TURN_{j}_MANIFEST.json' for j in range(1,6)]:
 for f in json.loads((p/name).read_text())['files']:
  b=(p/f['path']).read_bytes()
  assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256'],(name,f['path'])
  entries+=1
rows=[]
for j in range(1,6):
 b=subprocess.check_output([sys.executable,str(p/f'checks/verify_turn{j}.py')])
 assert b==(p/f'checks/turn{j}_output.json').read_bytes(),j
 rows.append({'turn':j,'assertions':json.loads(b)['assertions'],'sha256':hashlib.sha256(b).hexdigest()})
print(json.dumps({'status':'PASS_ALL_FIVE_AUTHOR_REPLAYS','historical_manifest_entries':entries,'total_assertions':sum(x['assertions'] for x in rows),'turns':rows,'scope':'Frozen bytes and finite controls; original finite-disk area transfer remains unproved.'},indent=2,sort_keys=True))

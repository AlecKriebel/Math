#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[5]
A=Path(__file__).resolve().parents[2]
S=json.loads((A/'SCOPE_AND_SNAPSHOT.json').read_text())
rows=[]
for rel,record in S['original_blobs'].items():
 p=A/'native'/rel
 b=p.read_bytes()
 original=subprocess.run(['git','show',S['original_head']+':'+rel],cwd=ROOT,capture_output=True,check=True).stdout
 good=len(b)==record['size'] and hashlib.sha256(b).hexdigest()==record['sha256'] and b==original
 rows.append({'path':rel,'size':len(b),'sha256':hashlib.sha256(b).hexdigest(),'matches_original_head':good})
result={'pr':662,'head':S['original_head'],'claimed_solved_at_capture':S['status']=='claimed_solved','files_checked':len(rows),'all_match':all(r['matches_original_head'] for r in rows),'records':rows}
print(json.dumps(result,indent=2))
if not result['all_match']:sys.exit(1)

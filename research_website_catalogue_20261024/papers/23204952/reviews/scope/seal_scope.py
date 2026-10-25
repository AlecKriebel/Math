from pathlib import Path
import hashlib,json,sys
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[2];O=R/'reviews/scope'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if '--verify' in sys.argv:
 x=json.loads((O/'SEALED_MANIFEST.json').read_text());bad=[]
 for row in x['files']:
  p=R/row['path']
  if not p.is_file() or p.stat().st_size!=row['bytes'] or sha(p)!=row['sha256']:bad.append(row['path'])
 print(json.dumps({'checked_files':len(x['files']),'mismatches':bad,'manifest_sha256':sha(O/'SEALED_MANIFEST.json')},indent=2))
 raise SystemExit(bool(bad))
rows=[]
for base in [R/'sources',O]:
 for p in sorted(base.rglob('*')):
  if not p.is_file() or p.name in ['SEALED_MANIFEST.json','SEALED_MANIFEST.sha256']:continue
  rel=p.relative_to(R).as_posix();rows.append({'path':rel,'bytes':p.stat().st_size,'sha256':sha(p),'private_reading_cache_do_not_publish_bytes':'/.cache/' in '/'+rel})
x={'record_id':23204952,'sheet_row':80,'work_id':'Z-23204951','sealed_utc':datetime.now(timezone.utc).isoformat(),'scope':'This intake source tree and reviews/scope only; independent reviewer/root outputs excluded. Third-party .cache bytes are locally preserved but excluded from repository publication. Hashes/receipts identify those private bytes.','scientific_verdict':None,'files':rows,'verification_command':'python3 reviews/scope/seal_scope.py --verify (from the paper folder)'}
(O/'SEALED_MANIFEST.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');digest=sha(O/'SEALED_MANIFEST.json');(O/'SEALED_MANIFEST.sha256').write_text(digest+'  SEALED_MANIFEST.json\n');print(json.dumps({'files':len(rows),'manifest_sha256':digest,'private_cache_files':sum(v['private_reading_cache_do_not_publish_bytes'] for v in rows)},indent=2))

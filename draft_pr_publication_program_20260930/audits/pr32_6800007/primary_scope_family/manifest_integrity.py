#!/usr/bin/env python3
"""Self-excluding first-party manifest; ignored reference caches are never promoted."""
import hashlib,json,pathlib,sys
from datetime import datetime,timezone
HERE=pathlib.Path(__file__).resolve().parent
SKIP_DIRS={'tmp','sources','isolated_original','isolated_controls','__pycache__'}
def sha(b):return hashlib.sha256(b).hexdigest()
def members():
 files=[]
 for p in sorted(HERE.rglob('*')):
  if not p.is_file() or p.name=='MANIFEST.json':continue
  relative=p.relative_to(HERE)
  if relative.parts[0] in SKIP_DIRS:
   if relative.parts[0]!='sources' or p.suffix!='.json':continue
  b=p.read_bytes();files.append({'path':relative.as_posix(),'size':len(b),'sha256':sha(b)})
 return files
seal=json.loads((HERE/'EARLY_PRIMARY_SEAL.json').read_text())
assert sha((HERE/seal['file']).read_bytes())==seal['sha256']
assert seal['prior_package_or_sibling_read'] is False
if '--create' in sys.argv:
 output={'created_utc':datetime.now(timezone.utc).isoformat(),'family':'pr32_6800007 primary_scope_family','self_excluding':True,
  'exclusions':['MANIFEST.json','tmp/','sources primary reference bytes/text/renders except first-party metadata JSON','isolated_original/','isolated_controls/','__pycache__/'],
  'meaning':'First-party report/programs/receipts/control output integrity, not mathematical correctness or historical novelty.',
  'early_seal_sha256':seal['sha256'],'files':members()}
 (HERE/'MANIFEST.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
manifest=json.loads((HERE/'MANIFEST.json').read_text())
assert manifest['self_excluding'] and manifest['files']==members()
assert not any(f['path']=='MANIFEST.json' for f in manifest['files'])
print(json.dumps({'members':len(manifest['files']),'integrity':True,'early_seal_unchanged':True,'manifest_sha256':sha((HERE/'MANIFEST.json').read_bytes())},indent=2))

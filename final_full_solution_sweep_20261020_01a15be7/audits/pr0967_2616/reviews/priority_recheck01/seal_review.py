#!/usr/bin/env python3
"""Create once or verify this review's complete hash inventory. No repository writes."""
import datetime,hashlib,json,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parent
EXCLUDE={'SEALED_MANIFEST.json','SEAL.sha256'}
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def entries():
 return [{'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':sha(p),'private':p.relative_to(ROOT).parts[0]=='private'} for p in sorted(ROOT.rglob('*')) if p.is_file() and str(p.relative_to(ROOT)) not in EXCLUDE]
if sys.argv[1:]==['create']:
 if any((ROOT/x).exists() for x in EXCLUDE):raise SystemExit('Refusing to replace an existing seal')
 manifest={'schema_version':1,'sealed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Complete priority_recheck01 artifacts including ignored private evidence; original scientific files remain outside this folder and immutable. No files are modified after sealing.','original_head':'b356dec5cb01e5f536b9cfeece56ad08844c03cb','original_source_snapshot_sha256':sha(ROOT.parent.parent/'SOURCE_SNAPSHOT.json'),'files':entries(),'exclusions':sorted(EXCLUDE),'caveat':'Hash seal is a local integrity boundary, not a trusted historical timestamp or third-party signature.'}
 with (ROOT/'SEALED_MANIFEST.json').open('x') as f:f.write(json.dumps(manifest,indent=2)+'\n')
 with (ROOT/'SEAL.sha256').open('x') as f:f.write(sha(ROOT/'SEALED_MANIFEST.json')+'  SEALED_MANIFEST.json\n')
 print(json.dumps({'created':True,'files':len(manifest['files']),'manifest_sha256':sha(ROOT/'SEALED_MANIFEST.json')}))
elif not sys.argv[1:] or sys.argv[1:]==['verify']:
 manifest=json.loads((ROOT/'SEALED_MANIFEST.json').read_text());expected=(ROOT/'SEAL.sha256').read_text().split()[0]
 if sha(ROOT/'SEALED_MANIFEST.json')!=expected:raise SystemExit('Manifest hash mismatch')
 if entries()!=manifest['files']:raise SystemExit('Inventory or content mismatch')
 print(json.dumps({'status':'PASS','files':len(manifest['files']),'private_files':sum(x['private'] for x in manifest['files']),'manifest_sha256':expected}))
else:raise SystemExit('Usage: seal_review.py [create|verify]')

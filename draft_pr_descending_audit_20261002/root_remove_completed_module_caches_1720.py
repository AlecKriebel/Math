import datetime,hashlib,json,os,subprocess
from pathlib import Path
P=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002')
folders=[f for f in (P/'audits').iterdir() if f.is_dir() and f.name.startswith('pr') and f.name.split('_')[0][2:].isdigit() and 368<=int(f.name.split('_')[0][2:])<=388]
KEEP=P/'audits/pr378_30004322/sources_effective_review'
journal=P/'ROOT_COMPLETED_RUNTIME_CACHE_REMOVAL_20261003_1720.jsonl'
files=[]
for folder in folders:
 for p in folder.rglob('*.pyc'):
  if p.is_symlink() or p.parent.name!='__pycache__' or p.resolve().is_relative_to(KEEP.resolve()):continue
  if not any(('private' in part or 'runtime' in part or part=='raw_sources') for part in p.relative_to(P).parts):continue
  if '.cpython-' not in p.name:continue
  source=p.parent.parent/(p.name.split('.cpython-')[0]+'.py')
  if not source.is_file():continue
  files.append((p,source))
tracked=subprocess.check_output(['git','ls-files','-z','--',*[str(f.relative_to(P.parent)) for f in folders]]).split(b'\0')
tracked=set(tracked);rows=[]
for p,source in files:
 assert str(p.relative_to(P.parent)).encode() not in tracked
 b=p.read_bytes();src=source.read_bytes()
 row={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cache_path':str(p.relative_to(P)),'cache_bytes':len(b),'cache_sha256':hashlib.sha256(b).hexdigest(),'preserved_source_path':str(source.relative_to(P)),'preserved_source_sha256':hashlib.sha256(src).hexdigest(),'regeneration':'Python compileall with preserved source; disposable compiled module cache only','state':'PLANNED'}
 with journal.open('a') as f:f.write(json.dumps(row,sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())
 p.unlink();row['state']='CACHE_REMOVED_SOURCE_UNCHANGED'
 with journal.open('a') as f:f.write(json.dumps(row,sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())
 assert source.read_bytes()==src
 rows.append(row)
summary={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Only completed own PR388–368 disposable compiled caches; active PR378 sources_effective_review interpreter, PR367 and PR366 wholly untouched','cache_files_removed':len(rows),'logical_bytes':sum(r['cache_bytes'] for r in rows),'all_module_source_bytes_preserved':True,'mathematical_source_or_output_files_removed':0,'journal':str(journal)}
(P/'ROOT_COMPLETED_RUNTIME_CACHE_REMOVAL_20261003_1720.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))


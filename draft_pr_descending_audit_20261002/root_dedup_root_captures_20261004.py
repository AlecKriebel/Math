"""Consolidate identical root-only capture files, preserving every byte/path/mode."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess
P=Path(__file__).resolve().parent; R=P.parent
canonical={};plan=[]
for A in sorted((P/'audits').glob('pr*')):
 for folder in sorted(A.glob('root*_private')):
  if not folder.is_dir():continue
  tracked=set(subprocess.check_output(['git','ls-files','-z','--',str(folder.relative_to(R))],cwd=R).split(b'\0'))
  for p in sorted(folder.rglob('*')):
   if not p.is_file() or p.is_symlink() or p.stat().st_size<32768:continue
   if str(p.relative_to(R)).encode() in tracked:continue
   if any(k in {'__pycache__','.venv','node_modules'} or 'runtime' in k for k in p.relative_to(folder).parts):continue
   b=p.read_bytes();h=hashlib.sha256(b).hexdigest();mode=p.stat().st_mode&0o7777;key=(len(b),h,mode)
   if key not in canonical:canonical[key]=p;continue
   c=canonical[key]
   if p.stat().st_ino==c.stat().st_ino:continue
   assert c.read_bytes()==b
   plan.append({'target':str(p.relative_to(R)),'canonical':str(c.relative_to(R)),'bytes':len(b),'sha256':h,'mode':mode})
receipt=P/'ROOT_CAPTURE_DEDUP_20261004T0140.json'
assert not receipt.exists()
data={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Only untracked root-owned root*_private captures; no closed agent namespace, candidate, public, runtime, foreign or tracked files.',
 'plan':plan,'files':len(plan),'logical_duplicate_bytes':sum(r['bytes'] for r in plan),'status':'PREPARED'}
receipt.write_text(json.dumps(data,indent=2)+'\n')
journal=P/'ROOT_CAPTURE_DEDUP_20261004T0140.jsonl'
for row in plan:
 p=R/row['target'];c=R/row['canonical'];b=p.read_bytes();assert hashlib.sha256(b).hexdigest()==row['sha256'] and c.read_bytes()==b
 with journal.open('a') as f:f.write(json.dumps({**row,'state':'PREPARED'})+'\n');f.flush();os.fsync(f.fileno())
 t=p.with_name(p.name+'.root_consolidation_pending');assert not t.exists();os.link(c,t);os.replace(t,p)
 assert p.read_bytes()==b and p.stat().st_ino==c.stat().st_ino and p.stat().st_mode&0o7777==row['mode']
 with journal.open('a') as f:f.write(json.dumps({**row,'state':'COMPLETE'})+'\n');f.flush();os.fsync(f.fileno())
data.update(status='COMPLETE_EVERY_BYTE_PATH_AND_MODE_PRESERVED',finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
receipt.write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps({k:v for k,v in data.items() if k!='plan'},indent=2))

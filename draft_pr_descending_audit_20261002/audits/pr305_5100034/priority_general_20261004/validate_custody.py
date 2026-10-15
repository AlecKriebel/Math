#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,stat
r=Path(__file__).resolve().parent
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
count=0;artifacts=set();errors=[]
for q in sorted((r/'custody').glob('*.json')):
 obj=json.loads(q.read_text());records=obj if isinstance(obj,list) else [obj]
 for v in records:
  if 'argv' not in v: continue
  count+=1
  for k in ['argv','cwd','start_utc','end_utc','exit_code','stdout_file','stdout_sha256','stderr_file','stderr_sha256']:
   if k not in v:errors.append((str(q),k,'missing'))
  if v.get('cwd')!=str(r):errors.append((str(q),'cwd','outside audit'))
  if v.get('exit_code')!=0:errors.append((str(q),'exit',v.get('exit_code')))
  for field in ['stdout','stderr']:
   p=Path(v[field+'_file'])
   if not p.is_file() or h(p)!=v[field+'_sha256']:errors.append((str(q),field,'hash mismatch'))
  if 'artifact' in v:
   p=Path(v['artifact']);artifacts.add(str(p))
   if not p.is_file() or h(p)!=v['sha256']:errors.append((str(q),'artifact','hash mismatch'))
   if p.stat().st_size!=v['bytes']:errors.append((str(q),'bytes','mismatch'))
   if stat.S_IMODE(p.stat().st_mode)!=0o600:errors.append((str(q),'mode','not 0600'))
print('Receipt operation records checked:',count)
print('Distinct source/extraction/render artifacts checked:',len(artifacts))
print('All full stdout and stderr streams retained and matched:',not errors)
print('Errors:',errors)
if errors: raise SystemExit(1)

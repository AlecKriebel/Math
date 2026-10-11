"""Exact public SOURCE custody, excluding only named private cache and closure auxiliaries."""
from pathlib import Path
import hashlib,json,os,stat
P=Path(__file__).absolute().parent
EXEMPT={'INDEX.json','SOURCE_READY.json','SOURCE_MANIFEST.json'}
def sha(b):return hashlib.sha256(b).hexdigest()
def need(v,m):
 if not v:raise ValueError(m)
def row(p):
 s=p.lstat();need(stat.S_ISREG(s.st_mode),'regular file required');b=p.read_bytes();return dict(path=str(p.relative_to(P)),bytes=len(b),sha256=sha(b),full_mode=stat.S_IMODE(s.st_mode))
def domain():
 files=[];dirs=['.']
 for base,ds,fs in os.walk(P,followlinks=False):
  q=Path(base)
  if q==P and 'private_cache' in ds:
   need(stat.S_ISDIR((P/'private_cache').lstat().st_mode),'private cache must be directory');ds.remove('private_cache')
  for n in ds:need(stat.S_ISDIR((q/n).lstat().st_mode),'directory, no symlink');dirs.append(str((q/n).relative_to(P)))
  for n in fs:
   f=q/n;need(stat.S_ISREG(f.lstat().st_mode),'regular public file, no symlink')
   if f.parent==P and n in EXEMPT:continue
   files.append(row(f))
 return sorted(files,key=lambda z:z['path']),sorted(dirs)
def verify(mode):
 raw=(P/'INDEX.json').read_bytes();idx=json.loads(raw);actual,dirs=domain();expected=idx['payloads'];need([z['path'] for z in actual]==[z['path'] for z in expected],'exact public SOURCE file domain');need(dirs==[z['path'] for z in idx['directories']],'exact public SOURCE directory domain')
 for a,e in zip(actual,expected):
  need(a['bytes']==e['bytes'] and a['sha256']==e['sha256'],'exact public whole bytes');need(a['full_mode']==(e['full_mode'] if mode=='prepared' else 292),'exact full file modes')
 for z in idx['directories']:
  need(stat.S_IMODE((P/z['path']).lstat().st_mode)==(z['full_mode'] if mode=='prepared' else 365),'exact directory mode')
 ready=json.loads((P/'SOURCE_READY.json').read_bytes());need(ready['index_sha256']==sha(raw) and ready['payload_count']==len(actual),'exact READY/index')
 need(stat.S_IMODE((P/'INDEX.json').lstat().st_mode)==(420 if mode=='prepared' else 292) and stat.S_IMODE((P/'SOURCE_READY.json').lstat().st_mode)==(420 if mode=='prepared' else 292),'exact auxiliary modes')
 return idx,ready,actual

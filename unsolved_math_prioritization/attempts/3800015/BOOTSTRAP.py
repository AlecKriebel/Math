#!/usr/bin/env python3
"""Externally authenticate these bytes before checking an untrusted delivery."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,math,os,re,stat,subprocess,sys
MANIFEST_SHA='cde4e36f8b70cee542927fcbe88a6f7a4a7305cf17c87f09785c4a896f4c0a4a'
FILE_COUNT=30
class Reject(Exception):pass
def need(x,m):
 if not x:raise Reject(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def pairs(items):
 d={}
 for k,v in items:
  need(k not in d,'duplicate JSON key');d[k]=v
 return d
def nonfinite(x):raise Reject('nonfinite JSON constant')
def floating(x):
 v=float(x);need(math.isfinite(v),'nonfinite JSON number');return v
def load(b):return json.loads(b,object_pairs_hook=pairs,parse_constant=nonfinite,parse_float=floating)
def safe(n):return type(n) is str and bool(n) and not n.startswith('/') and '\\' not in n and all(x not in ('','.','..') for x in n.split('/'))
def entry(r,key='path'):
 need(type(r) is dict and set(r)=={key,'bytes','sha256'},'entry schema');need(safe(r[key]),'entry path')
 need(type(r['bytes']) is int and 0<=r['bytes']<=2000000,'entry byte type/range')
 need(type(r['sha256']) is str and re.fullmatch('[0-9a-f]{64}',r['sha256']) is not None,'entry digest')
def manifest_schema(m):
 need(type(m) is dict and set(m)=={'schema','problem_id','rank','status','turns','full_target_resolved','scope','excluded_anchor_files','queue','files'},'manifest schema')
 for k,v in [('schema','line-arrangement-entire-delivery-v1'),('problem_id',3800015),('rank',1060),('status','exhausted'),('turns',5),('full_target_resolved',False),('scope','all public target files including acceptance and execution evidence; exact QUEUE bytes')]:need(type(m[k]) is type(v) and m[k]==v,'manifest identity: '+k)
 need(type(m['excluded_anchor_files']) is list and m['excluded_anchor_files']==['BOOTSTRAP.py','DELIVERY_MANIFEST.json'],'anchor exclusion')
 need(type(m['files']) is list and len(m['files'])==FILE_COUNT,'file count')
 names=set(m['excluded_anchor_files'])
 for row in m['files']:
  entry(row);need(row['path'] not in names,'duplicate/excluded path');names.add(row['path'])
 entry(m['queue'],'repository_path');need(m['queue']['repository_path']=='unsolved_math_prioritization/QUEUE.md','queue path')
 return names

def authenticate(root,queue):
 need(not root.is_symlink() and root.is_dir(),'delivery root');f={};dirs=set()
 def walk(d,prefix):
  for e in os.scandir(d):
   n=prefix+e.name;s=e.stat(follow_symlinks=False)
   need(not stat.S_ISLNK(s.st_mode),'symlink: '+n)
   if stat.S_ISDIR(s.st_mode):dirs.add(n);walk(Path(e.path),n+'/')
   else:
    need(stat.S_ISREG(s.st_mode),'nonregular member: '+n);need(s.st_size<=2000000,'oversized member: '+n);f[n]=Path(e.path).read_bytes()
 walk(root,'');need('DELIVERY_MANIFEST.json' in f,'missing manifest');need(sha(f['DELIVERY_MANIFEST.json'])==MANIFEST_SHA,'manifest trust anchor')
 m=load(f['DELIVERY_MANIFEST.json']);names=manifest_schema(m)
 need(set(f)==names,'file inventory');need(dirs=={str(p) for n in f for p in PurePosixPath(n).parents if str(p)!='.'},'directory inventory')
 need(f['BOOTSTRAP.py']==Path(__file__).read_bytes(),'bootstrap differs from trusted external copy')
 for r in m['files']:need(len(f[r['path']])==r['bytes'] and sha(f[r['path']])==r['sha256'],'payload binding: '+r['path'])
 for n,b in f.items():
  if n.endswith('.json'):load(b)
 for prefix,pin,count in [('author/','72d1f923599313b4f16be9505587277ac47aa232293972a7ef9737f99b82c23c',6),('audit/','821347924d6ef299cdb84be9a7acbf5f28def364ad6b367898988c0b43860435',8)]:
  need(sha(f[prefix+'MANIFEST.json'])==pin,'original manifest pin');inner=load(f[prefix+'MANIFEST.json'])
  need(type(inner) is dict and set(inner)=={'format','utc_date','files','manifest_self_excluded'} and inner['manifest_self_excluded'] is True,'original manifest schema')
  need(type(inner['files']) is list and len(inner['files'])==count,'original count');seen={prefix+'MANIFEST.json'}
  for r in inner['files']:
   entry(r);n=prefix+r['path'];need(n not in seen and n in f,'original inventory');seen.add(n);need(len(f[n])==r['bytes'] and sha(f[n])==r['sha256'],'original byte binding')
  need(seen=={n for n in f if n.startswith(prefix)},'original exact inventory')
 q=m['queue'];need(not queue.is_symlink() and queue.is_file() and stat.S_ISREG(queue.stat().st_mode),'queue regular file');need(queue.stat().st_size==q['bytes'],'queue size');qb=queue.read_bytes();need(sha(qb)==q['sha256'],'queue hash')
 return f,qb

def main():
 ap=argparse.ArgumentParser();ap.add_argument('delivery',type=Path);ap.add_argument('--queue',type=Path,required=True);ap.add_argument('--integrity-only',action='store_true');ap.add_argument('--source-dir',type=Path);ap.add_argument('--problems',type=Path);ap.add_argument('--research-results',type=Path);a=ap.parse_args()
 need((a.problems is None)==(a.research_results is None),'both corpus inputs required');need(not a.integrity_only or (a.source_dir is None and a.problems is None),'optional inputs require full replay')
 root=a.delivery.absolute();queue=a.queue.absolute();before=authenticate(root,queue)
 if a.integrity_only:print(json.dumps({'status':'PASS_ENTIRE_DELIVERY_INTEGRITY','problem_id':3800015,'files':len(before[0]),'queue_bound':True},sort_keys=True));return 0
 need(queue.stat().st_mode&0o222==0,'queue has write bits');flags=[] if sys.flags.optimize==0 else ['-O' if sys.flags.optimize==1 else '-OO'];rest=[]
 for k in ['source_dir','problems','research_results']:
  value=getattr(a,k)
  if value is not None:rest += ['--'+k.replace('_','-'),str(value.absolute())]
 env={'PATH':'/usr/bin:/bin','LANG':'C.UTF-8','PYTHONNOUSERSITE':'1','PYTHONDONTWRITEBYTECODE':'1'}
 p=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(root/'REPLAY.py'),str(root),*rest],env=env,capture_output=True,timeout=300)
 need(p.returncode==0 and p.stderr==b'','public replay failed: '+p.stderr.decode());load(p.stdout)
 if not rest:need(p.stdout==before[0]['evidence/'+['normal','O','OO'][sys.flags.optimize]+'.stdout.json'],'complete outer evidence mismatch')
 need(authenticate(root,queue)==before,'delivery or queue changed');sys.stdout.buffer.write(p.stdout);return 0
if __name__=='__main__':
 try:sys.exit(main())
 except (Reject,OSError,ValueError,TypeError,KeyError,UnicodeError,subprocess.SubprocessError) as e:print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)

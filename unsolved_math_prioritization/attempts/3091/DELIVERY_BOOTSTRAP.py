#!/usr/bin/env python3
"""Externally authenticate this entrypoint before verifying the complete public delivery."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,math,os,re,stat,subprocess,sys
MANIFEST_SHA='e96fc3341e2363ccecfa6fe7011c4995049d42b18cbd3f72e9e2effe1b42b695'
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
def finite_float(x):
 v=float(x);need(math.isfinite(v),'nonfinite JSON number');return v
def load(b):return json.loads(b,object_pairs_hook=pairs,parse_constant=nonfinite,parse_float=finite_float)
def safe(n):return type(n) is str and bool(n) and not n.startswith('/') and '\\' not in n and all(x not in ('','.','..') for x in n.split('/'))
def authenticate(root,queue):
 need(not root.is_symlink() and root.is_dir(),'delivery root must be a nonsymlink directory')
 f={};dirs=set()
 def walk(d,prefix):
  for e in os.scandir(d):
   n=prefix+e.name;s=e.stat(follow_symlinks=False)
   need(not stat.S_ISLNK(s.st_mode),'delivery symlink: '+n)
   if stat.S_ISDIR(s.st_mode):dirs.add(n);walk(Path(e.path),n+'/')
   else:
    need(stat.S_ISREG(s.st_mode),'delivery nonregular member: '+n);need(s.st_size<=2000000,'delivery oversized member: '+n);f[n]=Path(e.path).read_bytes()
 walk(root,'')
 need('DELIVERY_MANIFEST.json' in f,'missing delivery manifest');need(sha(f['DELIVERY_MANIFEST.json'])==MANIFEST_SHA,'delivery manifest trust anchor')
 m=load(f['DELIVERY_MANIFEST.json']);need(type(m) is dict and set(m)=={'schema','problem_id','scope','excluded_anchor_files','queue','files'},'delivery manifest schema')
 need(m['schema']=='empty-hexagons-entire-delivery-v1' and type(m['problem_id']) is int and m['problem_id']==3091,'delivery identity')
 need(m['scope']=='complete public target plus exact queue bytes; source-free accepted partials, unresolved','delivery scope')
 need(m['excluded_anchor_files']==['DELIVERY_BOOTSTRAP.py','DELIVERY_MANIFEST.json'],'delivery anchor exclusions')
 need(type(m['files']) is list and len(m['files'])==38,'delivery file count')
 expected=set(m['excluded_anchor_files'])
 for row in m['files']:
  need(type(row) is dict and set(row)=={'path','bytes','sha256'},'delivery entry schema');n=row['path'];need(safe(n) and n not in expected,'delivery unsafe/duplicate path');expected.add(n)
  need(n in f,'delivery missing file: '+n);need(type(row['bytes']) is int and 0<=row['bytes']<=2000000 and len(f[n])==row['bytes'],'delivery byte binding: '+n)
  need(type(row['sha256']) is str and re.fullmatch('[0-9a-f]{64}',row['sha256']) is not None and sha(f[n])==row['sha256'],'delivery hash binding: '+n)
 need(set(f)==expected,'delivery file inventory mismatch')
 need(dirs=={str(p) for n in f for p in PurePosixPath(n).parents if str(p)!='.'},'delivery directory inventory mismatch')
 need(f['DELIVERY_BOOTSTRAP.py']==Path(__file__).read_bytes(),'delivery bootstrap differs from trusted external copy')
 q=m['queue'];need(type(q) is dict and set(q)=={'repository_path','bytes','sha256'},'delivery queue schema')
 need(q['repository_path']=='unsolved_math_prioritization/QUEUE.md' and type(q['bytes']) is int and q['bytes']>0 and type(q['sha256']) is str and re.fullmatch('[0-9a-f]{64}',q['sha256']) is not None,'delivery queue fields')
 need(not queue.is_symlink() and queue.is_file() and stat.S_ISREG(queue.stat().st_mode),'delivery queue input must be regular')
 b=queue.read_bytes();need(len(b)==q['bytes'] and sha(b)==q['sha256'],'delivery queue binding')
 return f,b

def main():
 ap=argparse.ArgumentParser();ap.add_argument('delivery',type=Path);ap.add_argument('--queue',type=Path,required=True);a,rest=ap.parse_known_args()
 root=a.delivery.absolute();queue=a.queue.absolute();before=authenticate(root,queue)
 flags=[] if sys.flags.optimize==0 else ['-O' if sys.flags.optimize==1 else '-OO']
 env={k:v for k,v in os.environ.items() if not k.startswith('PYTHON')};env['PYTHONNOUSERSITE']='1'
 p=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(root/'packet/BOOTSTRAP.py'),str(root/'packet'),*rest],capture_output=True,env=env,timeout=300)
 need(authenticate(root,queue)==before,'complete delivery changed during replay')
 sys.stdout.buffer.write(p.stdout);sys.stderr.buffer.write(p.stderr);return p.returncode
if __name__=='__main__':
 try:sys.exit(main())
 except (Reject,OSError,ValueError,TypeError,KeyError,UnicodeError,subprocess.SubprocessError) as e:
  print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)

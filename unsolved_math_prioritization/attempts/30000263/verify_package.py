#!/usr/bin/env python3
"""Exact portable publication checks; effective with Python -O."""
import argparse,hashlib,json,os,subprocess,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).absolute().parent
PINS={'author':'40d9969d77bfd68150e59091340bfdee7a0f38d6d177282969905714d5eed0cf','audit':'0f3d4f2bbcea3484336e0490ff7f077060324f28211899e5f8c19a99055e995e'}
AUTHOR_ZIP='archives/DISCRETE_INTERACTION_30000263_AUTHOR_SAFE_FREEZE.zip'
def need(v,m):
 if not v:raise ValueError('PACKAGE FAILURE: '+m)
def sha(b):return hashlib.sha256(b).hexdigest()
def ident(b):return {'bytes':len(b),'sha256':sha(b)}
def unique(pairs):
 d={}
 for k,v in pairs:need(k not in d,'duplicate JSON key');d[k]=v
 return d
def decode(b):
 return json.loads(b,object_pairs_hook=unique,parse_constant=lambda x:need(False,'nonfinite JSON'))
def safe(n):
 p=Path(n);need(bool(n) and not p.is_absolute() and '..' not in p.parts and p.as_posix()==n,'unsafe path')
def inventory(root):
 fs=set();ds=set()
 for p in [root,*root.parents]:need(not p.is_symlink(),'linked package ancestor')
 for p in root.rglob('*'):
  need(not p.is_symlink(),'linked member');n=p.relative_to(root).as_posix()
  if p.is_file():fs.add(n)
  elif p.is_dir():ds.add(n)
  else:need(False,'nonregular member')
 return fs,ds
def check_manifest(root,name,expected=None):
 raw=(root/name).read_bytes();need(expected is None or sha(raw)==expected,'manifest pin');data=decode(raw);files=data['files'];fs,ds=inventory(root);need(set(files)==fs-{name},'exact file inventory');derived=set()
 for n,value in files.items():
  safe(n);need(n!=name,'self-listed manifest');need(ident((root/n).read_bytes())==value,'identity '+n);derived.update(p.as_posix() for p in Path(n).parents if p!=Path('.'))
 need(ds==derived,'exact directory inventory');return sha(raw)
def queue_check(a,b):
 before=Path(a).read_bytes();after=Path(b).read_bytes();d=decode((ROOT/'QUEUE_DELTA.json').read_bytes());need(ident(before)==d['before'] and ident(after)==d['after'],'queue identities');lines=before.splitlines(keepends=True);hits=[i for i,l in enumerate(lines) if b'| 30000263 / OWR-1050-014 |' in l];need(len(hits)==1,'unique queue row');i=hits[0];cells=lines[i].split(b'|');need(cells[1].strip()==b'806' and cells[8]==b' queued ' and cells[9]==b' 0/5 ','queue original cells');cells[8]=b' unsolved ';cells[9]=b' 5/5 ';lines[i]=b'|'.join(cells);need(b''.join(lines)==after,'exact two-cell patch');return {'status':'PASS','changed_cells':['Status','Turns'],'all_other_bytes_preserved':True}
def replay(path,opt,extras):
 env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env.pop('PYTHONPATH',None);env['PYTHONDONTWRITEBYTECODE']='1';cmd=[sys.executable]+(['-O'] if opt else [])+[str(ROOT/path),*extras];r=subprocess.run(cmd,cwd=ROOT.parent,env=env,capture_output=True,timeout=180);need(r.returncode==0,'replay '+path+': '+r.stderr.decode(errors='replace'));result=decode(r.stdout);need(result['optimized_python']==opt,'optimization indicator');expected='PASS_ARTIFACT_CHECKS_NOT_GENERAL_CONJECTURE' if path.startswith('author/') else 'PASS_PARTIAL_AUDIT_CHECKS_NOT_GENERAL_CONJECTURE';need(result['status']==expected,'replay verdict');return {'checker':path,'optimized':opt,'result':result}
def main():
 p=argparse.ArgumentParser();p.add_argument('--expected-manifest');p.add_argument('--queue-base',type=Path);p.add_argument('--queue-updated',type=Path);p.add_argument('--corpora',type=Path,nargs=3);p.add_argument('--source-dir',type=Path);args=p.parse_args();need(bool(args.queue_base)==bool(args.queue_updated),'both queue paths required');outer=check_manifest(ROOT,'PUBLICATION_MANIFEST.json',args.expected_manifest)
 for d,pin in PINS.items():check_manifest(ROOT/d,'MANIFEST.json',pin)
 verdict=decode((ROOT/'VERDICT.json').read_bytes());need(verdict['problem_id']==30000263 and verdict['status']=='unsolved' and verdict['turns_used']==5,'verdict');need(verdict['mandatory_mathematical_corrections']==0 and verdict['full_solution_claim'] is False,'scope');archives=[]
 for row in verdict['archives']:
  b=(ROOT/row['archive']).read_bytes();need(ident(b)=={'bytes':row['bytes'],'sha256':row['sha256']},'archive pin')
  with zipfile.ZipFile(ROOT/row['archive']) as z:
   ns=z.namelist();need(len(ns)==len(set(ns))==row['members'],'ZIP cardinality');need(z.testzip() is None,'ZIP CRC');fs,_=inventory(ROOT/row['directory']);need(set(ns)==fs,'ZIP exact inventory')
   for n in ns:safe(n);need(z.read(n)==(ROOT/row['directory']/n).read_bytes(),'ZIP member equality')
  archives.append({'archive':row['archive'],'members':len(ns),**ident(b)})
 extras=[]
 if args.corpora:extras+=['--corpora',*[str(p.resolve()) for p in args.corpora]]
 if args.source_dir:extras+=['--source-dir',str(args.source_dir.resolve())]
 runs=[]
 for opt in [False,True]:
  runs.append(replay('author/verify_release.py',opt,extras));runs.append(replay('audit/verify_audit.py',opt,['--author-zip',str(ROOT/AUTHOR_ZIP),*extras]))
 for row in runs:
  ext=row['result']['external'];pdfkey='pdfs' if row['checker'].startswith('author/') else 'source_pdfs';need(bool(args.corpora) or ext['corpora']=='NOT_PROVIDED','absent corpora honesty');need(bool(args.source_dir) or ext[pdfkey]=='NOT_PROVIDED','absent source honesty')
 # Normal and optimized modes must agree apart from the explicit mode flag.
 for i,j in [(0,2),(1,3)]:
  a=dict(runs[i]['result']);b=dict(runs[j]['result']);a.pop('optimized_python');b.pop('optimized_python');need(a==b,'normal/optimized semantic equality')
 result={'status':'PASS_SCOPED_PACKAGE_CHECKS','problem_id':30000263,'disposition':'unsolved_5_of_5','publication_manifest_sha256':outer,'package_files':len(inventory(ROOT)[0]),'archives':archives,'replays':runs,'queue':'NOT_PROVIDED','optimizer_trajectories':'NOT_RUN','full_target_solved':False,'formal_proof_machine_certified':False}
 if args.queue_base:result['queue']=queue_check(args.queue_base,args.queue_updated)
 print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':
 try:main()
 except Exception as e:print(str(e),file=sys.stderr);sys.exit(1)

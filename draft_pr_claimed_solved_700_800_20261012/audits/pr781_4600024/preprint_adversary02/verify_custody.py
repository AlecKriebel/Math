"""Read-only explicit-exception closed review custody; two externally supplied pins."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,os,re,stat,sys
HEAD='4a38c3ccc4cac918fb75fd4b97449f3ebd2e0f7f'
def need(x,m):
 if not x:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def unique(pairs):
 d={}
 for k,v in pairs:need(k not in d,'Duplicate JSON key');d[k]=v
 return d
def nonfinite(v):raise ValueError('Nonfinite JSON')
def parse(b):return json.loads(b,object_pairs_hook=unique,parse_constant=nonfinite)
def regular(p):
 need(stat.S_ISREG(p.lstat().st_mode),'Nonregular input')
 fd=os.open(p,os.O_RDONLY|os.O_NONBLOCK|os.O_NOFOLLOW)
 with os.fdopen(fd,'rb') as f:
  need(stat.S_ISREG(os.fstat(f.fileno()).st_mode),'Nonregular opened input')
  return f.read()
def rel(n):
 need(isinstance(n,str) and n and '\\' not in n,'Bad path type')
 p=PurePosixPath(n)
 need(not p.is_absolute() and str(p)==n and all(x not in ('','.','..') for x in n.split('/')),'Unsafe path')
 return p
def checked(root,n):
 p=root
 for part in rel(n).parts:
  p=p/part;need(not p.is_symlink(),'Symlink path')
 return regular(p)
def ident(raw):return {'bytes':len(raw),'sha256':sha(raw)}
def verify(root,inputs,pin,checkerpin):
 for p in (pin,checkerpin):need(re.fullmatch('[0-9a-f]{64}',p) is not None,'Bad external pin')
 need(root.is_dir() and not root.is_symlink(),'Packet root')
 need(inputs.is_dir() and not inputs.is_symlink(),'Input root')
 need(sha(regular(root/'verify_custody.py'))==checkerpin,'External checker mismatch')
 raw=regular(root/'MANIFEST.json');need(sha(raw)==pin,'External manifest mismatch')
 m=parse(raw);need(m['schema']=='pr781-preprint-review02/v1','Manifest schema')
 need(m['target']=={'pr':781,'problem_id':4600024,'head':HEAD},'Target')
 need(m['explicit_exceptions']==['MANIFEST.json'],'Explicit exceptions')
 files=m['files'];need(set(x.name for x in root.iterdir())==set(files)|{'MANIFEST.json'},'Closed flat inventory')
 for n,row in files.items():
  need(len(rel(n).parts)==1 and n!='MANIFEST.json','Flat name')
  need(ident(checked(root,n))==row,'Packet bytes differ: '+n)
 bindings=parse(regular(root/'INPUTS.json'));need(bindings['exact_head']==HEAD,'Input head')
 for n,row in bindings['files'].items():need(ident(checked(inputs,n))==row,'Input bytes differ: '+n)
 need(sha(checked(inputs,'source/MANIFEST.json'))==bindings['source_manifest_sha256'],'Source pin')
 source_names=set(bindings['source_file_paths'])
 actual=set()
 for p in (inputs/'source').rglob('*'):
  need(not p.is_symlink(),'Source symlink')
  if not p.is_dir():regular(p);actual.add(p.relative_to(inputs).as_posix())
 need(actual==source_names,'Source closure')
 freeze=parse(regular(root/'INITIAL_POSITION_FREEZE.json'))
 need(freeze['prior_reviews_opened'] is False and freeze['repair_conclusions_opened'] is False,'Initial independence')
 need(sha(regular(root/'INITIAL_POSITION.txt'))==freeze['initial_sha256'],'Initial freeze bytes')
 need(bindings['files']['paper.tex']['sha256']==freeze['paper_sha256'],'Initial paper binding')
 need(bindings['files']['source/audit/SELECTED_PUBLIC_RECORD.json']['sha256']==freeze['selected_record_sha256'],'Initial selected binding')
 verdict=parse(regular(root/'VERDICT.json'));need(verdict['actionable_issue_count']==0 and verdict['mathematical_issues']==[],'Verdict differs')
 return {'result':'PASS','manifest_sha256':pin,'checker_sha256':checkerpin,'packet_artifacts_excluding_manifest':len(files),'input_bindings':len(bindings['files']),'source_files':len(source_names),'explicit_exceptions':['MANIFEST.json'],'optimized':bool(sys.flags.optimize)}
def main():
 a=argparse.ArgumentParser();a.add_argument('--root',type=Path,default=Path(__file__).absolute().parent);a.add_argument('--input-root',type=Path,required=True);a.add_argument('--expected-manifest-sha256',required=True);a.add_argument('--expected-checker-sha256',required=True);x=a.parse_args()
 try:r=verify(x.root.absolute(),x.input_root.absolute(),x.expected_manifest_sha256,x.expected_checker_sha256)
 except Exception as e:print(json.dumps({'result':'FAIL','error':str(e)},sort_keys=True));return 1
 print(json.dumps(r,sort_keys=True));return 0
if __name__=='__main__':sys.exit(main())

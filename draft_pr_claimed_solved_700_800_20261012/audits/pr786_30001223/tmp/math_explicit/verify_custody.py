"""Read-only exact-flat review custody using externally supplied manifest/checker pins."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,os,re,stat,sys
HEAD='34f21454986a28ca49f24999be3a0fd1b42755f8'
def need(x,m):
 if not x:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def unique(ps):
 d={}
 for k,v in ps:need(k not in d,'Duplicate JSON key');d[k]=v
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
 need(isinstance(n,str) and n and '\\' not in n,'Bad name')
 p=PurePosixPath(n);need(not p.is_absolute() and str(p)==n and all(x not in ('','.','..') for x in n.split('/')),'Unsafe name')
 return p
def read(root,n):
 p=root
 for x in rel(n).parts:p=p/x;need(not p.is_symlink(),'Symlink path')
 return regular(p)
def identity(b):return {'bytes':len(b),'sha256':sha(b)}
def verify(root,inputs,pin,checker):
 for x in (pin,checker):need(re.fullmatch('[0-9a-f]{64}',x) is not None,'External pin syntax')
 need(root.is_dir() and not root.is_symlink(),'Packet root');need(inputs.is_dir() and not inputs.is_symlink(),'Input root')
 need(sha(regular(root/'verify_custody.py'))==checker,'External checker pin')
 raw=regular(root/'MANIFEST.json');need(sha(raw)==pin,'External manifest pin')
 m=parse(raw);need(m['schema']=='pr786-explicit-math/v1','Schema');need(m['head']==HEAD,'Head');need(m['explicit_exceptions']==['MANIFEST.json'],'Exceptions')
 files=m['files'];need(set(p.name for p in root.iterdir())==set(files)|{'MANIFEST.json'},'Flat closure')
 for n,row in files.items():
  need(len(rel(n).parts)==1 and n!='MANIFEST.json','Flat name');need(identity(read(root,n))==row,'Packet bytes:'+n)
 bindings=parse(regular(root/'INPUTS.json'));need(bindings['exact_head']==HEAD,'Input target')
 for n,row in bindings['files'].items():need(identity(read(inputs,n))==row,'Input bytes:'+n)
 actual={p.relative_to(inputs).as_posix() for p in (inputs/'original').rglob('*') if p.is_file() or p.is_symlink()}
 need(actual==set(bindings['original_file_paths']),'Original closure')
 freeze=parse(regular(root/'INDEPENDENCE_FREEZE.json'));need(freeze['before_author_proof'] and freeze['before_historical_audits'] and freeze['before_peer_root_conclusions'],'Initial independence')
 need(sha(regular(root/'INITIAL_POSITION.txt'))==freeze['initial_sha256'],'Initial freeze')
 need(bindings['files']['SELECTED_PUBLIC_RECORD.json']['sha256']==freeze['selected_record_sha256'],'Selected binding')
 d=parse(regular(root/'DERIVATION_FREEZE.json'));need(d['before_historical_audits'] and d['before_peer_root_mathematical_conclusions'],'Derivation independence');need(sha(regular(root/'INDEPENDENT_DERIVATION.md'))==d['derivation_sha256'],'Derivation freeze')
 v=parse(regular(root/'VERDICT.json'));need(v['mathematical_issues']==[] and v['verdict']=='PASS_EXPLICIT_MATHEMATICAL_FAMILY','Verdict')
 return {'result':'PASS','manifest_sha256':pin,'checker_sha256':checker,'packet_files_excluding_manifest':len(files),'input_bindings':len(bindings['files']),'originals':len(actual),'optimized':bool(sys.flags.optimize),'explicit_exceptions':['MANIFEST.json']}
def main():
 a=argparse.ArgumentParser();a.add_argument('--root',type=Path,default=Path(__file__).absolute().parent);a.add_argument('--input-root',type=Path,required=True);a.add_argument('--expected-manifest-sha256',required=True);a.add_argument('--expected-checker-sha256',required=True);x=a.parse_args()
 try:r=verify(x.root.absolute(),x.input_root.absolute(),x.expected_manifest_sha256,x.expected_checker_sha256)
 except Exception as e:print(json.dumps({'result':'FAIL','error':str(e)},sort_keys=True));return 1
 print(json.dumps(r,sort_keys=True));return 0
if __name__=='__main__':sys.exit(main())

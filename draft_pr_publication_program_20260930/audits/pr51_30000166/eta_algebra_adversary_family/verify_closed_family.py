#!/usr/bin/env python3
"""ROOT-invoked complete, read-only postclosure family check."""
from pathlib import Path
import argparse,hashlib,json,stat
F=Path(__file__).resolve().parent
M=F/'SELF_MANIFEST.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def strict(p):
 def pairs(xs):
  d={}
  for k,v in xs:
   if k in d:raise ValueError('duplicate key: '+k)
   d[k]=v
  return d
 return json.loads(p.read_bytes(),object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--manifest-sha256',required=True);a=ap.parse_args()
 assert not M.is_symlink() and M.is_file() and sha(M.read_bytes())==a.manifest_sha256 and stat.S_IMODE(M.stat().st_mode)==0o444
 r=strict(M);assert r['schema']=='pr51-eta-algebra-adversary-self-only-closure/v1' and type(r['files_count']) is int and r['files_count']==len(r['files'])==23 and r['root_acceptance_or_merge_authority'] is False
 expected=set()
 for row in r['files']:
  assert set(row)=={'path','bytes','sha256','mode'} and type(row['bytes']) is int and row['bytes']>=0 and row['mode']=='0o444'
  n=row['path'];assert isinstance(n,str) and n not in expected and not Path(n).is_absolute() and '..' not in Path(n).parts;expected.add(n)
  p=F/n;assert p.is_file() and not p.is_symlink();b=p.read_bytes()
  assert len(b)==row['bytes'] and sha(b)==row['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444
 actual=set();dirs={''}
 for p in F.rglob('*'):
  assert not p.is_symlink()
  if p.is_file():actual.add(str(p.relative_to(F)))
  elif p.is_dir():dirs.add(str(p.relative_to(F)))
  else:raise AssertionError('nonregular family member')
 assert actual==expected|{'SELF_MANIFEST.json'}
 assert r['self_excluded']==[{'path':'SELF_MANIFEST.json','mode':'0o444'}]
 declared=set()
 for row in r['directories']:
  assert set(row)=={'path','mode'} and row['mode']=='0o555' and row['path'] not in declared;declared.add(row['path'])
  assert stat.S_IMODE((F/row['path']).stat().st_mode)==0o555
 assert declared==dirs=={'','exact_checks_capture','original_helper_capture'}
 root=Path('/Users/alec/Documents/Math');inputs=strict(F/'FULL_INPUT_BINDINGS.json')['files'];assert len(inputs)==15
 for row in inputs:
  p=root/row['path'];assert p.is_file() and not p.is_symlink();b=p.read_bytes()
  assert len(b)==row['bytes'] and sha(b)==row['sha256'] and oct(stat.S_IMODE(p.stat().st_mode))==row['mode']=='0o444'
 print(json.dumps({'status':'PASS','manifest_sha256':a.manifest_sha256,'full_payload_read_count':len(expected),'full_original_input_read_count':len(inputs),'all_declared_modes_verified':True,'scope':'Read-only self-family closure; no merge authority'},indent=2))
if __name__=='__main__':main()

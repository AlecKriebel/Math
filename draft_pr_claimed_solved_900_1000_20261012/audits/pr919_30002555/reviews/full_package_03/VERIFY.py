#!/usr/bin/env python3
"""Authenticate this self-excluded curated map using an externally supplied seal."""
import argparse,hashlib,json,pathlib,re,stat
R=pathlib.Path(__file__).resolve().parent
def need(v,s):
 if not v:raise RuntimeError(s)
def strict(raw):
 def pairs(items):
  d={}
  for k,v in items:need(k not in d,'duplicate JSON');d[k]=v
  return d
 return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda _:(_ for _ in ()).throw(RuntimeError('nonfinite JSON')))
def verify(expected):
 need(type(expected) is str and re.fullmatch('[0-9a-f]{64}',expected),'external seal required');p=R/'MANIFEST.json';need(stat.S_ISREG(p.lstat().st_mode),'manifest must be regular');raw=p.read_bytes();need(hashlib.sha256(raw).hexdigest()==expected,'external seal mismatch');m=strict(raw)
 need(m['self_excluded']=='MANIFEST.json' and m['pr']==919 and m['problem_id']=='30002555','wrong manifest target');names=m['explicit_public_allowlist'];need(type(names) is list and len(names)==len(set(names)) and set(names)==set(m['files']) and 'MANIFEST.json' not in names,'invalid explicit map')
 for n,r in m['files'].items():
  q=pathlib.PurePosixPath(n);need(type(n) is str and not q.is_absolute() and q.as_posix()==n and all(x not in ('','.','..') for x in n.split('/')) and '\\' not in n,'unsafe member');p=R/n;need(stat.S_ISREG(p.lstat().st_mode),'nonregular member');raw=p.read_bytes();need(type(r) is dict and set(r)=={'bytes','sha256'} and type(r['bytes']) is int and r['bytes']==len(raw) and r['sha256']==hashlib.sha256(raw).hexdigest(),'member drift '+n)
 actual=set()
 for p in R.rglob('*'):
  rel=p.relative_to(R)
  if rel.parts[0] in ['private','__pycache__']:continue
  if p.is_dir():need(not p.is_symlink(),'linked public directory');continue
  need(stat.S_ISREG(p.lstat().st_mode),'nonregular public entry');actual.add(rel.as_posix())
 need(actual==set(names)|{'MANIFEST.json'},'unlisted public bytes')
 return {'status':'PASS','pr':919,'problem_id':'30002555','manifest_sha256':expected,'curated_public_files':len(names),'scope':'Byte identity only; no mathematical, priority, human-review or security certification.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--expected-manifest',required=True);a=p.parse_args();print(json.dumps(verify(a.expected_manifest),indent=2))

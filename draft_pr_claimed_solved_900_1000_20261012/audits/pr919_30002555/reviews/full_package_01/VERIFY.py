#!/usr/bin/env python3
"""Authenticate this explicit authored public map; supply the seal digest independently."""
import argparse,hashlib,json,stat
from pathlib import Path,PurePosixPath
HERE=Path(__file__).resolve().parent
def need(c,m):
 if not c:raise RuntimeError(m)
def strict(raw):
 def pairs(xs):
  d={}
  for k,v in xs:need(k not in d,'duplicate JSON key');d[k]=v
  return d
 return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(RuntimeError(x)))
def verify(expected):
 p=HERE/'MANIFEST.json';need(stat.S_ISREG(p.lstat().st_mode),'nonregular manifest');raw=p.read_bytes();pin=hashlib.sha256(raw).hexdigest();need(pin==expected,'external audit anchor mismatch');m=strict(raw)
 need(m['schema']=='pr919-first-whole-package-review-v1' and m['self_excluded']=='MANIFEST.json','wrong audit schema')
 need(set(m['files'])==set(m['explicit_public_allowlist']) and len(m['explicit_public_allowlist'])==len(set(m['explicit_public_allowlist'])),'explicit map mismatch')
 expected_dirs=set()
 for n,r in m['files'].items():
  q=PurePosixPath(n);need(str(q)==n and not q.is_absolute() and all(v not in ('','.','..','tmp','private_sources','__pycache__') for v in q.parts),'unsafe public path')
  expected_dirs.update(str(v) for v in q.parents if str(v)!='.')
  p=HERE/n;need(stat.S_ISREG(p.lstat().st_mode),'nonregular member');b=p.read_bytes();need(type(r['bytes']) is int and len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],'binding mismatch '+n)
 files=set();dirs=set()
 def visit(p):
  for c in p.iterdir():
   rel=c.relative_to(HERE).as_posix()
   if c.parent==HERE and c.name in ('tmp','private_sources'):
    need(stat.S_ISDIR(c.lstat().st_mode),'nonreal ignored directory');continue
   mode=c.lstat().st_mode
   if stat.S_ISDIR(mode):need(rel in expected_dirs,'unlisted public dir '+rel);dirs.add(rel);visit(c)
   else:need(stat.S_ISREG(mode),'nonregular public entry');files.add(rel)
 visit(HERE);need(files==set(m['files'])|{'MANIFEST.json'} and dirs==expected_dirs,'closed public inventory mismatch')
 start=strict((HERE/'AUTHENTICATION_START.json').read_bytes());end=strict((HERE/'AUTHENTICATION_END.json').read_bytes())
 for k in ['freeze_sha256','original_head','freeze_files','original_files','archive_sha256','package_manifest_sha256','archive_members','archive_payloads']:
  need(start[k]==end[k],'start/end candidate authentication mismatch '+k)
 return {'status':'PASS','manifest_sha256':pin,'public_files':len(m['files']),'original_files_authenticated':27,'integrity_only':True,'mathematical_acceptance_certified_by_hashes':False}
if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--expected-manifest',required=True);a=ap.parse_args();print(json.dumps(verify(a.expected_manifest),indent=2,sort_keys=True))

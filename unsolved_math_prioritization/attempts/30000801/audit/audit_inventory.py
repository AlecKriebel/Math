#!/usr/bin/env python3
"""Strict safe-audit inventory validation; the manifest is not a signature."""
import sys
sys.dont_write_bytecode=True
import argparse
import hashlib
import json
from pathlib import Path
FILES={'README.md','INDEPENDENT_AUDIT.md','MATHEMATICAL_AUDIT.md','PUBLIC_SOURCE_VERIFICATION.json','RESULTS.json','independent_verify.py','independent_adversarial.py','audit_inventory.py','requirements.txt'}
def require(ok,msg):
 if not ok:raise ValueError(msg)
def parse(raw):
 def unique(pairs):
  d={}
  for k,v in pairs:
   require(k not in d,'duplicate JSON key');d[k]=v
  return d
 return json.loads(raw,object_pairs_hook=unique)
def verify(root):
 paths=list(root.iterdir())
 require(not any(p.is_symlink() for p in paths),'symlink audit payload')
 require(all(p.is_file() for p in paths),'non-file audit payload')
 require({p.name for p in paths}==FILES|{'MANIFEST.json'},'missing/extra audit member')
 m=parse((root/'MANIFEST.json').read_bytes())
 require(set(m)=={'schema','files'} and m['schema']=='sha256-byte-inventory-v1','audit manifest schema')
 require(set(m['files'])==FILES,'audit manifest members')
 for name in sorted(FILES):
  b=(root/name).read_bytes()
  require(m['files'][name]=={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()},'audit integrity: '+name)
 return {'status':'PASS','file_count':len(FILES)+1,'full_resolution':False}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent);a=p.parse_args()
 print(json.dumps(verify(a.root),sort_keys=True))
if __name__=='__main__':
 try:main()
 except Exception as e:
  print(json.dumps({'status':'FAIL','error':str(e)}),file=sys.stderr);sys.exit(1)

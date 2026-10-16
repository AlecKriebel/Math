#!/usr/bin/env python3
"""Check this review's explicit public map against an independent external digest."""
import hashlib,json,re,stat,sys
from pathlib import Path,PurePosixPath
D=Path(__file__).resolve().parent
IGNORED={'tmp','__pycache__','reviewed_code/tmp','reviewed_helpers/audits'}
def need(x,s):
 if not x:raise RuntimeError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 need(len(sys.argv)==2 and re.fullmatch('[0-9a-f]{64}',sys.argv[1]),'Supply external review manifest SHA256');p=D/'MANIFEST.json';need(stat.S_ISREG(p.lstat().st_mode),'manifest nonregular');b=p.read_bytes();need(sha(b)==sys.argv[1],'external manifest anchor');m=json.loads(b);need(m['self_excluded']=='MANIFEST.json','self exclusion');records=m['files'];allowed=m['explicit_public_allowlist'];need(type(records) is dict and type(allowed) is list and len(allowed)==len(set(allowed)) and set(allowed)==set(records) and 'MANIFEST.json' not in allowed,'allowlist')
 for n,r in records.items():
  q=PurePosixPath(n);need(q.as_posix()==n and not q.is_absolute() and all(x not in ('','.','..') for x in n.split('/')) and '\\' not in n,'unsafe path');p=D/n;need(stat.S_ISREG(p.lstat().st_mode),'nonregular public member '+n);b=p.read_bytes();need(type(r['bytes']) is int and r=={'bytes':len(b),'sha256':sha(b)},'member '+n)
 found=set()
 def visit(p):
  for x in p.iterdir():
   n=x.relative_to(D).as_posix();mode=x.lstat().st_mode
   if n in IGNORED:need(stat.S_ISDIR(mode),'ignored non-directory');continue
   if stat.S_ISDIR(mode):visit(x)
   else:need(stat.S_ISREG(mode),'nonregular own entry');found.add(n)
 visit(D);need(found==set(allowed)|{'MANIFEST.json'},'public inventory mismatch')
 print(json.dumps({'status':'PASS_REVIEW_SEAL','manifest_sha256':sys.argv[1],'public_files':len(records),'scope':'Artifact identity only, not proof/priority certification'},indent=2))
if __name__=='__main__':main()

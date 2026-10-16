"""Read-only authored closure/history check. Optional --current-inputs checks live input bytes."""
from pathlib import Path, PurePosixPath
import argparse,hashlib,json,stat
ROOT=Path(__file__).resolve().parent

def require(v,m):
 if not v:raise ValueError(m)
def ident(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def safe(n):
 require(isinstance(n,str) and n and '\\' not in n and not PurePosixPath(n).is_absolute() and all(x not in ('','.','..') for x in n.split('/')),'unsafe authored path')
 return n
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--current-inputs',action='store_true');args=ap.parse_args()
 raw=(ROOT/'MANIFEST.json').read_bytes();m=json.loads(raw);rows=m['authored_files'];listed={}
 for row in rows:
  n=safe(row['path']);require(n!='MANIFEST.json' and n not in listed,'duplicate/self authored path');listed[n]=row
 actual={};dirs=set()
 for p in ROOT.rglob('*'):
  s=p.lstat();n=p.relative_to(ROOT).as_posix();require(not stat.S_ISLNK(s.st_mode),'authored symlink')
  if stat.S_ISDIR(s.st_mode):dirs.add(n)
  else:
   require(stat.S_ISREG(s.st_mode),'authored special');actual[n]=p
 require(set(actual)==set(listed)|{'MANIFEST.json'},'authored inventory mismatch')
 expected_dirs={p.as_posix() for n in actual for p in PurePosixPath(n).parents if p.as_posix()!='.'};require(dirs==expected_dirs,'authored empty directory')
 for n,row in listed.items():require(ident(actual[n].read_bytes())=={k:row[k] for k in ('bytes','sha256')},'authored bytes changed: '+n)
 require(len(listed)==m['authored_file_count'],'authored count')
 history=json.loads((ROOT/'CHECKED_INPUTS.json').read_bytes());require(history['before']==history['after'] and len(history['before'])==6,'frozen before/after history differs')
 current='NOT_CHECKED_AUTHORED_HISTORY_ONLY'
 if args.current_inputs:
  for row in history['after']:require(ident(Path(row['path']).read_bytes())=={k:row[k] for k in ('bytes','sha256')},'current publication differs from this historical review: '+row['path'])
  current='MATCHES_REVIEWED_SIX'
 print(json.dumps({'status':'PASS_AUTHORED_CLOSURE_AND_REVIEWED_INPUT_HISTORY','authored_files':len(listed),'manifest_sha256':ident(raw)['sha256'],'closed_at_utc':m['closed_at_utc'],'current_publication_inputs':current,'scope':'Integrity/history only; no theorem or authenticity certificate. A later current-publication change does not invalidate authored-only historical closure.'},indent=2))
if __name__=='__main__':main()

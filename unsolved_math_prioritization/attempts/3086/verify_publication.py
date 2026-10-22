#!/usr/bin/env python3
"""Offline integrity and exact replay, with frozen author assertions enabled."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, json, os, stat, subprocess, sys, zipfile
ROOT = Path(__file__).resolve().parent
ARCHIVES = {
 'author': ('UNIT_SQUARE_3086_AUTHOR_SAFE_FREEZE.zip',15344,'61b8680c989c6eec5574b818781b217b038349f222ab2089d6678a7a1eaffae3'),
 'audit': ('UNIT_SQUARE_3086_INDEPENDENT_AUDIT_SAFE_FREEZE.zip',16088,'00608c8528dfd2c8926771a152daf7b7647bffe81ed80819e012fced64b18269')}
def need(ok, message):
 if not ok: raise RuntimeError(message)
def digest(b): return hashlib.sha256(b).hexdigest()
def pairs(items):
 d={}
 for k,v in items:
  need(k not in d,'Duplicate JSON key: '+k);d[k]=v
 return d
def read_json(p):return json.loads(p.read_text(encoding='utf-8'),object_pairs_hook=pairs)
def safe(s):
 need(isinstance(s,str) and s and '\\' not in s,'Invalid path')
 p=PurePosixPath(s)
 need(not p.is_absolute() and '..' not in p.parts and '.' not in p.parts and str(p)==s,'Unsafe path: '+s)
 return s
def inventory(root):
 files=set();dirs=set()
 for p in root.rglob('*'):
  name=p.relative_to(root).as_posix()
  need(not p.is_symlink(),'Symlink: '+name)
  if p.is_file(): files.add(name)
  elif p.is_dir(): dirs.add(name)
  else: raise RuntimeError('Special file: '+name)
 return files,dirs
def manifest(root,name):
 m=read_json(root/name);entries=m['files'];names=[safe(e['path']) for e in entries]
 need(len(names)==len(set(names)),'Duplicate manifest path')
 expected=set(names)|{name};actual,dirs=inventory(root)
 expected_dirs={q.as_posix() for s in expected for q in PurePosixPath(s).parents if q.as_posix()!='.'}
 need(actual==expected,'File inventory mismatch: '+str(actual^expected))
 need(dirs==expected_dirs,'Directory inventory mismatch: '+str(dirs^expected_dirs))
 for e in entries:
  b=(root/e['path']).read_bytes()
  need(len(b)==e['bytes'] and digest(b)==e['sha256'],'File digest mismatch: '+e['path'])
 return len(expected)
def archive_check(folder,record):
 name,size,sha=record;p=ROOT/'archives'/name;b=p.read_bytes()
 need(len(b)==size and digest(b)==sha,'Original archive digest mismatch: '+name)
 with zipfile.ZipFile(p) as z:
  members=z.infolist();names=[safe(i.filename) for i in members]
  need(len(names)==len(set(names)),'Repeated ZIP member')
  files,_=inventory(ROOT/folder);need(set(names)==files,'Archive membership mismatch')
  for i in members:
   need(not i.is_dir() and not stat.S_ISLNK(i.external_attr>>16),'Unsafe ZIP entry')
   need(z.read(i)==(ROOT/folder/i.filename).read_bytes(),'Archive member mismatch: '+i.filename)
 return len(names)
def replay(folder,script,expected=None,optimized=False):
 p=ROOT/folder/script
 # -I ignores PYTHONOPTIMIZE and other inherited PYTHON* settings.
 # Normal children do not inherit the parent interpreter's -O flag.
 command=[sys.executable,'-I','-B']+(['-O'] if optimized else [])
 guard='' if optimized else "if not __debug__: raise RuntimeError('Assertions disabled')\n"
 command+=['-c',"import runpy,sys\n"+guard+"runpy.run_path(sys.argv[1],run_name='__main__')",str(p)]
 done=subprocess.run(command,cwd=ROOT,capture_output=True,check=False,timeout=120)
 need(done.returncode==0,'Replay failed: '+script+' '+done.stderr.decode(errors='replace'))
 if expected:need(done.stdout==(ROOT/folder/expected).read_bytes(),'Exact result mismatch: '+script)
 return {'script':folder+'/'+script,'optimized':optimized,'sha256_stdout':digest(done.stdout)}
def queue_check(path,v):
 b=path.read_bytes();q=v['queue'];need(len(b)==q['after_bytes'] and digest(b)==q['after_sha256'],'Queue digest mismatch')
 lines=b.splitlines(keepends=True);ids=[i for i,l in enumerate(lines) if b'| 3086 / OPG-37327 |' in l]
 need(len(ids)==1,'Target queue row count');i=ids[0];cells=lines[i].split(b'|')
 need(i+1==q['physical_line'] and cells[1].strip()==b'775','Wrong queue rank or line')
 need(cells[8]==b' unsolved ' and cells[9]==b' 4/5 ','Queue status/turns mismatch')
 cells[8]=b' queued ';cells[9]=b' 0/5 ';lines[i]=b'|'.join(cells);before=b''.join(lines)
 need(len(before)==q['before_bytes'] and digest(before)==q['before_sha256'],'Other queue bytes changed')
 return 'PASS: only target Status and Turns changed'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--queue',type=Path);args=ap.parse_args()
 count=manifest(ROOT,'PUBLICATION_MANIFEST.json');v=read_json(ROOT/'VERDICT.json')
 need(v['problem_id']==3086 and v['status']=='unsolved' and v['turns']=='4/5','Claim scope changed')
 need(v['original_all_n_conjecture_resolved'] is False and v['n4_conclusion_refuted'] is False and v['17_tile_cover_constructed'] is False,'Whole-target promotion')
 members=sum(archive_check(k,r) for k,r in ARCHIVES.items())
 author_count=manifest(ROOT/'author','manifest.json');audit_count=manifest(ROOT/'audit','manifest.json')
 runs=[replay('author','check_manifest.py'),replay('author','verify.py','results.json'),replay('audit','verify_manifest.py'),replay('audit','independent_check.py','independent_results.json'),replay('audit','independent_check.py','independent_results.json',True)]
 report={'status':'PASS','problem_id':3086,'scope':'Unsolved 4/5; local-lemma counterexample and audited partials only','publication_files':count,'author_files':author_count,'audit_files':audit_count,'original_archive_members':members,'author_assertions_enabled':True,'replays':runs,'queue':queue_check(args.queue,v) if args.queue else 'Not requested; use --queue for exact two-cell comparison'}
 print(json.dumps(report,indent=2,sort_keys=True))
if __name__=='__main__':main()

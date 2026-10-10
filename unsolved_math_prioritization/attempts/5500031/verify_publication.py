#!/usr/bin/env python3
"""Offline integrity and exact replay, with frozen author assertions enabled."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, json, os, stat, subprocess, sys, zipfile
ROOT = Path(__file__).resolve().parent
ARCHIVES = {
 'author': ('SEGMENT_MIRRORS_5500031_AUTHOR_SAFE_FREEZE.zip',18796,'7112c0fff3aaf9cbbd429af541d1e08b30677a380155382e5b96095e02ff57dd'),
 'audit': ('SEGMENT_MIRRORS_5500031_INDEPENDENT_AUDIT.zip',22659,'e3efa8877de3c832972d22d1d9132694c595291bbe1dc07e342f4742dbea328a')}
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
def replay(folder,script,expected=None,args=()):
 p=ROOT/folder/script
 # -I ignores inherited PYTHONOPTIMIZE; do not propagate the wrapper's -O.
 guard="import runpy,sys\nif not __debug__: raise RuntimeError('Assertions disabled')\nsys.argv=sys.argv[1:]\nrunpy.run_path(sys.argv[0],run_name='__main__')"
 command=[sys.executable,'-I','-B','-c',guard,str(p)]+[str(x) for x in args]
 done=subprocess.run(command,cwd=ROOT,capture_output=True,check=False,timeout=180)
 need(done.returncode==0,'Replay failed: '+script+' '+done.stderr.decode(errors='replace'))
 if expected:need(done.stdout==(ROOT/folder/expected).read_bytes(),'Exact result mismatch: '+script)
 return json.loads(done.stdout),{'script':folder+'/'+script,'assertions_enabled':True,'sha256_stdout':digest(done.stdout),'frozen_result_byte_identical':True if expected else 'Not compared to historical full-provenance result'}
def queue_check(path,v):
 b=path.read_bytes();q=v['queue'];need(len(b)==q['after_bytes'] and digest(b)==q['after_sha256'],'Queue digest mismatch')
 lines=b.splitlines(keepends=True);ids=[i for i,l in enumerate(lines) if b'| 5500031 / AMR-054-0031 |' in l]
 need(len(ids)==1,'Target queue row count');i=ids[0];cells=lines[i].split(b'|')
 need(i+1==q['physical_line'] and cells[1].strip()==b'776','Wrong queue rank or line')
 need(cells[8]==b' unsolved ' and cells[9]==b' 5/5 ','Queue status/turns mismatch')
 cells[8]=b' queued ';cells[9]=b' 0/5 ';lines[i]=b'|'.join(cells);before=b''.join(lines)
 need(len(before)==q['before_bytes'] and digest(before)==q['before_sha256'],'Other queue bytes changed')
 return 'PASS: only target Status and Turns changed'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--queue',type=Path);args=ap.parse_args()
 count=manifest(ROOT,'PUBLICATION_MANIFEST.json');v=read_json(ROOT/'VERDICT.json')
 need(v['problem_id']==5500031 and v['status']=='unsolved' and v['turns']=='5/5','Claim scope changed')
 need(v['unrestricted_problem_resolved'] is False and v['mathematical_correction_required'] is False,'Scope or audit changed')
 need(v['mandatory_nondestructive_addendum']=='audit/ADDENDUM.md','Required addendum missing')
 members=sum(archive_check(k,r) for k,r in ARCHIVES.items())
 ac=manifest(ROOT/'author','MANIFEST.json');ic=manifest(ROOT/'audit','MANIFEST.json')
 a,ar=replay('author','verify.py','check_results.json')
 i,ir=replay('audit','independent_verify.py','independent_results.json')
 f,fr=replay('audit','verify_artifacts.py',args=['--author-package',ROOT/'author','--author-zip',ROOT/'archives'/ARCHIVES['author'][0]])
 need(a['status']==i['status']==f['status']=='PASS','Replay status')
 need(a['assertions']==20012 and i['assertions']==58598,'Assertion count mismatch')
 need(i['concurrent_singular_trace_count']==6 and i['concurrent_trace_count']==840,'Singular-control scope mismatch')
 cert=dict(i['box_escape_certificate']);need(cert.pop('singular') is False,'Certificate not regular')
 need(cert==a['box_escape_certificate'],'Independent certificate mismatch')
 need(f['author_freeze']['exact_assertions']==20012 and f['independent_replay']['exact_assertions']==58598,'Artifact replay mismatch')
 need(f['author_freeze']['relocated_replay_byte_identical'] is True and f['independent_replay']['byte_identical'] is True,'Relocated frozen replay mismatch')
 need('provenance' not in f,'Unexpected provenance claim without optional inputs')
 report={'status':'PASS','problem_id':5500031,'scope':'Unsolved 5/5; independently audited partial claims with mandatory addendum','publication_files':count,'author_files':ac,'audit_files':ic,'original_archive_members':members,'all_frozen_assertions_enabled':True,'author_assertions':a['assertions'],'independent_assertions':i['assertions'],'independent_concurrent_singular_controls':6,'certificate_matches':True,'replays':[ar,ir,fr],'optional_external_provenance':{'status':'NOT_RUN','reason':'The nine optional external provenance inputs are not supplied. Historical full-provenance result is preserved without claiming a fresh identical replay.'},'queue':queue_check(args.queue,v) if args.queue else 'NOT_RUN: supply --queue for exact two-cell comparison'}
 print(json.dumps(report,indent=2,sort_keys=True))
if __name__=='__main__':main()

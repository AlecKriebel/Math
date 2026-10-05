#!/usr/bin/env python3
"""Offline integrity and exact replay, with frozen author assertions enabled."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, json, os, stat, subprocess, sys, zipfile
ROOT = Path(__file__).resolve().parent
ARCHIVES = {
 'author': ('CONICAL_BICOMBINGS_30004730_AUTHOR_SAFE_FREEZE.zip',19194,'4e7599d44d08aa72106fd94b91d12faea77d4b4e2c80dad1c6dbb87277f38334'),
 'audit': ('CONICAL_BICOMBINGS_30004730_INDEPENDENT_AUDIT_SAFE.zip',20546,'47c0a5b1674fbc411537d60f13cf7a176720fd396e0d07ba271d668e0e80ae8b')}
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
 return json.loads(done.stdout),{'script':folder+'/'+script,'assertions_enabled':True,'sha256_stdout':digest(done.stdout),'stdout_comparison':'Frozen reference bytes match' if expected else 'No raw stdout comparison; caller checks structured results'}
def queue_check(path,v):
 b=path.read_bytes();q=v['queue'];need(len(b)==q['after_bytes'] and digest(b)==q['after_sha256'],'Queue digest mismatch')
 lines=b.splitlines(keepends=True);ids=[i for i,l in enumerate(lines) if b'| 30004730 / OWR-8415335-002 |' in l]
 need(len(ids)==1,'Target queue row count');i=ids[0];cells=lines[i].split(b'|')
 need(i+1==q['physical_line'] and cells[1].strip()==b'783','Wrong queue rank or line')
 need(cells[8]==b' unsolved ' and cells[9]==b' 5/5 ','Queue status/turns mismatch')
 cells[8]=b' queued ';cells[9]=b' 0/5 ';lines[i]=b'|'.join(cells);before=b''.join(lines)
 need(len(before)==q['before_bytes'] and digest(before)==q['before_sha256'],'Other queue bytes changed')
 return 'PASS: only target Status and Turns changed'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--queue',type=Path);ap.add_argument('--integrity-only',action='store_true');args=ap.parse_args()
 count=manifest(ROOT,'PUBLICATION_MANIFEST.json');v=read_json(ROOT/'VERDICT.json')
 need(v['problem_id']==30004730 and v['status']=='unsolved' and v['turns']=='5/5','Claim scope changed')
 need(v['original_problem_resolved'] is False and v['mathematical_correction_required'] is False,'Scope or audit changed')
 supplement=read_json(ROOT/v['mandatory_metadata_addendum'])
 need(supplement['review_sha256']=='640a06a3fb07d9ffe0e56d4eca4f50420255e54dcd53ab02b926c6880be0883b','Review hash supplement mismatch')
 need(supplement['source_date_conflict']['header_version_date']=='2025-05-11' and supplement['source_date_conflict']['internal_manuscript_date']=='2026-08-24','Date discrepancy lost')
 members=sum(archive_check(k,r) for k,r in ARCHIVES.items())
 ac=manifest(ROOT/'author','MANIFEST.json');ic=manifest(ROOT/'audit','AUDIT_MANIFEST.json')
 queue=queue_check(args.queue,v) if args.queue else 'NOT_RUN: supply --queue for exact two-cell comparison'
 if args.integrity_only:
  print(json.dumps({'status':'PASS','integrity_only':True,'publication_files':count,'archive_members':members,'queue':queue},indent=2,sort_keys=True));return
 a,ar=replay('author','verify.py','../audit/author_replay.json')
 i,ir=replay('audit','independent_checks.py')
 f,fr=replay('audit','provenance_check.py',args=['--author-zip',ROOT/'archives'/ARCHIVES['author'][0]])
 need(a['status']==i['status']==f['status']=='PASS','Replay status')
 need(a['finite_checks']==read_json(ROOT/'author/verification_results.json'),'Frozen author result mismatch')
 need(i['independent_checks']==read_json(ROOT/'audit/independent_results.json'),'Frozen independent result mismatch')
 need(a['finite_checks']['counts']['conical_inequalities']==253125,'Author conical count mismatch')
 need(i['independent_checks']['counts']['cross_mesh_interpolation_equalities']==36400,'Independent cross-mesh count mismatch')
 need(set(f['checks'])=={'author'} and f['checks']['author']['members']==7,'Provenance replay scope mismatch')
 report={'status':'PASS','problem_id':30004730,'scope':'Unsolved 5/5; independently audited scoped partials; mandatory metadata addendum included','publication_files':count,'author_files':ac,'audit_files':ic,'original_archive_members':members,'all_frozen_assertions_enabled':True,'frozen_author_result_matches':True,'frozen_independent_result_matches':True,'replays':[ar,ir,fr],'optional_external_provenance':{'status':'NOT_RUN','reason':'Full corpora, catalog, dataset manifest and source PDFs were not supplied. Preserved historical audit evidence is not a fresh external-input replay.'},'queue':queue}
 print(json.dumps(report,indent=2,sort_keys=True))
if __name__=='__main__':main()

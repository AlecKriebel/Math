#!/usr/bin/env python3
"""ROOT-only self closure; actual outside capture/readback must follow this child exit."""
import argparse, datetime as dt, hashlib, json, os, re, stat
from pathlib import Path, PurePosixPath
F=Path(__file__).absolute().parent; R=F.parents[3]
def sha(b): return hashlib.sha256(b).hexdigest()
def need(x,m):
 if not x: raise ValueError(m)
def scan():
 files={}; dirs=set()
 for p in F.rglob('*'):
  need(not p.is_symlink(),'No symlink'); n=p.relative_to(F).as_posix(); need(not {'.git','__pycache__','..'}.intersection(PurePosixPath(n).parts),'Safe path')
  if p.is_file(): files[n]=p.read_bytes()
  else: need(stat.S_ISDIR(p.stat().st_mode),'No special members'); dirs.add(n)
 need(dirs=={q.as_posix() for n in files for q in PurePosixPath(n).parents if str(q)!='.'},'No extra/empty directory')
 return files,dirs
def inputs():
 o=json.loads((F/'INPUT_BINDINGS.json').read_bytes()); need(type(o['files_count']) is int and o['files_count']==len(o['files']),'Complete input list')
 for r in o['files']:
  p=R/r['path']; need(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'Regular input'); b=p.read_bytes()
  need(len(b)==r['bytes'] and sha(b)==r['sha256'] and stat.S_IMODE(p.stat().st_mode)==r['full_mode'],'Input changed')
parser=argparse.ArgumentParser(); parser.add_argument('--expected-report-sha256',required=True); args=parser.parse_args()
need(__debug__ and os.environ.get('PYTHONOPTIMIZE','') in ('','0'),'Unoptimized closure')
need(F.name=='current_source_adversary_family_v2' and R==Path('/Users/alec/Documents/Math'),'Exact anchor')
need(re.fullmatch('[0-9a-f]{64}',args.expected_report_sha256) and sha((F/'REPORT.md').read_bytes())==args.expected_report_sha256,'Exact report pin')
need(not (F/'SELF_MANIFEST.json').exists(),'Sole self manifest absent'); inputs()
files,dirs=scan()
for n in files: (F/n).chmod(0o444)
verdict=json.loads((F/'VERDICT.json').read_bytes()); need(verdict['mandatory_corrections']==[] and verdict['future_acceptance_approved'] is False,'Clean SOURCE without future acceptance')
members=[{'path':n,'bytes':len(b),'sha256':sha(b),'full_mode':0o444} for n,b in sorted(files.items())]
manifest={'schema':'pr47-source-v2-independent-self-only-closure/v1','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_closing_child_pid':os.getpid(),'files_count':len(members),'files':members,'directories':sorted(dirs),'self_excluded':['SELF_MANIFEST.json'],'full_permission_mode':'0444','closed_clean':True,'mandatory_corrections_count':0,'SOURCE_review_only':True,'production_import_compile_execution':False,'foreign_bodies_copied':False,'future_acceptance_approved':False,'current_freeze_or_merge_approved':False,'external_completed_closing_capture_required_AFTER_child_exit':True}
b=(json.dumps(manifest,indent=2)+'\n').encode()
with (F/'SELF_MANIFEST.json').open('xb') as h: h.write(b); h.flush(); os.fsync(h.fileno())
(F/'SELF_MANIFEST.json').chmod(0o444)
final,finaldirs=scan(); need(set(final)==set(files)|{'SELF_MANIFEST.json'} and finaldirs==dirs,'Exact final topology')
for n,old in files.items(): need(final[n]==old and stat.S_IMODE((F/n).stat().st_mode)==0o444,'Final bytes/full0444')
need(final['SELF_MANIFEST.json']==b and stat.S_IMODE((F/'SELF_MANIFEST.json').stat().st_mode)==0o444,'Final self bytes/full0444'); inputs()
print(json.dumps({'status':'CLOSED_CLEAN_SOURCE_V2_ONLY','manifest_sha256':sha(b),'files_count':len(members),'relative_directories':len(dirs),'actual_closing_child_pid':os.getpid(),'future_acceptance_approved':False},indent=2))

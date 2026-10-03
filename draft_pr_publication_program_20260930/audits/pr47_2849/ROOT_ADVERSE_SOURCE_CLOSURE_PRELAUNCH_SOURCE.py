#!/usr/bin/env python3
"""ROOT executes only after explicit readiness. Own first-party family closure only."""
from pathlib import Path, PurePosixPath
import datetime as dt, hashlib, json, os, stat, sys
assert __debug__ and not sys.flags.optimize
F=Path(__file__).absolute().parent; A=F.parent; R=A.parents[2]; name='SELF_MANIFEST.json'
assert F.name=='current_source_adversary_family' and A.name=='pr47_2849' and not (F/name).exists()
def sha(b): return hashlib.sha256(b).hexdigest()
def raw(p):
    assert not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode)
    return p.read_bytes()
verdict=json.loads(raw(F/'VERDICT.json')); report=raw(F/'REPORT.md')
assert verdict['verdict']=='REPAIR_REQUIRED_GENUINE_GIT_NULL_SOURCE_CONTRACT' and verdict['closed_clean'] is False and len(verdict['mandatory_corrections'])==1 and verdict['mandatory_corrections'][0]['line']==150
assert len(report)==verdict['report']['bytes'] and sha(report)==verdict['report']['sha256']
c=json.loads(raw(F/'CONTROL_RESULTS.json')); extended=json.loads(raw(F/'EXTENDED_CONTROL_RESULTS.json')); receipts=json.loads(raw(F/'CLOSURE_CAPTURE_VALIDATION.json'))
assert c['assertions']==31733 and extended['assertions']==93 and c['unique_full_fixed_body_reads']==919 and c['production_import_compile_execute'] is False and c['mathematical_helpers_run'] is False
for r in c['complete_readback_rows']+receipts['external_full_bindings']:
    assert type(r['path']) is str and not PurePosixPath(r['path']).is_absolute() and '..' not in PurePosixPath(r['path']).parts
    p=R/r['path']; b=raw(p)
    assert type(r['bytes']) is int and len(b)==r['bytes'] and sha(b)==r['sha256'] and type(r['full_mode']) is int and stat.S_IMODE(p.stat().st_mode)==r['full_mode']
files=[]; directories=[]
for p in sorted(F.rglob('*')):
    assert not p.is_symlink(); n=p.relative_to(F).as_posix(); assert not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts and '.git' not in PurePosixPath(n).parts and '__pycache__' not in PurePosixPath(n).parts
    if stat.S_ISDIR(p.stat().st_mode): directories.append(n); continue
    assert stat.S_ISREG(p.stat().st_mode) and p.suffix.lower() not in {'.pdf','.sqlite','.png','.jpg','.webp'}
    b=raw(p); p.chmod(0o444); assert stat.S_IMODE(p.stat().st_mode)==0o444
    files.append({'path':n,'bytes':len(b),'sha256':sha(b),'full_mode':0o444})
assert set(directories)=={q.as_posix() for r in files for q in PurePosixPath(r['path']).parents if str(q)!='.'}
manifest={'schema':'pr47-current-source-adversary-self-only-closure/v1','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_closing_child_pid':os.getpid(),'files_count':len(files),'files':files,'directories':directories,'self_excluded':[name],'full_permission_mode':'0444','closed_clean':False,'mandatory_corrections_count':1,'current_freeze_or_merge_approved':False,'foreign_bodies_copied':False,'external_completed_closing_capture_required_after_child_exit':True}
with (F/name).open('xb') as h:h.write((json.dumps(manifest,indent=2)+'\n').encode());h.flush();os.fsync(h.fileno())
(F/name).chmod(0o444)
for r in files:
    p=F/r['path']; b=raw(p); assert len(b)==r['bytes'] and sha(b)==r['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444
assert stat.S_IMODE((F/name).stat().st_mode)==0o444
print(json.dumps({'status':'CLOSED_ADVERSE_SOURCE_FAMILY','files_count':len(files),'directories':len(directories),'manifest_sha256':sha(raw(F/name)),'report_sha256':sha(report),'actual_closing_child_pid':os.getpid(),'mandatory_corrections_count':1,'production_execution':False,'current_or_merge_acceptance':False},indent=2))

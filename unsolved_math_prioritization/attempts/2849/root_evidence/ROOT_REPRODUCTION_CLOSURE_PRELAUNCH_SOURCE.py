"""Freeze completed ROOT evidence only, with a separately captured closing child."""
from pathlib import Path,PurePosixPath
import datetime as dt,hashlib,json,os,stat,sys
A=Path(__file__).resolve().parent;R=A.parents[2];D=A/'root_original_actual_reproduction';A45=A.parent/'pr45_9900007'
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):
 assert p.is_file()and not p.is_symlink()and all(not q.is_symlink()for q in p.parents)
 return p.read_bytes()
def dump(o):return(json.dumps(o,indent=2,allow_nan=False)+'\n').encode()
def ref(p):
 b=read(p);return{'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b)}
assert __debug__ and not sys.flags.optimize and not(D/'MANIFEST.json').exists()
source=read(Path(__file__).resolve());(A/'ROOT_REPRODUCTION_CLOSURE_PRELAUNCH_SOURCE.py').write_bytes(source)
operations=[]
for name,pid,code in [('root_pr47_original_reproduction_actual_capture',22446,0),('root_pr47_full_raw_SQL_actual_capture',21423,0),('root_cover_algebra_closed_readback_actual_capture',12271,0),('root_gauge_geometry_verify_actual_capture',10989,0),('root_cover_algebra_closure_actual_capture',10982,1)]:
 origin=A45/name;cap=json.loads(read(origin/'CAPTURE.json'))
 assert{p.name for p in origin.iterdir()}=={'CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin'}
 assert type(cap['pid'])is int and cap['pid']==pid and type(cap['exit_code'])is int and cap['exit_code']==code
 assert cap['actual_execution']is True and cap['completed']is True and cap['operator_unchanged']is True
 assert cap['cwd']==str(R)and cap['stdin_supplied']is False
 start=dt.datetime.fromisoformat(cap['started_utc']);end=dt.datetime.fromisoformat(cap['finished_utc'])
 assert start.utcoffset()==end.utcoffset()==dt.timedelta(0)and start<=end<=dt.datetime.now(dt.timezone.utc)
 assert sha(read(origin/'prelaunch_operator.py'))==cap['operator_sha256']=='c1ae969ccbbc48ed6fb486e96184da94329291a46b27d2b891ecb87185c909ec'
 for channel in ['stdout','stderr']:
  row=cap[channel];raw=read(origin/row['path']);assert len(raw)==row['bytes']and sha(raw)==row['sha256']
 dest=D/'completed_outer_captures'/name;dest.mkdir(parents=True,exist_ok=False)
 for p in origin.iterdir():(dest/p.name).write_bytes(read(p))
 operations.append({'source_capture':ref(origin/'CAPTURE.json'),'entire_actual_capture':cap})
result=json.loads(read(D/'ROOT_REPRODUCTION_RESULT.json'));assert result['actual_operator_pid']==22446 and len(result['complete_actual_Git_captures'])==33 and len(result['complete_actual_helper_captures'])==3
for cap in result['complete_actual_Git_captures']+result['complete_actual_helper_captures']:
 assert cap['actual_execution']is True and cap['completed']is True and type(cap['pid'])is int and cap['pid']>0 and type(cap['exit_code'])is int and cap['exit_code']==0 and cap['actual_operator_pid']==22446
 start=dt.datetime.fromisoformat(cap['started_utc']);end=dt.datetime.fromisoformat(cap['finished_utc']);assert start<=end
 for channel in ['stdout','stderr']:
  row=cap[channel];raw=read(R/row['path']);assert len(raw)==row['bytes']and sha(raw)==row['sha256']
 if cap['source']is not None:
  assert cap['source_unchanged']is True;row=cap['source'];raw=read(R/row['path']);assert len(raw)==row['bytes']and sha(raw)==row['sha256']
raw=json.loads(read(A/'ROOT_COMPLETE_RAW_SQL_AUDIT.json'));assert raw['actual_pid']==21423 and raw['all_SQL_rows']==15458 and raw['selected_prior_key_present']is False and raw['literal_original_prior_file_value']is None and raw['literal_original_prior_differs_from_upstream_absent_fallback']is True
for n in ['ROOT_MATHEMATICAL_REVIEW.md','ROOT_COMPLETE_RAW_SQL_AUDIT.json','ROOT_REPRODUCTION_PRELAUNCH_SOURCE.py','ROOT_RAW_AUDIT_PRELAUNCH_SOURCE.py','ROOT_REPRODUCTION_CLOSURE_PRELAUNCH_SOURCE.py','ROOT_COVER_ALGEBRA_CLOSURE_PRELAUNCH_SOURCE.py','ROOT_GAUGE_GEOMETRY_VERIFY_PRELAUNCH_SOURCE.py','ROOT_VERIFY_CLOSED_COVER_FAMILY.py']:
 (D/n).write_bytes(read(A/n))
summary={'schema':'pr47-root-current-complete-reproduction-summary/v1','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_closure_pid':os.getpid(),'status':'PASS_ROOT_COMPLETED_FIRST_PARTY_REPRODUCTION','entire_reproduction_result':result,'complete_outer_captures':operations,'raw_audit':ref(A/'ROOT_COMPLETE_RAW_SQL_AUDIT.json'),'mathematical_review':ref(A/'ROOT_MATHEMATICAL_REVIEW.md'),'original_substantive_attempts':1,'turn_limit':5,'new_substantive_attempts':0,'audit_turns':0,'status_recommendation':'unsolved','mandatory_original_mathematical_route_and_provenance_repairs_pending':True,'full_problem_solved':False,'future_acceptance_approved':False,'foreign_primary_SQL_raw_cache_body_copy':False,'duplicate_closure_failure_preserved':True,'cover_original_closure_capture_limitation':'Child10880 was directly tool-captured with exit0, but has no on-disk prelaunch/split streams or exact start/finish UTC; this package does not retrospectively certify them. ROOT readback12271 verifies closed bytes/topology/modes after that child, while duplicate close10982 honestly failed.'}
(D/'ROOT_CURRENT_REPRODUCTION_SUMMARY.json').write_bytes(dump(summary))
rows=[]
for p in sorted(D.rglob('*')):
 assert not p.is_symlink()
 if p.is_file():
  p.chmod(0o444);b=read(p);assert stat.S_IMODE(p.stat().st_mode)==0o444
  rows.append({'path':p.relative_to(D).as_posix(),'bytes':len(b),'sha256':sha(b),'full_mode':'0444'})
dirs=sorted(p.relative_to(D).as_posix()for p in D.rglob('*')if p.is_dir());expected={q.as_posix()for row in rows for q in PurePosixPath(row['path']).parents if str(q)!='.'};assert set(dirs)==expected
mf={'schema':'pr47-root-original-complete-reproduction-self-only-closure/v1','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_closure_pid':os.getpid(),'files_count':len(rows),'files':rows,'directories':dirs,'self_excluded':['MANIFEST.json'],'foreign_primary_raw_SQL_cache_bodies_copied':False,'future_acceptance_approved':False,'separate_completed_closing_capture_outside_this_manifest_required':True}
with(D/'MANIFEST.json').open('xb')as out:out.write(dump(mf));out.flush();os.fsync(out.fileno())
(D/'MANIFEST.json').chmod(0o444)
for row in rows:
 p=D/row['path'];b=read(p);assert len(b)==row['bytes']and sha(b)==row['sha256']and stat.S_IMODE(p.stat().st_mode)==0o444
assert read(Path(__file__).resolve())==source
print(json.dumps({'status':summary['status'],'actual_closure_pid':os.getpid(),'payload_files':len(rows),'directories':len(dirs),'manifest':ref(D/'MANIFEST.json'),'summary':ref(D/'ROOT_CURRENT_REPRODUCTION_SUMMARY.json'),'future_acceptance_approved':False}))

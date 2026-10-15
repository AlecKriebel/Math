"""Freeze completed ROOT reproduction; external closing capture exists only after exit."""
from pathlib import Path,PurePosixPath
import datetime as dt,hashlib,json,os,stat,sys
A=Path(__file__).absolute().parent;R=A.parents[2];D=A/'root_original_actual_reproduction_v2';B=A.parent/'pr45_9900007'
assert __debug__ and not sys.flags.optimize and not (D/'MANIFEST.json').exists()
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):
 assert not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode)
 return p.read_bytes()
def ref(p):
 b=read(p);return dict(path=p.relative_to(R).as_posix(),bytes=len(b),sha256=sha(b))
def put(p,b):
 with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def enc(o):return (json.dumps(o,indent=2,allow_nan=False)+'\n').encode()
operations=[]
for name,pid,code in [('root_pr48_original_reproduction_actual_capture',3042,1),('root_pr48_original_reproduction_v2_actual_capture',11716,0),('root_pr48_full_raw_SQL_actual_capture',16308,0),('root_pr48_smooth_geometry_closure_actual_capture',15467,0),('root_pr48_smooth_geometry_closed_readback_actual_capture',16307,0)]:
 C=B/name;c=json.loads(read(C/'CAPTURE.json'))
 assert {p.name for p in C.iterdir()}=={'CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin'}
 assert type(c['pid']) is int and c['pid']==pid and type(c['exit_code']) is int and c['exit_code']==code and c['actual_execution'] is True and c['completed'] is True and c['operator_unchanged'] is True
 start=dt.datetime.fromisoformat(c['started_utc']);end=dt.datetime.fromisoformat(c['finished_utc']);assert start.utcoffset()==end.utcoffset()==dt.timedelta(0) and start<=end<=dt.datetime.now(dt.timezone.utc)
 assert sha(read(C/'prelaunch_operator.py'))==c['operator_sha256']=='c1ae969ccbbc48ed6fb486e96184da94329291a46b27d2b891ecb87185c909ec'
 for k in ['stdout','stderr']:
  b=read(C/c[k]['path']);assert len(b)==c[k]['bytes'] and sha(b)==c[k]['sha256']
 dest=D/'completed_outer_captures'/name;dest.mkdir(parents=True)
 for p in C.iterdir():put(dest/p.name,read(p))
 operations.append(dict(source_capture=ref(C/'CAPTURE.json'),complete_capture=c))
result=json.loads(read(D/'ROOT_REPRODUCTION_RESULT.json'));assert result['actual_operator_pid']==11716 and len(result['complete_actual_Git_captures'])==38 and len(result['complete_actual_helper_captures'])==4
for c in result['complete_actual_Git_captures']+result['complete_actual_helper_captures']:
 assert c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0 and type(c['exit_code']) is int and c['exit_code']==0 and c['actual_operator_pid']==11716
 assert dt.datetime.fromisoformat(c['started_utc'])<=dt.datetime.fromisoformat(c['finished_utc'])
 for k in ['stdout','stderr']:
  r=c[k];b=read(R/r['path']);assert len(b)==r['bytes'] and sha(b)==r['sha256']
 if c['source'] is None:assert c['source_unchanged'] is None and c['schema']=='pr48-root-readonly-git-actual-capture/v1' and c['argv'][0]=='git' and c['argv'][1] in {'show','ls-tree','merge-base','diff'}
 else:
  r=c['source'];b=read(R/r['path']);assert len(b)==r['bytes'] and sha(b)==r['sha256'] and c['source_unchanged'] is True and c['schema']=='pr48-root-unchanged-helper-actual-capture/v1'
raw=json.loads(read(A/'ROOT_COMPLETE_RAW_SQL_AUDIT.json'));assert raw['actual_pid']==16308 and raw['all_SQL_rows']==15458 and raw['full_raw_and_prior_bytes']==149266659
assert len(raw['complete_selected_source_bindings'])==2 and all(r['raw_key_presence']=='ABSENT' and r['SQLite_typed_fallback']=={} and r['original_prior_report_file_exists'] is False for r in raw['complete_selected_source_bindings'])
for n in ['ROOT_MATHEMATICAL_REVIEW.md','ROOT_COMPLETE_RAW_SQL_AUDIT.json','ROOT_REPRODUCTION_PRELAUNCH_SOURCE.py','ROOT_REPRODUCTION_V2_PRELAUNCH_SOURCE.py','ROOT_RAW_AUDIT_PRELAUNCH_SOURCE.py','ROOT_REPRODUCTION_CLOSURE_PRELAUNCH_SOURCE.py']:
 put(D/n,read(A/n))
failed=A/'root_original_actual_reproduction';failed_rows=[ref(p) for p in sorted(failed.rglob('*')) if p.is_file()]
summary=dict(schema='pr48-root-current-complete-reproduction-summary/v1',created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),actual_closure_pid=os.getpid(),status='PASS_ROOT_COMPLETED_FIRST_PARTY_REPRODUCTION',entire_reproduction_result=result,complete_outer_captures=operations,raw_audit=ref(A/'ROOT_COMPLETE_RAW_SQL_AUDIT.json'),mathematical_review=ref(A/'ROOT_MATHEMATICAL_REVIEW.md'),failed_V1_complete_bindings=failed_rows,
 original_substantive_attempts=2,turn_limit=5,new_substantive_attempts=0,audit_turns=0,status_recommendation='unsolved',duplicate_id='30004403',duplicate_shared_budget=True,mandatory_original_provenance_repairs_pending=True,full_problem_solved=False,future_acceptance_approved=False,foreign_primary_SQL_raw_cache_body_copy=False,
 historical_final_note_change='Passed review sentence plus added no-human-peer-review disclosure; final receipt only note hash changes.',earlier_reproduction_result_raw_audit_PENDING_is_historical_field_now_supplemented_by_actual16308=True)
put(D/'ROOT_CURRENT_REPRODUCTION_SUMMARY.json',enc(summary))
rows=[];dirs=[]
for p in sorted(D.rglob('*')):
 assert not p.is_symlink()
 if p.is_dir():dirs.append(p.relative_to(D).as_posix());continue
 assert stat.S_ISREG(p.stat().st_mode);p.chmod(0o444);b=read(p);assert stat.S_IMODE(p.stat().st_mode)==0o444
 rows.append(dict(path=p.relative_to(D).as_posix(),bytes=len(b),sha256=sha(b),full_mode='0444'))
assert set(dirs)=={q.as_posix() for r in rows for q in PurePosixPath(r['path']).parents if str(q)!='.'}
m=dict(schema='pr48-root-original-complete-reproduction-self-only-closure/v1',created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),actual_closure_pid=os.getpid(),files_count=len(rows),files=rows,directories=dirs,self_excluded=['MANIFEST.json'],foreign_primary_raw_SQL_cache_bodies_copied=False,future_acceptance_approved=False,separate_completed_closing_capture_outside_this_manifest_required=True)
put(D/'MANIFEST.json',enc(m));(D/'MANIFEST.json').chmod(0o444)
for r in rows:
 p=D/r['path'];b=read(p);assert len(b)==r['bytes'] and sha(b)==r['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444
print(json.dumps(dict(status=summary['status'],actual_closure_pid=os.getpid(),payload_files=len(rows),directories=len(dirs),manifest=ref(D/'MANIFEST.json'),summary=ref(D/'ROOT_CURRENT_REPRODUCTION_SUMMARY.json'),future_acceptance_approved=False),indent=2))

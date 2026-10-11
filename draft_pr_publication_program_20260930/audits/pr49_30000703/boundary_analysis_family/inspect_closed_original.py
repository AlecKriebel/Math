"""Full independent original closure, topology, streams and native Git readback."""
from pathlib import Path,PurePosixPath
import datetime,hashlib,json,os,stat,subprocess
F=Path(__file__).resolve().parent;A=F.parent;P=A.parent;R=Path('/Users/alec/Documents/Math')
def sha(b):return hashlib.sha256(b).hexdigest()
def stamp(v):
 d=datetime.datetime.fromisoformat(v);assert d.utcoffset()==datetime.timedelta(0);return d
def binding(p):
 b=p.read_bytes();st=p.lstat();assert stat.S_ISREG(st.st_mode) and not p.is_symlink()
 return {'path':str(p.relative_to(R)),'bytes':len(b),'sha256':sha(b),'full_mode':stat.S_IMODE(st.st_mode)}
def inspect_capture(d,external=False):
 c=json.loads((d/'CAPTURE.json').read_bytes());assert c['actual_execution'] is True and c['completed'] is True
 assert type(c['pid']) is int and c['pid']>0 and type(c['exit_code']) is int
 assert stamp(c['started_utc'])<stamp(c['finished_utc']) and c['operator_unchanged'] is True and c['stdin_supplied'] is False
 source=(d/'prelaunch_operator.py').read_bytes();assert sha(source)==c['operator_sha256']
 for n in ['stdout','stderr']:
  b=(d/c[n]['path']).read_bytes();assert len(b)==c[n]['bytes'] and sha(b)==c[n]['sha256']
 if external:
  assert c['schema']=='root-explicit-command-capture/v1' and c['exit_code']==c['expected_exit_code']==0 and c['status']=='PASS'
  assert {p.name for p in d.iterdir()}=={'CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin'}
 else:
  assert c['schema'] in ['pr49-original-actual-command/v1','pr49-original-readonly-git-command/v1']
  pre=json.loads((d/'PRELAUNCH.json').read_bytes())
  assert pre['actual_execution'] is False and pre['completed'] is False and pre['pid'] is None and pre['exit_code'] is None
  for k in ['argv','cwd','operator_pid','operator_sha256','started_utc']:assert pre[k]==c[k]
  names={'CAPTURE.json','PRELAUNCH.json','prelaunch_operator.py','stdout.bin','stderr.bin'}
  target=c.get('target_source')
  if target is not None:
   assert type(target) is dict and c['target_unchanged'] is True and pre['target_source']==target
   b=(d/'prelaunch_target.py').read_bytes();assert len(b)==target['bytes'] and sha(b)==target['sha256'];names.add('prelaunch_target.py')
  elif 'target_source' in c:assert c['target_source'] is None and c['target_unchanged'] is None
  assert {p.name for p in d.iterdir()}==names
 return {'record':c,'capture_binding':binding(d/'CAPTURE.json'),'all_members':[binding(p) for p in sorted(d.iterdir())],'complete_body_streams_read':True}
mb=(A/'ORIGINAL_PREPARATION_MANIFEST.json').read_bytes();assert len(mb)==126347 and sha(mb)=='2eecad772938f3b220936c3317f1266d9a98de0f9d9750a6efa725c665f63b4c'
m=json.loads(mb);assert m['schema']=='pr49-original-preparation-self-only-manifest/v1' and m['files_count']==len(m['files'])==350
assert m['future_acceptance_authority'] is False and m['current_mathematical_verdict'] is None and m['outer_capture_status_at_child_closure']=='PENDING_CHILD_EXIT'
assert m['self_excluded']==['ORIGINAL_PREPARATION_MANIFEST.json']
assert stat.S_IMODE((A/'ORIGINAL_PREPARATION_MANIFEST.json').stat().st_mode)==0o444
rows=[];total=0
for row in m['files']:
 q=PurePosixPath(row['path']);assert not q.is_absolute() and '..' not in q.parts
 f=A/row['path'];b=f.read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256'] and stat.S_IMODE(f.lstat().st_mode)==row['full_mode']==0o444 and not f.is_symlink()
 if f.suffix=='.json':json.loads(b)
 total+=len(b);rows.append(row)
actual_files=set(m['authorship_root_files']);actual_dirs=set()
for root in m['authorship_directory_roots']:
 d=A/root;assert d.is_dir() and not d.is_symlink()
 for p in [d]+list(d.rglob('*')):
  assert not p.is_symlink() and (p.is_file() or p.is_dir())
  if p.is_file():actual_files.add(p.relative_to(A).as_posix())
  else:actual_dirs.add(p.relative_to(A).as_posix())
assert actual_files=={v['path'] for v in rows}
assert actual_dirs==set(m['owned_directories'])=={v['path'] for v in m['owned_directory_bindings']} and len(actual_dirs)==63
for v in m['owned_directory_bindings']:assert stat.S_IMODE((A/v['path']).lstat().st_mode)==v['full_mode']
assert stat.S_IMODE(A.stat().st_mode)==m['authorship_root_full_mode']
captures=[]
for entry in m['complete_prior_actual_captures']:
 c=inspect_capture((A/entry['path']).parent)
 assert c['capture_binding']['sha256']==entry['capture_sha256']
 for k in ['argv','pid','operator_pid','started_utc','finished_utc','exit_code','schema']:assert c['record'][k]==entry[k]
 captures.append(c)
assert len(captures)==58 and sorted(c['record']['exit_code'] for c in captures if c['record']['exit_code']!=0)==[1,128]
closure=inspect_capture(P/'pr45_9900007/root_pr49_original_preparation_closure_actual_capture',True)
post=inspect_capture(P/'pr45_9900007/root_pr49_original_preparation_closed_readback_actual_capture',True)
assert closure['record']['pid']==m['actual_pid']==48827 and post['record']['pid']==49240
assert stamp(closure['record']['started_utc'])<stamp(m['created_utc'])<stamp(closure['record']['finished_utc'])<stamp(post['record']['started_utc'])<stamp(post['record']['finished_utc'])<datetime.datetime.now(datetime.timezone.utc)
closer=(A/'close_original_preparation.py').read_bytes()
assert closer==(A/'CLOSURE_PRELAUNCH_SOURCE.py').read_bytes()==(A/'ROOT_ORIGINAL_CLOSURE_PRELAUNCH_SOURCE.py').read_bytes()
assert sha((A/'ORIGINAL_CLAIM_INVENTORY.md').read_bytes())==closure['record']['argv'][-1]
cs=json.loads((P/'pr45_9900007/root_pr49_original_preparation_closure_actual_capture/stdout.bin').read_bytes());ps=json.loads((P/'pr45_9900007/root_pr49_original_preparation_closed_readback_actual_capture/stdout.bin').read_bytes())
assert cs['manifest_sha256']==ps['manifest_sha256']==sha(mb) and cs['owned_files']==ps['owned_files']==350 and cs['owned_directories']==ps['owned_directories']==63
assert cs['acceptance_verdict'] is None and ps['acceptance_verdict'] is None and cs['helper_execution_performed'] is False
# Independently read full fixed native Git bodies behind both dated inspections.
native_actual=[]
for receipt in ['ORIGINAL_NATIVE_SELECTED_READ.json','ORIGINAL_NATIVE_SELECTED_READ_V2.json']:
 n=json.loads((A/receipt).read_bytes())
 assert n['native_writes'] is False and n['authority_for_future_main'] is False and n['canonical_count']==13
 for v in n['head_native_bindings']:
  assert v['git_ref']==m['head']
  for operation in v['complete_actual_read_operations']:
   started=datetime.datetime.now(datetime.timezone.utc).isoformat();child=subprocess.Popen(operation['argv'],cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=child.communicate();finished=datetime.datetime.now(datetime.timezone.utc).isoformat()
   assert child.returncode==0 and len(out)==operation['stdout']['bytes'] and sha(out)==operation['stdout']['sha256'] and err==b''
   native_actual.append({'argv':operation['argv'],'pid':child.pid,'operator_pid':os.getpid(),'started_utc':started,'finished_utc':finished,'actual_execution':True,'completed':True,'exit_code':0,'stdin_supplied':False,'operator_sha256':sha(Path(__file__).read_bytes()),'stdout_bytes':len(out),'stdout_sha256':sha(out),'stderr_bytes':0,'stderr_sha256':sha(err),'foreign_native_body_retained':False,'all_output_body_read':True})
assert len(native_actual)==32
raw=json.loads((A/'ORIGINAL_COMPLETE_RAW_SQL_READ.json').read_bytes());assert raw['literal_importer_verified_rows']==15458
assert raw['selected']['upstream_report_presence']=='ABSENT' and raw['selected']['sqlite_report_literal']=='{}' and raw['selected']['original_prior_report_equals_SQLite_importer_report'] is False
res={'schema':'pr49-boundary-complete-original-closed-validation/v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),'original_manifest':binding(A/'ORIGINAL_PREPARATION_MANIFEST.json'),'all_original_manifest_members_read_in_full':True,'all_original_files':rows,'original_payload_body_bytes_read':total,'original_payload_files':350,'original_total_files_with_self_manifest':351,'exact_owned_topology_and_full_4096_permission_modes_verified':True,'owned_directory_bindings':m['owned_directory_bindings'],'complete_actual_original_capture_validation':True,'all_58_original_actual_captures':captures,'original_failures_retained':2,'genuine_ROOT_closure':closure,'genuine_ROOT_after_exit_readback':post,'closure_chronology_verified':True,'original_child_honestly_left_own_outer_exit_pending':True,'all_32_historical_native_operations_independently_repeated':native_actual,'root_adjacent_prelaunch_source':binding(A/'ROOT_ORIGINAL_CLOSURE_PRELAUNCH_SOURCE.py'),'raw_provenance_checked_independently_in':'INDEPENDENT_RAW_READ.json','current_dated_native_inputs_are_future_authority':False,'future_acceptance_authority':False}
(F/'ORIGINAL_CLOSED_VALIDATION.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps({'status':'PASS_COMPLETE_ORIGINAL_CLOSED_SCOPE','original_files':350,'original_body_bytes':total,'original_captures':58,'native_operations':32,'full_modes_and_topology':True,'post_child_exit_chronology':True,'future_authority':False},indent=2))

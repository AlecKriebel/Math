"""Own final first-party/source-only seal; proposed production remains unexecuted."""
from pathlib import Path,PurePosixPath
import datetime,hashlib,json,os,stat
F=Path(__file__).absolute().parent
A=F.parent
def sha(raw):return hashlib.sha256(raw).hexdigest()
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def regular(path):
 assert not path.is_symlink() and all(not p.is_symlink() for p in path.parents)
 assert stat.S_ISREG(path.stat().st_mode)
 return path.read_bytes()
def main():
 own=regular(Path(__file__))
 assert not (F/'OWN_CLOSURE.json').exists()
 preps={
 'PREPARATION_MANIFEST.json':'be1217cc9c67dad1d5e528b547d332463e0b742dd1592602efe601b4c2d165a1',
 'prepare_current_packet.py':'7bde800ce050ddf1a9ac071ff54551813e87309eae9834805b3ef632b4342aff',
 'capture_root_builder_operation.py':'7f9c717bd3b8ef32160d4388f38ddaf3617c04c1e5c8c3884dd04725684acd3f'}
 for name,expected in preps.items():assert sha(regular(A/'current_preparation_family'/name))==expected
 expected={'healthy':0,'mutant_types':1,'mutant_path':1,'mutant_modes':1,'mutant_queue':1,'mutant_duplicate_capture':1,'mutant_publication':1}
 assert {p.name for p in (F/'actual_runs').iterdir()}==set(expected)
 sources=[];runs=[]
 for name,exit_code in expected.items():
  d=F/'actual_runs'/name
  assert {p.name for p in d.iterdir()}=={'PRELAUNCH_SOURCE.py','PRELAUNCH_OPERATOR.py','PRELAUNCH.json','LAUNCHED.json','stdout.bin','stderr.bin','CAPTURE.json'}
  pre=json.loads(regular(d/'PRELAUNCH.json'));cap=json.loads(regular(d/'CAPTURE.json'));launch=json.loads(regular(d/'LAUNCHED.json'))
  assert cap['actual_execution'] is True and cap['completed'] is True and type(cap['pid']) is int and cap['pid']>0
  assert type(cap['exit_code']) is int and cap['exit_code']==cap['expected_exit_code']==exit_code
  assert cap['status']=='PASS_OWN_EXPECTED_CONTROL_OUTCOME' and cap['source_unchanged'] is True and cap['operator_unchanged'] is True
  assert cap['stdin_supplied'] is False and cap['production_import_compile_or_execution'] is False
  assert launch['pid']==cap['pid'] and launch['operator_pid']==cap['operator_pid']
  assert sha(regular(d/'PRELAUNCH.json'))==launch['prelaunch_sha256']
  clocks=[datetime.datetime.fromisoformat(pre['started_utc']),datetime.datetime.fromisoformat(launch['launched_utc']),datetime.datetime.fromisoformat(cap['finished_utc'])]
  assert all(t.tzinfo and t.utcoffset()==datetime.timedelta(0) for t in clocks) and clocks==sorted(clocks)
  for source,key in [('PRELAUNCH_SOURCE.py','source_sha256'),('PRELAUNCH_OPERATOR.py','operator_sha256')]:assert sha(regular(d/source))==cap[key]==pre[key]
  for channel in ['stdout','stderr']:
   row=cap[channel];raw=regular(d/row['path']);assert len(raw)==row['bytes'] and sha(raw)==row['sha256']
  sources.append(cap['source_sha256']);runs.append({'directory':'actual_runs/'+name,'child_pid':cap['pid'],'exit_code':cap['exit_code'],'capture_sha256':sha(regular(d/'CAPTURE.json'))})
 assert len(set(sources))==1 and sources[0]==sha(regular(F/'independent_source_controls.py'))
 healthy=json.loads(regular(F/'actual_runs/healthy/stdout.bin'));assert healthy['assertions']==848 and healthy['child_pid']==84687 and healthy['future_runtime_PASS'] is False
 assert len(healthy['input_inspection']['individual_foreign_hash_bindings'])==64
 for row in healthy['input_inspection']['inputs_read_in_full_for_hash_and_structure']:
  role=row['role']
  if role=='source-preparation':base=A/'current_preparation_family'
  elif role=='original18':base=A/'source_snapshot'
  elif role=='original-preparation':base=A
  elif role in {'family-manifest','authored-family','foreign-hash-only'}:
   # Same relative names can occur in two families; select the uniquely matching pinned member.
   candidates=[A/fam/row['path'] for fam in ['probability_metric_family','literal_priority_family']]
   matches=[p for p in candidates if p.is_file() and len(regular(p))==row['bytes'] and sha(regular(p))==row['sha256']]
   assert matches;continue
  else:raise ValueError(role)
  raw=regular(base/row['path']);assert len(raw)==row['bytes'] and sha(raw)==row['sha256']
 verdict=json.loads(regular(F/'VERDICT.json'));assert verdict['mandatory_source_corrections']==[] and verdict['production_import_compile_or_execution'] is False
 now=utc()
 with (F/'RESEARCH_LOG.md').open('a') as handle:
  handle.write('\n'+now+' — Final own closure checkpoint. Audit completion estimate: 100%; discovery: 0%. Exact preparation pins rechecked. Healthy848 and six deliberate rejected mutant captures independently validated, complete first-party only topology checked; dated special-bit fixtures frozen0444. No production/native/original helper execution or acceptance. Optional hardening remains optional under the explicit truthful ROOT attestation boundary.\n')
 paths=sorted(F.rglob('*'));assert all(not p.is_symlink() for p in paths)
 files=[p for p in paths if p.is_file()];dirs={p.relative_to(F).as_posix() for p in paths if p.is_dir()}
 names={p.relative_to(F).as_posix() for p in files}
 needed={q.as_posix() for name in names for q in PurePosixPath(name).parents if q.as_posix()!='.'}
 assert dirs==needed
 for p in files:
  assert stat.S_ISREG(p.stat().st_mode);p.chmod(0o444);assert stat.S_IMODE(p.stat().st_mode)==0o444
 rows=[{'path':p.relative_to(F).as_posix(),'bytes':len(regular(p)),'sha256':sha(regular(p))} for p in files]
 result={'schema':'PR45_NEW_SOURCE_ADVERSARY_SELF_ONLY_CLOSURE_v1','created_utc':now,'actual_seal_child_pid':os.getpid(),'self_excluded':['OWN_CLOSURE.json'],'files_count':len(rows),'files':rows,'directories':sorted(dirs),'full_mode':'0444','all_members_first_party_authored_or_own_control_artifacts':True,'foreign_primary_access_OCR_cache_SQL_bodies_copied':False,'production_import_compile_or_execution':False,'ROOT_approval_or_future_runtime_certified':False,'verdict':'PASS_SOURCE_ONLY_QUALIFIED_NO_MANDATORY_CORRECTION','verdict_sha256':sha(regular(F/'VERDICT.json')),'report_sha256':sha(regular(F/'REPORT.md')),'source_input_pins':preps,'own_actual_control_captures':runs,'audit_completion_percent':100,'new_discovery_percent':0,'Git_full_modes_or_empty_directories_preserved':False,'local_mode_restoration_required_in_fresh_checkout':True}
 with (F/'OWN_CLOSURE.json').open('xb') as handle:handle.write((json.dumps(result,indent=2,sort_keys=True)+'\n').encode());handle.flush();os.fsync(handle.fileno())
 (F/'OWN_CLOSURE.json').chmod(0o444)
 actual={p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_file()}
 assert actual==names|{'OWN_CLOSURE.json'}
 for row in rows:
  p=F/row['path'];raw=regular(p);assert len(raw)==row['bytes'] and sha(raw)==row['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444
 assert stat.S_IMODE((F/'OWN_CLOSURE.json').stat().st_mode)==0o444 and regular(Path(__file__))==own
 print(json.dumps({'closed':True,'own_files_including_self':len(actual),'manifest_bytes':len(regular(F/'OWN_CLOSURE.json')),'manifest_sha256':sha(regular(F/'OWN_CLOSURE.json')),'verdict_sha256':result['verdict_sha256'],'report_sha256':result['report_sha256'],'audit_completion_percent':100,'discovery_percent':0,'production_executed':False},indent=2))
if __name__=='__main__':main()

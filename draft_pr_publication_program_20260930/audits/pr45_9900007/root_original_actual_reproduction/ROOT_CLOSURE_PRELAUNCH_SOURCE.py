"""ROOT genuine complete first-party closure after personal mathematical/source reading."""
from pathlib import Path
import datetime as dt,hashlib,json,os,stat
A=Path(__file__).resolve().parent;R=A.parents[2];D=A/'root_original_actual_reproduction'
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def pin(p,base=A):
 b=p.read_bytes();return {'path':p.relative_to(base).as_posix(),'bytes':len(b),'sha256':sha(b)}
def check(base,z,frozen=False):
 p=base/z['path'];assert p.is_file() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents)
 assert p.resolve().is_relative_to(R.resolve());b=p.read_bytes();assert type(z['bytes']) is int and len(b)==z['bytes'] and sha(b)==z['sha256']
 if frozen:assert stat.S_IMODE(p.stat().st_mode)==0o444
 return b
def typed(a,b):
 if type(a) is not type(b):return False
 if type(a) is dict:return set(a)==set(b) and all(typed(a[k],b[k]) for k in a)
 if type(a) is list:return len(a)==len(b) and all(typed(x,y) for x,y in zip(a,b))
 return a==b
def topology(root,names):
 assert {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}==names
 assert not any(p.is_symlink() for p in root.rglob('*'))
 assert {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_dir()}=={q.as_posix() for n in names for q in Path(n).parents if str(q)!='.'}
assert __debug__ and os.environ.get('PYTHONOPTIMIZE','') in ('','0')
source=Path(__file__).read_bytes();(D/'ROOT_CLOSURE_PRELAUNCH_SOURCE.py').write_bytes(source)
checked_closures=[]
for family,mname,pinned,count in [('current_preparation_family','PREPARATION_MANIFEST.json','be1217cc9c67dad1d5e528b547d332463e0b742dd1592602efe601b4c2d165a1',47),('current_source_adversary_family','OWN_CLOSURE.json','bc8495cf37aae77021d2ef10f0868f0b69eefbff02131ae979b9de354814203b',70)]:
 F=A/family;mraw=(F/mname).read_bytes();assert sha(mraw)==pinned;m=json.loads(mraw);assert len(m['files'])==count
 names={z['path'] for z in m['files']}|{mname};assert len(names)==count+1;topology(F,names)
 for z in m['files']:check(F,z,True)
 assert stat.S_IMODE((F/mname).stat().st_mode)==0o444;checked_closures.append({'family':family,'manifest':pin(F/mname),'owned_rows':count,'exact_topology_full_modes':True})
pins=load(A/'current_preparation_family/STATIC_INPUT_BINDINGS.json')
for z in pins['auxiliary']:check(A,z)
check(A,pins['snapshot_manifest'],True);check(A,pins['original_metadata'])
foreign=[]
for family,j in pins['families'].items():
 F=A/family;names={z['path'] for z in j['copied_members']+j['foreign_members']}|{j['manifest']['path']};topology(F,names)
 check(F,j['manifest'],True)
 for z in j['copied_members']+j['foreign_members']:check(F,z,True)
 for z in j['foreign_members']:foreign.append({**z,'path':family+'/'+z['path']})
 checked_closures.append({'family':family,'manifest':pin(F/j['manifest']['path']),'owned_plus_manifest':len(j['copied_members'])+1,'foreign_individually_checked':len(j['foreign_members']),'exact_topology_full_modes':True})
assert len(foreign)==64
S=A/'source_snapshot';mf=load(A/'snapshot_manifest.json');assert len(mf['files'])==18
for z in mf['files']:check(S,{'path':z['relative_path'],'bytes':z['bytes'],'sha256':z['sha256']},True)
topology(S,{z['relative_path'] for z in mf['files']})
diff=(A/'original_diff.patch').read_bytes();assert len(diff)==183402 and sha(diff)=='e35d109f694c8abb0a83c3b5604ede674a14d33025ae124340d4102829c3e6ba'
parts=diff.split(b'diff --git ')[1:];assert len(parts)==19;reconstructed=[]
for part in parts:
 path=part.splitlines()[0].split(b' b/',1)[1].decode()
 if path=='unsolved_math_prioritization/QUEUE.md':continue
 prefix='unsolved_math_prioritization/attempts/9900007/';assert path.startswith(prefix);name=path[len(prefix):]
 body=b''.join(x[1:] for x in part.splitlines(keepends=True) if x.startswith(b'+') and not x.startswith(b'+++'))
 assert b'new file mode 100644\n' in part and body==(S/name).read_bytes();reconstructed.append(name)
assert set(reconstructed)=={z['relative_path'] for z in mf['files']}
repro=load(D/'ROOT_REPRODUCTION_RESULT.json');raw=load(D/'ROOT_RAW_SQL_AUDIT.json');assert repro['actual_root_pid']==88783 and raw['actual_pid']==89614
for name,saved in [('current_author','binary_verification.json'),('historical_submitted','review/submitted_results.json'),('historical_independent','review/independent_results.json')]:
 F=D/name;cap=load(F/'CAPTURE.json');assert cap['actual_execution'] is cap['completed'] is True and cap['exit_code']==0 and cap['byte_exact_saved_result'] is True
 check(R,cap['prelaunch_source']);check(R,cap['source_origin'])
 for k in ['stdout','stderr']:check(R,cap[k])
 assert (F/'ACTUAL_RESULT.json').read_bytes()==(S/saved).read_bytes() and typed(load(F/'ACTUAL_RESULT.json'),load(S/saved))
 assert cap['source_unchanged'] is True
assert (D/'historical_independent/PARTIAL.md').read_bytes()==(S/'review/PARTIAL.md').read_bytes()
assert raw['raw_prior_key_present'] is True and raw['SQL_empty_object_is_absent_key_fallback'] is False and raw['retrieved_raw_null_prior'] is False
assert raw['entire_original_problem_object_equal'] is raw['entire_original_upstream_report_equal'] is True
refs=[]
for old,new,pid,code in [('root_helper_reproduction_actual_capture','actual_helper_outer_capture',88783,0),('root_full_raw_SQL_v2_actual_capture','actual_raw_SQL_outer_capture',89614,0),('root_full_raw_SQL_actual_capture','failed_first_raw_SQL_wrapper_capture',88914,1)]:
 F=A/old;cap=load(F/'CAPTURE.json');assert cap['schema']=='root-explicit-command-capture/v1' and cap['pid']==pid and cap['exit_code']==code and cap['actual_execution'] is cap['completed'] is True
 assert sha((F/'prelaunch_operator.py').read_bytes())==cap['operator_sha256']
 for k in ['stdout','stderr']:check(F,cap[k])
 target=D/new;target.mkdir(exist_ok=False)
 for p in F.iterdir():assert p.is_file() and not p.is_symlink();(target/p.name).write_bytes(p.read_bytes())
 if code==0:refs.append(pin(target/'CAPTURE.json'))
assert len(refs)==2 and refs[0]['path']!=refs[1]['path']
ledger=[json.loads(x) for x in (S/'turns.jsonl').read_bytes().splitlines()];assert len(ledger)==1 and ledger[0]['turn']==1
summary={'schema':'PR45_ROOT_CURRENT_REPRODUCTION_SUMMARY_v1','actual_reproductions_completed':True,'entire_author_result':repro['author_result'],'entire_independent_result':repro['independent_result'],'author_receipt_byte_exact':True,'independent_receipt_byte_exact':True,'full_original18_verified':True,'whole_original_ledger':ledger,'finite_checks_do_not_prove_universal_coupling_or_full_problem':True,'whole_raw_bytes':149266659,'whole_SQL_rows':15458,'prior_raw_key_present':True,'original_substantive_attempts':1,'new_substantive_attempts':0,'audit_turns':0,'actual_replay_captures':refs,'actual_capture_scope_qualification':'Two distinct genuine C1 outer runs: combined three unchanged finite helpers and whole raw/SQL comparison. Complete inner sources, captures, streams, private PARTIAL and full receipts retained. These capture archives are later byte-exact copies, not imaginary earlier first-save times. Failed original raw wrapper is also preserved. Finite checks do not prove all-fixed-couplings or broad characterization.','entire_three_helper_result_record':pin(D/'ROOT_REPRODUCTION_RESULT.json'),'entire_raw_SQL_record':pin(D/'ROOT_RAW_SQL_AUDIT.json'),'full_original19_path_diff_and18_new_hunks_verified':True,'new_independent_families_and_SOURCE_closures':checked_closures,'historical_execution_or_human_review_certified':False}
assert typed(summary['entire_author_result'],load(S/'binary_verification.json')) and typed(summary['entire_independent_result'],load(S/'review/independent_results.json'))
(D/'ROOT_CURRENT_REPRODUCTION_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
for p in D.rglob('*'):
 if p.is_file():
  assert p.stat().st_size<10_000_000 and not any(p.read_bytes()==(A/z['path']).read_bytes() for z in foreign if p.stat().st_size==z['bytes'])
  assert not any(q.is_symlink() for q in p.parents)
rows=[pin(p,D) for p in sorted(D.rglob('*')) if p.is_file()]
m={'schema':'pr45-root-original-reproduction/v1','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_closure_pid':os.getpid(),'original_head':'d9b4acf5d070d1f04ffac86a4f08916a5629ff16','source_snapshot_manifest_sha256':'7180aa194d0fe99806e8aed1a92cbbc456676f26e0b2a18ad24cfcef4cd77833','original_substantive_attempts':1,'new_substantive_attempts':0,'audit_turns':0,'files_count':len(rows),'files':rows,'self_excluded':['MANIFEST.json'],'foreign_original_cache_inputs_individually_pinned_not_copied':raw['foreign_original_cache_inputs_individually_pinned_not_copied'],'literal64_foreign_bodies_individually_excluded_and_not_present':True}
(D/'MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
for p in D.rglob('*'):
 if p.is_file():p.chmod(0o444)
for z in rows:check(D,z,True)
topology(D,{z['path'] for z in rows}|{'MANIFEST.json'});assert stat.S_IMODE((D/'MANIFEST.json').stat().st_mode)==0o444 and Path(__file__).read_bytes()==source
print(json.dumps({'status':'PASS_ROOT_COMPLETE_ORIGINAL_REPRODUCTION_AND_SOURCE_CLOSURES','actual_pid':os.getpid(),'owned_reproduction_members':len(rows),'manifest':pin(D/'MANIFEST.json'),'summary':pin(D/'ROOT_CURRENT_REPRODUCTION_SUMMARY.json'),'all18_diff_hunks_verified':True,'foreign64_not_copied':True,'prior_raw_key_present':True,'full_target_solved':False}))

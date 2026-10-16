"""Execute frozen implementations only in this reviewer's ignored private replica."""
from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
P=ROOT/'draft_pr_publication_program_20260930/audits/pr34_7000004'
R=HERE/'tmp/replica'
Q=R/'draft_pr_publication_program_20260930/audits/pr34_7000004'
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
rows=[]
def check_bindings():
 for z in load(HERE/'BINDINGS_BEFORE.json')['bindings']:
  b=(ROOT/z['path']).read_bytes();assert len(b)==z['bytes'] and sha(b)==z['sha256'],z['path']
def run(label,code,args=(),expected=None,result=None,expected_failure=None):
 d=HERE/'actual_replays'/label;d.mkdir(parents=True,exist_ok=True)
 if (d/'receipt.json').exists():
  old=load(d/'receipt.json');assert old['implementation_sha256']==sha(code.read_bytes());rows.append(old)
  print(label,'PREVIOUS ACTUAL RECEIPT',flush=True);return None
 r=subprocess.run(['/usr/bin/python3',str(code)]+[str(x) for x in args],capture_output=True,timeout=240)
 (d/'stdout.txt').write_bytes(r.stdout);(d/'stderr.txt').write_bytes(r.stderr)
 out={'name':label,'implementation_sha256':sha(code.read_bytes()),'exit':r.returncode,'stderr_empty':not r.stderr,'stdout_sha256':sha(r.stdout)}
 if expected_failure:
  assert r.returncode!=0 and expected_failure.encode() in r.stderr,(label,r.stderr.decode())
  out['preserved_expected_failure']=expected_failure
 else:
  assert r.returncode==0 and not r.stderr,(label,r.returncode,r.stderr.decode())
 if expected:
  if expected.suffix=='.json' and label in ['linking_full']:
   assert json.loads(r.stdout)==load(expected);out['whole_json_equal']=True
  else:assert r.stdout==expected.read_bytes();out['stdout_byte_exact']=True
 if result:
  actual,want=result;assert actual.read_bytes()==want.read_bytes(),label
  (d/'result.json').write_bytes(actual.read_bytes());out['result_byte_exact']=True
 (d/'receipt.json').write_text(json.dumps(out,indent=2)+'\n');rows.append(out)
 print(label, 'EXPECTED FAILURE' if expected_failure else 'PASS',flush=True)
 return r
check_bindings()
for label,rel,want,generated in [('original_author','verify.py','verification.json','verification.json'),('original_submitted','review/submitted_verify.py','review/submitted_results.json','verification.json'),('original_independent','review/independent_checks.py','review/independent_results.json','independent_results.json')]:
 d=HERE/'tmp/entrypoints'/label;d.mkdir(parents=True,exist_ok=True);c=d/Path(rel).name;shutil.copyfile(P/'source_snapshot'/rel,c)
 run(label,c,expected=P/'source_snapshot'/want,result=(d/generated,P/'source_snapshot'/want))
for label,folder,code,want in [('differential_exact','differential_family','exact_controls.py','exact_results.json'),('differential_actual_mutations','differential_family','mutation_replay.py','mutation_results.json'),('current_v2_verifier','reviewed_candidate_v2','verify.py','exact_results.json')]:
 run(label,Q/folder/code,expected=P/folder/want,result=(Q/folder/want,P/folder/want))
run('linking_full',Q/'linking_family/reproduce.py',['--output',HERE/'tmp/linking_outputs'],P/'linking_family/REPRODUCTION_RESULTS.json')
run('primary_source',Q/'primary_scope_family/source_priority_controls.py',result=(Q/'primary_scope_family/source_priority_controls_results.json',P/'primary_scope_family/source_priority_controls_results.json'))
cache=ROOT/'unsolved_math_prioritization/cache'
run('actual_queue_importer',Q/'differential_family/qualification_readiness_hash/verify_hash_roles.py',['--repo',ROOT,'--problems',cache/'problems.json','--reports',cache/'research_results.json'],P/'differential_family/qualification_readiness_hash/RESULTS.json',(Q/'differential_family/qualification_readiness_hash/RESULTS.json',P/'differential_family/qualification_readiness_hash/RESULTS.json'))
# Execute all immutable failed source revisions, preserving the failure.
run('initial_linking_harness_failure',Q/'linking_family/revisions/candidate_controls_initial_failed.py',expected_failure='CoercionFailed')
badprimary=Q/'primary_scope_family/initial_failed_source_priority_controls.py'
shutil.copyfile(Q/'primary_scope_family/revisions/source_priority_controls-before-symbolic-comparison-repair.py',badprimary)
run('initial_primary_harness_failure',badprimary,expected_failure='AssertionError')
badroot=Q/'initial_failed_root_families.py';shutil.copyfile(Q/'root_replay_revisions/reproduce_root_families-before-size-field.py',badroot)
run('initial_root_size_field_failure',badroot,expected_failure="KeyError: 'bytes'")
run('root_families',Q/'reproduce_root_families.py')
old=load(P/'ROOT_REMAINING_FAMILY_REPRODUCTION.json');new=load(Q/'ROOT_REMAINING_FAMILY_REPRODUCTION.json')
assert {k:v for k,v in old.items() if k!='utc'}=={k:v for k,v in new.items() if k!='utc'}
rows[-1]['whole_result_equal_except_actual_clock']=True
# Root's entire prior whole-review replay invokes nine outer implementations and five mutants.
run('root_first_whole_replay',Q/'reproduce_root_new1.py')
old=load(P/'ROOT_NEW1_ACTUAL_REPRODUCTION.json');new=load(Q/'ROOT_NEW1_ACTUAL_REPRODUCTION.json')
assert {k:v for k,v in old.items() if k!='utc'}=={k:v for k,v in new.items() if k!='utc'}
rows[-1]['whole_result_equal_except_actual_clock']=True
# Restore private deterministic frozen receipts before reproducing the builder.
for z in load(P/'reviewed_candidate_v2/CURRENT_PROOF_DEPENDENCIES.json')['files']:
 if '/' not in z['path']:
  shutil.copyfile(P/z['path'],Q/z['path'])
hold=HERE/'tmp/v2_original';shutil.copytree(Q/'reviewed_candidate_v2',hold,dirs_exist_ok=True);shutil.rmtree(Q/'reviewed_candidate_v2')
r=run('active_v2_preparation',Q/'prepare_current_packet_v2.py')
new=Q/'reviewed_candidate_v2';old=P/'reviewed_candidate_v2'
newtime=load(new/'MANIFEST.json')['utc'];oldtime=load(old/'MANIFEST.json')['utc']
clock_files=[]
for z in load(old/'MANIFEST.json')['files']:
 f=z['path'];a=(new/f).read_bytes();b=(old/f).read_bytes()
 if f=='CURRENT_PROOF_DEPENDENCIES.json':continue
 assert a.replace(newtime.encode(),oldtime.encode())==b,f
 if a!=b:clock_files.append(f)
deps=load(new/'CURRENT_PROOF_DEPENDENCIES.json');orig=load(old/'CURRENT_PROOF_DEPENDENCIES.json')
assert [z['path'] for z in deps['files']]==[z['path'] for z in orig['files']]
for a,b in zip(deps['files'],orig['files']):
 if a!=b:
  assert a['path']=='ROOT_V2_ADMINISTRATIVE_REPAIR.json'
  assert (Q/a['path']).read_bytes().replace(newtime.encode(),oldtime.encode())==(P/a['path']).read_bytes()
for z in load(new/'MANIFEST.json')['files']:
 b=(new/z['path']).read_bytes();assert len(b)==z['bytes'] and sha(b)==z['sha256']
rows[-1]['all38_generated_members_equal_except_actual_clock_and_derived_clock_hash_bindings']=True
rows[-1]['clock_affected_files']=clock_files
# Run the old immutable v1 builder in a separate private original layout. Historical metadata defect remains.
shutil.rmtree(Q/'reviewed_candidate')
run('historical_v1_preparation',Q/'prepare_current_packet.py')
v=Q/'reviewed_candidate';vm=load(v/'MANIFEST.json')
assert len(vm['files'])==38
assert load(v/'readiness.json')['budget']['time_cap_utc']=='2026-09-30T06:43:00Z'
assert (v/'RESULT.md').read_bytes()==(P/'reviewed_candidate/RESULT.md').read_bytes()
rows[-1]['scientific_result_byte_exact']=True
rows[-1]['historical_metadata_defect_reproduced']=True
check_bindings()
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runs':rows,'outer_runs':len(rows),'frozen_bindings_before_after':273,'all_frozen_bytes_unchanged':True,'original_substantive_attempts_added':0,'scope':'Unchanged actual private execution. Universal proof remains the theorem certificate. Initial historical expected failures remain failures. No entrypoint of queue.py runs.'}
(HERE/'ACTUAL_REPLAYS.json').write_text(json.dumps(out,indent=2)+'\n')
print('ALL REPLAYS CLOSED',len(rows),flush=True)

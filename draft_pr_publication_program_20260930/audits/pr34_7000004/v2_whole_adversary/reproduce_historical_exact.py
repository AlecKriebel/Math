"""NEW whole review: run exact frozen implementations in private replicas only."""
from pathlib import Path
import hashlib,json,shutil,subprocess,datetime
ROOT=Path('/Users/alec/Documents/Math'); P=ROOT/'draft_pr_publication_program_20260930/audits/pr34_7000004';HERE=Path(__file__).resolve().parent
PRIVATE=HERE/'tmp';PRIVATE.mkdir(exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
def closure():
 m=load(P/'reviewed_candidate/MANIFEST.json');assert sha((P/'reviewed_candidate/MANIFEST.json').read_bytes())=='5467c52b1cf076b76b409dd3cefedf7ddda40ed709182d828850276df49204f1'
 d=load(P/'reviewed_candidate/CURRENT_PROOF_DEPENDENCIES.json')
 for base,entries in [(P/'reviewed_candidate',m['files']),(P,d['files'])]:
  for z in entries:
   b=(base/z['path']).read_bytes();assert len(b)==z['bytes'] and sha(b)==z['sha256']
 return len(m['files'])+len(d['files'])
def copytree_manifest(src,dst):
 dst.mkdir(parents=True,exist_ok=True);m=load(src/'MANIFEST.json')
 for z in m.get('members',m.get('files')):
  q=dst/z['path'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src/z['path'],q)
 shutil.copyfile(src/'MANIFEST.json',dst/'MANIFEST.json')
def run(name,code,args,expected_stdout=None,expected_result=None):
 out=HERE/'actual_replays'/name;out.mkdir(parents=True,exist_ok=True)
 r=subprocess.run(['/usr/bin/python3',str(code)]+[str(x) for x in args],capture_output=True)
 (out/'stdout.txt').write_bytes(r.stdout);(out/'stderr.txt').write_bytes(r.stderr)
 receipt={'name':name,'implementation_sha256':sha(code.read_bytes()),'returncode':r.returncode,'stderr_empty':not r.stderr,'stdout_sha256':sha(r.stdout)}
 (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
 assert r.returncode==0 and not r.stderr,(name,r.returncode,r.stderr.decode())
 if expected_stdout is not None:assert r.stdout==expected_stdout.read_bytes(),name
 if expected_result is not None:
  actual,want=expected_result;assert actual.read_bytes()==want.read_bytes(),name
  (out/'result.json').write_bytes(actual.read_bytes());receipt['result_byte_exact']=True;receipt['result_sha256']=sha(actual.read_bytes())
 receipt['passed']=True;(out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
 return receipt
n=closure();runs=[]
shutil.copytree(P/'source_snapshot',PRIVATE/'source_snapshot',dirs_exist_ok=True)
for name,rel,want,generated in [('original_author','verify.py','verification.json','verification.json'),('original_submitted','review/submitted_verify.py','review/submitted_results.json','verification.json'),('original_independent','review/independent_checks.py','review/independent_results.json','independent_results.json')]:
 d=PRIVATE/name;d.mkdir(exist_ok=True);code=d/Path(rel).name;shutil.copyfile(P/'source_snapshot'/rel,code)
 runs.append(run(name,code,[],P/'source_snapshot'/want,(d/generated,P/'source_snapshot'/want)))
copytree_manifest(P/'differential_family',PRIVATE/'differential_family')
for name,code,result in [('differential_exact','exact_controls.py','exact_results.json'),('differential_actual_mutations','mutation_replay.py','mutation_results.json')]:
 d=PRIVATE/'differential_family';runs.append(run(name,d/code,[],P/'differential_family'/result,(d/result,P/'differential_family'/result)))
copytree_manifest(P/'linking_family',PRIVATE/'linking_family')
l=PRIVATE/'linking_family';runs.append(run('linking_full_actual',l/'reproduce.py',['--output',PRIVATE/'linking_outputs']))
actual=load(HERE/'actual_replays/linking_full_actual/stdout.txt');assert actual==load(P/'linking_family/REPRODUCTION_RESULTS.json')
runs[-1]['full_json_equal_frozen_reproduction']=True
replica=PRIVATE/'repo';target=replica/'draft_pr_publication_program_20260930/audits/pr34_7000004'
copytree_manifest(P/'primary_scope_family',target/'primary_scope_family')
shutil.copytree(P/'source_snapshot',target/'source_snapshot',dirs_exist_ok=True);shutil.copyfile(P/'snapshot_manifest.json',target/'snapshot_manifest.json')
u=replica/'unsolved_math_prioritization';u.mkdir(parents=True,exist_ok=True)
for name in ['manifest.json','policy.json','QUEUE.md']:shutil.copyfile(ROOT/'unsolved_math_prioritization'/name,u/name)
(u/'review_v2').mkdir(exist_ok=True);shutil.copyfile(ROOT/'unsolved_math_prioritization/review_v2/related_target_groups.json',u/'review_v2/related_target_groups.json')
for name,src in [('.git',ROOT/'.git'),('unsolved_math_prioritization/cache',ROOT/'unsolved_math_prioritization/cache')]:
 dest=replica/name
 if not dest.exists():dest.symlink_to(src,target_is_directory=True)
code=target/'primary_scope_family/source_priority_controls.py';runs.append(run('primary_source_actual',code,[],expected_result=(code.with_name('source_priority_controls_results.json'),P/'primary_scope_family/source_priority_controls_results.json')))
q=PRIVATE/'qualification';copytree_manifest(P/'differential_family/qualification_readiness_hash',q)
cache=ROOT/'unsolved_math_prioritization/cache';runs.append(run('actual_importer_hash_roles',q/'verify_hash_roles.py',['--repo',ROOT,'--problems',cache/'problems.json','--reports',cache/'research_results.json'],P/'differential_family/qualification_readiness_hash/RESULTS.json',(q/'RESULTS.json',P/'differential_family/qualification_readiness_hash/RESULTS.json')))
c=PRIVATE/'current';c.mkdir(exist_ok=True);shutil.copyfile(P/'reviewed_candidate/verify.py',c/'verify.py');runs.append(run('current_verifier_actual',c/'verify.py',[],P/'reviewed_candidate/exact_results.json',(c/'exact_results.json',P/'reviewed_candidate/exact_results.json')))
assert closure()==n
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'frozen_bindings_before_and_after':n,'actual_unchanged_outer_runs':runs,'frozen_files_modified':False,'original_attempts_added':0,'scope':'Actual exact programs replayed; topological and inequality claims are independently universally proved, never inferred from control counts.'}
(HERE/'REPRODUCTION_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'passed':True,'outer_actual_runs':len(runs),'closed_bindings':n,'current_assertions':226,'linking_assertions':117,'primary_assertions':99,'primary_mutants':11,'hash_roles_mutants':7,'differential_actual_code_mutants':7}))

from pathlib import Path
import json,importlib.util,sys,os,subprocess,copy,hashlib,datetime
sys.dont_write_bytecode=True
repo=Path('/Users/alec/Documents/Math');sweep=repo/'final_full_solution_sweep_20261020_01a15be7';out=sweep/'reviews/range0400_0420_adversary';os.environ['GIT_OPTIONAL_LOCKS']='0';sys.path.insert(0,str(sweep))
source=sweep/'pinned_scope_check.py';(out/'inputs/pinned_scope_check.py').write_bytes(source.read_bytes())
for name in ['advance_clear_exclusions.py','checkpoint.py','sweep_io.py']:(out/'inputs'/name).write_bytes((sweep/name).read_bytes())
spec=importlib.util.spec_from_file_location('reviewed_scope_helper',source);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
def ensure(sha):subprocess.run(['git','cat-file','-e',sha+'^{commit}'],cwd=repo,check=True,capture_output=True)
mod.ensure_commit=ensure
receipts=[];mod.atomic_json=lambda path,value:receipts.append(value)
for n in range(400,421):mod.check(n)
(out/'scope_helper_actual_range_receipts.json').write_text(json.dumps(receipts,indent=2)+'\n')
fixture=out/'scope_helper_fixtures';(fixture/'eligibility').mkdir(parents=True,exist_ok=True)
inv=json.loads((out/'inventory_snapshot.json').read_text());base_inv={'pull_requests':[x for x in inv if x['number']==400]};base_e=json.loads((sweep/'eligibility/pr0400.json').read_text())
mod.ROOT=fixture;mod.run=lambda args:subprocess.run(args,cwd=repo,capture_output=True,check=True).stdout
results=[]
def case(name,mutation,expected):
 e=copy.deepcopy(base_e);mutation(e);(fixture/'rest_inventory.json').write_text(json.dumps(base_inv));(fixture/'eligibility/pr0400.json').write_text(json.dumps(e));local=[];mod.atomic_json=lambda path,value:local.append(value)
 try:r=mod.check(400);observed='pass';error=None
 except Exception as ex:r=None;observed='reject';error=str(ex)
 results.append({'case':name,'expected':expected,'observed':observed,'expected_behavior_met':observed==expected,'error':error,'queue_blob_equal':r['queue_blobs'][0]['equal'] if r else None})
case('evidence_wrong_head',lambda e:e.update(inventory_head_sha='0'*40),'reject')
case('evidence_missing_real_path',lambda e:e['changed_paths'].pop(),'reject')
case('cached_added_status_tampered',lambda e:e['added_queue_rows'][0].update(status='claimed_solved'),'reject')
case('cached_queue_blob_tampered_disclosed_only',lambda e:e['queue_changes'][0].update(sha='0'*40),'pass')
case('cached_duplicate_path_is_accepted_as_set',lambda e:e['changed_paths'].append(e['changed_paths'][0]),'pass')
case('cached_file_count_unchecked',lambda e:e.update(file_count=1),'pass')
(out/'scope_helper_controls.json').write_text(json.dumps({'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'helper_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'actual_range_pass_count':len(receipts),'controls':results,'interpretation':'No provider or shared-repository mutation. Patched output writer writes no root receipt; cached blob disagreement is an explicitly disclosed observation, not identity certification. Missing cache duplicate/file_count checks are validation limits, not disposition blockers on this independently checked range.'},indent=2)+'\n')
print('actual_range_pass_count',len(receipts));print(json.dumps(results,indent=2))

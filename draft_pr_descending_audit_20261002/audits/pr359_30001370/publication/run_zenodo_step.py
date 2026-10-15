"""Run one authorized repository-tool step on the exact cleared submission.
No automatic repeat of any mutation; retain complete redacted tool outputs.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,sys
D=Path(__file__).resolve().parent;A=D.parent
REPO=Path('/Users/alec/Documents/Math');MANIFEST=A/'preprint/zenodo-deposit.json'
step=sys.argv[1]
assert step in {'stage','inspect_draft','publish','inspect_published'}
def load(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
c=load(A/'PUBLISHING_CLEARANCE.json')
assert c['status']=='READY_AFTER_TWO_SEQUENTIAL_FRESH_PREPRINT_REVIEWS' and c['second_review_mandatory_findings']==0
for r in c['sealed_submission_files']:
 b=(A/'preprint'/r['path']).read_bytes();assert len(b)==r['bytes'] and sha(b)==r['sha256']
m=load(A/'ACTUAL_MERGE_VERIFICATION.json')
assert m['status']=='claimed_solved' and m['all_expected_paths_exact']==43 and m['all_target_file_hashes_exact']==42 and m['all_other_queue_bytes_equal']
root=load(A/'root_exact_live_receipt.json')
assert root['status']=='PASS_COMPLETE_PR359_EXACT_LIVE_AND_SUBMISSION' and root['head']==m['reviewed_head']
assert root['fresh_root_complete_package_replay'] and root['all_agent_full_outputs_compared']
post=load(A/'ROOT_POST_MERGE_VERIFICATION.json')
assert post['status']=='PASS_COMPLETE_PR359_POST_MERGE' and post['actual_merge']==m['actual_merge']
assert post['all_43_source_bindings_exact'] and post['all_37_original_math_files_unchanged'] and post['closed_namespaces_unchanged']
for e in c['sealed_submission_files']:
 b=(REPO/'problems/30001370_basin_boundaries/preprint'/e['path']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256']
cmd={'stage':'stage','inspect_draft':'inspect','publish':'publish','inspect_published':'inspect'}[step]
args=['python3',str(REPO/'zenodo_deposit_tool/zenodo.py'),cmd,str(MANIFEST)]
if step=='stage':assert not (D/'stage_receipt.json').exists() and not (D/'stage.stdout').exists() and not (D/'publish_receipt.json').exists(),'Do not duplicate a stage; inspect saved state after an uncertain outcome'
else:
 staged=load(D/'stage_receipt.json');assert staged['environment']=='production' and type(staged['id']) is int
 if step=='publish':
  draft=load(D/'inspect_draft_receipt.json');assert draft['id']==staged['id'] and draft['state']=='ready_to_publish'
  assert not (D/'publish_receipt.json').exists() and not (D/'publish.stdout').exists(),'Existing or uncertain publication attempt; use read-only inspect'
  args+=['--confirm-id',str(staged['id'])]
 if step=='inspect_published':args+=['--check-doi']
started=datetime.now(timezone.utc).isoformat()
result=subprocess.run(args,cwd=REPO,capture_output=True)
(D/(step+'.stdout')).write_bytes(result.stdout);(D/(step+'.stderr')).write_bytes(result.stderr)
execution={'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),'command':args,'exit_code':result.returncode,'stdout_bytes':len(result.stdout),'stdout_sha256':sha(result.stdout),'stderr_bytes':len(result.stderr),'stderr_sha256':sha(result.stderr),'automatic_mutation_retry':False}
(D/(step+'_execution.json')).write_text(json.dumps(execution,indent=2)+'\n')
assert result.returncode==0,(step,result.returncode,result.stderr.decode(errors='replace'))
receipt=json.loads(result.stdout)
assert receipt['environment']=='production' and receipt['title']==load(MANIFEST)['metadata']['title']
assert len(receipt['files'])==2
for r in receipt['files']:
 b=(A/'preprint'/r['name']).read_bytes();assert len(b)==r['size'] and sha(b)==r['sha256']
assert receipt['metadata_normalizations']==[],'Stop if even a supported metadata representation changed; inspect exact reviewed metadata before promotion'
if step in {'publish','inspect_published'}:
 assert receipt['state']=='published' and receipt['id']==staged['id'] and receipt['doi']
 assert receipt['doi_url']=='https://doi.org/'+receipt['doi'] and receipt['record_url']=='https://zenodo.org/records/'+str(receipt['id'])
else:assert receipt['state']=='ready_to_publish'
(D/(step+'_receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))

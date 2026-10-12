"""One explicitly authorized production kit step; no automatic mutation retry."""
from pathlib import Path
import datetime,hashlib,json,subprocess,sys
D=Path(__file__).resolve().parent;A=D.parent;REPO=A.parents[2]
def load(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
step=sys.argv[1];assert step in {'stage','inspect_draft','publish','inspect_published'}
assert not load(A.parents[1]/'SHARED_GIT_WINDOW_STATUS.json')['shared_git_writes_paused'] or step in {'inspect_draft','inspect_published'}, 'Wait for released shared window before publication mutation.'
sys.path.insert(0,str(A))
from root_submission_gate import current_clearance
clear=current_clearance()
for e in clear['sealed_submission_files']:
 b=(A/'preprint'/e['path']).read_bytes()
 assert (REPO/'problems/30005649_qss_self_duality/preprint'/e['path']).read_bytes()==b
m=load(A/'ACTUAL_MERGE_VERIFICATION.json');assert m['status']=='claimed_solved' and m['all_expected_paths_exact']==21 and m['all_target_file_hashes_exact']==20 and m['all_other_queue_bytes_equal']
live=load(A/'root_exact_live_receipt.json');assert live['status']=='PASS_COMPLETE_PR344_EXACT_LIVE_AND_SUBMISSION' and live['head']==m['reviewed_head']
assert live['all_agent_full_outputs_compared'] and live['closed_namespaces_unchanged']
post=load(A/'ROOT_POST_MERGE_VERIFICATION.json');assert post['status']=='PASS_COMPLETE_PR344_POST_MERGE' and post['actual_merge']==m['actual_merge']
assert post['all_21_source_bindings_exact'] and post['all_15_original_math_files_unchanged'] and post['closed_namespaces_unchanged']
manifest=A/'preprint/zenodo-deposit.json';local=load(manifest)
args=['python3',str(REPO/'zenodo_deposit_tool/zenodo.py'),{'stage':'stage','inspect_draft':'inspect','publish':'publish','inspect_published':'inspect'}[step],str(manifest)]
assert not (D/(step+'.stdout')).exists() and not (D/(step+'_receipt.json')).exists(),'Prior or uncertain attempt exists; inspect read-only with a new capture label instead of repeating a mutation.'
if step=='stage':assert not (D/'publish_receipt.json').exists()
else:
 staged=load(D/'stage_receipt.json');assert staged['environment']=='production' and type(staged['id']) is int
 if step=='publish':
  draft=load(D/'inspect_draft_receipt.json');assert draft['id']==staged['id'] and draft['state']=='ready_to_publish'
  args+=['--confirm-id',str(staged['id'])]
 if step=='inspect_published':args+=['--check-doi']
started=utc();(D/(step+'_preexecution.json')).write_text(json.dumps({'utc':started,'argv':args,'manifest_sha256':sha(manifest.read_bytes()),'orchestrator_sha256':sha(Path(__file__).read_bytes())},indent=2)+'\n')
p=subprocess.run(args,cwd=REPO,capture_output=True)
(D/(step+'.stdout')).write_bytes(p.stdout);(D/(step+'.stderr')).write_bytes(p.stderr)
(D/(step+'_execution.json')).write_text(json.dumps({'started_utc':started,'finished_utc':utc(),'argv':args,'exit_code':p.returncode,'stdout_bytes':len(p.stdout),'stdout_sha256':sha(p.stdout),'stderr_bytes':len(p.stderr),'stderr_sha256':sha(p.stderr),'automatic_mutation_retry':False},indent=2)+'\n')
assert p.returncode==0,(step,p.stderr.decode(errors='replace'))
r=json.loads(p.stdout);assert r['environment']=='production' and r['title']==local['metadata']['title'] and r['metadata_normalizations']==[]
assert len(r['files'])==2 and {e['name'] for e in r['files']}=={Path(e['path']).name for e in local['files']}
for e in r['files']:
 b=(A/'preprint'/e['name']).read_bytes();assert len(b)==e['size'] and sha(b)==e['sha256']
if step in {'publish','inspect_published'}:
 assert r['state']=='published' and r['id']==staged['id'] and r['doi']
 assert r['doi_url']=='https://doi.org/'+r['doi'] and r['record_url']=='https://zenodo.org/records/'+str(r['id'])
else:assert r['state']=='ready_to_publish'
(D/(step+'_receipt.json')).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))

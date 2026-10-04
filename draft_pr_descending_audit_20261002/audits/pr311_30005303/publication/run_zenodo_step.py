"""One production-kit operation after exact merge; never retry mutations automatically."""
from pathlib import Path
import sys, subprocess, json

D = Path(__file__).resolve().parent
A = D.parent
sys.path.insert(0,str(A))
from root_submission_gate import current_clearance, load, pin, utc, sha, R, O, window

step = sys.argv[1]
assert step in {'stage','inspect_draft','publish','inspect_published'}
if step in {'stage','publish'}:
    window()
clear = current_clearance()
merged = load(A/'ACTUAL_MERGE_VERIFICATION.json')
post = load(A/'ROOT_POST_MERGE_VERIFICATION.json')
assert merged['status'] == 'PASS_PR311_EXACT_MERGE'
assert post['status'] == 'PASS_PR311_POST_MERGE_EXACT_SUBMISSION' and post['actual_merge'] == merged['actual_merge']
assert post['original_attempt_files_unchanged'] == 29 and post['all_other_queue_bytes_equal']
assert post['all_five_formal_Git_disk_cleared_bytes_modes_equal'] and post['closed_scientific_and_review_inputs_unchanged']
manifest = O/'zenodo-deposit.json'
local = load(manifest)
kit = R/'zenodo_deposit_tool/zenodo.py'
assert pin(kit)['sha256'] == '26f264df93b657137b343acc05ae87a3e8e60d46cbbb8b822bc327d77b89c277'
assert len(local['metadata']) == 11 and len(local['files']) == 2
for n,e in clear['formal_submission_files'].items():
    assert pin(O/n) == e
assert not (D/(step+'_preexecution.json')).exists(), 'Prior or uncertain attempt exists; inspect saved state read-only before repeating any mutation.'
argv = ['/opt/homebrew/bin/python3','-B',str(kit),
        {'stage':'stage','inspect_draft':'inspect','publish':'publish','inspect_published':'inspect'}[step],str(manifest)]
if step != 'stage':
    staged = load(D/'stage_receipt.json')
    assert staged['environment'] == 'production' and type(staged['id']) is int
    if step == 'publish':
        draft = load(D/'inspect_draft_receipt.json')
        assert draft['id'] == staged['id'] and draft['state'] == 'ready_to_publish'
        argv += ['--confirm-id',str(staged['id'])]
    if step == 'inspect_published':
        argv += ['--check-doi']
start = utc()
(D/(step+'_preexecution.json')).write_text(json.dumps({'utc':start,'argv':argv,'manifest':pin(manifest),
    'kit':pin(kit),'orchestrator':pin(Path(__file__))},indent=2)+'\n')
run = subprocess.run(argv,cwd=R,capture_output=True)
for kind,b in [('stdout',run.stdout),('stderr',run.stderr)]:
    (D/(step+'.'+kind)).write_bytes(b)
(D/(step+'_execution.json')).write_text(json.dumps({'started_utc':start,'ended_utc':utc(),'argv':argv,
    'exit_code':run.returncode,'stdout_bytes':len(run.stdout),'stdout_sha256':sha(run.stdout),
    'stderr_bytes':len(run.stderr),'stderr_sha256':sha(run.stderr),'automatic_mutation_retry':False},indent=2)+'\n')
assert run.returncode == 0, (step,run.stderr.decode(errors='replace'))
record = json.loads(run.stdout)
assert record['environment'] == 'production' and record['title'] == local['metadata']['title']
assert isinstance(record['metadata_normalizations'],list)
assert len(record['files']) == 2 and {x['name'] for x in record['files']} == {x['path'] for x in local['files']}
for x in record['files']:
    b = (O/x['name']).read_bytes()
    assert len(b) == x['size'] and sha(b) == x['sha256']
if step in {'publish','inspect_published'}:
    assert record['state'] == 'published' and record['id'] == staged['id']
    assert record['doi'] and record['doi_url'] == 'https://doi.org/'+record['doi']
    assert record['record_url'] == 'https://zenodo.org/records/'+str(record['id'])
else:
    assert record['state'] == 'ready_to_publish'
current_clearance()
(D/(step+'_receipt.json')).write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))

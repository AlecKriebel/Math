"""Fresh complete live-source and cleared-submission binding before PR359 merge."""
import base64, json
from pathlib import Path
from root_submission_gate import A, R, Q, Capture, current_clearance, load, sha, utc, package_replay, closed_reviews, queue_binding

clear = current_clearance()
reviewed = load(A/'repaired_snapshot_manifest.json')
original = load(A/'snapshot_manifest.json')
H, B = reviewed['head'], reviewed['base']
original_by = {e['path']: e for e in original['files']}
expected = {e['path'] for e in reviewed['files']}
assert len(expected) == 43 and len(original_by) == 38
capture = Capture('exact_live')
git = capture.git
assert git('branch', '--show-current').strip() == b'main'
assert capture.run('merge_head', ['git', 'rev-parse', '-q', '--verify', 'MERGE_HEAD'], ok=(0, 1)).returncode == 1
assert git('rev-parse', 'HEAD').decode().strip() == B
ix = Path(git('rev-parse', '--git-path', 'index').decode().strip())
ix = ix if ix.is_absolute() else R/ix
index = ix.read_bytes()
pr = json.loads(capture.run('api_pr_before', ['gh', 'api', 'repos/AlecKriebel/Math/pulls/359']).stdout)
assert pr['state'] == 'open' and pr['head']['sha'] == H and pr['base']['sha'] == B
assert pr['head']['ref'] == 'math/30001370-basin-boundaries-reviewed'
assert set(git('diff', '--name-only', B, H).decode().splitlines()) == expected
bindings = []
for i, e in enumerate(reviewed['files']):
    path = e['path']
    b = git('show', f'{H}:{path}')
    assert len(b) == e['bytes'] and sha(b) == e['sha256'] and b == (A/'repaired_snapshot'/path).read_bytes()
    meta = git('ls-tree', H, '--', path).split(b'\t', 1)[0].split()
    assert meta == [b'100644', b'blob', e['git_blob_sha'].encode()]
    api = json.loads(capture.run('api_blob_'+str(i), ['gh', 'api', f"repos/AlecKriebel/Math/git/blobs/{e['git_blob_sha']}"]).stdout)
    assert api['sha'] == e['git_blob_sha'] and api['encoding'] == 'base64' and api['size'] == len(b)
    assert base64.b64decode(api['content']) == b
    if path in original_by and path != Q:
        old = original_by[path]
        assert (e['bytes'], e['sha256'], e['git_blob_sha']) == (old['bytes'], old['sha256'], old['git_blob_sha'])
    bindings.append({**e, 'fresh_entire_API_body_matches': True})
for e in clear['sealed_submission_files']:
    native_path = 'problems/30001370_basin_boundaries/preprint/'+e['path']
    assert git('show', f'{H}:{native_path}') == (A/'preprint'/e['path']).read_bytes()
queue = queue_binding(capture, B, H)
package = package_replay(capture)
closures = closed_reviews(capture)
last = json.loads(capture.run('api_pr_after', ['gh', 'api', 'repos/AlecKriebel/Math/pulls/359']).stdout)
remote = json.loads(capture.run('api_main_after', ['gh', 'api', 'repos/AlecKriebel/Math/git/ref/heads/main']).stdout)
assert last['state'] == 'open' and last['head']['sha'] == H and last['base']['sha'] == B
assert remote['object']['sha'] == B and git('rev-parse', 'HEAD').decode().strip() == B
assert ix.read_bytes() == index
current_clearance()
result = {'utc': utc(), 'status': 'PASS_COMPLETE_PR359_EXACT_LIVE_AND_SUBMISSION', 'pr': 359,
          'head': H, 'base': B, 'original_head': original['head'], 'fresh_complete_bindings': bindings,
          'original_math_files_unchanged': 37, **queue, 'fresh_root_complete_package_replay': True,
          'all_agent_full_outputs_compared': True, 'package': package, 'fresh_closed_reviews': closures,
          'entire_index_and_head_unchanged': True, 'source_and_proof_percent': 100,
          'priority_certified': False, 'acceptance_publication_workflow_percent': 80,
          'actual_merge_zenodo_tracker_pending': True, 'captures': capture.entries,
          'program_sha256': sha(Path(__file__).read_bytes()),
          'shared_checker_sha256': sha((A/'root_submission_gate.py').read_bytes()),
          'scope': 'Fresh exact live Git/API/head/queue/submission and whole-output comparisons. Universal mathematics and bounded priority are evaluated in the analytical reports, not inferred from finite executions.'}
(A/'root_exact_live_receipt.json').write_text(json.dumps(result, indent=2)+'\n')
c = load(A/'acceptance_criteria.json')
c.update(accepted_status='claimed_solved', exact_live_root_and_whole_gates_pending=False,
         fresh_whole_exact_live_pending=False, workflow_completion_percent=80)
(A/'acceptance_criteria.json').write_text(json.dumps(c, indent=2)+'\n')
print(json.dumps({k: v for k, v in result.items() if k not in {'captures', 'fresh_complete_bindings'}}, indent=2))

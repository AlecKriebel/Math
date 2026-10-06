"""Fresh actual-merge/source/submission/replay verification before publication."""
import base64, json
from pathlib import Path
from root_submission_gate import A, R, Q, Capture, current_clearance, load, sha, utc, package_replay, closed_reviews, queue_binding

clear = current_clearance()
accepted = load(A/'ACTUAL_MERGE_VERIFICATION.json')
m = load(A/'repaired_snapshot_manifest.json')
original = load(A/'snapshot_manifest.json')
M, H, B = accepted['actual_merge'], m['head'], m['base']
assert accepted['reviewed_head'] == H and accepted['actual_parents'] == [B, H]
assert accepted['all_expected_paths_exact'] == 22 and accepted['all_target_file_hashes_exact'] == 21
capture = Capture('post_merge')
git = capture.git
assert git('branch', '--show-current').strip() == b'main'
assert capture.run('merge_head', ['git', 'rev-parse', '-q', '--verify', 'MERGE_HEAD'], ok=(0, 1)).returncode == 1
current = git('rev-parse', 'HEAD').decode().strip()
ix = Path(git('rev-parse', '--git-path', 'index').decode().strip())
ix = ix if ix.is_absolute() else R/ix
index = ix.read_bytes()
pr = json.loads(capture.run('api_pr_merged', ['gh', 'api', 'repos/AlecKriebel/Math/pulls/356']).stdout)
assert pr['merged'] and pr['merge_commit_sha'] == M and pr['head']['sha'] == H
assert git('show', '-s', '--format=%P', M).decode().strip().split() == [B, H]
assert git('show', '-s', '--format=%T', M) == git('show', '-s', '--format=%T', H)
assert set(git('diff', '--name-only', B, M).decode().splitlines()) == {e['path'] for e in m['files']}
capture.run('merge_ancestor_local', ['git', 'merge-base', '--is-ancestor', M, 'HEAD'])
remote = json.loads(capture.run('api_main', ['gh', 'api', 'repos/AlecKriebel/Math/git/ref/heads/main']).stdout)
capture.run('merge_ancestor_remote', ['git', 'merge-base', '--is-ancestor', M, remote['object']['sha']])
original_by = {e['path']: e for e in original['files']}
bindings = []
for i, e in enumerate(m['files']):
    path = e['path']
    b = git('show', f'{M}:{path}')
    assert len(b) == e['bytes'] and sha(b) == e['sha256']
    assert (R/path).read_bytes() == b == git('show', f'{current}:{path}')
    meta = git('ls-tree', M, '--', path).split(b'\t', 1)[0].split()
    assert meta == [b'100644', b'blob', e['git_blob_sha'].encode()]
    api = json.loads(capture.run('api_blob_'+str(i), ['gh', 'api', f"repos/AlecKriebel/Math/git/blobs/{e['git_blob_sha']}"]).stdout)
    assert api['sha'] == e['git_blob_sha'] and api['encoding'] == 'base64' and api['size'] == len(b)
    assert base64.b64decode(api['content']) == b
    if path in original_by and path != Q:
        old = original_by[path]
        assert (e['bytes'], e['sha256'], e['git_blob_sha']) == (old['bytes'], old['sha256'], old['git_blob_sha'])
    bindings.append({**e, 'fresh_entire_API_body_and_current_disk_match': True})
for e in clear['sealed_submission_files']:
    assert (R/'problems/30001552_antimorphic_periods/preprint'/e['path']).read_bytes() == (A/'preprint'/e['path']).read_bytes()
queue = queue_binding(capture, B, M)
package = package_replay(capture)
closures = closed_reviews(capture)
assert ix.read_bytes() == index and git('rev-parse', 'HEAD').decode().strip() == current
current_clearance()
result = {'utc': utc(), 'status': 'PASS_COMPLETE_PR356_POST_MERGE', 'pr': 356,
          'actual_merge': M, 'reviewed_head': H, 'actual_parents': [B, H],
          'all_22_source_bindings_exact': True, 'all_16_original_math_files_unchanged': True,
          'closed_namespaces_unchanged': True, 'entire_index_and_head_unchanged': True,
          'fresh_complete_source_bindings': bindings, **queue, 'package': package,
          'fresh_closed_reviews': closures, 'all_agent_full_outputs_compared': True,
          'captures': capture.entries, 'program_sha256': sha(Path(__file__).read_bytes()),
          'shared_checker_sha256': sha((A/'root_submission_gate.py').read_bytes()),
          'scope': 'Actual ordered two-parent merge, all reviewed source blobs/current disk/API, final submission, whole replays and closed namespaces verified. Production publication and tracker remain separate.'}
(A/'ROOT_POST_MERGE_VERIFICATION.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({k: v for k, v in result.items() if k not in {'captures', 'fresh_complete_source_bindings'}}, indent=2))

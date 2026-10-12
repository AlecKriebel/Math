"""Prepared exact-live gate for the reviewed PR344 integration head."""
from pathlib import Path
import base64, json
from root_submission_gate import (A, R, Q, TARGET, ORIGINAL_HEAD, BRANCH, Capture,
                                  current_clearance, load, pin, sha, tree_binding,
                                  package_integrity, utc, window)

assert not (A / 'root_exact_live_receipt.json').exists()
window()
clear = current_clearance()
manifest = load(A / 'repaired_snapshot_manifest.json')
assert manifest['pr'] == 344 and manifest['original_frozen_head'] == ORIGINAL_HEAD
capture = Capture('exact_live')
index_path = Path(capture.git('rev-parse', '--git-path', 'index').decode().strip())
if not index_path.is_absolute():
    index_path = R / index_path
index_before = index_path.read_bytes()
assert capture.git('branch', '--show-current').strip() == b'main'
assert capture.git('rev-parse', 'HEAD').decode().strip() == manifest['base']
api = json.loads(capture.run('live_pr', ['gh', 'api', 'repos/AlecKriebel/Math/pulls/344']).stdout)
assert api['state'] == 'open' and api['head']['sha'] == manifest['head']
assert api['head']['ref'] == BRANCH and api['base']['sha'] == manifest['base']
parents = capture.git('show', '-s', '--format=%P', manifest['head']).decode().strip().split()
assert parents == [ORIGINAL_HEAD, manifest['base']]
binding = tree_binding(capture, manifest['base'], manifest['head'])
rows = json.loads(capture.run('live_files', ['gh', 'api',
                     'repos/AlecKriebel/Math/pulls/344/files?per_page=100']).stdout)
expected = {entry['path']: entry for entry in manifest['files']}
assert len(rows) == 21 and {row['filename'] for row in rows} == set(expected)
for number, row in enumerate(rows):
    name = row['filename']
    entry = expected[name]
    assert row['sha'] == entry['git_blob_sha']
    assert row['status'] == ('modified' if name == Q else 'added')
    blob = json.loads(capture.run('live_blob_' + str(number), ['gh', 'api',
                       'repos/AlecKriebel/Math/git/blobs/' + row['sha']]).stdout)
    assert blob['encoding'] == 'base64' and blob['sha'] == entry['git_blob_sha']
    body = base64.b64decode(blob['content'])
    assert len(body) == blob['size'] == entry['bytes'] and sha(body) == entry['sha256']
    assert (A / 'repaired_snapshot' / name).read_bytes() == body
    if name.startswith(TARGET + '/preprint/'):
        assert (A / 'preprint' / Path(name).name).read_bytes() == body
package = package_integrity(capture)
current_clearance()
last = json.loads(capture.run('last_live_pr', ['gh', 'api', 'repos/AlecKriebel/Math/pulls/344']).stdout)
remote = json.loads(capture.run('last_main_ref', ['gh', 'api', 'repos/AlecKriebel/Math/git/ref/heads/main']).stdout)
assert last['state'] == 'open' and last['head']['sha'] == manifest['head']
assert last['base']['sha'] == remote['object']['sha'] == manifest['base']
assert capture.git('rev-parse', 'HEAD').decode().strip() == manifest['base']
assert index_path.read_bytes() == index_before
receipt = dict(utc=utc(), status='PASS_COMPLETE_PR344_EXACT_LIVE_AND_SUBMISSION',
               head=manifest['head'], base=manifest['base'], actual_head_parents=parents,
               **binding, package=package, full_api_git_blob_disk_bytes_modes_exact=21,
               fresh_root_package_integrity_and_prior_full_comparison=True,
               all_agent_full_outputs_compared=True, closed_namespaces_unchanged=True,
               current_eight_author_inputs_unchanged=True,
               historical_adverse_reviews_retained=True,
               final_clean_review=3, first_priority_certified=False,
               checkout_and_entire_index_unchanged=True,
               native_capture_directory=str(capture.directory), program=pin(Path(__file__)),
               workflow_percent=85, merge_pending=True, production_publication_pending=True)
(A / 'root_exact_live_receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
criteria = load(A / 'acceptance_criteria.json')
criteria.update(updated_utc=receipt['utc'], exact_live_root_and_whole_gates_pending=False,
                fresh_whole_exact_live_pending=False, workflow_completion_percent=85,
                reviewed_integration_head=manifest['head'], reviewed_literal_main_base=manifest['base'])
(A / 'acceptance_criteria.json').write_text(json.dumps(criteria, indent=2) + '\n')
print(json.dumps(receipt, indent=2))

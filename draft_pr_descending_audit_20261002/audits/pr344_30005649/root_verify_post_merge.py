"""Prepared read-only source/package/evidence gate after actual PR344 merge."""
from pathlib import Path
import json
from root_submission_gate import (A, R, Capture, current_clearance, load, pin,
                                  tree_binding, package_integrity, utc)

assert not (A / 'ROOT_POST_MERGE_VERIFICATION.json').exists()
clear = current_clearance()
merged = load(A / 'ACTUAL_MERGE_VERIFICATION.json')
manifest = load(A / 'repaired_snapshot_manifest.json')
assert merged['status'] == 'claimed_solved' and merged['reviewed_head'] == manifest['head']
assert merged['all_expected_paths_exact'] == 21 and merged['all_target_file_hashes_exact'] == 20
assert merged['actual_parents'] == [manifest['base'], manifest['head']]
capture = Capture('post_merge')
index_path = Path(capture.git('rev-parse', '--git-path', 'index').decode().strip())
if not index_path.is_absolute():
    index_path = R / index_path
index_before = index_path.read_bytes()
head_before = capture.git('rev-parse', 'HEAD').strip()
assert capture.git('branch', '--show-current').strip() == b'main'
api = json.loads(capture.run('actual_merged_pr', ['gh', 'pr', 'view', '344', '--json',
                              'state,headRefOid,mergeCommit,mergedAt,url']).stdout)
assert api['state'] == 'MERGED' and api['headRefOid'] == manifest['head']
assert api['mergeCommit']['oid'] == merged['actual_merge'] and api['mergedAt'] == merged['merged_at']
assert capture.git('show', '-s', '--format=%P', merged['actual_merge']).decode().strip().split() == merged['actual_parents']
assert capture.run('merge_ancestor', ['git', 'merge-base', '--is-ancestor',
                                  merged['actual_merge'], 'HEAD']).returncode == 0
binding = tree_binding(capture, manifest['base'], merged['actual_merge'], require_disk=True)
package = package_integrity(capture)
current_clearance()
assert capture.git('rev-parse', 'HEAD').strip() == head_before
assert index_path.read_bytes() == index_before
receipt = dict(utc=utc(), status='PASS_COMPLETE_PR344_POST_MERGE',
               actual_merge=merged['actual_merge'], reviewed_head=manifest['head'],
               **binding, all_21_source_bindings_exact=True,
               all_15_original_math_files_unchanged=True,
               closed_namespaces_unchanged=True, current_eight_author_inputs_unchanged=True,
               package=package, checkout_and_entire_index_unchanged=True,
               native_capture_directory=str(capture.directory), program=pin(Path(__file__)),
               workflow_percent=90, production_publication_pending=True, tracker_pending=True)
(A / 'ROOT_POST_MERGE_VERIFICATION.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))

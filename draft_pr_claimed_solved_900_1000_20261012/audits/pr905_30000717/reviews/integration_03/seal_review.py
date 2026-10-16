#!/usr/bin/env python3
"""Validate the independent evidence and seal this review's explicit public files."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parents[1]
ROOT = AUDIT.parents[2]
HEAD = 'fb2d639e2508cc45c9327e02624ae7a38e82b58a'
ORIGINAL = '330a544a53b9e3e01bb0ed70817a5f4a79cc6a0a'
MAIN = '01ad94d92e7938d71aa38a2e504c64fc4eae04fb'
TREE = 'eb329e2c8d6772d7b5f56fc2ba281bd04db97630'


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


utc = datetime.now(timezone.utc).isoformat()
tree = json.loads((HERE / 'evidence/tree_and_frozen_checks.json').read_text())
remote = json.loads((HERE / 'evidence/remote_metadata.json').read_text())
sources = json.loads((HERE / 'evidence/fresh_source_hashes.json').read_text())
need(tree['verdict'] == 'PASS_LOCAL_TREE_AND_FROZEN_BYTE_CHECKS', 'Local tree evidence must pass')
need(tree['original_head'] == ORIGINAL and tree['integrated_head'] == HEAD and tree['main_parent'] == MAIN, 'Local identity mismatch')
need(sources['source_count'] == 6 and sources['all_source_hashes_unchanged'], 'Fresh source hashes must pass')
for snapshot in [remote['connector_snapshot'], remote['rest_snapshot']]:
    need(snapshot['head_sha'] == HEAD and snapshot['base_sha'] == MAIN and snapshot['state'] == 'open' and not snapshot['draft'] and not snapshot['merged'] and snapshot['changed_files'] == 31, 'Live PR identity/status mismatch')
commit = remote['remote_git_commit']
need(commit['sha'] == HEAD and commit['tree'] == TREE and commit['parents'] == [ORIGINAL, MAIN], 'Remote Git object metadata mismatch')
files = remote['remote_changed_files']
need(len(files) == 31 and sorted(x['filename'] for x in files) == tree['tree_differences_from_main'], 'Live PR changed-file membership mismatch')
for item in files:
    oid = subprocess.check_output(['git', 'rev-parse', HEAD + ':' + item['filename']], cwd=ROOT, text=True).strip()
    need(oid == item['sha'], 'Remote changed-file Git blob SHA mismatch: ' + item['filename'])
    if item['filename'].endswith('/QUEUE.md'):
        need(item['status'] == 'modified' and item['additions'] == item['deletions'] == 1, 'Live queue diff mismatch')
    else:
        need(item['status'] == 'added' and item['deletions'] == 0, 'Live packet addition mismatch')
result = {'schema_version': 1, 'review_family': 'independent_nonmathematical_merge_integration_03', 'utc': utc, 'pr': 905, 'problem_id': '30000717', 'problem_number': 'OWR-1465-011', 'candidate_revision': 2, 'original_audited_head': ORIGINAL, 'integrated_head': HEAD, 'main_parent': MAIN, 'integrated_tree': TREE, 'verdict': 'PASS_CLEAN_INTEGRATION_NO_REPAIRS', 'required_repairs': [], 'integration_gap': False, 'candidate_mutations': False, 'git_mutations': False, 'branch': 'main', 'external_human_contact_initiated_or_prepared': False, 'merge_deposit_spreadsheet_actions': False, 'raw_third_party_source_data_copied': False, 'original_packet_files_byte_identical': 30, 'frozen_publication_files_byte_identical': 8, 'main_difference_paths': 31, 'unrelated_main_leaf_entries_preserved': tree['unrelated_main_leaf_entries_preserved'], 'nontarget_queue_bytes_preserved': tree['queue']['nontarget_bytes'], 'target_queue_row': {'byte_identical_to_original': True, 'status': 'claimed_solved', 'turns': '1/5', 'holds': [], 'only_changed_columns': ['Status', 'Turns', 'Findings']}, 'source_identity_hashes_independently_recomputed': True, 'source_identity_and_holds_unchanged_across_original_main_integrated': True, 'fresh_primary_source_hashes_unchanged': 6, 'remote_commit_tree_and_parents_match': True, 'remote_changed_file_git_blob_hashes_match': 31, 'live_pr_status': remote['rest_snapshot'], 'mergeability_observation': 'Connector snapshot reported true; subsequent REST snapshot returned null/unknown. This transient API field is not used as an integration proof; recheck ordinary merge eligibility before merging.', 'strongest_verified_result': 'The integrated PR differs from its recorded main parent only by the unchanged original 30-file target packet and a byte-exact transplant of the original accepted target queue row. All unrelated main tree entries and all other queue bytes are preserved; frozen publication revision 2 and source identity/holds are unchanged.', 'promotion_scope': 'Clears only the nonmathematical integration gate for the exact integrated head and recorded main parent. Completed mathematical/full-package reviews retain their original scope and limitations.', 'remaining_integration_gap': None, 'completion_percent': 100, 'completion_scope': 'This narrow integration audit, not exhaustive mathematics or literature discovery', 'public_artifact_manifest': 'MANIFEST.json'}
(HERE / 'REVIEW_RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
review = f'''# PR905 independent integration review

**PASS — clean integration, no repairs.** Completed {utc}; completion estimate
100% of this narrow nonmathematical integration review. No integration gap was
found. This review does not replace the completed mathematical, computation,
source/model, or sequential full-package reviews.

## Exact claim and falsifiable success criteria

The integrated commit `{HEAD}` must preserve the original packet at
`{ORIGINAL}` and the eight frozen publication files of revision 2. Relative to
its recorded main parent `{MAIN}`, differences must be confined to the 30
target packet files and the exact accepted target 30000717 queue row. Every
other tree entry and queue byte must be preserved, source identity and holds
must remain unchanged, and live PR metadata must identify the same objects.
Any unexpected path, mode, object hash, packet byte, queue cell, source hash,
hold, or identity change falsifies the clean-integration conclusion.

## Independently reproduced evidence

- Recomputed Git SHA1 object identities from raw commit/root-tree bytes for
  the original head, recorded main parent, and integrated head. The integrated
  tree is `{TREE}`; its ordered parents are the original audited head and
  recorded main parent. Their common base is the original commit's parent.
- Enumerated the complete recursive trees. The difference from main has
  exactly 31 paths: 30 added target packet files and `QUEUE.md`. All
  {tree['unrelated_main_leaf_entries_preserved']:,} other main leaf entries,
  including their modes and object IDs, are identical. The packet has exactly
  its original 30-file membership, unchanged modes and blob IDs. Recomputed
  each file's SHA256 and Git blob SHA1; compared original commit, integrated
  commit, and captured local bytes directly against `ORIGINAL_SNAPSHOT.json`.
- Removed the unique target row from both main and integrated queues and
  directly compared the remainder: all {tree['queue']['nontarget_bytes']:,}
  bytes are identical. The integrated target row equals both the original
  row and `GATED_QUEUE_ROW.md` byte-for-byte. Only Status, Turns, and Findings
  differ from main; status is `claimed_solved`, turns are `1/5`, holds empty.
  This also checks headers, whitespace, row ordering, unrelated notes/links,
  newline termination, and every other queue cell.
- Recomputed `statement_hash` from the private statement bytes and
  `review_hash` from the documented sorted-JSON encoding of problem and prior
  research. They match the preflight and all original/main/integrated
  catalogue/assessment records. Target identity remains 30000717 /
  OWR-1465-011, present; catalogue and assessment holds remain empty. The
  original native state remains absent. No private statement content is
  redistributed in this review.
- Compared all eight active publication files by size and SHA256 to
  `PREPUBLICATION_FREEZE.json`, including PDF, ZIP and deposit metadata. They
  match frozen revision 2 exactly. The latest full-package review still binds
  the original head and says `PASS_FROZEN_REVISION2_NO_REPAIRS`.
- Independently refreshed all six previously identified primary-source URLs
  in memory. All sizes and SHA256 values match the fresh full-package review;
  no PDF or other raw third-party source data was saved or copied.
- Two authenticated read-only GitHub metadata routes identify the same live
  open, nondraft, unmerged PR head and recorded base. GitHub's Git commit API
  confirms the tree and both ordered parents. Its paginated changed-file
  list has exactly the expected 31 paths, and every reported Git blob SHA
  matches the independently checked local integrated tree. The queue has
  one addition and one deletion; all 30 packet files are additions.

## Boundary and promotion conclusion

No mathematical candidate edit occurred. A merge commit's comparison with
its first parent includes inherited main history; the relevant preservation
test is its comparison with the recorded current-main second parent. That
comparison contains no unrelated changes. The eight publication files are
local frozen artifacts, so their preservation is checked separately from
the original PR's 30-file packet.

The exact integration is cleared. The latest REST response's mergeability
field was `null/unknown`, after a connector response reported `true`; this
transient field is not evidence for or against byte preservation. Ordinary
live merge eligibility should be checked by the root at the action boundary.
The exact-head and exact-parent checks are time-bound observations; a later
head/base movement requires a renewed identity check. No first-priority,
current-open-status, conventional human-peer-review, or exhaustive-literature
claim is added by this review. Existing package limitations remain intact.

## Checkable artifacts and action boundary

`verify_integration.py` reproduces local tree, packet, queue, source-identity,
and frozen-byte checks using read-only Git operations. `refresh_source_hashes.py`
repeats only the six source-byte checks in memory. `seal_review.py` validates
recorded remote metadata and seals the explicit public allowlist. Evidence is
in `evidence/tree_and_frozen_checks.json`, `evidence/fresh_source_hashes.json`,
and `evidence/remote_metadata.json`.

All writes were confined to this integration review folder. The shared
checkout remained on `main`; no Git mutation, candidate change, external
human contact, merge, deposit, release, or spreadsheet action was performed.
The parent/root remains responsible for its separately authorized actions.
'''
(HERE / 'REVIEW.md').write_text(review)
log = HERE / 'RESEARCH_LOG.md'
log.write_text(log.read_text() + f'''- {tree['utc_completed']} — Local exact-tree checks passed: 30 packet files,
  eight frozen publication files, exactly 31 changed paths, all 170,884
  unrelated main leaf entries, and all 411,942 nontarget queue bytes preserved.
  Source identity hashes were recomputed and empty holds confirmed at all
  three refs. Completion estimate: 80% of this integration review.
- {sources['utc']} — All six fresh source sizes and hashes matched the
  completed package review; bytes were processed only in memory. Completion
  estimate: 90% of this integration review.
- {utc} — Remote Git tree/parents and all 31 changed-file blob hashes match
  the independently checked local objects. Open/nondraft/unmerged exact head
  and base identity confirmed. Sealed PASS_CLEAN_INTEGRATION_NO_REPAIRS; no
  integration gap or repair. Completion estimate: 100% of this review.
''')
allowlist = ['.gitignore', 'REVIEW.md', 'REVIEW_RESULT.json', 'RESEARCH_LOG.md', 'verify_integration.py', 'refresh_source_hashes.py', 'seal_review.py', 'evidence/tree_and_frozen_checks.json', 'evidence/fresh_source_hashes.json', 'evidence/remote_metadata.json']
artifacts = {}
for name in allowlist:
    data = (HERE / name).read_bytes()
    artifacts[name] = {'bytes': len(data), 'sha256': sha(data)}
manifest = {'schema_version': 1, 'utc': utc, 'review_family': result['review_family'], 'pr': 905, 'problem_id': '30000717', 'candidate_revision': 2, 'original_head': ORIGINAL, 'integrated_head': HEAD, 'main_parent': MAIN, 'verdict': result['verdict'], 'completion_percent': 100, 'artifacts': artifacts, 'public_artifact_allowlist': allowlist, 'artifact_selection': 'Explicit intentional public allowlist; never infer publication membership by scanning the directory', 'manifest_self_hash_excluded': True, 'raw_third_party_source_data_included': False, 'private_or_temporary_directories': ['private_sources/', 'tmp/', '__pycache__/'], 'no_git_or_candidate_mutations': True, 'no_external_human_contact': True, 'verification': 'Recompute every allowlisted size/SHA256; rerun verify_integration.py for local object/byte checks. Remote metadata is a time-bound exact-head observation.'}
(HERE / 'MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps({'verdict': result['verdict'], 'completion_percent': 100, 'public_artifacts': len(allowlist), 'manifest_sha256': sha((HERE / 'MANIFEST.json').read_bytes()), 'review_result_sha256': sha((HERE / 'REVIEW_RESULT.json').read_bytes())}))

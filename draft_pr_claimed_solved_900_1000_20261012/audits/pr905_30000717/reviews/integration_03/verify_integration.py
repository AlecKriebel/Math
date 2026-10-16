#!/usr/bin/env python3
"""Read-only Git and local frozen-byte audit; writes only this review's evidence."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parents[1]
ROOT = AUDIT.parents[2]
ORIGINAL = '330a544a53b9e3e01bb0ed70817a5f4a79cc6a0a'
INTEGRATED = 'fb2d639e2508cc45c9327e02624ae7a38e82b58a'
MAIN = '01ad94d92e7938d71aa38a2e504c64fc4eae04fb'
PACKET = 'unsolved_math_prioritization/attempts/30000717/'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'
TARGET = b'30000717 / OWR-1465-011'


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def object_hash(kind, data):
    return hashlib.sha1(kind.encode() + b' ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def blob(ref, path):
    return git('show', ref + ':' + path)


def entries(ref):
    result = {}
    for item in git('ls-tree', '-rz', '--full-tree', ref).split(b'\0'):
        if item:
            info, path = item.split(b'\t', 1)
            mode, kind, oid = info.decode().split(' ')
            result[path.decode()] = {'mode': mode, 'type': kind, 'oid': oid}
    return result


def target_row(data):
    lines = data.splitlines(keepends=True)
    hits = [i for i, line in enumerate(lines) if line.startswith(b'|') and line.split(b'|')[2].strip() == TARGET]
    need(len(hits) == 1, 'Target must occur exactly once in each queue')
    idx = hits[0]
    return lines[idx], b''.join(lines[:idx] + lines[idx + 1:]), idx


def main():
    started = datetime.now(timezone.utc).isoformat()
    branch = git('branch', '--show-current').decode().strip()
    head = git('rev-parse', 'HEAD').decode().strip()
    need(branch == 'main', 'Shared checkout must remain on main')
    receipt = json.loads((AUDIT / 'MERGE_INTEGRATION_RECEIPT.json').read_text())
    snapshot = json.loads((AUDIT / 'ORIGINAL_SNAPSHOT.json').read_text())
    freeze = json.loads((AUDIT / 'publication/PREPUBLICATION_FREEZE.json').read_text())
    identity = json.loads((AUDIT / 'TARGET_IDENTITY_PREFLIGHT.json').read_text())
    need(receipt['original_audited_head'] == ORIGINAL and receipt['integrated_head'] == INTEGRATED and receipt['main_parent'] == MAIN, 'Receipt identity mismatch')
    need(snapshot['head'] == ORIGINAL and len(snapshot['files']) == 30, 'Original snapshot identity/count mismatch')
    need(freeze['reviewed_head'] == ORIGINAL and freeze['candidate_revision'] == 2 and len(freeze['files']) == 8, 'Publication freeze identity/count mismatch')

    object_checks = []
    for ref in [ORIGINAL, MAIN, INTEGRATED]:
        raw_commit = git('cat-file', 'commit', ref)
        need(object_hash('commit', raw_commit) == ref, 'Commit object hash mismatch')
        header = raw_commit.split(b'\n\n', 1)[0].decode().splitlines()
        tree = next(x.split(' ', 1)[1] for x in header if x.startswith('tree '))
        parents = [x.split(' ', 1)[1] for x in header if x.startswith('parent ')]
        tree_data = git('cat-file', 'tree', tree)
        need(object_hash('tree', tree_data) == tree, 'Root tree object hash mismatch')
        object_checks.append({'commit': ref, 'parents': parents, 'tree': tree, 'commit_git_sha1_recomputed': True, 'root_tree_git_sha1_recomputed': True})
    need(object_checks[2]['parents'] == [ORIGINAL, MAIN], 'Integrated commit parent order mismatch')
    need(object_checks[2]['tree'] == receipt['tree'], 'Integrated tree does not match receipt')
    need(git('merge-base', ORIGINAL, MAIN).decode().strip() == object_checks[0]['parents'][0], 'Unexpected common base')

    original_entries, main_entries, integrated_entries = [entries(ref) for ref in [ORIGINAL, MAIN, INTEGRATED]]
    original_packet = {p: v for p, v in original_entries.items() if p.startswith(PACKET)}
    integrated_packet = {p: v for p, v in integrated_entries.items() if p.startswith(PACKET)}
    need(set(original_packet) == set(snapshot['files']), 'Snapshot is not the exact original packet membership')
    need(original_packet == integrated_packet, 'Packet membership, blob identity, or mode changed')
    packet_checks = []
    for path, expected_sha256 in snapshot['files'].items():
        old = blob(ORIGINAL, path)
        new = blob(INTEGRATED, path)
        local = (AUDIT / 'original' / path).read_bytes()
        need(old == new == local, 'Packet bytes changed: ' + path)
        need(digest(old) == expected_sha256, 'Snapshot SHA256 mismatch: ' + path)
        need(object_hash('blob', old) == original_packet[path]['oid'], 'Packet Git blob SHA1 mismatch: ' + path)
        need(original_packet[path]['mode'] == '100644' and original_packet[path]['type'] == 'blob', 'Unexpected packet mode/type')
        packet_checks.append({'path': path, 'bytes': len(old), 'sha256': digest(old), 'git_blob_sha1': object_hash('blob', old), 'original_integrated_local_bytes_identical': True, 'snapshot_sha256_matches': True})

    changed = sorted(p for p in set(main_entries) | set(integrated_entries) if main_entries.get(p) != integrated_entries.get(p))
    expected_changed = sorted([QUEUE] + list(snapshot['files']))
    need(changed == expected_changed, 'Unexpected tree differences from recorded main parent')
    need(all(p not in main_entries for p in snapshot['files']), 'Packet additions unexpectedly overwrite main files')
    need(all(main_entries.get(p) == integrated_entries.get(p) for p in set(main_entries) | set(integrated_entries) if p not in expected_changed), 'Unrelated tree entry changed')
    diff_paths = git('diff-tree', '-r', '--no-commit-id', '--name-only', MAIN, INTEGRATED).decode().splitlines()
    need(sorted(diff_paths) == changed, 'Independent Git diff path set disagrees')

    main_queue, original_queue, integrated_queue = [blob(ref, QUEUE) for ref in [MAIN, ORIGINAL, INTEGRATED]]
    main_row, main_others, _ = target_row(main_queue)
    old_row, _, _ = target_row(original_queue)
    integrated_row, integrated_others, _ = target_row(integrated_queue)
    need(main_others == integrated_others, 'Nontarget queue bytes changed')
    need(old_row == integrated_row == (AUDIT / 'GATED_QUEUE_ROW.md').read_bytes(), 'Exact claimed_solved row was not transplanted')
    cells_old = main_row.rstrip(b'\n').split(b'|')
    cells_new = integrated_row.rstrip(b'\n').split(b'|')
    changed_columns = [i for i, (a, b) in enumerate(zip(cells_old, cells_new)) if a != b]
    need(len(cells_old) == len(cells_new) and changed_columns == [8, 9, 11], 'Unexpected target queue cell changes')
    need(cells_new[8].strip() == b'claimed_solved' and cells_new[9].strip() == b'1/5' and not cells_new[10].strip(), 'Target status, turns, or holds changed')
    queue_checks = {'main_sha256': digest(main_queue), 'original_sha256': digest(original_queue), 'integrated_sha256': digest(integrated_queue), 'transplanted_row_sha256': digest(integrated_row), 'nontarget_bytes': len(main_others), 'nontarget_sha256': digest(main_others), 'every_nontarget_byte_identical': True, 'target_row_byte_identical_to_original_and_gate': True, 'changed_pipe_columns': changed_columns, 'changed_column_names': ['Status', 'Turns', 'Findings'], 'status': 'claimed_solved', 'turns': '1/5', 'holds': []}
    for ref, raw in [(MAIN, main_queue), (ORIGINAL, original_queue), (INTEGRATED, integrated_queue)]:
        oid = [original_entries, main_entries, integrated_entries][[ORIGINAL, MAIN, INTEGRATED].index(ref)][QUEUE]['oid']
        need(object_hash('blob', raw) == oid, 'Queue Git blob SHA1 mismatch')
    need(main_entries[QUEUE]['mode'] == original_entries[QUEUE]['mode'] == integrated_entries[QUEUE]['mode'] == '100644', 'Queue mode changed')

    source = json.loads((AUDIT / 'source_record_private.txt').read_text())
    review_hash = digest(json.dumps([source['problem'], source['prior_research']], sort_keys=True).encode())
    statement_hash = digest(source['problem']['statement'].encode())
    need(review_hash == source['review_hash'] == identity['review_hash'] and statement_hash == identity['statement_hash'], 'Private source record identity mismatch')
    source_checks = []
    for ref in [ORIGINAL, MAIN, INTEGRATED]:
        catalog = json.loads(blob(ref, 'unsolved_math_prioritization/catalog.json'))
        target = [x for x in catalog if str(x['id']) == '30000717']
        need(len(target) == 1, 'Ambiguous catalogue identity')
        target = target[0]
        assessment = json.loads(blob(ref, 'unsolved_math_prioritization/assessments.json'))['30000717']
        state = json.loads(blob(ref, 'unsolved_math_prioritization/state.json')).get('30000717')
        need(target['statement_hash'] == statement_hash and target['review_hash'] == review_hash, 'Catalogue identity changed')
        need(target['holds'] == [] and assessment['holds'] == [], 'Source holds appeared or changed')
        need(target['present'] and target['problem_number'] == identity['problem_number'] and target['title'] == identity['title'], 'Target source identity changed')
        need(assessment['statement_hash'] == statement_hash and assessment['review_hash'] == review_hash, 'Assessment identity changed')
        need(state is None, 'Unexpected native target state at integration')
        source_checks.append({'ref': ref, 'id': target['id'], 'problem_number': target['problem_number'], 'statement_hash': statement_hash, 'review_hash': review_hash, 'catalog_holds': target['holds'], 'assessment_holds': assessment['holds'], 'present': target['present'], 'native_state_present': False})

    frozen_checks = []
    for path, expected in freeze['files'].items():
        data = (AUDIT / 'publication' / path).read_bytes()
        need(len(data) == expected['bytes'] and digest(data) == expected['sha256'], 'Frozen publication changed: ' + path)
        frozen_checks.append({'path': path, 'bytes': len(data), 'sha256': digest(data), 'unchanged': True})
    prior_review = json.loads((AUDIT / 'reviews/full_package_02/REVIEW_RESULT.json').read_text())
    need(prior_review['candidate_revision'] == 2 and prior_review['reviewed_head'] == ORIGINAL and prior_review['verdict'] == 'PASS_FROZEN_REVISION2_NO_REPAIRS' and prior_review['required_repairs'] == [], 'Prior accepted mathematical package identity changed')
    need(git('branch', '--show-current').decode().strip() == branch and git('rev-parse', 'HEAD').decode().strip() == head, 'Shared checkout moved during verification')
    result = {'schema_version': 1, 'utc_started': started, 'utc_completed': datetime.now(timezone.utc).isoformat(), 'pr': 905, 'problem_id': '30000717', 'original_head': ORIGINAL, 'integrated_head': INTEGRATED, 'main_parent': MAIN, 'branch': branch, 'shared_checkout_head_unchanged': head, 'verdict': 'PASS_LOCAL_TREE_AND_FROZEN_BYTE_CHECKS', 'git_object_checks': object_checks, 'original_packet_files_checked': packet_checks, 'tree_differences_from_main': changed, 'all_other_tree_entries_identical': True, 'unrelated_main_leaf_entries_preserved': len(main_entries) - 1, 'queue': queue_checks, 'source_identity_and_holds': source_checks, 'frozen_publication_files': frozen_checks, 'original_snapshot_sha256': digest((AUDIT / 'ORIGINAL_SNAPSHOT.json').read_bytes()), 'freeze_sha256': digest((AUDIT / 'publication/PREPUBLICATION_FREEZE.json').read_bytes()), 'integration_receipt_sha256': digest((AUDIT / 'MERGE_INTEGRATION_RECEIPT.json').read_bytes()), 'full_package_02_result_sha256': digest((AUDIT / 'reviews/full_package_02/REVIEW_RESULT.json').read_bytes()), 'git_mutations': False, 'candidate_mutations': False, 'third_party_raw_data_copied': False}
    (HERE / 'evidence').mkdir(exist_ok=True)
    (HERE / 'evidence/tree_and_frozen_checks.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'verdict': result['verdict'], 'packet_files': len(packet_checks), 'frozen_files': len(frozen_checks), 'changed_paths': len(changed), 'unrelated_main_leaf_entries_preserved': result['unrelated_main_leaf_entries_preserved'], 'nontarget_queue_bytes_preserved': len(main_others), 'source_identity_and_holds_unchanged': True}))


if __name__ == '__main__':
    main()

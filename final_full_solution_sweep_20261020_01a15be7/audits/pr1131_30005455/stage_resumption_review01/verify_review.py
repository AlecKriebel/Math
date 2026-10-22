"""Read-only verification of this review's pinned evidence, never lifecycle code."""
import argparse
import collections
import hashlib
import json
import pathlib
import stat

D = pathlib.Path(__file__).resolve().parent
WRAPPER = 'cc3b78b9728f4dbc9b5f3a899e7d5029c872387ab5af989ecddd1feb04d5bf6a'
OPS = 'eab69e53e9d32510bbf00d74c1b94b70542a8b29cf326c42f5d974e510f09d00'
PROPOSAL = 'a278e6ace55e2a1bcecc7d916ac01bb6ee0e0d2e35b0828cbffb5f9152388c5c'
CAP = 50 * 1024 * 1024

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            need(key not in result, 'duplicate JSON key')
            result[key] = value
        return result
    return json.loads(path.read_bytes(), object_pairs_hook=unique)

def safe_path(base, relative):
    relative = pathlib.PurePosixPath(relative)
    need(not relative.is_absolute() and '..' not in relative.parts, 'unsafe inventory path')
    return base.joinpath(*relative.parts)

def verify_results():
    action = read(D / 'ACTION_REVIEW.json')
    need(action['decision'] == 'HOLD' and action['production_execution_cleared'] is False, 'wrong decision')
    need(action['proposal_manifest_sha256'] == PROPOSAL and action['actual_wrapper_sha256'] == WRAPPER and action['operations_manifest_sha256'] == OPS, 'decision pin mismatch')
    need(action['real_service_mutations'] == 0 and action['copied_inputs_final_rehashed'] == 282, 'custody/mutation summary')
    need({item['id'] for item in action['findings']} == {'F1', 'F2', 'F3'}, 'missing finding')
    need(digest(D / 'private/resume_known_unattempted_stage.py') == WRAPPER, 'copied wrapper changed')
    mode_summaries = []
    for mode in ('normal', 'O', 'OO'):
        w = read(D / ('RESULTS_' + mode + '.json'))
        p = read(D / ('PR_REFERENCE_RESULTS_' + mode + '.json'))
        g = read(D / ('MAIN_GUARD_RESULTS_' + mode + '.json'))
        need(w['mode'] == p['mode'] == g['mode'] == mode, 'mode mismatch')
        need(w['source_sha256'] == g['actual_wrapper_sha256'] == WRAPPER, 'wrapper result source pin')
        need(w['operations_sha256'] == p['operations_manifest_sha256'] == OPS, 'operations result pin')
        need(p['fixture_driver_sha256'] == digest(D / 'actual_wrapper_controls.py'), 'fixture driver pin')
        need(w['actual_external_mutations'] == p['actual_service_mutations'] == g['service_mutations'] == 0, 'external mutation')
        need(w['real_escape_attempts'] == p['real_escape_attempts'] == g['real_escape_attempts'] == [], 'escape attempt')
        wc = {c['case']: c for c in w['cases']}
        pc = {c['case']: c for c in p['cases']}
        need(len(wc) == len(w['cases']) == w['case_count'] == 14, 'wrapper case closure')
        need(len(pc) == len(p['cases']) == p['case_count'] == 6, 'PR case closure')
        need(len(g['cases']) == 3 and all(c['rejected'] is True for c in g['cases']), 'CLI component controls')
        need({c['case'] for c in g['cases']} == {'no_execute_flag', 'wrong_wrapper_hash', 'wrong_bootstrap_hash'}, 'CLI control closure')
        valid = wc['valid_first_actual_stage']
        need(valid['create_POSTs'] == 1 and valid['upload_attempts'] == 2 and valid['update_attempts'] == 1 and valid['stage_verified'] is True and valid['exception'] is None, 'valid stage control')
        no_create = ['initial_adoption_known_attempt_not_false', 'initial_adoption_unresolved', 'initial_adoption_wrong_action', 'existing_saved_state', 'existing_resumption_intent', 'gate_fails_before_create', 'late_original_clearance_change', 'late_merge_head_change']
        for name in no_create:
            c = wc[name]
            need(c['create_POSTs'] == c['upload_attempts'] == c['update_attempts'] == 0 and c['stage_verified'] is False and c['exception'], 'pre-create refusal failed: ' + name)
        expected_ids = {'gate_fails_before_create': None, 'create_succeeds_response_lost': None, 'known_ID_native_policy_rejects': 777, 'upload_succeeds_response_lost': 777}
        for name, identifier in expected_ids.items():
            c = wc[name]
            need(c['resumption_intent'] is True and c['failure_receipt'] is True and c['stage_verified'] is False, 'failure custody: ' + name)
            need(c['reentry_error']['message'] == 'resumption already entered; GET-only reconcile', 'reentry was allowed: ' + name)
            need(c['failure_capture']['client_target_id'] == identifier and c['failure_capture']['no_mutation_retry_authorized'] is True and c['failure_capture']['unknown_outcome_requires_GET_only_reconciliation'] is True, 'unknown outcome promoted: ' + name)
        need(wc['create_succeeds_response_lost']['native_calls'] == ['create'], 'lost create response control')
        need(wc['known_ID_native_policy_rejects']['native_calls'] == ['create'], 'native rejection control')
        need(wc['upload_succeeds_response_lost']['create_POSTs'] == 1 and wc['upload_succeeds_response_lost']['upload_attempts'] == 1, 'lost upload response control')
        f1 = wc['late_resumption_adoption_revoked']
        f2 = wc['late_old_stage_intent_changed']
        for c in (f1, f2):
            need(c['counterexample'] is True and c['full_stage_gates'] == 4 and c['stage_verified'] is True and c['create_POSTs'] == 1 and c['upload_attempts'] == 2 and c['update_attempts'] == 1, 'wrapper counterexample lost')
            need(c['account_page_observations'] > 0 and c['dual_numeric_reads'] > 0, 'full stage gate absent')
        need(f1['exception'] is None and f1['result']['state'] == 'ready_to_publish' and f1['adoption_original_sha'] != f1['adoption_final_sha'] and f1['old_intent_original_sha'] == f1['old_intent_final_sha'], 'F1 evidence')
        need(f2['exception']['message'] == 'old stage intent altered' and f2['old_intent_original_sha'] != f2['old_intent_final_sha'] and f2['adoption_original_sha'] == f2['adoption_final_sha'], 'F2 evidence')
        need(w['counterexamples'] == ['late_resumption_adoption_revoked', 'late_old_stage_intent_changed'], 'wrapper findings closure')
        for name in ('known_compact_pull_request', 'known_spaced_pull_request', 'known_hash_pull_request'):
            c = pc[name]
            need(c['counterexample'] is True and c['full_actual_parsed_production_CLI'] is True and c['create_POSTs'] == 1 and len(c['native_calls']) == 4 and c['stage_verified'] is True and c['exception'] is None, 'F3 evidence: ' + name)
            need(c['account_page_observations'] > 0 and c['numeric_view_reads'] > 0, 'PR full gate absent')
            need(c['existing_row'][1:3] == ['', ''] and c['reference'] in c['existing_row'][3], 'PR row drift')
        for name in ('known_PR_hash_control', 'known_full_URL_control'):
            c = pc[name]
            need(c['create_POSTs'] == 0 and c['native_calls'] == [] and c['stage_verified'] is False and c['exception']['message'] == 'New/changed ledger lead requires root review', 'known PR positive control')
        nearby = pc['nearby_11310_control']
        need(nearby['counterexample'] is False and nearby['create_POSTs'] == 1 and nearby['stage_verified'] is True and nearby['exception'] is None, 'nearby PR boundary')
        need(all(c['actual_external_mutations'] == 0 for c in wc.values()) and all(c['real_service_mutations'] == 0 for c in pc.values()), 'case service mutation')
        creates = sum(c['create_POSTs'] for c in wc.values()) + sum(c['create_POSTs'] for c in pc.values())
        uploads = sum(c['upload_attempts'] for c in wc.values()) + sum(sum(v.startswith('upload:') for v in c['native_calls']) for c in pc.values())
        updates = sum(c['update_attempts'] for c in wc.values()) + sum(c['native_calls'].count('update') for c in pc.values())
        need((creates, uploads, updates) == (10, 15, 7), 'native call counters')
        summary = next(item for item in action['modes'] if item['mode'] == mode)
        need(summary['actual_wrapper_cases'] == 14 and summary['actual_parsed_production_stage_cases'] == 6 and summary['component_CLI_refusals'] == 3 and summary['fake_create_POSTs'] == creates and summary['fake_uploads'] == uploads and summary['fake_metadata_updates'] == updates, 'decision/counter disagreement')
        mode_summaries.append({'mode': mode, 'substantive_cases': 20, 'component_refusals': 3, 'counterexamples': 5})
    copy = read(D / 'private/exact_source/COPY_RECEIPT.json')
    need(len(copy['files']) == 282 and copy['no_credentials_copied'] is True and copy['all282original_and_copy_inodes_distinct'] is True, 'input copy custody')
    mirror = D / 'private/exact_source/Math'
    for name, pin in copy['files'].items():
        path = safe_path(mirror, name)
        need(path.stat().st_size == pin['bytes'] and digest(path) == pin['sha256'], 'copied input drift: ' + name)
    rev = read(D / 'PRODUCTION_REVOCATION_OBSERVATION.json')
    need(rev['original_path_absent'] is True and rev['reviewer_mutation'] is False and rev['sha256'] == '866ffab146f1e649cbbbb8ccc1a499813b7c8e887ffe6db844d04bea52859f8d', 'revocation observation')
    return mode_summaries

def verify_inventory(expected_sha):
    manifest_path = D / 'MANIFEST.json'
    need(digest(manifest_path) == expected_sha, 'external manifest pin mismatch')
    manifest = read(manifest_path)
    need(manifest['excluded_exact_paths'] == ['MANIFEST.json'], 'custody exclusion')
    files = {}
    directories = {}
    inode_counts = collections.Counter()
    inode_stats = {}
    directory_allocation = D.stat().st_blocks * 512
    for path in D.rglob('*'):
        st = path.lstat()
        name = path.relative_to(D).as_posix()
        need(not stat.S_ISLNK(st.st_mode), 'symlink in review')
        if stat.S_ISDIR(st.st_mode):
            directories[name] = {'mode': stat.S_IMODE(st.st_mode), 'mtime_ns': st.st_mtime_ns}
            directory_allocation += st.st_blocks * 512
        else:
            need(stat.S_ISREG(st.st_mode), 'special file in review')
            inode = (st.st_dev, st.st_ino)
            inode_counts[inode] += 1
            inode_stats[inode] = st
            if name != 'MANIFEST.json':
                files[name] = {'bytes': st.st_size, 'sha256': digest(path), 'mode': stat.S_IMODE(st.st_mode), 'mtime_ns': st.st_mtime_ns}
    need(files == manifest['files'], 'full recursive file closure or metadata mismatch')
    need(directories == manifest['directories'], 'directory closure or metadata mismatch')
    need(all(inode_counts[key] == value.st_nlink for key, value in inode_stats.items()), 'outside review hardlink')
    allocated = sum(st.st_blocks * 512 for st in inode_stats.values()) + directory_allocation
    need(allocated <= CAP, 'review allocation cap exceeded')
    public = read(D / 'PUBLIC_MANIFEST.json')
    for name, pin in public['files'].items():
        need('/' not in name and name not in ('PUBLIC_MANIFEST.json', 'MANIFEST.json'), 'public scope')
        path = safe_path(D, name)
        need(path.stat().st_size == pin['bytes'] and digest(path) == pin['sha256'], 'public pin mismatch')
    return {'sealed_files_excluding_exact_self': len(files), 'directories': len(directories), 'allocated_bytes_unique_inodes_and_directories_including_seal': allocated, 'outside_hardlinks': False}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seal-sha256')
    args = parser.parse_args()
    result = {'decision': 'HOLD', 'modes': verify_results(), 'substantive_cases': 60, 'component_refusals': 9, 'counterexamples': 15, 'real_service_mutations': 0}
    if args.seal_sha256:
        result['custody'] = verify_inventory(args.seal_sha256)
        result['seal_verified'] = True
    else:
        result['seal_verified'] = False
    print(json.dumps(result, sort_keys=True))

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Final own evidence/source recheck and typed verdict; no reviewed code execution."""
import datetime as dt
import hashlib
import json
import math
import os
from pathlib import Path
import stat

OWN = Path(__file__).resolve().parent
A = OWN.parent
R = A.parents[2]
P = A / 'acceptance_preparation_family'
EXPECTED = '6e8d07a73f68177ae3b7f446a1416ae39eabd560352fd7685464bcb129d0bcdc'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def parse(raw):
    def pairs(rows):
        out = {}
        for k, value in rows:
            if k in out:
                raise ValueError('Duplicate JSON key')
            out[k] = value
        return out
    def floating(v):
        value = float(v)
        if not math.isfinite(value):
            raise ValueError('Nonfinite JSON number')
        return value
    return json.loads(raw, object_pairs_hook=pairs, parse_float=floating,
                      parse_constant=lambda v: (_ for _ in ()).throw(ValueError(v)))


def demand(ok, reason):
    if not ok:
        raise ValueError(reason)


def pin(path):
    raw = path.read_bytes()
    return {'path': path.relative_to(R).as_posix(), 'bytes': len(raw), 'sha256': sha(raw)}


def put(name, obj):
    with (OWN / name).open('x') as stream:
        json.dump(obj, stream, indent=2)
        stream.write('\n')


def main():
    ledger = parse((OWN / 'READ_LEDGER.json').read_bytes())
    for z in ledger['files']:
        path = R / z['path']
        demand(path.is_file() and not path.is_symlink() and
               all(not q.is_symlink() for q in path.parents) and
               stat.S_ISREG(path.stat().st_mode), 'Unsafe external member')
        raw = path.read_bytes()
        demand(len(raw) == z['bytes'] and sha(raw) == z['sha256'] and
               path.stat().st_mode & 0o7777 == z['worktree_mode'], 'External source changed')
    raw_manifest = (P / 'PREPARATION_MANIFEST.json').read_bytes()
    demand(sha(raw_manifest) == EXPECTED, 'Source preparation changed')
    manifest = parse(raw_manifest)
    demand(len(manifest['files']) == 35, 'Source35 changed')
    expected_files = {x['path'] for x in manifest['files']} | {'PREPARATION_MANIFEST.json'}
    observed_files, observed_dirs = set(), set()
    for f in P.rglob('*'):
        demand(not f.is_symlink(), 'Source symlink')
        if f.is_dir():
            observed_dirs.add(f.relative_to(P).as_posix())
        else:
            demand(f.is_file() and stat.S_ISREG(f.stat().st_mode) and
                   f.stat().st_mode & 0o7777 == 0o444, 'Source exact0444')
            observed_files.add(f.relative_to(P).as_posix())
    expected_dirs = {q.as_posix() for n in expected_files for q in Path(n).parents
                     if q.as_posix() != '.'}
    demand(observed_files == expected_files and observed_dirs == expected_dirs,
           'Source exact topology changed')
    for name in ['input_inspection_actual_capture', 'finite_controls_actual_capture']:
        capture = OWN / name
        c = parse((capture / 'CAPTURE.json').read_bytes())
        demand(type(c['pid']) is int and c['pid'] > 0 and c['exit_code'] == 0 and
               c['actual_execution'] is True and c['completed'] is True and
               c['stdin_supplied'] is False, 'Own genuine capture')
        demand(dt.datetime.fromisoformat(c['started_utc']) <=
               dt.datetime.fromisoformat(c['finished_utc']), 'Own clock order')
        for z in [c['stdout'], c['stderr']]:
            b = (capture / z['path']).read_bytes()
            demand(len(b) == z['bytes'] and sha(b) == z['sha256'], 'Own complete channels')
        demand(sha((capture / 'prelaunch_source.py').read_bytes()) == c['source_sha256'],
               'Own prelaunch source changed')
    mirror = R / 'draft_pr_publication_program_20260930/infrastructure/accepted_state_sync/revision2/accepted_state_sync_v2.py'
    demand(sha(mirror.read_bytes()) ==
           'ca7576ece5bc37a6e569a62764541de773243d38bffa811f4d1174f25635667f',
           'Actually reviewed administrative mirror changed')
    source_pins = [pin(f) for f in sorted(P.rglob('*.py'))] + [pin(mirror)]
    put('SOURCE_PINS_AND_READ_COVERAGE.json', {
        'fully_read_unique_preparation_sources_and_historical_copies': source_pins,
        'sources_imported_compiled_or_executed': False,
        'source_review_scope': 'Administrative mechanisms/interfaces; no primary-proof recertification',
        'all_bound_inputs_byte_read_in': 'READ_LEDGER.json',
        'complete_typed_JSON_keysets_and_nodes_in': 'COMPLETE_TYPED_NODES.jsonl',
        'foreign_dependency_rows_in': 'FOREIGN_DEPENDENCIES.json',
        'foreign_bodies_copied_into_family': False})
    result = {
        'schema': 'pr41-independent-acceptance-source-adversary/v1',
        'verdict': 'MANDATORY_ADMINISTRATIVE_SOURCE_REPAIRS_BEFORE_EXECUTION',
        'review_completed': True, 'review_completion_estimate_percent': 100,
        'reported_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'actual_final_check_pid': os.getpid(), 'reviewed_preparation_manifest_sha256': EXPECTED,
        'original_packet_unchanged_after_audit': True,
        'source_preparation_members': 35, 'current_members': 547, 'dependency_members': 469,
        'whole_authored_members': 143, 'whole_foreign_members': 17,
        'whole_manifest_sha256': '233867cfb7e18b910f1ec17c9a57a386eadd1793ff3a44328260e204d8304130',
        'actual_root_whole_inspection_sha256': '28addc78a418ac5ad72a1e7f8cfacda16ec52ba5db52132b16c92602a3f4965e',
        'mandatory_repairs': [
            {'id': 'S1', 'priority': 2,
             'file': 'state_mirror_reconciliation.py', 'start': 25, 'end': 26,
             'claim': 'Complete derived typed inventory is not verified; actual program/workflow completion values and clocks can differ.'},
            {'id': 'S2', 'priority': 2,
             'file': 'pr41_guards.py', 'start': 371, 'end': 374,
             'claim': 'Accepted receipt and external ROOT schemas admit meaningful additional authority/scope fields.'},
            {'id': 'S3', 'priority': 2,
             'file': 'pr41_guards.py', 'start': 313, 'end': 315,
             'claim': 'Frozen0444 modes are missing or checked only with0777; permission-only changes are not rejected.'}],
        'mandatory_mathematical_repairs_found': [],
        'mathematical_scope_recertified': False,
        'literal_target_status': 'UNSOLVED', 'full_problem_solved': False,
        'novelty_claimed': False, 'human_peer_review_asserted': False,
        'strongest_preserved': 'Unconditional interior expectation law/full lower bound; full law only with additional t^4 P(D>t)->0.',
        'exact_remaining_gap': 'Expected exterior prescribed all-pair union length o(k) under ordinary SIRSN axioms, or admissible full-SIRSN counterexample.',
        'original_substantive_attempts': 2, 'turn_limit': 5,
        'new_substantive_attempts': 0, 'audit_turns': 0,
        'current_model': None, 'current_reasoning_effort': None, 'current_deadline_utc': None,
        'candidate_helpers_imported_compiled_or_executed': False,
        'scientific_helpers_reexecuted': False,
        'future_external_ROOT_bindings_plan_final_capture_status': 'UNKNOWN_NOT_CERTIFIED',
        'future_PR40_predecessor_mirror_post_status': 'UNKNOWN_NOT_CERTIFIED',
        'future_fresh13_native_runtime_status': 'UNKNOWN_NOT_CERTIFIED',
        'future_acceptance_execution_estimate_percent': 0,
        'unconditional_discovery_estimate_percent': 0,
        'shared_native_canonical_Git_index_remote_branch_writes': False,
        'external_human_contact': False, 'paper_or_new_DOI_or_tracker': False,
        'own_failed_captured_runs': [], 'own_finite_controls': 25,
        'own_input_inspection_capture': pin(OWN / 'input_inspection_actual_capture/CAPTURE.json'),
        'own_finite_controls_capture': pin(OWN / 'finite_controls_actual_capture/CAPTURE.json'),
        'report': pin(OWN / 'REPORT.md'),
        'next_required': 'NEW adjacent repaired source revision; NEW independent source review and actual ROOT full read; no edit to the closed original packet.'}
    put('RESULT.json', result)
    put('FINAL_CHECK_RESULT.json', {
        'status': 'PASS_OWN_FINAL_EVIDENCE_AND_ORIGINAL_PACKET_UNCHANGED_CHECK',
        'utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'actual_pid': os.getpid(),
        'external_full_files_rechecked': len(ledger['files']),
        'reviewed_preparation_manifest_sha256': EXPECTED,
        'candidate_runtime_verdict': result['verdict'],
        'candidate_helpers_imported_compiled_or_executed': False})
    print(json.dumps({'status': 'PASS_OWN_FINAL_EVIDENCE_AND_ORIGINAL_PACKET_UNCHANGED_CHECK',
                      'actual_pid': os.getpid(), 'candidate_runtime_verdict': result['verdict'],
                      'mandatory_administrative_repairs': 3,
                      'review_completion_estimate_percent': 100,
                      'unconditional_discovery_estimate_percent': 0}, indent=2))


if __name__ == '__main__':
    main()

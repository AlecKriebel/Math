#!/usr/bin/env python3
"""Private independent predicate/publication controls; no reviewed source loaded."""
import copy
import datetime as dt
import hashlib
import json
import os
from pathlib import Path

OWN = Path(__file__).resolve().parent
A = OWN.parent
P = A / 'acceptance_preparation_family'
RESULTS = []


def same(a, b):
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return set(a) == set(b) and all(same(a[k], b[k]) for k in a)
    if type(a) is list:
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b


def subset(obj, expected):
    return type(obj) is dict and all(k in obj and same(obj[k], value)
                                   for k, value in expected.items())


def record(name, observed, expected, kind, detail):
    if observed != expected:
        raise ValueError('Own control failed: ' + name)
    RESULTS.append({'name': name, 'status': 'PASS_OWN_AUDIT_CONTROL',
                    'observed': observed, 'expected': expected,
                    'kind': kind, 'detail': detail})


def inventory_model(old, new):
    # Independent transcription of the documented allowed projections and
    # local accepted() checks, isolated from all unavailable future gates.
    selected_allowed = {'stage', 'outcome', 'queue_status', 'audited_head', 'merge_commit',
        'merged_at', 'workflow_completion_estimate_percent', 'original_attempts',
        'new_substantive_attempts', 'cumulative_attempts', 'paper_or_new_doi_or_tracker'}
    root_allowed = {'items', 'updated_at_utc', 'last_checkpoint_utc', 'completed_count',
        'program_completion_estimate_percent', 'completion_estimate_percent', 'current_pr'}
    if not same({k: v for k, v in old.items() if k not in root_allowed},
                {k: v for k, v in new.items() if k not in root_allowed}):
        return False
    if [x['number'] for x in old['items']] != [x['number'] for x in new['items']]:
        return False
    for before, after in zip(old['items'], new['items']):
        if before['number'] != 41 and not same(before, after):
            return False
        if before['number'] == 41 and not same(
                {k: v for k, v in before.items() if k not in selected_allowed},
                {k: v for k, v in after.items() if k not in selected_allowed}):
            return False
    return subset(new, {'current_pr': 42, 'completed_count': 31}) and \
        sum(x.get('stage') == 'complete' for x in new['items']) == 31 and subset(
            next(x for x in new['items'] if x['number'] == 41),
            {'stage': 'complete', 'outcome': 'unsolved_accepted_partial',
             'queue_status': 'unsolved', 'audited_head': '292b95ca601f166e6d246e609cf7ed5ca5653e25',
             'merge_commit': '1' * 40, 'merged_at': '2026-10-02T22:00:00+00:00',
             'original_attempts': '2/5', 'cumulative_attempts': '2/5',
             'new_substantive_attempts': 0, 'paper_or_new_doi_or_tracker': False})


def main():
    baseline = {'items': [{'number': i, 'stage': 'complete'} for i in range(1, 31)] +
                [{'number': 41, 'stage': 'pending', 'headRefName': 'dot/math-9700035'}],
                'completed_count': 30, 'current_pr': 41, 'total': 180,
                'program_completion_estimate_percent': 30 / 180 * 100,
                'completion_estimate_percent': 30 / 180 * 100,
                'updated_at_utc': '2026-10-02T21:00:00+00:00',
                'last_checkpoint_utc': '2026-10-02T21:00:00+00:00'}
    good = copy.deepcopy(baseline)
    good.update(completed_count=31, current_pr=42,
        program_completion_estimate_percent=31 / 180 * 100,
        completion_estimate_percent=31 / 180 * 100,
        updated_at_utc='2026-10-02T22:00:00+00:00',
        last_checkpoint_utc='2026-10-02T22:00:00+00:00')
    good['items'][-1].update(stage='complete', outcome='unsolved_accepted_partial',
        queue_status='unsolved', audited_head='292b95ca601f166e6d246e609cf7ed5ca5653e25',
        merge_commit='1' * 40, merged_at='2026-10-02T22:00:00+00:00',
        workflow_completion_estimate_percent=100, original_attempts='2/5',
        cumulative_attempts='2/5', new_substantive_attempts=0,
        paper_or_new_doi_or_tracker=False)
    record('inventory_baseline', inventory_model(baseline, good), True, 'positive',
           'Artificial source-predicate fixture; no real future inventory certified.')
    mutants = []
    for field, value in [('program_completion_estimate_percent', 100),
                         ('completion_estimate_percent', 100),
                         ('program_completion_estimate_percent', False),
                         ('completion_estimate_percent', None),
                         ('updated_at_utc', None), ('last_checkpoint_utc', False)]:
        obj = copy.deepcopy(good)
        obj[field] = value
        name = 'inventory_' + field + '_' + type(value).__name__
        record(name, inventory_model(baseline, obj), True, 'countercontrol',
               'Source local gate accepts incompatible allowed field; complete derived equality rejects.')
        mutants.append({'name': name, 'field': field, 'value': value, 'source_local_gate_accepts': True})
    obj = copy.deepcopy(good)
    obj['items'][-1]['workflow_completion_estimate_percent'] = False
    record('inventory_workflow_false', inventory_model(baseline, obj), True, 'countercontrol',
           'Selected workflow100 is omitted from accepted inventory verification.')
    mutants.append({'name': 'inventory_workflow_false', 'field': 'items/41/workflow_completion_estimate_percent',
                    'value': False, 'source_local_gate_accepts': True})
    for name, mutate in [('identity', lambda x: x['items'][-1].update(number=42)),
                         ('unselected', lambda x: x['items'][0].update(stage='pending')),
                         ('budget_bool', lambda x: x['items'][-1].update(new_substantive_attempts=False))]:
        obj = copy.deepcopy(good)
        mutate(obj)
        record('inventory_reject_' + name, inventory_model(baseline, obj), False, 'negative',
               'A nearby enforced invariant rejects; false is distinct from numeric zero.')
    expected_receipt = {'schema': 'pr41-accepted-qualified-conditional-partial/v1',
                        'full_problem_solved': False, 'novelty_claimed': False,
                        'current_model': None, 'scientific_scope': json.loads((P / 'SCIENTIFIC_SCOPE.json').read_bytes())}
    extra = {**expected_receipt, 'human_peer_review_asserted': True}
    record('accepted_receipt_meaningful_extra', subset(extra, expected_receipt), True, 'countercontrol',
           'Required subset accepts top-level peer-review true while exact nested scientific scope says false.')
    record('accepted_receipt_exact_schema_rejects_extra', same(extra, expected_receipt), False, 'negative',
           'Complete key/type equality rejects the conflicting additional authority field.')
    missing = {k: v for k, v in expected_receipt.items() if k != 'current_model'}
    record('present_null_is_required', subset(missing, expected_receipt), False, 'negative',
           'Absent current_model does not satisfy present null.')
    bool_number = {**expected_receipt, 'full_problem_solved': 0}
    record('false_not_numeric_zero', subset(bool_number, expected_receipt), False, 'negative',
           'Existing typed subset comparison correctly rejects numeric0 replacing false.')
    modes = []
    for mode in [0o444, 0o2444, 0o4444, 0o644]:
        actual = (mode & 0o777) == 0o444
        strict = (mode & 0o7777) == 0o444
        modes.append({'mode_octal': oct(mode), 'source_mask_accepts': actual,
                      'strict_0444_accepts': strict})
        record('mode_' + oct(mode), actual, mode != 0o644, 'mode_predicate',
               'Permission predicate only; no reviewed file chmod.')
    scratch = OWN / 'publication_controls'
    scratch.mkdir()
    for name, preexisting in [('new_target', False), ('existing_target', True), ('symlink_target', True)]:
        d = scratch / name
        d.mkdir()
        target, temporary = d / 'target.bin', d / 'target.bin.audit-tmp'
        old = b'OLD TARGET BYTES\n'
        if name == 'existing_target':
            target.write_bytes(old)
        if name == 'symlink_target':
            (d / 'referent.bin').write_bytes(old)
            target.symlink_to('referent.bin')
        temporary.write_bytes(b'COMPLETE NEW BYTES\n')
        rejected = False
        try:
            os.link(temporary, target, follow_symlinks=False)
        except FileExistsError:
            rejected = True
        record('publication_' + name, rejected, preexisting, 'private_publication',
               'Independent hard-link absence mechanism; completed temporary and existing target retained.')
        if preexisting:
            record('publication_preservation_' + name,
                   temporary.read_bytes() == b'COMPLETE NEW BYTES\n' and target.read_bytes() == old,
                   True, 'private_publication', 'Failure preserves both full bodies.')
        else:
            record('publication_new_complete', target.read_bytes() == b'COMPLETE NEW BYTES\n',
                   True, 'private_publication', 'New target exposes complete bytes.')
        if target.is_symlink():
            # Convert only own fixture into a regular record before sealing.
            target.unlink()
            target.write_bytes(b'EXPLICIT POST-CONTROL FIXTURE REPLACEMENT\n')
    obj = {'status': 'PASS_OWN_FINITE_SOURCE_PREDICATE_AND_PUBLICATION_CONTROLS',
           'utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'actual_pid': os.getpid(),
           'checks': RESULTS, 'checks_count': len(RESULTS),
           'inventory_baseline': baseline, 'authorized_after_fixture': good,
           'inventory_mutants': mutants, 'receipt_extra_fixture': extra,
           'mode_controls': modes, 'candidate_helpers_imported_compiled_or_executed': False,
           'future_runtime_inputs_are_artificial_fixtures': True,
           'future_runtime_PASS_claimed': False, 'scientific_reexecution_claimed': False,
           'writes_outside_own_family': False}
    with (OWN / 'FINITE_CONTROLS_RESULT.json').open('x') as out:
        json.dump(obj, out, indent=2)
        out.write('\n')
    print(json.dumps(obj, indent=2))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Own finite contract predicates and private publication controls, not candidate execution."""
import ast
import copy
import datetime as dt
import errno
import hashlib
import json
import os
import re
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
A = HERE.parent
S = A / 'acceptance_execution_preparation_family/integration_source_revision'
CONTROLS = []


def insist(ok, why):
    if not ok:
        raise ValueError(why)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def record(label, observed, expected, inputs):
    insist(observed is expected, 'Unexpected own control ' + label)
    CONTROLS.append({'label': label, 'observed_acceptance': observed, 'expected_acceptance': expected,
                     'inputs': inputs, 'status': 'PASS'})


def accepts(function, *args):
    try:
        function(*args)
    except (ValueError, TypeError, KeyError, OSError):
        return False
    return True


def clock(value):
    insist(type(value) is str and value and value == value.strip(), 'String clock')
    result = dt.datetime.fromisoformat(value[:-1] + '+00:00' if value.endswith('Z') else value)
    insist(result.tzinfo is not None and result.utcoffset() == dt.timedelta(0), 'Aware UTC')
    return result


def interval(start, end, receipt):
    s, e, r = clock(start), clock(end), clock(receipt)
    insist(s <= e and s <= r <= e, 'Ordered contained UTC interval')


def canonical_name(n):
    insist(type(n) is str and n and '\\' not in n and '\0' not in n, 'Relative string')
    p = PurePosixPath(n)
    insist(not p.is_absolute() and '..' not in p.parts and p.as_posix() == n, 'Canonical relative path')
    return p


def four_names(capture, parent_direct, stdout, stderr):
    insist(capture == 'CAPTURE.json' and parent_direct is True, 'Literal adjacent capture')
    for n in (stdout, stderr):
        insist(len(canonical_name(n).parts) == 1 and n not in {'CAPTURE.json', 'prelaunch_source.py'}, 'Distinct root stream')
    insist(len({capture, 'prelaunch_source.py', stdout, stderr}) == 4, 'Four distinct files')


def fresh_record(value, now):
    created = clock(value['created_utc'])
    insist(created <= now, 'Creation not future')
    insist(type(value['reason_date_utc']) is str and value['reason_date_utc'] == created.date().isoformat(), 'Reason date matches UTC')
    reason = value['reason']
    insist(type(reason) is str and reason == reason.strip() and len(reason) >= 40 and len(reason.split()) >= 6, 'Reviewed substantive lexical reason')
    insist(type(value['current_head']) is str and re.fullmatch('[0-9a-f]{40}', value['current_head']), 'Separate fresh HEAD')


def exact_equal(a, b):
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return a.keys() == b.keys() and all(exact_equal(a[k], b[k]) for k in a)
    if type(a) is list:
        return len(a) == len(b) and all(exact_equal(x, y) for x, y in zip(a, b))
    return a == b


def actual_link_control(name, collide):
    root = HERE / 'private_publication_fixtures' / name
    root.mkdir(parents=True)
    target, temporary = root / 'target.bin', root / 'target.bin.pr40-tmp'
    new = b'Complete fsynced new receipt bytes\x00\xff\n'
    old = b'Intervening complete preimage receipt\x00\xfe\n'
    insist(not target.exists(), 'Initially absent target')
    with temporary.open('xb') as stream:
        stream.write(new)
        stream.flush()
        os.fsync(stream.fileno())
    if collide:
        with target.open('xb') as stream:
            stream.write(old)
            stream.flush()
            os.fsync(stream.fileno())
        (root / 'complete_target_preimage.bin').write_bytes(old)
    try:
        os.link(temporary, target, follow_symlinks=False)
    except FileExistsError as e:
        insist(collide and e.errno == errno.EEXIST, 'Expected exclusive-link collision')
        insist(target.read_bytes() == old and temporary.read_bytes() == new, 'Collision preserves both complete versions')
        outcome = 'ATOMIC_COLLISION_REJECTED_BOTH_COMPLETE_VERSIONS_RETAINED'
        error = {'exception': type(e).__name__, 'errno': e.errno, 'message': str(e)}
    else:
        insist(not collide and target.read_bytes() == new, 'Absent target published complete')
        temporary.unlink()
        insist(not temporary.exists(), 'Temp unlinked only after successful publication')
        outcome = 'ABSENT_TARGET_COMPLETE_BYTES_PUBLISHED_TEMP_UNLINKED'
        error = None
    fd = os.open(root, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
    return {'name': name, 'outcome': outcome, 'retained_error': error,
            'all_regular_retained_members': [{'path': p.relative_to(HERE).as_posix(), 'bytes': len(p.read_bytes()),
                                              'sha256': sha(p.read_bytes())} for p in sorted(root.iterdir())]}


def main():
    guard = (S / 'pr40_guards.py').read_text()
    tree = ast.parse(guard)
    functions = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    excerpts = {n: ast.get_source_segment(guard, functions[n]) for n in ['write', 'utc_clock', 'gates', 'plan_scope', 'revision_basis']}
    # AST/source comparisons bind own local contract controls to the actual source
    # predicates. No AST node is compiled or evaluated as executable code.
    for text in ["started<=finished", "started<=utc_clock(receipt['utc']", "ps['reconciliation_capture'].name=='CAPTURE.json' and cb.parent==A",
                 "len(relative(n).parts)==1", "n not in {'CAPTURE.json','prelaunch_source.py'}", "created<=dt.datetime.now(dt.timezone.utc)",
                 "fresh['reason_date_utc']==created.date().isoformat()", "len(fresh['reason'])>=40", "len(fresh['reason'].split())>=6"]:
        insist(text in excerpts['gates'], 'Required bound guard missing ' + text)
    write_source = excerpts['write']
    insist('os.link(tmp,p,follow_symlinks=False)' in write_source and write_source.index('os.fsync(s.fileno())') < write_source.index('os.link(tmp,p,follow_symlinks=False)') < write_source.index('tmp.unlink()'), 'Complete temp/link/success unlink order')
    insist('else:\n        os.replace(tmp,p)' in write_source, 'Intentional replacement remains nonexclusive branch')
    start, end = '2026-10-02T20:00:00+00:00', '2026-10-02T20:00:02Z'
    for label, s, e, receipt, expected in [
        ('valid_interior', start, end, '2026-10-02T20:00:01+00:00', True),
        ('valid_left_boundary', start, end, start, True),
        ('valid_right_boundary', start, end, end, True),
        ('valid_zero_interval', start, start, start, True),
        ('invalid_arbitrary_text', 'banana', 'orange', 'fruit', False),
        ('invalid_naive', '2026-10-02T20:00:00', end, start, False),
        ('invalid_nonUTC', '2026-10-02T20:00:00+01:00', end, start, False),
        ('invalid_reversed', end, start, start, False),
        ('invalid_receipt_before', start, end, '2026-10-02T19:59:59Z', False),
        ('invalid_receipt_after', start, end, '2026-10-02T20:00:03Z', False),
        ('invalid_receipt_naive', start, end, '2026-10-02T20:00:01', False),
        ('invalid_bool_clock', True, end, start, False),
        ('invalid_null_clock', None, end, start, False),
        ('invalid_whitespace', ' ' + start, end, start, False),
        ('invalid_date_only', '2026-10-02', end, start, False),
    ]:
        record('S2_' + label, accepts(interval, s, e, receipt), expected, {'start': s, 'end': e, 'receipt': receipt})
    for label, cap, direct, out, err, expected in [
        ('valid_literal', 'CAPTURE.json', True, 'stdout.bin', 'stderr.bin', True),
        ('valid_alternative_declared_streams', 'CAPTURE.json', True, 'all-out', 'all-err', True),
        ('invalid_stream_alias', 'CAPTURE.json', True, 'stdout.bin', 'stdout.bin', False),
        ('invalid_source_alias', 'CAPTURE.json', True, 'stdout.bin', 'prelaunch_source.py', False),
        ('invalid_capture_alias', 'CAPTURE.json', True, 'CAPTURE.json', 'stderr.bin', False),
        ('invalid_nested_stream', 'CAPTURE.json', True, 'nested/stdout.bin', 'stderr.bin', False),
        ('invalid_capture_name', 'OTHER.json', True, 'stdout.bin', 'stderr.bin', False),
        ('invalid_nested_capture', 'CAPTURE.json', False, 'stdout.bin', 'stderr.bin', False),
        ('invalid_parent_traversal', 'CAPTURE.json', True, '../stdout.bin', 'stderr.bin', False),
        ('invalid_noncanonical_dot', 'CAPTURE.json', True, './stdout.bin', 'stderr.bin', False),
        ('invalid_absolute', 'CAPTURE.json', True, '/stdout.bin', 'stderr.bin', False),
        ('invalid_empty', 'CAPTURE.json', True, '', 'stderr.bin', False),
        ('invalid_backslash', 'CAPTURE.json', True, 'nested\\stdout.bin', 'stderr.bin', False),
        ('invalid_null_name', 'CAPTURE.json', True, None, 'stderr.bin', False),
    ]:
        record('S3_' + label, accepts(four_names, cap, direct, out, err), expected,
               {'capture': cap, 'direct_audit_child': direct, 'stdout': out, 'stderr': err})
    # The previous exact local set predicate accepted the source-alias vector;
    # this does not assert a complete forged old or revised gate was executed.
    old_names = {'CAPTURE.json', 'prelaunch_source.py', 'stdout.bin', 'prelaunch_source.py'}
    insist(len(old_names) == 3, 'Old alias witness must collapse to three files')
    now = dt.datetime.now(dt.timezone.utc)
    good = {'created_utc': now.isoformat(), 'reason_date_utc': now.date().isoformat(),
            'reason': 'Root checked the completed PR39 native mirror and fresh published main evidence.',
            'current_head': 'a' * 40}
    record('S5_valid_fresh_record', accepts(fresh_record, good, now), True, good)
    for label, key, value in [('token_reason', 'reason', 'yes'), ('six_short_words', 'reason', 'a b c d e f'),
                              ('wrong_reason_date', 'reason_date_utc', '1999-01-01'), ('naive_creation', 'created_utc', '2026-10-02T20:00:00'),
                              ('future_creation', 'created_utc', (now + dt.timedelta(days=1)).isoformat()),
                              ('missing_clock', 'created_utc', None), ('padded_reason', 'reason', ' ' + good['reason']),
                              ('wrong_HEAD_length', 'current_head', 'a' * 39), ('bool_HEAD', 'current_head', False)]:
        bad = {**good, key: value}
        record('S5_invalid_' + label, accepts(fresh_record, bad, now), False, bad)
    for label, a, b, expected in [('int_vs_bool', 0, False, False), ('int_vs_float', 0, 0.0, False),
                                 ('present_null_vs_missing', {'runtime': None}, {}, False),
                                 ('nested_bool_zero', {'turns': [0]}, {'turns': [False]}, False),
                                 ('nested_good', {'runtime': None, 'turns': [0]}, {'runtime': None, 'turns': [0]}, True)]:
        record('typed_' + label, exact_equal(a, b), expected, {'left': a, 'right': b})
    scope = json.loads((S / 'SCIENTIFIC_SCOPE.json').read_text())
    draft = json.loads((S / 'DRAFT_FINAL_PLAN.json').read_text())
    insist(exact_equal(scope, draft['scientific_scope']), 'Both entire scope copies equal')
    coverage = scope['credited_existing_coverage']
    insist(len(coverage) == 4 and coverage[2].startswith('cusped orientable: published Kuhlmann2006 Theorem1.1')
           and coverage[3].startswith('cusped nonorientable: Xia2110.14376v1 Theorems1.2/4.1')
           and 'credited preprint' in coverage[3], 'S1 all cusp credit distinctions')
    integrate = (S / 'integrate_reviewed_partial.py').read_text()
    mirror = (S / 'state_mirror_reconciliation.py').read_text()
    insist('current_pr=41' in integrate and "{'current_pr':41,'completed_count':30}" in mirror, 'S6 final and later typed next-target guards')
    publication = [actual_link_control('intervening_target', True), actual_link_control('initially_absent_target', False)]
    output = {'schema': 'pr40-fresh-revised-static-finite-controls/v1', 'utc': dt.datetime.now(dt.timezone.utc).isoformat(),
              'status': 'PASS_STATIC_CONTRACT_CONTROLS_ONLY', 'predicate_control_count': len(CONTROLS),
              'predicate_controls': CONTROLS, 'real_private_publication_controls': publication,
              'source_guard_excerpts': excerpts, 'source_sha256': sha(guard.encode()),
              'S1_complete_scope_and_draft_credit_checked': True, 'S6_next_target_write_and_later_guard_checked': True,
              'previous_alias_vector_collapsed_to_three': True, 'reviewed_helper_import_compile_execution': False,
              'entire_candidate_gate_executed_or_forged_PASS_claimed': False, 'future_final_acceptance_claimed': False,
              'Git_SQL_native_canonical_shared_remote_writes': False, 'original_substantive_attempts': 0,
              'turn_limit': 5, 'new_substantive_attempts': 0, 'audit_turns': 0, 'full_problem_solved': False,
              'novelty_claimed': False, 'paper_or_new_DOI_or_tracker': False}
    print(json.dumps(output, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()

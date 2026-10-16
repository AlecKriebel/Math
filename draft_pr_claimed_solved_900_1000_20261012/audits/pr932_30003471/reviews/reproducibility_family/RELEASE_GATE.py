#!/usr/bin/env python3
"""Separately scoped current replay gate; preserves and reports one numeric receipt drift.

External bootstrap: authenticate this gate, PACKET_GUARD.py, and PINNED_SNAPSHOT.json
through the curated public map before execution. No frozen packet bytes are edited.
The only nonexact receipt value allowed is numeric_max_jacobi_error, with the exact
float type and the original finite, nonnegative, strict 3e-7 check bound on BOTH
historical and current values. Every other key, type and value must match exactly.
"""
import argparse
import importlib.util
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).absolute().parent
SNAPSHOT_PIN = 'f05112fa43eb99a0c9cd4687b14beeef5eb4d190dcebae9b15c1d84c9acc656f'
DIAGNOSTIC = 'numeric_max_jacobi_error'
LIMIT = 3e-7
spec = importlib.util.spec_from_file_location('release_packet_guard', HERE/'PACKET_GUARD.py')
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)


def compare_independent(actual, historical):
    g.need(type(actual) is dict and type(historical) is dict and actual.keys() == historical.keys(), 'independent receipt schema')
    for result in (actual, historical):
        value = result.get(DIAGNOSTIC)
        g.need(type(value) is float and math.isfinite(value) and 0 <= value < LIMIT,
               'Jacobi diagnostic must be a finite nonnegative float strictly below original 3e-7 bound')
    g.need(all(g.typed_equal(actual[key], historical[key]) for key in historical if key != DIAGNOSTIC),
           'independent receipt differs outside the one bounded nonproof diagnostic')
    return {'all_other_keys_types_values_exact': True, 'field': DIAGNOSTIC,
            'historical_value': historical[DIAGNOSTIC], 'current_value': actual[DIAGNOSTIC],
            'bound_exclusive': LIMIT, 'type': 'float', 'exact_value_equal': actual[DIAGNOSTIC] == historical[DIAGNOSTIC],
            'analytic_theorem_verified': False}


def run(packet, snapshot, scratch, python):
    start = g.authenticate(str(packet), snapshot)
    expected_author = g.strict_json(g.regular(packet/'audit_a/CONTROL_REPLAY.json'))['runs'][0]['result']
    historical = g.strict_json(g.regular(packet/'audit_b/INDEPENDENT_CONTROL_RESULTS.json'))
    g.need(historical['counts'].pop('source_pin') == 9 and historical['total_checks'] == 4146, 'historical source-selection accounting')
    historical['total_checks'] -= 9
    historical['source_verification'] = 'NOT_RUN_NO_SEPARATELY_SUPPLIED_SOURCES'
    rows = []
    environment = {k:v for k,v in os.environ.items() if not k.startswith('PYTHON')}
    environment['PYTHONDONTWRITEBYTECODE'] = '1'
    environment['OPENBLAS_NUM_THREADS'] = '1'
    environment['OMP_NUM_THREADS'] = '1'
    for label, flags in [('normal', []), ('-O', ['-O']), ('-OO', ['-OO'])]:
        with tempfile.TemporaryDirectory(prefix='current-gate-', dir=scratch) as temporary:
            work = Path(temporary); copied = work/'packet'; shutil.copytree(packet, copied)
            # Recheck the complete copied inventory before EVERY executable entry point.
            def invoke(entrypoint, arguments):
                before = g.authenticate(str(copied), snapshot)
                cp = subprocess.run([python, '-I', '-B', *flags, str(copied/entrypoint), *arguments],
                                    cwd=work, env=environment, capture_output=True, timeout=120)
                g.need(g.typed_equal(before, g.authenticate(str(copied), snapshot)), 'copied input changed')
                g.need(cp.returncode == 0 and cp.stderr == b'', entrypoint+' execution failed')
                return g.strict_json(cp.stdout), cp.stdout
            packaging, _ = invoke('VERIFY_PUBLICATION.py', ['--packet', str(copied), '--expected-manifest', g.OUTER_PIN, '--check-only'])
            g.need(packaging['status'] == 'PASS' and packaging['bound_files'] == 28 and packaging['check_only'] is True,
                   'legacy identity-only gate result')
            author, author_stdout = invoke('public/verify_packet.py', ['--manifest-sha256', '1cd8291f2025524b351c5cc3cb5780b35ba5fa4c4afde78c6e288daddd350e9f', '--self-test'])
            g.need(g.typed_equal(author, expected_author), 'author receipt must remain recursively exact')
            g.need(author_stdout == (json.dumps(expected_author,sort_keys=True)+'\n').encode(), 'author canonical stdout differs')
            controls, controls_stdout = invoke('public/controls.py', [])
            g.need(controls_stdout == g.regular(copied/'public/CONTROL_RESULTS.json') and
                   g.typed_equal(controls,g.strict_json(g.regular(copied/'public/CONTROL_RESULTS.json'))), 'author raw stdout differs')
            independent, independent_stdout = invoke('PORTABLE_INDEPENDENT.py', ['--packet-root', str(copied)])
            comparison = compare_independent(independent, historical)
            rows.append({'mode':label, 'all_29_auth_before_each_execution':True, 'unchanged_after_each_execution':True,
                         'author_finite_checks':5066, 'author_negative_controls':19,
                         'author_raw_control_stdout_exact':True, 'author_receipt_types_values_exact':True,
                         'independent_checks':4137, 'external_source_checks_not_run':9,
                         'independent_stdout_sha256':g.sha(independent_stdout), 'comparison':comparison})
    g.need(g.typed_equal(start,g.authenticate(str(packet),snapshot)), 'source packet changed')
    return {'schema':'pr932-current-replay-gate-v1', 'current_gate':'PASS_WITH_DISCLOSED_BOUNDED_NONPROOF_DIAGNOSTIC',
            'legacy_exact_receipt_gate_superseded':False, 'legacy_exact_receipt_equality':all(row['comparison']['exact_value_equal'] for row in rows),
            'snapshot_sha256':SNAPSHOT_PIN, 'replays':rows, 'mathematical_acceptance':False,
            'external_sources_verified':False, 'concurrent_attacker_or_OS_sandbox_protection':False,
            'scope':'Fixed all-29 byte identity plus exact finite receipts except the one observed bounded Jacobi diagnostic; no analytic theorem certification.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--packet',required=True)
    p.add_argument('--scratch',required=True,type=Path)
    p.add_argument('--python',default=sys.executable)
    args=p.parse_args()
    try:
        snapshot=g.load_snapshot(HERE/'PINNED_SNAPSHOT.json',SNAPSHOT_PIN)
        packet=g.canonical_root(args.packet)
        args.scratch.mkdir(parents=True,exist_ok=True)
        print(json.dumps(run(packet,snapshot,args.scratch,args.python),indent=2,sort_keys=True))
    except (g.Rejected,OSError,ValueError,subprocess.SubprocessError) as error:
        print('CURRENT_GATE_REJECT: '+str(error),file=sys.stderr)
        return 1
    return 0


if __name__=='__main__':
    raise SystemExit(main())

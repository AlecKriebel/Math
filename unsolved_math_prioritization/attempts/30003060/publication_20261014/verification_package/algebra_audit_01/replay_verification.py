#!/usr/bin/env python3
"""Replay the exact checker in both modes and reject a corrupted expectation."""
import ast
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    here = Path(__file__).resolve().parent
    checker = here / 'exact_chain_check.py'
    tree = ast.parse(checker.read_text())
    need(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)),
         'Current checker still contains removable assertion statements')
    original_manifest = json.loads((here / 'historical_v1/PRESERVED_MANIFEST.json').read_text())
    for name, details in original_manifest.items():
        historical = here / 'historical_v1' / name
        need(digest(historical) == details['sha256']
             and historical.stat().st_size == details['bytes'],
             f'Historical artifact changed: {name}')
    runs = []
    outputs = {}
    for mode, flags in [('normal', []), ('optimized', ['-O'])]:
        path = here / f'RESULTS_{mode.upper()}.json'
        completed = subprocess.run([sys.executable, *flags, str(checker),
                                    '--output', str(path)], capture_output=True,
                                   text=True, timeout=60, cwd=here)
        need(completed.returncode == 0,
             f'{mode} positive replay failed: {completed.stderr}')
        result = json.loads(path.read_text())
        need(result['checker_sha256'] == digest(checker),
             f'{mode} replay has wrong checker digest')
        need(result['all_passed'] and result['matrix_period_comparisons'] == 234
             and result['witness_primes'] == 14 and result['negative_controls'] == 10,
             f'{mode} replay has incomplete or failing mathematical coverage')
        need(result['verification_checks_performed'] > 0,
             f'{mode} replay recorded no executed acceptance checks')
        outputs[mode] = result
        runs.append({'mode': mode, 'python_flags': flags, 'returncode': completed.returncode,
                     'output': path.name, 'output_sha256': digest(path),
                     'verification_checks_performed': result['verification_checks_performed'],
                     'stdout': completed.stdout, 'stderr': completed.stderr})
    ignored = ['timestamp_utc', 'checker_sha256']
    semantic = lambda result: {k: v for k, v in result.items() if k not in ignored}
    need(semantic(outputs['normal']) == semantic(outputs['optimized']),
         'Normal and optimized modes disagree after ignoring timestamp/checker SHA')
    old = json.loads((here / 'historical_v1/RESULTS.json').read_text())
    unchanged_keys = ['frozen_head', 'independence', 'arithmetic', 'matrix_period_comparisons',
                      'witness_primes', 'negative_controls', 'all_passed', 'cases',
                      'witnesses', 'mutation_controls']
    for key in unchanged_keys:
        need(outputs['normal'][key] == old[key],
             f'Hardening changed a historical mathematical result: {key}')
    negative = []
    expected_error = ('Matrix/necklace mismatch: r=2, n=2, characteristic=2, '
                      'quantity=higher_h1, matrix=1, expected=2')
    with tempfile.TemporaryDirectory(prefix='hardening_reject_', dir=here) as temporary:
        for mode, flags in [('normal', []), ('optimized', ['-O'])]:
            path = Path(temporary) / f'REJECTED_{mode.upper()}.json'
            completed = subprocess.run([sys.executable, *flags, str(checker),
                                        '--inject-wrong-expectation', '--output', str(path)],
                                       capture_output=True, text=True, timeout=60, cwd=here)
            need(completed.returncode != 0,
                 f'{mode} mode accepted the deliberately corrupted expectation')
            need(expected_error in completed.stderr,
                 f'{mode} mode did not reject for the intended mismatch: {completed.stderr}')
            need(not path.exists(),
                 f'{mode} mode wrote an acceptance artifact after the forced failure')
            negative.append({'mode': mode, 'python_flags': flags,
                             'returncode': completed.returncode,
                             'corruption': 'r=2,n=2,char=2 higher_h1 expected 1 changed to 2',
                             'expected_error': expected_error,
                             'rejected_for_expected_reason': True,
                             'acceptance_artifact_written': path.exists(),
                             'stdout': completed.stdout, 'stderr': completed.stderr})
    # Keep the conventional current filename equal to the verified normal output.
    (here / 'RESULTS.json').write_bytes((here / 'RESULTS_NORMAL.json').read_bytes())
    receipt = {'timestamp_utc': datetime.now(timezone.utc).isoformat(),
               'checker_sha256': digest(checker), 'replay_script_sha256': digest(Path(__file__)),
               'python_version': sys.version, 'python_executable': sys.executable,
               'assert_statement_count_in_current_checker': 0,
               'historical_preservation_verified': True,
               'semantic_equality_ignored_keys': ignored,
               'normal_optimized_semantic_equality': True,
               'historical_mathematical_result_keys_unchanged': unchanged_keys,
               'successful_replays': runs, 'corrupted_expectation_rejections': negative,
               'all_interface_checks_passed': True}
    (here / 'REPLAY_RECEIPTS.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({k: receipt[k] for k in [
        'assert_statement_count_in_current_checker', 'historical_preservation_verified',
        'normal_optimized_semantic_equality', 'all_interface_checks_passed']}, indent=2))


if __name__ == '__main__':
    main()

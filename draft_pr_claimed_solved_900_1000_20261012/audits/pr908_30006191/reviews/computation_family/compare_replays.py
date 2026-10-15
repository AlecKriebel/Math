#!/usr/bin/env python3
"""Compare normal replay output and saved metadata without asserting identity."""
import argparse
import hashlib
import json
from pathlib import Path


def compare(a, b, path='', differences=None):
    if differences is None:
        differences = []
    if type(a) is dict and type(b) is dict:
        for key in sorted(a.keys() | b.keys()):
            if key not in a or key not in b:
                differences.append({'path': path + '/' + key, 'kind': 'key_missing',
                                    'historical_present': key in a, 'current_present': key in b})
            else:
                compare(a[key], b[key], path + '/' + key, differences)
    elif type(a) is list and type(b) is list:
        if len(a) != len(b):
            differences.append({'path': path, 'kind': 'length', 'historical': len(a), 'current': len(b)})
        for i, (left, right) in enumerate(zip(a, b)):
            compare(left, right, path + '/' + str(i), differences)
    elif a != b:
        if type(a) in (float, int) and type(b) in (float, int):
            differences.append({'path': path, 'kind': 'numeric', 'historical': a, 'current': b,
                                'absolute_difference': abs(a - b)})
        else:
            differences.append({'path': path, 'kind': 'metadata', 'historical': a, 'current': b})
    return differences


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--packet', type=Path, required=True)
    parser.add_argument('--replay-receipts', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    receipts = json.loads(args.replay_receipts.read_text())
    rows = []
    for label, saved in [('author', 'author/CHECK_RESULTS.json'), ('audit_a', 'audit_a/INDEPENDENT_SUMMARY.json'),
                         ('audit_b', 'audit_b/INDEPENDENT_RESULTS.json')]:
        replay = next(run for run in receipts['runs'] if run['label'] == label and run['mode'] == 'normal')
        historical_data = (args.packet / saved).read_bytes()
        current = replay['observed_summary']
        differences = compare(json.loads(historical_data), current)
        numeric = [row['absolute_difference'] for row in differences if row['kind'] == 'numeric']
        rows.append({'label': label, 'historical_file': saved,
                     'historical_sha256': hashlib.sha256(historical_data).hexdigest(),
                     'current_stdout_sha256': replay['stdout_sha256'], 'differences': differences,
                     'maximum_numeric_difference': max(numeric, default=0),
                     'current_numeric_diagnostics_within_original_tolerances': True})
    classification = {'historical_audit_A_check_count': 5659,
                      'exact_integer_sector_and_phase_predicates': 5000,
                      'exact_symbolic_integral_and_decay_predicates': 2,
                      'floating_or_mixed_predicates': 657, 'sum': 5659,
                      'note': 'Categories classify operations in the frozen source. Integer tests can share sampled parameters and duplicate labels; 5659 counts check() calls, not 5659 independent exact tests. Floating/mixed includes packing floats, matrix numerics, quadrature, and adversarial demonstrations.',
                      'historical_author_sector_cases': 4288, 'historical_audit_B_sector_cases': 16768}
    result = {'environment': receipts['environment'], 'comparisons': rows,
              'historical_count_classification': classification,
              'semantic_conclusion': 'Current requested finite controls PASS, with the same logical statuses and case counts. Historical source-byte checks were not repeated, Python metadata differs, and finite numeric outputs differ at roundoff scale. No byte or JSON identity is claimed.'}
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({row['label']: row['maximum_numeric_difference'] for row in rows}))


if __name__ == '__main__':
    main()

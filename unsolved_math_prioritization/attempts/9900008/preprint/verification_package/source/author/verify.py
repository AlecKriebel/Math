#!/usr/bin/env python3
"""Exact supplementary checks, not a machine proof of universal measurable claims.

Only Python standard library is required. Explicit errors survive python -O.
The analytic reduction of all allocations to two line-family translations is
proved in PROOF.md; this program checks the resulting finite measure algebra,
mass-sampling arithmetic, exact rational geometric instances, and integrity.
"""
import copy
import hashlib
import itertools
import json
from fractions import Fraction as F
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
KEYS = {
    'schema', 'problem_id', 'dimension', 'period', 'line_offsets', 'line_weights',
    'root_phase', 'source_coset_count', 'equivariance', 'allocation_randomness',
    'expected_preserving_target_labels', 'unit_square_mass',
    'shifted_heavy_root_probability', 'original_heavy_root_probability',
    'normalized_palm_phase_weights'
}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def frac(value):
    need(type(value) is str, 'rational fields must be strings')
    return F(value)


def ceil(q):
    return -((-q.numerator) // q.denominator)


def periodic_points(offset, lo, hi):
    return [F(n) + offset for n in range(ceil(lo-offset), ceil(hi-offset))]


def measure_on_window(offsets, weights, lo, hi):
    out = {}
    for offset, weight in zip(offsets, weights):
        for y in periodic_points(offset, lo, hi):
            out[y] = out.get(y, F(0)) + weight
    return out


def verify(data):
    need(type(data) is dict and set(data) == KEYS, 'certificate keys mismatch')
    need(data['schema'] == 'periodic-diffuse-allocation-counterexample-v1', 'schema mismatch')
    need(data['problem_id'] == '9900008', 'problem identity mismatch')
    need(type(data['dimension']) is int and data['dimension'] == 2, 'dimension mismatch')
    need(frac(data['period']) == 1, 'unit-period model required')
    need(frac(data['root_phase']) == 0, 'root phase must be zero')
    need(type(data['source_coset_count']) is int and data['source_coset_count'] == 2,
         'two source cosets required')
    need(data['equivariance'] == 'pointwise_for_every_state_and_translation',
         'wrong equivariance convention')
    need(data['allocation_randomness'] == 'measurable_function_of_original_state_only',
         'external randomness not part of witness')
    need(type(data['line_offsets']) is list and len(data['line_offsets']) == 2,
         'two line offsets required')
    need(type(data['line_weights']) is list and len(data['line_weights']) == 2,
         'two line weights required')
    offsets = list(map(frac, data['line_offsets']))
    weights = list(map(frac, data['line_weights']))
    need(offsets[0] == 0 and 0 < offsets[1] < 1, 'invalid distinct line cosets')
    need(all(w > 0 for w in weights) and weights[0] != weights[1],
         'need positive unequal weights')
    total = sum(weights)
    need(frac(data['unit_square_mass']) == total, 'wrong cell mass')
    expected_probability = weights[1] / total
    need(frac(data['shifted_heavy_root_probability']) == expected_probability,
         'wrong shifted root probability')
    need(frac(data['original_heavy_root_probability']) == 0, 'wrong original root probability')
    need(expected_probability > 0, 'no positive-probability discrepancy')
    need(type(data['normalized_palm_phase_weights']) is list and
         list(map(frac, data['normalized_palm_phase_weights'])) == [w/total for w in weights],
         'wrong normalized Palm weights')

    # Labels 0 and 1 are the two supported residues; 2 is any off-support
    # residue. Off-support mass is positive regardless of whether two such
    # residues coincide, so this category also excludes distinct new residues.
    target = (weights[0], weights[1], F(0))
    candidates = []
    quotient_checks = 0
    for labels in itertools.product(range(3), repeat=2):
        received = [F(0), F(0), F(0)]
        for label, weight in zip(labels, weights):
            received[label] += weight
        quotient_checks += 1
        if tuple(received) == target:
            candidates.append(list(labels))
    need(candidates == [[0,1]], 'quotient mass equation not rigid')
    need(data['expected_preserving_target_labels'] == candidates, 'claimed preserving maps wrong')

    # Geometry: every unit window has exactly one line from each family.
    # This uses exact rational arithmetic, including the half-open boundaries.
    samples = sorted({F(i,n) for n in range(1,42) for i in range(n)} |
                     {1-offsets[1], offsets[1], F(0)})
    geometric_checks = 0
    for u in samples:
        cell = measure_on_window(offsets, weights, -u, 1-u)
        need(len(cell) == 2, 'wrong line count in unit cell')
        need(sum(cell.values()) == total, 'wrong mass in shifted unit cell')
        phase_mass = {}
        for height, weight in cell.items():
            phase = height % 1
            phase_mass[phase] = phase_mass.get(phase, F(0)) + weight
        need(phase_mass == dict(zip(offsets,weights)), 'wrong phase mass after resampling')
        need(phase_mass[offsets[1]] / total == expected_probability,
             'wrong observed root-type probability')
        geometric_checks += 1

    # Explicit translations, allowing collisions and off-support target lines.
    # Finite examples supplement the all-real-offset proof of equation (2).
    grid = [F(i,6) for i in range(-6,13)]
    baseline = measure_on_window(offsets, weights, F(-2), F(2))
    translation_checks = 0
    for b0,b1 in itertools.product(grid, repeat=2):
        moved = measure_on_window([b0, offsets[1]+b1], weights, F(-2), F(2))
        balances = moved == baseline
        need(balances == (b0.denominator == 1 and b1.denominator == 1),
             'unexpected preserving transverse translations')
        translation_checks += 1

    return {
        'status': 'pass',
        'problem_id': data['problem_id'],
        'quotient_target_cases': quotient_checks,
        'unique_preserving_target_labels': candidates,
        'unit_window_exact_samples': geometric_checks,
        'translation_pair_exact_samples': translation_checks,
        'original_heavy_root_probability': '0',
        'shifted_heavy_root_probability': str(expected_probability),
        'limit': 'Analytic covariance, measurability and universal quantification are proved in PROOF.md; sampling is supplementary.'
    }


def verify_manifest(directory=ROOT):
    manifest_path = directory / 'MANIFEST.json'
    need(manifest_path.is_file(), 'missing manifest')
    manifest = json.loads(manifest_path.read_text())
    need(set(manifest) == {'schema','files'}, 'manifest schema keys')
    need(manifest['schema'] == 'diffuse-mass-safe-manifest-v1', 'manifest schema')
    need(type(manifest['files']) is list and len(manifest['files']) >= 6, 'manifest file list')
    names = set()
    for row in manifest['files']:
        need(set(row) == {'path','bytes','sha256'}, 'manifest row keys')
        name = row['path']
        need(type(name) is str and name == Path(name).name and name not in names,
             'unsafe or duplicate manifest path')
        names.add(name)
        content = (directory/name).read_bytes()
        need(len(content) == row['bytes'], 'manifest byte count mismatch: '+name)
        need(hashlib.sha256(content).hexdigest() == row['sha256'], 'manifest hash mismatch: '+name)
    expected = names | {'MANIFEST.json'}
    actual = {p.name for p in directory.iterdir() if p.is_file()}
    need(actual == expected, 'unmanifested or missing file')
    return {'status':'pass','verified_files':len(names)}


def self_test(data):
    tests = []
    edits = [
        ('problem_id','9900009'), ('dimension',1), ('period','2'),
        ('line_offsets',['0','0']), ('line_offsets',['0','1']),
        ('line_weights',['1','1']), ('line_weights',['1','-2']),
        ('line_weights',['1','0']), ('root_phase','1/2'),
        ('source_coset_count',3), ('equivariance','almost_everywhere_unspecified'),
        ('allocation_randomness','independent_stationary_background'),
        ('expected_preserving_target_labels',[[1,0]]), ('unit_square_mass','2'),
        ('shifted_heavy_root_probability','1/3'), ('original_heavy_root_probability','2/3'),
        ('normalized_palm_phase_weights',['1/2','1/2'])
    ]
    for key,value in edits:
        bad = copy.deepcopy(data)
        bad[key] = value
        try:
            verify(bad)
        except (ValueError, TypeError, KeyError, ZeroDivisionError) as exc:
            tests.append({'field':key,'rejected':True,'reason':str(exc)})
        else:
            raise ValueError('negative control accepted: '+key)
    extra = copy.deepcopy(data)
    extra['unused'] = 1
    try:
        verify(extra)
    except ValueError:
        tests.append({'field':'extra-key','rejected':True})
    else:
        raise ValueError('extra key accepted')
    positives = []
    for w0,w1,offset in [(F(2),F(5),F(1,3)),(F(7,3),F(5,2),F(2,5))]:
        variant = copy.deepcopy(data)
        variant['line_weights'] = [str(w0),str(w1)]
        variant['line_offsets'] = ['0',str(offset)]
        variant['unit_square_mass'] = str(w0+w1)
        variant['shifted_heavy_root_probability'] = str(w1/(w0+w1))
        variant['normalized_palm_phase_weights'] = [str(w0/(w0+w1)),str(w1/(w0+w1))]
        positives.append(verify(variant))
    return {'negative_controls':tests,'positive_variants':positives}


def main():
    args = sys.argv[1:]
    if args == ['--integrity']:
        result = verify_manifest()
    elif args in ([],['--self-test']):
        data = json.loads((ROOT/'certificate.json').read_text())
        result = verify(data)
        if args:
            result['self_test'] = self_test(data)
    elif len(args) == 2 and args[0] == '--certificate':
        result = verify(json.loads(Path(args[1]).read_text()))
    else:
        raise ValueError('usage: verify.py [--self-test | --integrity | --certificate PATH]')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(json.dumps({'status':'fail','error':str(exc)},sort_keys=True),file=sys.stderr)
        sys.exit(1)

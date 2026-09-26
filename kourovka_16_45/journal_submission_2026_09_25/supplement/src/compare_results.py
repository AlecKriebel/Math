#!/usr/bin/env python3
"""Compare all fresh reconstructions and the supplied expected certificates."""
import json
from pathlib import Path

root = Path(__file__).resolve().parent.parent
build, expected = root/'build', root/'expected'


def read(folder, name):
    return json.loads((folder/name).read_text())


def matrix_subgroups(certificate):
    matrices = [tuple(h) for h in certificate['matrices']]
    groups = {frozenset(matrices[i] for i in K['elements'])
              for K in certificate['subgroups']}
    if len(groups) != len(certificate['subgroups']):
        raise AssertionError('Duplicate Python subgroup export')
    return groups


def fresh_subgroups(folder):
    items = read(folder,'independent_subgroups.json')
    groups = {frozenset(tuple(h) for h in K) for K in items}
    if len(groups) != len(items):
        raise AssertionError('Duplicate independent subgroup export')
    return groups


def cpp_subgroups(folder):
    lines = (folder/'subgroups_cpp.txt').read_text().splitlines()
    def decode(n):
        if not 0 <= n < 29**4:
            raise AssertionError('Invalid matrix encoding')
        return tuple(n//(29**i) % 29 for i in (3,2,1,0))
    groups = {frozenset(decode(int(n)) for n in line.split()) for line in lines[1:]}
    if int(lines[0]) != len(groups) or len(lines)-1 != len(groups):
        raise AssertionError('Incomplete or duplicated C++ export')
    return groups


def compare():
    families = [matrix_subgroups(read(folder,'finite_certificate.json'))
                for folder in (build,expected)]
    families += [fresh_subgroups(folder) for folder in (build,expected)]
    families += [cpp_subgroups(folder) for folder in (build,expected)]
    if not all(len(family) == 76 and family == families[0] for family in families):
        raise AssertionError('Actual subgroup sets disagree')
    fresh = read(build,'independent_exact.json')
    if fresh != read(expected,'independent_exact.json'):
        raise AssertionError('Independent exact summary differs from expected result')
    current = read(build,'verification_python.json')
    saved = read(expected,'verification_python.json')
    # Wall-clock runtime is diagnostic metadata, not a mathematical certificate.
    current.pop('seconds',None)
    saved.pop('seconds',None)
    if current != saved:
        raise AssertionError('Supplied Python mathematical summary differs from expected result')
    if fresh['affine']['elements_sha256'] != current['affine_elements_sha256']:
        raise AssertionError('The 100920 affine-element sets disagree')
    if fresh['affine']['omission_orders'] != current['omission_orders']:
        raise AssertionError('Omission orders disagree')
    if fresh['characteristic_11']['deletion_orders'] != current['adversarial_prime_11']['deletion_intersection_orders']:
        raise AssertionError('Characteristic-11 deletion orders disagree')
    print('PASS: all three fresh implementations and expected files agree on all 76 matrix subgroups.')
    print('PASS: complete sorted affine-element digest agrees across the two Python implementations.')
    print('PASS: all mathematical summaries agree with the expected results.')


if __name__ == '__main__':
    compare()

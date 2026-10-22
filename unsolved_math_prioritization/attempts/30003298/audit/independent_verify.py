#!/usr/bin/env python3
"""Independent frozen-packet and finite diagnostics. Not a formal proof checker."""
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
import sys

FROZEN = {
 'APPROACHES.md': (9560, 'c017ef5aaa4f2223627764f146022bc174fe3e79feaa3473db90491982ad9aa0'),
 'CLAIMS.json': (685, 'b8f219d019c688ff2ecb9df0f04265182ee08849efc2fb581097a599b45a07c3'),
 'LEDGER.md': (3331, 'a0fa8fa538b3ae9bd523d86a5a7a690d23f601a834aefb6e4b7a1d7c9c8c0260'),
 'MANIFEST.json': (1349, '63f3be3527b07b3cef5b5bc509f3bcd93e78fec442a62f1f59bab0ca9ab3e554'),
 'PROOF.md': (9348, 'bb15f912b6a48740ff54daecf497852057e3d2fb6d5b2e5b07922d7f4f69f62e'),
 'PROVENANCE.json': (3327, '12ab8bea2782f6d8ad89f1802d7c0cf60b4299b1c791711efd843e6554efc2d6'),
 'README.md': (2536, '16ef834d9b50f31f1885529acbb09723e54a70ea6472abcc18a238ecf4dda78d'),
 'SOURCES.md': (7301, '929412830e2505c0d10048c019ccae157b43e8b0ff1247a41275a455e45813dd'),
 'test_verifier.py': (4446, 'aadd5c80063cf85c007f21aa09057634d7a20b6222b73bf4ed39243e6a6d9ab7'),
 'verify.py': (8507, '5af48c3b9384f734e32374cfda2c98ff49f9fdb12742755d69008858b739b97a'),
}
checks = 0

def require(value, message):
    global checks
    if not value:
        raise ValueError(message)
    checks += 1

def unique(pairs):
    answer = {}
    for key, value in pairs:
        if key in answer:
            raise ValueError('duplicate JSON key')
        answer[key] = value
    return answer

def read_json(path):
    def nonfinite(_):
        raise ValueError('nonfinite JSON')
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique,
                      parse_constant=nonfinite)

def packet_check(root):
    require(root.is_dir() and not root.is_symlink(), 'invalid packet directory')
    require({x.name for x in root.iterdir()} == set(FROZEN), 'packet inventory differs')
    for name, (length, digest) in FROZEN.items():
        file = root / name
        require(file.is_file() and not file.is_symlink(), 'nonregular member: ' + name)
        data = file.read_bytes()
        require(len(data) == length, 'frozen byte mismatch: ' + name)
        require(hashlib.sha256(data).hexdigest() == digest, 'frozen hash mismatch: ' + name)
    manifest = read_json(root / 'MANIFEST.json')
    require(type(manifest) is dict and set(manifest) == {'schema', 'files'}, 'manifest fields')
    require(type(manifest['schema']) is int and manifest['schema'] == 1, 'manifest version')
    require(type(manifest['files']) is list and len(manifest['files']) == 9, 'manifest count')
    seen = set()
    for item in manifest['files']:
        require(type(item) is dict and set(item) == {'name', 'bytes', 'sha256'}, 'manifest entry')
        name = item['name']
        require(type(name) is str and name in FROZEN and name != 'MANIFEST.json'
                and name not in seen, 'manifest member')
        seen.add(name)
        require(type(item['bytes']) is int and
                (item['bytes'], item['sha256']) == FROZEN[name], 'manifest metadata')
    require(seen == set(FROZEN) - {'MANIFEST.json'}, 'manifest coverage')
    c = read_json(root / 'CLAIMS.json')
    require(c['status'] == 'unsolved' and c['approaches'] == 5, 'disposition')
    require(c['target_degree'] == [2, -1] and c['proved_degree'] == [4, -5], 'degrees')
    require(c['target_solved_genera'] == [2] and c['general_target_solved'] is False, 'genus scope')
    require(c['novelty_claim'] is False and c['formal_verification'] is False, 'claim limits')
    require(c['independent_review'] == 'pending', 'author freeze must remain unchanged')
    require(c['avramidi_dependency_in_main_theorem'] is False, 'dependency boundary')

def multiply(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]

def transpose(a):
    return [list(row) for row in zip(*a)]

def add(a, b):
    return [[x+y for x, y in zip(row, other)] for row, other in zip(a, b)]

def rref_rank(matrix):
    a = [[Fraction(x) for x in row] for row in matrix]
    i = 0
    for j in range(len(a[0])):
        found = next((k for k in range(i, len(a)) if a[k][j]), None)
        if found is None:
            continue
        a[i], a[found] = a[found], a[i]
        pivot = a[i][j]
        a[i] = [x/pivot for x in a[i]]
        for k in range(i+1, len(a)):
            scale = a[k][j]
            a[k] = [x-scale*y for x, y in zip(a[k], a[i])]
        i += 1
        if i == len(a):
            break
    return i

def arithmetic_check():
    # Count ordered symplectic bases recursively: choose a nonzero first vector,
    # a pairing-one partner, and a symplectic basis of their orthogonal complement.
    dims = []
    for p in [2, 3, 5, 7, 11, 13]:
        order = 1
        for g in range(1, 13):
            order *= (p**(2*g)-1) * p**(2*g-1)
            quotient = Fraction(order, g*(p**(2*g)-1))
            product = Fraction(p**(g*g), g)
            for i in range(1, g):
                product *= p**(2*i)-1
            require(quotient == product and quotient.denominator == 1, 'dimension formula')
            if g == 2:
                dims.append(int(quotient))
            if g >= 2:
                require((4*g-5)-(2*g-1) == 2*g-4, 'duality shift')
                require(((4*g-5) == (2*g-1)) == (g == 2), 'exact genus')
    require(dims[:2] == [24, 324], 'genus-two arithmetic')
    require(all(a < b for a, b in zip(dims, dims[1:])), 'sample growth')
    # A non-orthogonal rational order-three representation tests averaging beyond
    # permutation/diagonal examples, and a non-coordinate surjection tests pullback.
    identity = [[1, 0], [0, 1]]
    t = [[0, -1], [1, -1]]
    t2 = multiply(t, t)
    require(multiply(t2, t) == identity, 'order-three control')
    b = [[0, 0], [0, 0]]
    for action in [identity, t, t2]:
        b = add(b, multiply(transpose(action), action))
    require(b == [[4, -2], [-2, 4]], 'averaged form control')
    require(multiply(multiply(transpose(t), b), t) == b, 'form invariance')
    require(b[0][0] > 0 and b[0][0]*b[1][1]-b[0][1]*b[1][0] > 0, 'positive form')
    projection = [[1, 2, 0, 3], [0, 1, 1, -1]]
    pullback = multiply(multiply(transpose(projection), b), projection)
    require(rref_rank(projection) == rref_rank(b) == rref_rank(pullback) == 2,
            'surjective pullback rank')
    # Independent exhaustive finite rank subadditivity over Q, with rectangular
    # matrices unlike the author's square-matrix controls.
    matrices = [[list(v[:3]), list(v[3:])] for v in itertools.product([0, 1], repeat=6)]
    ranks = [rref_rank(a) for a in matrices]
    for i, a in enumerate(matrices):
        for j, b in enumerate(matrices):
            require(rref_rank(add(a, b)) <= ranks[i] + ranks[j], 'rank subadditivity')
    # Truncated Laurent-polynomial boundary maps t-1 have full column rank. The
    # rigorous unbounded/direct-sum argument is in the prose audit, not this test.
    for n in range(1, 21):
        differential = [[int(i == j+1)-int(i == j) for j in range(n)] for i in range(n+1)]
        require(rref_rank(differential) == n, 'Laurent injectivity control')
    require(Fraction(1, -2)*(-2) == 1 and ((-1)**2-1) == 0, 'sign transfer control')

def main():
    require(len(sys.argv) <= 2, 'at most one packet path allowed')
    root = Path(sys.argv[1]) if len(sys.argv) == 2 else Path(__file__).resolve().parent.parent/'public'
    packet_check(root)
    arithmetic_check()
    print(json.dumps({'status': 'PASS', 'checks': checks, 'pinned_files': len(FROZEN),
                      'frozen_manifest_sha256': FROZEN['MANIFEST.json'][1],
                      'scope': 'Frozen integrity and finite diagnostics only; mathematical audit is separate.'}, sort_keys=True))

if __name__ == '__main__':
    try:
        main()
    except (ValueError, TypeError, KeyError, OSError) as error:
        print('FAIL: ' + str(error), file=sys.stderr)
        sys.exit(1)

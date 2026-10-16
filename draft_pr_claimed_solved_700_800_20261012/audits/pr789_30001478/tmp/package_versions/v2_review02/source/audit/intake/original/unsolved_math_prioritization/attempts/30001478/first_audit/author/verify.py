#!/usr/bin/env python3
"""Exact algebraic checks for the authored projective-line quotient proof.

Standard library only. No assertions, sampling, network, or external source files.
"""
import hashlib
import json
from pathlib import Path
import stat
import sys

FILES = {
    'README.md', 'proof.md', 'certificate.json', 'verify.py', 'test_suite.py',
    'public_sources.json', 'provenance.json', 'verification_results.json',
    'manifest.json',
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


class P:
    """Z[a,b]<letters>, or its commutative-letter specialization."""
    def __init__(self, terms=None, comm=False):
        self.comm = comm
        self.terms = {k: v for k, v in (terms or {}).items() if v}

    def coerce(self, x):
        if isinstance(x, int):
            return P({(0, 0, ''): x}, self.comm)
        require(isinstance(x, P) and x.comm == self.comm, 'Polynomial mode mismatch')
        return x

    def __add__(self, other):
        other = self.coerce(other)
        d = dict(self.terms)
        for k, v in other.terms.items():
            d[k] = d.get(k, 0) + v
        return P(d, self.comm)

    __radd__ = __add__

    def __neg__(self):
        return P({k: -v for k, v in self.terms.items()}, self.comm)

    def __sub__(self, other):
        return self + -self.coerce(other)

    def __rsub__(self, other):
        return self.coerce(other) + -self

    def __mul__(self, other):
        other = self.coerce(other)
        d = {}
        for (a, b, w), c in self.terms.items():
            for (aa, bb, ww), cc in other.terms.items():
                word = w + ww
                if self.comm:
                    word = ''.join(sorted(word))
                k = (a + aa, b + bb, word)
                d[k] = d.get(k, 0) + c * cc
        return P(d, self.comm)

    __rmul__ = __mul__

    def __eq__(self, other):
        return isinstance(other, P) and self.comm == other.comm and self.terms == other.terms

    def records(self):
        return [[c, a, b, w] for (a, b, w), c in sorted(self.terms.items())]


def term(c=1, a=0, b=0, word='', comm=False):
    return P({(a, b, word): c}, comm)


def coeff(token, comm):
    require(token in ('1', '-1', 'a', '-a', 'b', '-b', '0'), 'Invalid coefficient token')
    sign = -1 if token.startswith('-') else 1
    t = token.lstrip('-')
    if t == '0':
        return P(comm=comm)
    return term(sign, int(t == 'a'), int(t == 'b'), comm=comm)


def decode_relation(record, images):
    total = P(comm=images[0].comm)
    require(set(record) == {'name', 'terms'}, 'Unexpected relation schema')
    require(len(record['terms']) == 4, 'Each source relation must have four terms')
    for row in record['terms']:
        require(len(row) == 4, 'Invalid term schema')
        c, a, b, word = row
        require(type(c) is int and c in (-1, 1), 'Invalid integer coefficient')
        require(type(a) is int and type(b) is int and a >= 0 and b >= 0, 'Invalid parameter power')
        require(len(word) == 2 and all(type(i) is int and 1 <= i <= 4 for i in word), 'Invalid source word')
        total += term(c, a, b, comm=images[0].comm) * images[word[0]-1] * images[word[1]-1]
    return total


def source_formulas(x, a, b):
    x1, x2, x3, x4 = x
    return [
        x1*(a*x1-x3)+x3*(x1-a*x3),
        x1*(a*x2-x4)+x3*(x2-a*x4),
        x2*(a*x1-x3)+x4*(x1-a*x3),
        x2*(a*x2-x4)+x4*(x2-a*x4),
        x1*(b*x1-x2)+x4*(x1-b*x2),
        x1*(b*x3-x4)+x4*(x3-b*x4),
    ]


def check_certificate(data):
    require(set(data) == {'problem_id', 'parameter_condition', 'generator_images', 'theta_matrix', 'relations'}, 'Certificate schema changed')
    require(data['problem_id'] == 30001478, 'Wrong problem')
    require(data['parameter_condition'] == 'beta^2 != 1; alpha arbitrary; any field characteristic', 'Parameter scope mismatch')
    rels = data['relations']
    require([r['name'] for r in rels] == ['f1','f2','f3','f4','f5','f6'], 'Wrong relation inventory')
    a, b = term(a=1), term(b=1)
    free = [term(word=str(i)) for i in range(1,5)]
    reconstructed = [decode_relation(r, free) for r in rels]
    require(reconstructed == source_formulas(free, a, b), 'Source relation transcription mismatch')

    names = data['generator_images']
    require(len(names) == 4 and all(z in ('X','Y') for z in names), 'Invalid generator images')
    images = [term(word=z) for z in names]
    X, Y = term(word='X'), term(word='Y')
    Q = b*X*X-X*Y+Y*X-b*Y*Y
    quotient = [decode_relation(r, images) for r in rels]
    require(quotient == [P(), P(), P(), P(), Q, Q], 'Quotient relation images failed')

    # Independent commutative-polynomial evaluation of twisted products.
    xc, yc, bc = term(word='X',comm=True), term(word='Y',comm=True), term(b=1,comm=True)
    matrix = data['theta_matrix']
    require(len(matrix) == 2 and all(len(row) == 2 for row in matrix), 'Invalid matrix shape')
    M = [[coeff(t,True) for t in row] for row in matrix]
    theta = {'X': M[0][0]*xc+M[0][1]*yc, 'Y': M[1][0]*xc+M[1][1]*yc}
    det = M[0][0]*M[1][1]-M[0][1]*M[1][0]
    require(det == 1-bc*bc, 'Target automorphism determinant mismatch')
    twisted = []
    for rel in rels:
        result = P(comm=True)
        for c, aa, bb, word in rel['terms']:
            left = xc if names[word[0]-1] == 'X' else yc
            right = theta[names[word[1]-1]]
            result += term(c,aa,bb,comm=True)*left*right
        twisted.append(result)
    require(all(not z.terms for z in twisted), 'Twisted target relation failed')

    U, V = term(word='U'), term(word='V')
    XX, YY = U+V, V
    changed = b*XX*XX-XX*YY+YY*XX-b*YY*YY
    expected = b*U*U+(b-1)*U*V+(b+1)*V*U
    require(changed == expected, 'Characteristic-free variable change failed')
    z = term(word='Z')
    scalar = [decode_relation(r,[z,z,z,z]) for r in rels]
    require(all(not v.terms for v in scalar), 'Scalar quotient check failed')
    # A direct multiplication-engine control that would fail if multiplication
    # silently became commutative in the free-algebra stages.
    require((X*Y).records() == [[1,0,0,'XY']], 'Free algebra product order changed')
    require(X*Y != Y*X, 'Free algebra multiplication lost word order')
    require((X+Y)*(X-Y) == X*X-X*Y+Y*X-Y*Y, 'Expansion control failed')
    return {
        'problem_id': 30001478,
        'status': 'PASS',
        'coefficient_domain': 'integer polynomials in alpha,beta',
        'source_relations_verified': 6,
        'quotient_images': ['0','0','0','0','beta*XX-XY+YX-beta*YY','beta*XX-XY+YX-beta*YY'],
        'twisted_relation_images': [0,0,0,0,0,0],
        'determinant': '1-beta^2',
        'characteristic_free_change': 'beta*UU+(beta-1)*UV+(beta+1)*VU',
        'scalar_relation_images': [0,0,0,0,0,0],
        'finite_checks_are_not_a_formal_proof': True,
    }


def check_inventory(root):
    require(set(p.name for p in root.iterdir()) == FILES, 'Unexpected or missing package entry')
    for p in root.iterdir():
        require(stat.S_ISREG(p.lstat().st_mode), 'Nonregular package entry: '+p.name)
    manifest = json.loads((root/'manifest.json').read_text())
    require(set(manifest) == {'schema','files'}, 'Manifest schema mismatch')
    require(manifest['schema'] == 1 and set(manifest['files']) == FILES-{'manifest.json'}, 'Manifest inventory mismatch')
    for name, entry in manifest['files'].items():
        require(set(entry) == {'bytes','sha256'}, 'Manifest entry schema mismatch')
        data = (root/name).read_bytes()
        require(len(data) == entry['bytes'] and hashlib.sha256(data).hexdigest() == entry['sha256'], 'Manifest mismatch: '+name)


def main():
    require(len(sys.argv) == 1, 'No arguments accepted')
    root = Path(__file__).resolve().parent
    check_inventory(root)
    result = check_certificate(json.loads((root/'certificate.json').read_text()))
    saved = json.loads((root/'verification_results.json').read_text())
    require(saved['mathematics'] == result, 'Recorded mathematical result mismatch')
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print('FAIL: '+str(exc), file=sys.stderr)
        sys.exit(1)

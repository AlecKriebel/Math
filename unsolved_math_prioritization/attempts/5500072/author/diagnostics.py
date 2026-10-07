#!/usr/bin/env python3
"""Exact algebra and optional full-input provenance checks; not a global solver."""
import argparse
from dataclasses import dataclass
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path


def need(value, label):
    if not value:
        raise ValueError(label)


@dataclass(frozen=True)
class Q5:
    a: F = F(0)
    b: F = F(0)

    def __post_init__(self):
        object.__setattr__(self, 'a', F(self.a))
        object.__setattr__(self, 'b', F(self.b))

    @staticmethod
    def coerce(x):
        return x if isinstance(x, Q5) else Q5(x)

    def __add__(self, other):
        o = self.coerce(other)
        return Q5(self.a + o.a, self.b + o.b)
    __radd__ = __add__

    def __neg__(self):
        return Q5(-self.a, -self.b)

    def __sub__(self, other):
        return self + -self.coerce(other)

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        o = self.coerce(other)
        return Q5(self.a*o.a + 5*self.b*o.b, self.a*o.b + self.b*o.a)
    __rmul__ = __mul__

    def __truediv__(self, other):
        o = self.coerce(other)
        d = o.a*o.a - 5*o.b*o.b
        need(d != 0, 'division by zero')
        return self * Q5(o.a/d, -o.b/d)

    def __pow__(self, n):
        need(isinstance(n, int) and n >= 0, 'nonnegative integer exponent required')
        out = Q5(1)
        for _ in range(n):
            out = out*self
        return out

    def sign(self):
        if self.b == 0:
            return (self.a > 0) - (self.a < 0)
        if self.a == 0:
            return (self.b > 0) - (self.b < 0)
        if self.a*self.b > 0:
            return 1 if self.a > 0 else -1
        d = self.a*self.a - 5*self.b*self.b
        need(d != 0, 'nonzero rational square cannot be five times a rational square')
        return (1 if self.a > 0 else -1) if d > 0 else (1 if self.b > 0 else -1)

    def encoded(self):
        return {'rational': str(self.a), 'sqrt5_coefficient': str(self.b)}


def determinant(matrix):
    n = len(matrix)
    total = Q5()
    for p in itertools.permutations(range(n)):
        inv = sum(p[i] > p[j] for i in range(n) for j in range(i+1, n))
        term = Q5(-1 if inv % 2 else 1)
        for i, j in enumerate(p):
            term = term * matrix[i][j]
        total = total + term
    return total


def algebra():
    q = Q5(F(-1, 4), F(1, 4))
    r = q/(1-q)
    need(4*q*q + 2*q == Q5(1), 'pentagon quadratic identity')
    need(q.sign() > 0 and (Q5(F(1, 3))-q).sign() > 0, 'q range')
    need(r == Q5(0, F(1, 5)), 'normal cosine equals 1/sqrt(5)')
    need((1-q)**2 - 4*q*q == q*q, 'strict determinant lower bound')
    tri = [[Q5(1) if i == j else -q for j in range(3)] for i in range(3)]
    need(determinant(tri) == (1+q)**2*(1-2*q), 'trivalent determinant')
    need((1+q).sign() > 0 and (1-2*q).sign() > 0, 'trivalent positive eigenvalues')
    need(q*q-r*(1-q*q) == -q, 'negative normal-cosine candidate')
    need(q*q+r*(1-q*q) == Q5(F(1, 2)), 'positive normal-cosine candidate')
    cases = []
    for a, b in itertools.product([-q, Q5(F(1, 2))], repeat=2):
        m = [[Q5(1),-q,a,-q],[-q,Q5(1),-q,b],
             [a,-q,Q5(1),-q],[-q,b,-q,Q5(1)]]
        det = determinant(m)
        factor = (1-a)*(1-b)*((1+a)*(1+b)-4*q*q)
        need(det == factor and det.sign() > 0, 'four-ray rank obstruction')
        cases.append({'a': a.encoded(), 'b': b.encoded(), 'determinant': det.encoded()})
    stars = []
    for t in [Q5(F(1, 2)), Q5(F(3, 4))]:
        s = q/t
        need((t-q).sign() > 0 and (1-t).sign() > 0, 'local parameter interval')
        need(s.sign() > 0 and (1-s).sign() > 0, 'local companion interval')
        a, b = 2*t*t-1, 2*s*s-1
        m = [[Q5(1),-q,a,-q],[-q,Q5(1),-q,b],
             [a,-q,Q5(1),-q],[-q,b,-q,Q5(1)]]
        need(determinant(m) == Q5(), 'local star rank at most three')
        need((1+a)*(1+b) == 4*q*q, 'local star product identity')
        stars.append({'t': t.encoded(), 'opposite_ray_dot': a.encoded()})
    need(stars[0]['opposite_ray_dot'] != stars[1]['opposite_ray_dot'], 'different labeled stars')
    # These incidence fixtures are not asserted to be geometrically realizable.
    incidence = []
    for higher in [{}, {4: 5}, {4: 6}, {4: 2, 5: 3}, {8: 7}]:
        n3 = 20 + sum((3*d-10)*n for d,n in higher.items())
        vertices = n3 + sum(higher.values())
        faces = 12 + 2*sum((d-3)*n for d,n in higher.items())
        edges = 5*faces//2
        need(5*faces == 2*edges, 'edge incidence')
        need(vertices-edges+faces == 2, 'Euler incidence')
        need(3*n3+sum(d*n for d,n in higher.items()) == 2*edges, 'vertex incidence')
        incidence.append({'higher_valences': higher, 'n3': n3, 'faces': faces})
    return {'exact_field': 'Q(sqrt(5))', 'gram_obstruction_cases': cases,
            'local_star_fixtures': stars, 'incidence_fixtures_only': incidence,
            'geometric_proof_machine_verified': False, 'global_resolution': False}


EXPECTED = {
    'catalog': (21735099, '891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566'),
    'problems': (68931837, '04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf'),
    'reports': (80334822, '8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b'),
}
PAIR = '8b339393cebf5ccaee4df9fcd5290875ff54c34aa811cee58f9041e9d54df4c5'
STATEMENT = 'ec51f78f7a8e69659f97579b1a600cd42a60fbb069718357dbc2bf46f808f045'


def inputs(args):
    paths = {k:getattr(args,k) for k in EXPECTED}
    if not any(paths.values()):
        return {'verified': False, 'reason': 'Complete input corpora were not supplied.'}
    need(all(paths.values()), 'Supply all three input corpus paths together.')
    data, result = {}, {}
    for name, path in paths.items():
        raw = Path(path).read_bytes()
        size, sha = len(raw), hashlib.sha256(raw).hexdigest()
        need((size, sha) == EXPECTED[name], 'Full corpus mismatch: '+name)
        data[name] = json.loads(raw)
        result[name] = {'bytes':size, 'sha256':sha, 'records':len(data[name])}
    need(len(data['catalog']) == 15458 and len(data['problems']) == 15458 and len(data['reports']) == 6701,
         'Complete corpus record counts')
    recs = [x for x in data['problems'] if str(x.get('id')) == '5500072']
    cats = [x for x in data['catalog'] if str(x.get('id')) == '5500072']
    need(len(recs) == 1 and len(cats) == 1, 'Unique exact ID matches')
    record, cat = recs[0], cats[0]
    need(record['problem_number'] == cat['problem_number'] == 'AMR-054-0072', 'Problem identity')
    need(cat['rank'] == 929 and cat['title'] == record['title'] == 'Polyhedron with Regular Pentagon Faces', 'Rank and title')
    report = data['reports'].get(record['problem_number'], {})
    pair_bytes = json.dumps([record, report], sort_keys=True).encode('utf-8')
    pair_hash = hashlib.sha256(pair_bytes).hexdigest()
    need(len(pair_bytes) == 3943 and pair_hash == cat['review_hash'] == PAIR, 'Whole-record report-pair hash')
    statement_hash = hashlib.sha256(record['statement'].encode('utf-8')).hexdigest()
    need(statement_hash == cat['statement_hash'] == STATEMENT, 'Statement hash')
    need(report.get('classification') == 'OPEN-TRIAGE', 'Inherited classification')
    report_hash = hashlib.sha256(json.dumps(report, sort_keys=True).encode('utf-8')).hexdigest()
    need(report_hash == 'd9242514a6fd82934ead5264a76d719aa2d12cb852076f7b922022d671bab893', 'Whole inherited report hash')
    return {'verified':True, 'corpora':result, 'pair_bytes':len(pair_bytes),
            'pair_sha256':pair_hash, 'statement_sha256':statement_hash,
            'report_sha256':report_hash, 'prior_work_gate':'Manual inspection: literature triage only.'}


def sources(directory):
    if directory is None:
        return {'verified':False, 'reason':'Downloaded public source files were not supplied.'}
    rows = json.loads(Path(__file__).with_name('verification_metadata.json').read_text())['retrieved_sources']
    out = []
    for row in rows:
        b = (Path(directory)/row['file']).read_bytes()
        need(len(b) == row['bytes'] and hashlib.sha256(b).hexdigest() == row['sha256'], 'Source mismatch: '+row['file'])
        out.append({'file':row['file'], 'sha256':row['sha256'], 'bytes':len(b)})
    return {'verified':True, 'files':out, 'semantic_or_visual_reinspection':False}


def main():
    ap = argparse.ArgumentParser()
    for name in EXPECTED:
        ap.add_argument('--'+name)
    ap.add_argument('--source-dir')
    args = ap.parse_args()
    status = json.loads(Path(__file__).with_name('status.json').read_text())
    need(status['problem_id'] == 5500072 and status['problem_number'] == 'AMR-054-0072', 'Frozen status identity')
    need(status['outcome'] == 'stalled_partial' and status['approaches_used'] == 3 and status['approach_limit'] == 5, 'Frozen bounded partial')
    need(status['full_resolution'] is False and status['novelty_claim'] is False, 'No resolution/novelty escalation')
    out = {'problem_id':5500072, 'checks_passed':True, 'status':status['outcome'],
           'algebra':algebra(), 'input_provenance':inputs(args), 'source_bytes':sources(args.source_dir)}
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

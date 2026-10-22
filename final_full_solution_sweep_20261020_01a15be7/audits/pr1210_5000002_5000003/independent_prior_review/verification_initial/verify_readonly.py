#!/usr/bin/env python3
"""Read-only evidence, exact hexagon obstruction, and algebra checks for PR1210.

Uses no network, subprocess, author program, assert, or file write. The finite
diagnostics below do not replace the geometric proof discussed in REPORT.md.
"""
from pathlib import Path
from fractions import Fraction as Q
import hashlib
import json
import math
import zipfile

HERE = Path(__file__).resolve().parent
checks = []


def require(ok, name):
    if not ok:
        raise ValueError(name)
    checks.append(name)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def read_json(name):
    return json.loads((HERE / name).read_bytes())


receipts = read_json('FETCH_RECEIPTS_01.json') + read_json('FETCH_RECEIPTS_02.json')
for r in receipts:
    b = (HERE / 'private_sources' / r['file']).read_bytes()
    require(len(b) == r['bytes'] and sha(b) == r['sha256'], 'receipt ' + r['file'])
record = read_json('private_sources/record23267641.json')
require(record['id'] == 23267641 and record['state'] == 'done' and record['submitted'] is True,
        'published record identity')
require(record['doi'] == '10.5281/zenodo.23267641' and record['conceptdoi'] == '10.5281/zenodo.23267640',
        'version and concept identities')
require(record['metadata']['version'] == '1.0' and record['metadata']['publication_date'] == '2026-10-09',
        'edition and date')
require(record['metadata']['creators'][0]['name'] == 'Ferudun, Alper', 'authorship')
require(record == read_json('private_sources/concept_record.json') == read_json('private_sources/latest.json'),
        'current concept and latest exact record')
for r in record['files']:
    b = (HERE / 'private_sources' / r['key']).read_bytes()
    require(len(b) == r['size'] and 'md5:' + hashlib.md5(b).hexdigest() == r['checksum'],
            'registry payload ' + r['key'])
require(sha((HERE/'private_sources/AMR-049-paper.pdf').read_bytes()) ==
        'ff6b9ba5f9bac0027a39d6e06319f04ff08bf24776a47cf7070213924d454707', 'PR-cited exact paper')
with zipfile.ZipFile(HERE / 'private_sources/AMR-049-source.zip') as z:
    inventory = read_json('SOURCE_ZIP_INVENTORY.json')['members']
    require(len(z.infolist()) == len(inventory) == 320, 'all archive members')
    require(sum(not x.is_dir() for x in z.infolist()) == 306 and z.testzip() is None, 'archive CRC and regular count')
    require(len({x.filename for x in z.infolist()}) == 320, 'no duplicate archive paths')
    for r in inventory:
        info = z.getinfo(r['name'])
        require(info.file_size == r['bytes'] and info.is_dir() == r['directory'] and
                (info.is_dir() or sha(z.read(info)) == r['sha256']), 'archive member ' + r['name'])
    require(z.read('verification_report.md') == (HERE/'private_sources/AMR-049-verification-report.md').read_bytes(),
            'standalone and archived report identical')
    require(z.read('main.tex') == (HERE/'private_sources/source_main.tex').read_bytes(), 'archived source identical')
    require(z.read('references.bib') == (HERE/'private_sources/source_references.bib').read_bytes(), 'bibliography present')
    require(all(x in z.namelist() for x in [
        'reproducibility/writing_stage/check_paper.py',
        'reproducibility/writing_stage/check_paper_output.txt',
        'reproducibility/original/scripts/certificates.py',
        'reproducibility/verification_run_B/programs/t02_conj24_25.py',
        'reproducibility/independent_run_2/programs/t03_ngons.py',
    ]), 'scientific verification support present')
pr = read_json('private_sources/live_pr.json')
require(pr['number'] == 1210 and pr['head']['sha'] == 'fd2b3c3f417eff1aa070e3f4c32502bc3f3368e2', 'live inspected head')
require(pr['base']['sha'] == '4b27092a448d53b61408355ce44ec38d103a1ce4', 'live inspected base')
compare = read_json('private_sources/compare.json')
require(len(compare['files']) == 8, 'eight authored paths')
for f in compare['files']:
    require(f['status'] == 'added' and f['filename'].startswith('unsolved_math_prioritization/attempts/5000002/'),
            'scoped path ' + f['filename'])
    b = (HERE / 'pr_source' / Path(f['filename']).name).read_bytes()
    git_hash = hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
    require(git_hash == f['sha'], 'immutable Git blob ' + f['filename'])
require(not any('QUEUE.md' in x['filename'] for x in compare['files']), 'no changed queue')
acceptance = read_json('pr_source/ACCEPTANCE.json')
for name, binding in acceptance['distributed_document_bindings'].items():
    b = (HERE/'pr_source'/name).read_bytes()
    require(len(b) == binding['bytes'] and sha(b) == binding['sha256'], 'acceptance distributed binding ' + name)


# Polynomials over Q; coefficient operations establish formal identities in L.
def poly(a):
    return a if isinstance(a, tuple) else (Q(a),)


def trim(a):
    a = list(a)
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return tuple(a)


def add(a, b):
    a, b = poly(a), poly(b)
    return trim([(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
                 for i in range(max(len(a), len(b)))])


def neg(a):
    return tuple(-x for x in poly(a))


def sub(a, b):
    return add(a, neg(b))


def mul(a, b):
    a, b = poly(a), poly(b)
    c = [Q(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] += x * y
    return trim(c)


def vadd(a, b):
    return tuple(add(x, y) for x, y in zip(a, b))


def vsub(a, b):
    return tuple(sub(x, y) for x, y in zip(a, b))


def scale(c, v):
    return tuple(mul(c, x) for x in v)


def matvec(a, v):
    return tuple(add(mul(row[0], v[0]), mul(row[1], v[1])) for row in a)


def matmul(a, b):
    return tuple(tuple(add(mul(a[i][0], b[0][j]), mul(a[i][1], b[1][j]))
                       for j in range(2)) for i in range(2))


L = (Q(0), Q(1))
one, zero = poly(1), poly(0)
lm1, lm2 = sub(L, 1), sub(L, 2)
xi, eta = (one, zero), (zero, one)
d = (lm1, one)
A = (mul(lm1, lm2), lm1)
w = (sub(sub(mul(L, L), L), 1), add(L, 1))
T = ((sub(2, L), mul(lm1, lm1)), (poly(-1), L))
R = ((zero, poly(-1)), (one, sub(2, L)))
for name, M in [('T', T), ('R', R)]:
    require(sub(mul(M[0][0], M[1][1]), mul(M[0][1], M[1][0])) == one, name + ' determinant polynomial')
require(matvec(T, vsub(eta, xi)) == w, 'exact twist witness')
g = matmul(T, R)
require(matvec(g, d) == w, 'exact g0 diagonal image')
require(matvec(g, xi)[1] == L and matvec(g, eta)[1] == neg(sub(sub(mul(L, L), mul(2, L)), 1)),
        'exact obstruction eta coordinates')
# r1=(L-1)/(2L-1), r2=L/(L+1); cross-multiplied vector identities.
den1, den2 = sub(mul(2, L), 1), add(L, 1)
require(scale(lm1, w) == vadd(scale(den1, A), scale(lm1, vsub(d, A))), 'first collision formal identity')
C = vsub(vadd(A, d), xi)
require(scale(L, w) == vadd(scale(den2, C), scale(L, xi)), 'second collision formal identity')
require(w == vadd(C, d), 'terminal vertex formal identity')
require(sub(mul(L, den1), mul(lm1, den2)) == add(sub(mul(L, L), L), 1), 'positive collision difference numerator')
require(matvec(T, vsub(xi, eta)) != w, 'negative control wrong twist sign')
require(vadd(C, xi) != w, 'negative control wrong terminal endpoint')
require((Q(3), Q(4)) != tuple(sum(c * Q(3)**i for i, c in enumerate(x)) for x in w),
        'negative control wrong hexagon witness')


def determinant(u, v):
    return u[0] * v[1] - u[1] * v[0]


def reachable(p):
    a, b = p
    if a < 0 or b < 0 or (a + b) % 3 == 2 or a + b == 0:
        return False
    h = math.gcd(a, b)
    return h == 1 or h == 2 and (a + b) % 3 == 1


def vertices(u, v):
    return [(0, 0), v, (2*v[0]+u[0], 2*v[1]+u[1]),
            (2*v[0]+2*u[0], 2*v[1]+2*u[1]),
            (v[0]+2*u[0], v[1]+2*u[1]), u]


def interior_candidates(w):
    # Side positions are excluded by the all-hexagon coordinate-sum lemma;
    # middle position is impossible if a coordinate of w is odd. For positions
    # 2 and 4 positivity bounds both components of the doubled side by w/2.
    out, attempted = [], 0
    for index in [2, 4]:
        for a in range(w[0] // 2 + 1):
            for b in range(w[1] // 2 + 1):
                attempted += 1
                doubled, other = (a, b), (w[0]-2*a, w[1]-2*b)
                v, u = (doubled, other) if index == 2 else (other, doubled)
                if determinant(u, v) == 1:
                    out.append({'index': index, 'u': u, 'v': v,
                                'all_reachable': all(reachable(x) for x in vertices(u, v)[1:])})
    return out, attempted


# Exhaustive residue proof that both side endpoint sums must be 1 modulo 3:
# neither can be 2; reachability of the even middle point implies their sum 2.
require([(a, b) for a in [0, 1] for b in [0, 1] if (a + b) % 3 == 2] == [(1, 1)],
        'all-hexagon side-coordinate-sum lemma')
hex_results = []
for point, expected in [((5, 4), 0), ((4, 5), 0), ((1, 2), 1)]:
    require(reachable(point) and sum(point) % 3 == 0 and any(c % 2 for c in point), 'hexagon position exclusions ' + str(point))
    cand, count = interior_candidates(point)
    good = [x for x in cand if x['all_reachable']]
    require(len(good) == expected, 'complete hexagon obstruction ' + str(point))
    hex_results.append({'w': point, 'bounded_pairs': count, 'determinant_one_candidates': cand,
                        'reachable_polygon_count': len(good)})
require(not reachable((1, 1)) and not reachable((3, 2)), 'negative control determinant alone insufficient')
require(reachable((0, 1)) and reachable((1, 0)), 'nonempty hexagon positive control')

diagonal_count = 0
for n in range(5, 81):
    for k in range(n - 1):
        alpha, beta = Q(n-2-k, n), Q(n-k, n)
        j = (alpha + beta) * n / 2
        require(j.denominator == 1 and (n-1-int(j)) % (n-2) == k % (n-2), 'exact diagonal parity')
        require(beta - alpha == Q(2, n), 'shortcut overlap')
        diagonal_count += 1
    if n % 2:
        m = (n-1)//2
        require(all(Q(n-2*(k+1), n) < 0 for k in [m, m+1]), 'empty printed odd-index extras')
        require((2*n) * Q(n-2, n) == 2*(n-2), 'odd corner cycle')
    else:
        require(n * Q(n-2, n) == n-2, 'even corner cycles')

# These are floating-point diagnostics, explicitly not an all-n proof.
diagnostics, common = 0, 0
for n in list(range(5, 101)) + [257, 1000]:
    t = math.pi/n
    lam, S = 2*math.cos(t), math.sin(2*t)
    lengths = lambda k: math.sin((k+1)*t)/math.sin(t)
    require(abs((lam*lam-2)*math.sin(t) - (math.sin(3*t)-math.sin(t))) < 1e-12,
            'second-cylinder height diagnostic')
    eligible = [k for k in range(n-2) if math.cos((2*k+3)*t) >= math.cos(3*t)-1e-12]
    require(eligible == [0, n-3], 'D endpoint inequality diagnostic')
    for j in range(2, n):
        height = math.sin((j-1)*t)
        ell = lengths(j-1) + lengths(j-3)
        require(abs(ell/height - 2/math.tan(t)) < 1e-7, 'cylinder modulus diagnostic')
        diagnostics += 1
    for k in range(1, n-2):
        a = lengths(k)*math.sin((k+2)*t)/S
        b = lengths(k)*math.sin(k*t)/S
        c1, c2 = lam*lengths(k-1)/lengths(k), lam*lengths(k+1)/lengths(k)
        kap = math.sin(k*t)*math.sin((k+2)*t)/math.sin(t)**2
        require(abs(a*c1-kap) < 1e-6 and abs(b*c2-kap) < 1e-6 and kap > 1,
                'common-integer coefficient diagnostic')
        common += 1

print(json.dumps({'status':'PASS', 'evidence_checks_including_member_checks': len(checks),
                  'formal_polynomial_identities': 9,
                  'exact_n6_results': hex_results,
                  'exact_diagonal_cases': diagonal_count,
                  'finite_cylinder_diagnostics': diagnostics,
                  'finite_common_integer_diagnostics': common,
                  'scope':'Read-only evidence and exact finite/algebraic controls; not a proof assistant, author-code rerun, full priority certification, or all-n enumeration.'},
                 indent=2, sort_keys=True))

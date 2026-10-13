#!/usr/bin/env python3
"""Independent standard-library audit. Never writes in the author directory.
Usage: python3 audit_controls.py [author_public_directory]
Output: audit_controls.json beside this script. No network or source PDFs needed.
The checks validate bounded algebra and frozen bytes, not geometric theorems.
"""
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

PIN = '089b4bef99b12d6ba3d41149f21282fe8d569d4b46f3c1a4b3ab8b0e29740a3a'
EXPECTED_FILES = ['README.md', 'PROOF.md', 'RESEARCH_LOG.md', 'SOURCE_GATE.md',
                  'check_exact.py', 'exact_results.json']


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def det(matrix):
    """Rational Gaussian elimination; independent of permutation expansion."""
    a = [list(map(F, row)) for row in matrix]
    n = len(a)
    result = F(1)
    for j in range(n):
        pivot = next((i for i in range(j, n) if a[i][j]), None)
        if pivot is None:
            return F(0)
        if pivot != j:
            a[j], a[pivot] = a[pivot], a[j]
            result *= -1
        q = a[j][j]
        result *= q
        for i in range(j + 1, n):
            ratio = a[i][j] / q
            for k in range(j + 1, n):
                a[i][k] -= ratio * a[j][k]
            a[i][j] = 0
    return result


def times(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def ident(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def det_shift(a, t):
    return det([[t*int(i == j) - a[i][j] for j in range(len(a))]
                for i in range(len(a))])


def poly_trim(p):
    p = list(map(F, p))
    while len(p) > 1 and p[0] == 0:
        p.pop(0)
    return p


def evaluate(p, x):
    value = F(0)
    for c in p:
        value = value*x + c
    return value


def remainder(a, b):
    a, b = poly_trim(a), poly_trim(b)
    while len(a) >= len(b) and any(a):
        q = a[0] / b[0]
        for j in range(len(b)):
            a[j] -= q*b[j]
        a = poly_trim(a)
    return a


def sturm(p):
    p = poly_trim(p)
    q = [c*(len(p)-i-1) for i, c in enumerate(p[:-1])]
    sequence = [p, q]
    while any(sequence[-1]):
        r = [-c for c in remainder(sequence[-2], sequence[-1])]
        if not any(r):
            break
        sequence.append(r)
    return sequence


def variations(seq, x):
    signs = [(v > 0) - (v < 0) for p in seq if (v := evaluate(p, x))]
    return sum(a != b for a, b in zip(signs, signs[1:]))


def roots_between(p, lo, hi):
    require(evaluate(p, lo) != 0 and evaluate(p, hi) != 0, 'root on interval boundary')
    seq = sturm(p)
    return variations(seq, lo) - variations(seq, hi)


def cyc(a):
    """Z[C7]/(1+z+...+z^6): canonical 7-vector with last coordinate zero."""
    return tuple(x-a[6] for x in a)


def cadd(a, b):
    return cyc([x+y for x, y in zip(a, b)])


def cmul(a, b):
    return cyc([sum(a[i]*b[(k-i) % 7] for i in range(7)) for k in range(7)])


def constant(n):
    return (n, 0, 0, 0, 0, 0, 0)


def monomial(k):
    return cyc([int(i == k % 7) for i in range(7)])


def cmatrix(a):
    columns = [cmul(a, monomial(k))[:6] for k in range(6)]
    return [list(row) for row in zip(*columns)]


def validate_author_result(result):
    family = result['matrix_family']
    require([r['m'] for r in family] == list(range(3, 101)), 'matrix coverage mismatch')
    for row in family:
        m = row['m']
        require(row['determinant'] == -1, 'determinant sign mismatch')
        require(row['characteristic_ascending'] == [1, -m, 0, 1], 'characteristic mismatch')
        require(row['root_brackets'] == [[-m-1, -1], [0, 1], [1, m+1]], 'brackets mismatch')
        require(row['endpoint_signs'] == [[-1, 1], [1, -1], [-1, 1]], 'signs mismatch')
    x = result['x7']
    require(x['cyclotomic_polynomial_ascending'] == [1]*7, 'Phi7 mismatch')
    require(x['unit_inverse_product_mod_phi7'] == [1], 'unit inverse mismatch')
    require(x['squared_modulus_elementary_symmetric_values'] == [5, 6, 1], 'symmetric values mismatch')
    require(x['squared_modulus_polynomial_ascending'] == [-1, 6, -5, 1], 'X7 polynomial mismatch')
    require(x['ascending_root_brackets'] == [['1/8', '1/4'], ['3/2', '8/5'], ['16/5', '13/4']], 'X7 brackets mismatch')
    require(x['endpoint_signs'] == [[-1, 1], [1, -1], [-1, 1]], 'X7 signs mismatch')
    require(x['degree_relation'] == 'd1=a, d2=a*b=1/c>d1>1', 'X7 degree direction mismatch')
    require(result['rank_two_cubic_absolute_weight_exponents'] == [-3, -1, 1, 3], 'cubic weights mismatch')
    require(result['scalar_orders_preserving_three_form'] == [3], 'scalar order mismatch')
    require(result['invariant_h21_weights_on_cover_only'] == {
        '3': [1]*9, '7': [2, 1, 6, 4, 3, 1, 5, 4, 2]}, 'cover H21 weights mismatch')


def main():
    author = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent/'public'
    manifest_path = author/'FROZEN_AUTHOR_MANIFEST.json'
    require(sha(manifest_path) == PIN, 'wrong frozen manifest')
    manifest = json.loads(manifest_path.read_text())
    require([x['path'] for x in manifest['public_allowlist']] == EXPECTED_FILES, 'unexpected allowlist')
    require(manifest['attempts'] == 5 and manifest['status'] == 'unresolved_exhausted', 'wrong disposition')
    require(manifest['full_target_solved'] is False and manifest['novelty_claim'] is False, 'unsupported promotion')
    before = {item['path']: sha(author/item['path']) for item in manifest['public_allowlist']}
    for item in manifest['public_allowlist']:
        file = author/item['path']
        require(file.stat().st_size == item['bytes'], 'byte length mismatch: '+item['path'])
        require(before[item['path']] == item['sha256'], 'hash mismatch: '+item['path'])
    recorded = json.loads((author/'exact_results.json').read_text())
    validate_author_result(recorded)
    with tempfile.TemporaryDirectory(prefix='cy-audit-') as tmp:
        checker = Path(tmp)/'check_exact.py'
        shutil.copyfile(author/'check_exact.py', checker)
        run = subprocess.run([sys.executable, '-B', str(checker)], cwd=tmp,
                             text=True, capture_output=True, check=True, timeout=60)
        replay = Path(tmp)/'exact_results.json'
        require(replay.read_bytes() == (author/'exact_results.json').read_bytes(), 'replay differs')
        replay_summary = json.loads(run.stdout)

    rows = []
    for m in range(3, 101):
        p = [[0, 1, 0], [0, 0, 1], [-1, m, 0]]
        q = [[m, 0, -1], [1, 0, 0], [0, 1, 0]]
        require(det(p) == -1, 'independent determinant failure')
        require(times(p, q) == times(q, p) == ident(3), 'independent inverse failure')
        # Four exact evaluations identify the degree-three characteristic polynomial.
        for t in (-2, 0, 1, 3):
            require(det_shift(p, t) == t**3-m*t+1, 'independent characteristic failure')
        p3 = times(times(p, p), p)
        require([[p3[i][j]-m*p[i][j]+int(i == j) for j in range(3)] for i in range(3)] == [[0]*3 for _ in range(3)], 'Cayley-Hamilton failure')
        root_counts = [roots_between([1, 0, -m, 1], lo, hi) for lo, hi in [(-m-1, -1), (0, 1), (1, m+1)]]
        require(root_counts == [1, 1, 1], 'independent Sturm failure')
        rows.append({'m': m, 'determinant': -1, 'sturm_root_counts': root_counts})

    one = constant(1)
    unit = cadd(one, monomial(1))
    opposite_inverse = cadd(cadd(monomial(1), monomial(3)), monomial(5))
    inverse = tuple(-x for x in opposite_inverse)
    require(cmul(unit, inverse) == one, 'independent cyclotomic inverse failure')
    require(det(cmatrix(unit)) == 1, 'independent norm failure')
    w = [cadd(constant(2), cadd(monomial(k), monomial(-k))) for k in (1, 2, 4)]
    e1 = cadd(cadd(w[0], w[1]), w[2])
    e2 = cadd(cadd(cmul(w[0], w[1]), cmul(w[0], w[2])), cmul(w[1], w[2]))
    e3 = cmul(cmul(w[0], w[1]), w[2])
    require([e1, e2, e3] == [constant(5), constant(6), one], 'independent symmetric values failure')
    for x in w:
        require(cadd(cadd(cmul(cmul(x, x), x), tuple(-5*y for y in cmul(x, x))), cadd(tuple(6*y for y in x), constant(-1))) == constant(0), 'independent cubic failure')
        # A degree-six characteristic identity follows from seven distinct exact evaluations.
        for t in range(7):
            require(det_shift(cmatrix(x), t) == (t**3-5*t*t+6*t-1)**2, 'independent regular-representation failure')
    brackets = [(F(1, 8), F(1, 4)), (F(3, 2), F(8, 5)), (F(16, 5), F(13, 4))]
    require([roots_between([1, -5, 6, -1], a, b) for a, b in brackets] == [1, 1, 1], 'X7 Sturm failure')
    require(brackets[0][1] < 1 < brackets[1][0] < brackets[1][1] < brackets[2][0], 'X7 degree separation failure')

    negative_controls = []
    for label, mutate in [
        ('determinant_plus_one', lambda r: r['matrix_family'][0].update(determinant=1)),
        ('wrong_matrix_polynomial', lambda r: r['matrix_family'][3].update(characteristic_ascending=[-1, -6, 0, 1])),
        ('missing_matrix_instance', lambda r: r['matrix_family'].pop()),
        ('wrong_root_interval', lambda r: r['matrix_family'][0].update(root_brackets=[[-4, -1], [0, 2], [1, 4]])),
        ('wrong_x7_symmetric_values', lambda r: r['x7'].update(squared_modulus_elementary_symmetric_values=[5, 7, 1])),
        ('unsigned_x7_inverse', lambda r: r['x7'].update(unit_inverse_product_mod_phi7=[-1])),
        ('reversed_x7_degrees', lambda r: r['x7'].update(degree_relation='d1>d2>1')),
        ('even_dimensional_weights_substituted', lambda r: r.update(rank_two_cubic_absolute_weight_exponents=[-4, -2, 0, 2, 4])),
        ('extra_scalar_order', lambda r: r.update(scalar_orders_preserving_three_form=[3, 6])),
        ('cover_rigidity_weight_mutation', lambda r: r['invariant_h21_weights_on_cover_only']['7'].__setitem__(0, 0)),
    ]:
        bad = deepcopy(recorded)
        mutate(bad)
        try:
            validate_author_result(bad)
        except AssertionError:
            negative_controls.append(label)
        else:
            raise AssertionError('undetected mutation: '+label)
    # Algebra-level controls, separate from checking known output fields.
    require(cmul(unit, opposite_inverse) == constant(-1), 'missing inverse sign control ineffective')
    require(evaluate([1, 0, -2, 1], F(1)) == 0, 'm=2 boundary control ineffective')
    require(0 in [2*i-4 for i in range(5)] and 0 not in [2*i-3 for i in range(4)], 'odd dimension control ineffective')
    negative_controls.extend(['cyclotomic_wrong_inverse_gives_minus_one', 'm2_has_boundary_root', 'even_dimension_has_zero_weight'])
    after = {name: sha(author/name) for name in before}
    require(before == after and sha(manifest_path) == PIN, 'frozen bytes changed')
    extras = sorted(str(p.relative_to(author)) for p in author.rglob('*') if p.is_file()
                    and str(p.relative_to(author)) not in EXPECTED_FILES + ['FROZEN_AUTHOR_MANIFEST.json'])
    result = {
        'status': 'PASS_PARTIAL', 'full_target_solved': False, 'novelty_claim': False,
        'frozen_manifest_sha256': PIN, 'frozen_files_checked': 6,
        'frozen_files_unchanged': True, 'author_replay_byte_identical': True,
        'author_replay_summary': replay_summary, 'matrix_instances_independently_checked': len(rows),
        'matrix_checks': rows,
        'x7_controls': {'cyclotomic_inverse': 'verified in cyclic-group-ring quotient',
                        'unit_norm': 1, 'symmetric_values': [5, 6, 1],
                        'regular_representation_characteristic': '(t^3-5t^2+6t-1)^2',
                        'exact_sturm_root_counts': [1, 1, 1], 'degree_order': 'd2>d1>1'},
        'negative_controls_rejected_or_distinguished': negative_controls,
        'unallowlisted_author_files_excluded_from_publication': extras,
        'scope': 'Exact algebra and byte integrity only. Geometric hypotheses are reviewed in AUDIT_REPORT.md.'
    }
    output = Path(__file__).with_name('audit_controls.json')
    output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps({key: result[key] for key in ['status', 'matrix_instances_independently_checked',
          'author_replay_byte_identical', 'frozen_files_unchanged', 'negative_controls_rejected_or_distinguished']}, sort_keys=True))


if __name__ == '__main__':
    main()

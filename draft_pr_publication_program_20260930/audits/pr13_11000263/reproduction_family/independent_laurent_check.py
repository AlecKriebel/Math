#!/usr/bin/env python3
"""Independent exact sparse-vector checks from the defining presentation.

No candidate module is imported. Laurent-polynomial arithmetic is implemented
here with integer coefficients and exponent pairs (q exponent, u exponent).
Only scalar-factor controls use SymPy. Finite full-word checks support, but do
not replace, the support-based arbitrary-index proof recorded in REPORT.md.
"""
from fractions import Fraction
from datetime import datetime, timezone
from pathlib import Path
import json
import sympy as s

class Laurent:
    def __init__(self, terms=None):
        if isinstance(terms, int):
            terms = {(0, 0): terms}
        self.terms = {e: c for e, c in (terms or {}).items() if c}
    def __add__(self, other):
        other = poly(other)
        out = self.terms.copy()
        for e, c in other.terms.items():
            out[e] = out.get(e, 0)+c
        return Laurent(out)
    __radd__ = __add__
    def __neg__(self):
        return Laurent({e: -c for e, c in self.terms.items()})
    def __sub__(self, other):
        return self+-poly(other)
    def __rsub__(self, other):
        return poly(other)+-self
    def __mul__(self, other):
        other = poly(other)
        out = {}
        for (a, b), c in self.terms.items():
            for (d, e), f in other.terms.items():
                key = (a+d, b+e)
                out[key] = out.get(key, 0)+c*f
        return Laurent(out)
    __rmul__ = __mul__
    def __pow__(self, n):
        if n < 0:
            assert len(self.terms) == 1
            ((a, b), c), = self.terms.items()
            assert c in (-1, 1)
            return Laurent({(a*n, b*n): c**(-n)})
        out = poly(1)
        for unused in range(n):
            out = out*self
        return out
    def __eq__(self, other):
        return self.terms == poly(other).terms
    def __bool__(self):
        return bool(self.terms)
    def at(self, qvalue, uvalue):
        return sum((Fraction(c)*Fraction(qvalue)**a*Fraction(uvalue)**b
                    for (a, b), c in self.terms.items()), Fraction(0))
    def json(self):
        return [{'q_power': a, 'u_power': b, 'coefficient': c}
                for (a, b), c in sorted(self.terms.items())]

def poly(value):
    return value if isinstance(value, Laurent) else Laurent(value)

Q = Laurent({(1, 0): 1})
U = Laurent({(0, 1): 1})
ZERO = poly(0)

def basis(n, j):
    return tuple(poly(int(k == j)) for k in range(n))

def scale(c, vector):
    return tuple(c*x for x in vector)

def add(*vectors):
    return tuple(sum(entries, ZERO) for entries in zip(*vectors))

def minus(a, b):
    return add(a, scale(-1, b))

def generator(vector, i, inverse=False):
    """Apply the block on positions i,i+1; i is one-based."""
    out = list(vector)
    a, b = out[i-1:i+1]
    if inverse:
        out[i-1], out[i] = b, U**-1*a+(1-U**-1)*b
    else:
        out[i-1], out[i] = (1-U)*a+U*b, a
    return tuple(out)

def word(vector, indices, inverse=False):
    ids = tuple(indices)
    # W=B_i1...B_is acts right-to-left. W^-1 reverses factors and thus
    # acts with inverse blocks in the original listed order.
    for i in ids if inverse else reversed(ids):
        vector = generator(vector, i, inverse)
    return vector

def wrong_bar(vector, indices):
    for i in reversed(tuple(indices)):
        vector = generator(vector, i, True)
    return vector

def X2(vector):
    return add(scale(Q, generator(vector, 1, True)), scale(1-Q, vector),
               scale(-1, generator(vector, 1)))

def recurrence(vector, k):
    return minus(scale(Q**(k-1), word(vector, range(k-1, 0, -1), True)),
                 word(vector, range(1, k)))

def v(n, r):
    out = [ZERO]*n
    out[r-1], out[r] = U**(1-r), -U**(-r)
    return tuple(out)

checks = []
def equal(label, a, b):
    assert a == b, label
    checks.append(label)

def main():
    # Homogeneous local calculation: the amplitude may be arbitrary because
    # every operator is linear; translating the block preserves this identity.
    normalized = (poly(1), -U**-1, ZERO)
    equal('local inverse left', generator(generator(normalized, 1, True), 1), normalized)
    equal('local inverse right', generator(generator(normalized, 1), 1, True), normalized)
    equal('local forward two-block propagation', word(normalized, [1, 2]),
          (ZERO, poly(1), -U**-1))
    equal('local inverse two-block propagation', word(normalized, [2, 1], True),
          (ZERO, U**-1, -U**-2))
    exceptional_left = add(scale(Q, generator(normalized, 2, True)),
                           scale(1-Q, normalized), scale(-1, generator(normalized, 2)))
    exceptional_right = minus(scale(Q, word(normalized, [2, 1], True)),
                              word(normalized, [1, 2]))
    equal('local exceptional R2', exceptional_left, exceptional_right)
    equal('local exceptional R2 value', exceptional_left, scale(Q-U, v(3, 2)))
    inverse_wrong_detected = False
    relation_wrong_detected = False
    row_manifest = []
    all_x = {}
    for n in range(3, 13):
        columns = [basis(n, j) for j in range(n)]
        for i in range(1, n):
            for j, e in enumerate(columns):
                equal(f'm={n} generator {i} inverse left column {j}',
                      generator(generator(e, i, True), i), e)
                equal(f'm={n} generator {i} inverse right column {j}',
                      generator(generator(e, i), i, True), e)
                # This unintended additional kernel relation is allowed; the
                # witness need not be faithful to detect a nonzero element.
                equal(f'm={n} Burau quadratic column {j} generator {i}',
                      add(generator(generator(e, i), i),
                          scale(U-1, generator(e, i)), scale(-U, e)), tuple([ZERO]*n))
                if i < n-1:
                    equal(f'm={n} adjacent braid {i} column {j}',
                          word(e, [i, i+1, i]), word(e, [i+1, i, i+1]))
            for k in range(i+2, n):
                for j, e in enumerate(columns):
                    equal(f'm={n} distant commute {i},{k} column {j}',
                          word(e, [i, k]), word(e, [k, i]))
        for ids in ([2, 1], tuple(range(n-1, 0, -1)), tuple(range(1, n)), [1, 2]*3):
            for j, e in enumerate(columns):
                equal(f'm={n} whole-word inverse left {ids} column {j}',
                      word(word(e, ids, True), ids), e)
                equal(f'm={n} whole-word inverse right {ids} column {j}',
                      word(word(e, ids), ids, True), e)
                inverse_wrong_detected |= word(wrong_bar(e, ids), ids) != e
        images = {2: [X2(e) for e in columns]}
        coefficient = poly(1)
        for k in range(2, n+1):
            coefficient = coefficient*(Q**(k-1)-U)
            if k > 2:
                images[k] = [recurrence(e, k) for e in images[k-1]]
            for j in range(n):
                amplitude = -1 if j == 0 else 1 if j == 1 else 0
                equal(f'm={n} X{k} formula column {j}', images[k][j],
                      scale(coefficient*amplitude, v(n, k-1)))
        for j, e in enumerate(images[2]):
            left = add(scale(Q, generator(e, 2, True)), scale(1-Q, e),
                       scale(-1, generator(e, 2)))
            right = minus(scale(Q, word(e, [2, 1], True)), word(e, [1, 2]))
            equal(f'm={n} R2 column {j}', left, right)
            bad = minus(scale(Q, wrong_bar(e, [2, 1])), word(e, [1, 2]))
            relation_wrong_detected |= left != bad
        legal = [2]
        for k in range(3, n):
            legal.append(k)
            for j, e in enumerate(images[k]):
                left = minus(scale(Q**(k-1), word(e, range(k, 1, -1), True)),
                             word(e, range(2, k+1)))
                right = minus(scale(Q**(k-1), word(e, range(k, 0, -1), True)),
                              word(e, range(1, k+1)))
                equal(f'm={n} R{k} column {j}', left, right)
        row_manifest.append({'matrix_strands': n, 'A_n_parameter': n,
                             'A_n_rows_checked': legal,
                             'C_n_parameter': n-1 if n>=4 else None,
                             'C_n_rows_checked': legal if n>=4 else None})
        for j, e in enumerate(images[2]):
            equal(f'm={n} X2 twist column {j}', generator(e, 1), scale(-U, e))
        for j, e in enumerate(images[3]):
            equal(f'm={n} X3 central twist column {j}', word(e, [1, 2]*3), scale(U**3, e))
        all_x[n] = images
    assert inverse_wrong_detected and relation_wrong_detected
    checks.extend(['wrong inverse order detected by round-trip control',
                   'wrong inverse order detected by defining R2 control'])

    generic_entry = all_x[3][3][0][1]
    equal('generic X3 visible entry', generic_entry, -(Q-U)*(Q**2-U)*U**-1)
    assert generic_entry.terms[(0, 1)] == -1
    checks.append('nonzero entry has coefficient -1 at u')

    specializations = []
    for n in range(3, 8):
        for qvalue in [Fraction(-2), Fraction(-1), Fraction(0), Fraction(1), Fraction(2), Fraction(2, 3)]:
            values = {Fraction(-3), Fraction(-1), Fraction(1), Fraction(2), qvalue, qvalue**2, qvalue**3}
            for uvalue in sorted(values):
                if not uvalue:
                    continue
                mat3 = s.Matrix([[s.Rational(all_x[n][3][j][i].at(qvalue, uvalue))
                                  for j in range(n)] for i in range(n)])
                expected = 0 if uvalue in (qvalue, qvalue**2) else 1
                assert mat3.rank() == expected
                checks.append(f'm={n} specialized rank q={qvalue},u={uvalue}')
                rank4 = None
                if n >= 4:
                    mat4 = s.Matrix([[s.Rational(all_x[n][4][j][i].at(qvalue, uvalue))
                                      for j in range(n)] for i in range(n)])
                    rank4 = mat4.rank()
                    expected4 = 0 if uvalue in (qvalue, qvalue**2, qvalue**3) else 1
                    assert rank4 == expected4
                    checks.append(f'm={n} specialized X4 rank q={qvalue},u={uvalue}')
                specializations.append({'strands': n, 'q': str(qvalue), 'u': str(uvalue),
                                        'rank_X3': expected, 'rank_X4': rank4,
                                        'q_zero_outside_unit_q_source_scope': not bool(qvalue)})

    q, z = s.symbols('q z')
    x2 = q/z+1-q-z
    x3 = (q**2/z**2-z**2)*x2
    r2 = q/z+1-q-z-q/z**2+z**2
    r3 = q**2/z**2-z**2-q**2/z**3+z**3
    r4 = q**3/z**3-z**3-q**3/z**4+z**4
    scalar_factors = [('X2', x2, (1-z)*(z+q)/z),
                      ('X3', x3, (q**2-z**4)*(1-z)*(z+q)/z**3),
                      ('R2 coefficient', r2, (z**2-q)*(z**2-z+1)/z**2),
                      ('R3 coefficient', r3, (z-1)*(q**2+z**5)/z**3),
                      ('R4 coefficient', r4, (z-1)*(q**3+z**7)/z**4)]
    for label, raw, factored in scalar_factors:
        assert s.cancel(raw-factored) == 0, label
        checks.append('scalar '+label)
    # Polynomial remainder calculations avoid numerical roots of unity.
    phi6 = z**2-z+1
    assert s.rem(z**3+1, phi6, z) == 0
    assert s.rem(z**6-1, phi6, z) == 0
    assert s.rem(q**2+z**5, phi6, z) == q**2-z+1
    assert s.rem((q**2+z**5).subs(q,z), phi6, z) == 0
    assert s.cancel(x2.subs(q, -z)) == 0
    x4 = (q**3/z**3-z**3)*x3
    scalar_qz_r4 = s.cancel((r4*x4).subs(q,z))
    scalar_qz_r4_remainder = s.rem(s.fraction(scalar_qz_r4)[0], phi6, z)
    assert scalar_qz_r4_remainder != 0
    checks.extend(['primitive-sixth-root reductions', 'special q=-z kills X2',
                   'special q=z fails R4 with X4 nonzero'])

    out = {'status': 'passed', 'timestamp_utc': datetime.now(timezone.utc).isoformat(),
           'mechanism': 'integer-coefficient Laurent polynomials and sparse-vector actions',
           'sympy_version_for_scalar_controls': s.__version__, 'check_count': len(checks),
           'all_index_proof_mechanism': 'homogeneous translated three-coordinate identity and disjoint-support fixation; see REPORT.md',
           'finite_word_scope': 'm=3,...,12; all basis columns; every legal row; A_n through n=12 and C_n through n=11',
           'wrong_order_controls_detect_failure': True,
           'generic_X3_entry_expansion': generic_entry.json(),
           'row_manifest': row_manifest, 'specialization_case_count': len(specializations),
           'specializations': specializations,
           'scalar_factorizations': {name: str(s.factor(raw)) for name, raw, unused in scalar_factors},
           'scalar_q_equals_z_R4X4_numerator_remainder_mod_phi6': str(scalar_qz_r4_remainder),
           'not_proved_by_finite_checks': ['all strand counts', 'author-intended correction',
                                         'nonzero under every parameter specialization',
                                         'finite dimension of any universal quotient',
                                         'historical novelty or priority'],
           'checks': checks}
    Path(__file__).with_name('independent_laurent_receipt.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({key: value for key, value in out.items() if key not in ('checks', 'specializations')}, indent=2))

if __name__ == '__main__':
    main()

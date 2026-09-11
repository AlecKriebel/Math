#!/usr/bin/env python3
"""Replay the exact rational SOS certificate using only Python's standard library.

No floating-point arithmetic, SDP solver, or numerical eigenvalue test is used.
The independent target polynomial is fixed in this checker, not read from the
candidate certificate.  This checks identities in the *-algebra of two commuting
parties with self-adjoint involutive generators. It is NOT a Lean kernel check.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
from typing import Any

Word = tuple[tuple[int, ...], tuple[int, ...]]
Poly = dict[Word, F]
I: Word = ((), ())
A0: Word = ((0,), ())
A1: Word = ((1,), ())
A2: Word = ((2,), ())
B0: Word = ((), (0,))
B1: Word = ((), (1,))
WORDS = [I, A0, A1, A2, B0, B1,
         ((0,), (0,)), ((0,), (1,)), ((1,), (0,)), ((1,), (1,)),
         ((2,), (0,)), ((2,), (1,))]
BOUND = F(289, 10)


def require(p: bool, message: str) -> None:
    if not p:
        raise ValueError(message)


def reduce_word(w: tuple[int, ...]) -> tuple[int, ...]:
    result: list[int] = []
    for a in w:
        if result and result[-1] == a:
            result.pop()
        else:
            result.append(a)
    return tuple(result)


def word_mul(a: Word, b: Word) -> Word:
    return reduce_word(a[0] + b[0]), reduce_word(a[1] + b[1])


def word_star(a: Word) -> Word:
    return tuple(reversed(a[0])), tuple(reversed(a[1]))


def clean(p: Poly) -> Poly:
    return {w: c for w, c in p.items() if c}


def linear(*terms: tuple[F | int, Word]) -> Poly:
    p: Poly = defaultdict(F)
    for c, w in terms:
        p[w] += F(c)
    return clean(p)


def add(*polys: Poly) -> Poly:
    out: Poly = defaultdict(F)
    for p in polys:
        for w, c in p.items():
            out[w] += c
    return clean(out)


def scale(c: F | int, p: Poly) -> Poly:
    return clean({w: F(c)*v for w, v in p.items()})


def multiply(p: Poly, q: Poly) -> Poly:
    out: Poly = defaultdict(F)
    for u, a in p.items():
        for v, b in q.items():
            out[word_mul(u, v)] += a*b
    return clean(out)


def star(p: Poly) -> Poly:
    return {word_star(w): c for w, c in p.items()}


def square(p: Poly) -> Poly:
    return multiply(star(p), p)


def chsh(a0: Poly, a1: Poly, b0: Poly, b1: Poly) -> Poly:
    return add(multiply(a0, add(b0, b1)),
               multiply(a1, add(b0, scale(-1, b1))))


def bell02(a0: Poly, a1: Poly, a2: Poly, b0: Poly, b1: Poly) -> Poly:
    return add(linear((F(7,20), I)), scale(10, chsh(a0, a1, b0, b1)),
               scale(F(3,20), b0), scale(F(1,5), b1),
               scale(F(-1,20), a2), scale(F(3,20), multiply(a2,b0)),
               scale(F(-1,5), multiply(a2,b1)))


def parse_matrix(value: Any, n: int) -> list[list[F]]:
    require(isinstance(value, list) and len(value) == n, "matrix row count")
    require(all(isinstance(row, list) and len(row) == n for row in value), "matrix column count")
    return [[F(x) for x in row] for row in value]


def verify_certificate(data: dict[str, Any]) -> dict[str, Any]:
    require(F(data['bound']) == BOUND, "the certified bound must be exactly 289/10")
    require(F(data['bell_constant']) == F(7,20), "unexpected Bell constant")
    require([(tuple(w[0]), tuple(w[1])) for w in data['words']] == WORDS,
            "unexpected ordered monomial basis")
    n = len(WORDS)
    denominator = F(data['gram_common_denominator'])
    require(denominator > 0, "Gram denominator must be positive")
    numerator = parse_matrix(data['gram_integer_numerator'], n)
    require(all(x.denominator == 1 for row in numerator for x in row), "Gram numerator not integral")
    Q = [[x/denominator for x in row] for row in numerator]
    L = parse_matrix(data['ldl_unit_lower'], n)
    D = [F(x) for x in data['ldl_positive_diagonal']]
    require(len(D) == n, "diagonal length")
    require(all(x > 0 for x in D), "an LDL pivot is not positive")
    require(all(L[i][i] == 1 and all(L[i][j] == 0 for j in range(i+1,n)) for i in range(n)),
            "LDL factor is not unit lower triangular")
    require(all(Q[i][j] == Q[j][i] for i in range(n) for j in range(n)), "Gram symmetry")
    for i in range(n):
        for j in range(n):
            require(Q[i][j] == sum((L[i][k]*D[k]*L[j][k] for k in range(n)),F(0)),
                    f"LDL identity failed at ({i},{j})")

    a0,a1,a2,b0,b1 = [linear((1,w)) for w in (A0,A1,A2,B0,B1)]
    target = add(linear((BOUND,I)), scale(-1,bell02(a0,a1,a2,b0,b1)))
    gram: Poly = defaultdict(F)
    for i,u in enumerate(WORDS):
        for j,v in enumerate(WORDS):
            gram[word_mul(word_star(u),v)] += Q[i][j]
    all_word_keys = set(gram) | set(target)
    for w in all_word_keys:
        require(gram.get(w,F(0)) == target.get(w,F(0)), f"unreversed word coefficient failed: {w}")

    # Independently expand the twelve weighted squares, not just their Gram matrix.
    squares = add(*(scale(D[k], square(linear(*[(L[i][k], WORDS[i]) for i in range(n)])))
                    for k in range(n)))
    require(squares == target, "sum-of-squares identity failed")

    # {1,2} support: replace (A0,A1,B0) by (-A1,-A0,-B0).
    swapped_chsh = chsh(scale(-1,a1),scale(-1,a0),scale(-1,b0),b1)
    require(swapped_chsh == chsh(a0,a1,b0,b1), "support-12 CHSH substitution")
    expected12 = add(scale(10,chsh(a0,a1,b0,b1)),
                     scale(F(3,20),multiply(add(linear((1,I)),a2),add(linear((1,I)),scale(-1,b0)))),
                     scale(F(1,5),multiply(add(linear((1,I)),scale(-1,a2)),add(linear((1,I)),b1))))
    require(bell02(scale(-1,a1),scale(-1,a0),a2,scale(-1,b0),b1) == expected12,
            "support-12 full Bell substitution")

    # {0,1} support: a separate small exact rational SOS.
    bell01 = add(scale(10,chsh(a0,a1,b0,b1)),
                 linear((F(3,10),I)), scale(F(3,10),multiply(a2,b0)))
    residual01 = add(linear((BOUND,I)),scale(-1,bell01))
    sos01 = add(scale(F(25,7),square(add(scale(F(7,5),a0),scale(-1,b0),scale(-1,b1)))),
                scale(F(25,7),square(add(scale(F(7,5),a1),scale(-1,b0),b1))),
                scale(F(3,20),square(add(linear((1,I)),scale(-1,multiply(a2,b0))))),
                linear((F(1,70),I)))
    require(residual01 == sos01, "support-01 small SOS")

    # Rational comparisons which imply C < U < L0 after the separate real sqrt fact.
    sqrt_lower = F(707,500)
    require(sqrt_lower > 0 and sqrt_lower**2 < 2, "sqrt(2) lower comparison")
    lower_witness_margin = 20*sqrt_lower + F(16,25) - BOUND
    lower_paper_upper_margin = (5003*sqrt_lower + 154)/250 - BOUND
    require(lower_witness_margin > 0, "rational bound not strictly below witness")
    require(lower_paper_upper_margin > 0, "rational bound not below paper U")
    return {
        'passed': True, 'arithmetic': 'fractions.Fraction only',
        'lean_kernel_checked': False,
        'gram_shape': [n,n], 'positive_ldl_pivots': n,
        'exact_ldl_entry_equalities': n*n,
        'exact_unreversed_word_coefficients': len(all_word_keys),
        'weighted_square_expansion': 'passed',
        'all_three_auxiliary_support_pairs': 'exact algebra passed',
        'certified_rational_bound': str(BOUND),
        'rational_sqrt2_lower': str(sqrt_lower),
        'witness_margin_lower_bound': str(lower_witness_margin),
        'paper_U_minus_bound_lower_bound': str(lower_paper_upper_margin),
        'scope': ('A finite universal noncommutative identity with positive rational square weights; '
                  'the state, qubit PVM support, and Born-rule bridges are separate mathematical proofs.')
    }


def mutation_tests(data: dict[str, Any]) -> int:
    failures = 0
    for mut in range(5):
        changed = copy.deepcopy(data)
        if mut == 0:
            changed['gram_integer_numerator'][0][0] += 1
        elif mut == 1:
            changed['ldl_positive_diagonal'][0] = '-1'
        elif mut == 2:
            changed['bound'] = '288/10'
        elif mut == 3:
            changed['words'][1],changed['words'][2] = changed['words'][2],changed['words'][1]
        else:
            changed['ldl_unit_lower'][3][0] = '0'
        try:
            verify_certificate(changed)
        except (ValueError, ZeroDivisionError, KeyError):
            failures += 1
        else:
            raise AssertionError(f'corrupted certificate {mut} was accepted')
    return failures


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--certificate', type=Path, default=root/'certificates/binary_pair_sos.json')
    ap.add_argument('--report', type=Path, default=root/'reports/sos_exact_checks.json')
    args = ap.parse_args()
    raw = args.certificate.read_bytes()
    data = json.loads(raw)
    report = verify_certificate(data)
    report['rejected_corrupted_certificates'] = mutation_tests(data)
    report['certificate_sha256'] = hashlib.sha256(raw).hexdigest()
    report['checker_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()

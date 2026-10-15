#!/usr/bin/env python3
"""Independent B3 normal-form and projective-action controls, standard library only.

This is a reproducible implementation consistency audit, not a finite-search proof
of faithfulness. The universal proof is in EARLY_SEAL.md and REPORT.md. No n>=4
braid representation or new proof-search attempt is performed here.
"""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import platform

I = (1, 0, 0, 1)
U = (1, 1, 0, 1)
V = (1, 0, -1, 1)
checks = Counter()


def check(category, condition):
    if not condition:
        raise AssertionError(category)
    checks[category] += 1


def mul(m, n):
    a, b, c, d = m
    e, f, g, h = n
    return (a*e+b*g, a*f+b*h, c*e+d*g, c*f+d*h)


def det(m):
    a, b, c, d = m
    return a*d-b*c


def scale(c, m):
    return tuple(c*t for t in m)


def inv(m):
    a, b, c, d = m
    k = F(1, det(m))
    return (k*d, -k*b, -k*c, k*a)


def power(m, n):
    if n < 0:
        return power(inv(m), -n)
    out = I
    while n:
        if n & 1:
            out = mul(out, m)
        m = mul(m, m)
        n //= 2
    return out


S = mul(mul(U, V), U)
R = mul(U, V)
MATRIX = {1: U, 2: V, -1: inv(U), -2: inv(V)}
ORDER = {'A': 2, 'B': 3}
WEIGHT = {'A': 3, 'B': 2}
# x=B^-1 A, y=A^-1 B^2, x^-1=A^-1 B, y^-1=B^-2 A.
# Negative factor powers are written as z^-1 times their positive remainder.
LETTER_NF = {
    1: (-1, (('B', 2), ('A', 1))),
    2: (-1, (('A', 1), ('B', 2))),
    -1: (-1, (('A', 1), ('B', 1))),
    -2: (-1, (('B', 1), ('A', 1))),
}


def combine(left, right):
    """Multiply z^k times alternating A/B remainders; carries are central."""
    k = left[0] + right[0]
    stack = list(left[1])
    for factor, exp in right[1]:
        if stack and stack[-1][0] == factor:
            exp += stack.pop()[1]
        carry, rem = divmod(exp, ORDER[factor])
        k += carry
        if rem:
            stack.append((factor, rem))
    return k, tuple(stack)


def nf(word):
    out = (0, ())
    for letter in word:
        out = combine(out, LETTER_NF[letter])
    return out


def nf_power(normal, n):
    out = (0, ())
    for _ in range(n):
        out = combine(out, normal)
    return out


def quotient_reduce(syllables):
    return combine((0, ()), (0, tuple(syllables)))[1]


def nf_exponent(normal):
    return 6*normal[0] + sum(WEIGHT[f]*p for f, p in normal[1])


def qmatrix(syllables):
    out = I
    for factor, exp in syllables:
        out = mul(out, power(S if factor == 'A' else R, exp))
    return out


def nf_matrix(normal):
    return scale(-1 if normal[0] % 2 else 1, qmatrix(normal[1]))


def word_matrix(word):
    out = I
    for letter in word:
        out = mul(out, MATRIX[letter])
    return out


def exponent(word):
    return sum(1 if i > 0 else -1 for i in word)


def inverse_word(word):
    return tuple(-i for i in reversed(word))


def braid_power(word, n):
    return tuple(word)*n if n >= 0 else inverse_word(word)*(-n)


def rho(word, c=F(2)):
    return scale(c**exponent(word), word_matrix(word))


def projective_key(m):
    # For a determinant-one matrix, its sign is the only ambiguity in PSL2.
    first = next(t for t in m if t)
    return m if first > 0 else scale(-1, m)


def act(m, t):
    a, b, c, d = m
    if c*t+d == 0:
        return None
    return F(a*t+b, c*t+d)


def word_stream(max_length):
    """All freely reduced x,y words; different words may be the same braid."""
    yield ()
    def extend(prefix, last, remaining):
        if not remaining:
            yield prefix
        else:
            for i in (1, 2, -1, -2):
                if i != -last:
                    yield from extend(prefix+(i,), i, remaining-1)
    for length in range(1, max_length+1):
        for first in (1, 2, -1, -2):
            yield from extend((first,), first, length-1)


def quotient_stream(max_syllables):
    for length in range(1, max_syllables+1):
        for first in ('A', 'B'):
            factors = [first if i % 2 == 0 else ('B' if first == 'A' else 'A')
                       for i in range(length)]
            choices = [(1,) if f == 'A' else (1, 2) for f in factors]
            for exps in product(*choices):
                yield tuple(zip(factors, exps))


def commutation_rows(C):
    rows = []
    for index in range(4):
        unit = tuple(1 if j == index else 0 for j in range(4))
        left, right = mul(unit, C), mul(C, unit)
        rows.append(tuple(a-b for a, b in zip(left, right)))
    return [list(r) for r in zip(*rows)]


def nullspace(rows):
    matrix = [[F(x) for x in row] for row in rows]
    pivots = []
    current = 0
    for col in range(4):
        pivot = next((r for r in range(current, len(matrix)) if matrix[r][col]), None)
        if pivot is None:
            continue
        matrix[current], matrix[pivot] = matrix[pivot], matrix[current]
        divisor = matrix[current][col]
        matrix[current] = [x/divisor for x in matrix[current]]
        for r in range(len(matrix)):
            if r != current and matrix[r][col]:
                scalar = matrix[r][col]
                matrix[r] = [a-scalar*b for a, b in zip(matrix[r], matrix[current])]
        pivots.append(col)
        current += 1
    basis = []
    for col in range(4):
        if col not in pivots:
            v = [F(0)]*4
            v[col] = F(1)
            for r, pivot in enumerate(pivots):
                v[pivot] = -matrix[r][col]
            basis.append(tuple(v))
    return basis


def json_matrix(m):
    return [[str(m[0]), str(m[1])], [str(m[2]), str(m[3])]]


def main():
    started = datetime.now(timezone.utc).isoformat()
    check('braid_relations', mul(mul(U, V), U) == mul(mul(V, U), V))
    check('presentation_matrix_orders', power(S, 2) == power(R, 3) == scale(-1, I))
    check('presentation_inverse_substitutions', mul(inv(R), S) == U)
    check('presentation_inverse_substitutions', mul(inv(S), power(R, 2)) == V)
    check('noncommuting_generators', mul(U, V) != mul(V, U))
    for word in [(1,2,1), (2,1,2)]:
        check('presentation_normal_forms', nf(word) == (0, (('A',1),)))
    z = (1,2)*3
    check('center_normal_form', nf(z) == (1, ()))
    check('untwisted_center_sign', word_matrix(z) == scale(-1, I))
    check('twisted_center_scale', rho(z) == scale(-64, I))
    check('integral_group_boundary', det(rho((1,))) == 4)
    check('integral_group_boundary', any(F(t).denominator != 1 for t in inv(rho((1,)))))

    central_summary = []
    for c in [F(1),F(-1),F(2),F(-2),F(1,2)]:
        gamma = -c**6
        for k in range(-12, 13):
            word = braid_power(z,k)
            check('negative_and_positive_center_powers', rho(word,c) == scale(gamma**k,I))
            expected = (k % 2 == 0) if abs(c) == 1 else (k == 0)
            check('center_detection_or_deliberate_kernel', (rho(word,c) == I) == expected)
        central_summary.append({'c':str(c),'central_image':str(gamma),
                                'center_z_squared_killed':rho(z+z,c)==I})

    # Universal proof supplies completeness; these checks audit the implementation.
    count = 0
    seen = {}
    for word in word_stream(9):
        count += 1
        normal, m, e = nf(word), word_matrix(word), exponent(word)
        check('word_normal_form_exponent', nf_exponent(normal) == e)
        check('word_normal_form_matrix', nf_matrix(normal) == m)
        check('exact_number_types', all(isinstance(t,(int,F)) for t in nf_matrix(normal)))
        check('word_projective_kernel', (projective_key(m)==I) == (normal[1] == ()))
        check('word_untwisted_kernel', (m==I) == (normal[1]==() and normal[0]%2==0))
        check('word_twisted_identity', (rho(word)==I) == (normal==(0,())))
        check('word_twisted_determinant', det(rho(word)) == F(4)**e)
        key = (projective_key(m),e)
        check('projective_and_exact_exponent_collision_control', key not in seen or seen[key]==normal)
        seen[key] = normal
    check('enumeration_count', count == 1+2*(3**9-1))

    # Ping-pong witness algorithm checks the mechanism, including even words.
    qcount = 0
    even_conjugations = 0
    for syllables in quotient_stream(12):
        qcount += 1
        check('quotient_nonempty_matrix_nonidentity', projective_key(qmatrix(syllables)) != I)
        witness_word = syllables
        if len(syllables)%2 == 0:
            if syllables[0][0] == 'B':
                witness_word = syllables[1:]+syllables[:1]
            r = witness_word[-1][1]
            t = 3-r
            witness_word = quotient_reduce((('B',t),)+witness_word+(('B',-t),))
            even_conjugations += 1
            check('even_word_conjugation_shape', len(witness_word)%2==1 and
                  witness_word[0][0]==witness_word[-1][0]=='B')
        factor = witness_word[0][0]
        t = F(1) if factor == 'A' else F(-1)
        result = act(qmatrix(witness_word),t)
        check('ping_pong_projective_witness', result is not None and result*t < 0)
    for t in [F(-17,3),F(-1),F(-1,7)]:
        check('ping_pong_domain_partition', 0 < act(R,t) < 1 < act(power(R,2),t))
    for t in [F(1,7),F(1),F(17,3)]:
        check('ping_pong_domain_partition', act(S,t)<0)

    # Five intentionally insufficient/incorrect constructions must be rejected.
    commutator = (1,2,-1,-2)
    check('determinant_only_mutant_rejected', exponent(commutator)==0 and
          det(rho(commutator))==1 and rho(commutator)!=I)
    check('projective_only_mutant_rejected', projective_key(word_matrix(z))==I and rho(z)!=I)
    check('exponent_mod_six_mutant_rejected', exponent(z)%6==0 and nf(z)!=(0,()))
    sample = (1,-2,1)
    check('same_projective_image_exponent_ambiguity',
          projective_key(word_matrix(sample))==projective_key(word_matrix(sample+z)) and
          exponent(sample+z)-exponent(sample)==6 and rho(sample+z)!=rho(sample))
    check('untwisted_plus_minus_identity_mutant_rejected',
          word_matrix(z)==scale(-1,I) and word_matrix(z+z)==I and nf(z+z)!=(0,()))
    a,b = scale(2,U),scale(3,V)
    check('unequal_generator_scale_mutant_rejected', mul(mul(a,b),a)!=mul(mul(b,a),b))
    for c in [F(1),F(-1)]:
        check('root_of_unity_twist_mutant_rejected', rho(z+z,c)==I and nf(z+z)!=(0,()))

    # Centralizer controls are independent linear algebra over rational numbers.
    centralizers = []
    for name,C in [('nonsplit',(0,2,1,0)),('Jordan',(1,1,0,1)),
                   ('split',(2,0,0,3)),('det_minus_one',(0,1,1,0)),
                   ('hyperbolic_unimodular',(2,1,1,1)),('scaled_Jordan',(2,1,0,2))]:
        basis = nullspace(commutation_rows(C))
        check('nonscalar_centralizer_dimension', len(basis)==2)
        for b in basis:
            check('nonscalar_centralizer_equations', mul(b,C)==mul(C,b))
        for b1,b2 in product(basis,repeat=2):
            check('nonscalar_centralizer_commutativity', mul(b1,b2)==mul(b2,b1))
        # I and C are independent precisely because C is nonscalar.
        check('centralizer_polynomial_basis', C[1]!=0 or C[2]!=0 or C[0]!=C[3])
        centralizers.append({'type':name,'C':json_matrix(C),'dimension':len(basis)})
    check('scalar_centralizer_exception', len(nullspace(commutation_rows(scale(2,I))))==4)
    check('scalar_centralizer_exception', mul(U,V)!=mul(V,U))
    for integer in range(-7,8):
        check('integral_scalar_units', (abs(det(scale(integer,I)))==1)==(abs(integer)==1))
    check('rational_scalar_infinite_center_exception', power(scale(-64,I),2)!=I)

    finite_fields = []
    check('characteristic_two_twist_singular', det(scale(2,U))%2 == 0)
    for p in [3,5,7,11]:
        degree = p*(p-1)
        word = (1,)*degree
        reduced = tuple(int(t%p) for t in rho(word))
        check('finite_field_deliberate_kernel', reduced==I and nf(word)!=(0,()))
        finite_fields.append({'prime':p,'kernel_word':'sigma1^'+str(degree),
                              'integer_exponent':degree,'matrix_mod_p':list(reduced)})

    # Projective torsion lift checks never assume B3 is torsion-free.
    for normal in [(0,(('A',1),)),(0,(('B',1),)),(0,(('B',2),))]:
        degree = 2 if normal[1][0][0]=='A' else 3
        lifted = nf_power(normal,degree)
        check('projective_torsion_lift', lifted[1]==() and lifted[0]!=0)
    check('n1_trivial_case', I==power(I,1))
    for k in range(-20,21):
        check('n2_infinite_cyclic_detection', (F(2)**k==1)==(k==0))

    receipt = {
        'status':'PASS','started_utc':started,
        'finished_utc':datetime.now(timezone.utc).isoformat(),
        'python_version':platform.python_version(),
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'assertions':sum(checks.values()),'checks_by_category':dict(checks),
        'freely_reduced_braid_words':count,'maximum_braid_word_length':9,
        'distinct_projective_exponent_pairs':len(seen),
        'reduced_quotient_words':qcount,'maximum_quotient_syllables':12,
        'even_word_conjugation_witnesses':even_conjugations,
        'twist_controls':central_summary,'centralizer_controls':centralizers,
        'finite_field_controls':finite_fields,
        'sample_commutator':{'word':[1,2,-1,-2],'e':0,'matrix':json_matrix(rho(commutator))},
        'scope':'New implementation consistency checks for the sealed universal B3 proof. Bounded enumeration is not a faithfulness proof. No n>=4 search or all-n conclusion.',
        'defective_mechanisms_detected':['determinant alone','projectivization alone',
             'exponent modulo six','untwisted central kernel','root-of-unity twists',
             'unequal generator scales','finite-field reduction','scalar centralizer exception'],
    }
    Path(__file__).with_name('modular_results.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:receipt[k] for k in ('status','assertions','freely_reduced_braid_words',
          'reduced_quotient_words','even_word_conjugation_witnesses','script_sha256')},indent=2))


if __name__ == '__main__':
    main()

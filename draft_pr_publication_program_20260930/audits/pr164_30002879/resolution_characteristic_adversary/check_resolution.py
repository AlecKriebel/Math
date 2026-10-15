#!/usr/bin/env python3
"""Independent bounded diagnostics; the universal proof is FIRST_ASSESSMENT.md.

No `assert` is a correctness gate. Every failed check raises DiagnosticFailure
in ordinary and optimized Python. This program does not read author code or
third-party full texts. Matrices are constructed from elementary multiplication.
"""
import argparse
import itertools
import json
import math
import sys


class DiagnosticFailure(Exception):
    pass


CHECKS = 0
DETAILS = {}


def require(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise DiagnosticFailure(message)


def amul(a, b):
    """Basis 1,x,y,xy encoded by squarefree exponent masks 0,1,2,3."""
    return None if a & b else a | b


def rank2(columns):
    pivots = {}
    for column in columns:
        while column:
            pivot = column.bit_length() - 1
            if pivot in pivots:
                column ^= pivots[pivot]
            else:
                pivots[pivot] = column
                break
    return len(pivots)


def apply(columns, vector):
    result = 0
    while vector:
        bit = vector & -vector
        result ^= columns[bit.bit_length() - 1]
        vector ^= bit
    return result


def complex_check(matrices, dimensions, augmented_rank, label):
    require(rank2(matrices[0]) == augmented_rank, label + ': augmentation is onto')
    ranks = [rank2(d) for d in matrices]
    for n in range(1, len(matrices)):
        require(all(apply(matrices[n-1], c) == 0 for c in matrices[n]),
                label + ': differential square/augmentation vanishes at ' + str(n))
        require(dimensions[n-1] - ranks[n-1] == ranks[n],
                label + ': exactness at ' + str(n-1))
    return ranks


def ae_multiply(mask, generator, right=False):
    return amul(mask, generator << (2 if right else 0))


def bimodule_matrix(n):
    if n == 0:
        return [0 if amul(a & 3, a >> 2) is None
                else 1 << amul(a & 3, a >> 2) for a in range(16)]
    columns = []
    for i in range(n+1):
        j = n-i
        for a in range(16):
            column = 0
            for present, index, variable in [(i, i-1, 1), (j, i, 2)]:
                if present:
                    for right in [False, True]:
                        b = ae_multiply(a, variable, right)
                        if b is not None:
                            column ^= 1 << (16*index+b)
            columns.append(column)
    return columns


def module_action(a, m, mutation):
    if a == 0:
        return m
    if a == 3:
        return None
    if mutation == 'trivial_module':
        return None
    regular_variable = 2 if mutation == 'swapped_module' else 1
    return 1 if a == regular_variable and m == 0 else None


def tensor_matrix(n, mutation):
    if n == 0:
        return [0 if module_action(a, m, mutation) is None
                else 1 << module_action(a, m, mutation)
                for a in range(4) for m in range(2)]
    columns = []
    for i in range(n+1):
        j = n-i
        for a in range(4):
            for m in range(2):
                column = 0
                for present, index, variable in [(i, i-1, 1), (j, i, 2)]:
                    if not present:
                        continue
                    b = amul(a, variable)
                    if b is not None:
                        column ^= 1 << (8*index+2*b+m)
                    b = module_action(variable, m, mutation)
                    if b is not None and not (mutation == 'omit_x_right' and variable == 1):
                        column ^= 1 << (8*index+2*a+b)
                columns.append(column)
    return columns


def q_matrix(n, mutation):
    if n == 0:
        return [0 if module_action(a, 0, mutation) is None
                else 1 << module_action(a, 0, mutation) for a in range(4)]
    return [0 if amul(a, 2) is None else 1 << amul(a, 2) for a in range(4)]


def comparison(n, mutation):
    # A-linear map 1 -> e_(0,n) tensor 1_M, including the coefficient a.
    scale = 0 if mutation == 'zero_high_comparison' and n >= 2 else 1
    return [scale << (2*a) for a in range(4)]


def cochain_on_tensor(n, summand_i, coefficient, vector, mutation):
    result = 0
    while vector:
        bit = vector & -vector
        index = bit.bit_length()-1
        i, remainder = divmod(index, 8)
        a, m = divmod(remainder, 2)
        if i == summand_i:
            product = amul(coefficient, a)
            action = None if product is None else module_action(product, m, mutation)
            if action is not None:
                result ^= 1 << action
        vector ^= bit
    return result


def xor_term(vector, key):
    if key in vector:
        vector.remove(key)
    else:
        vector.add(key)


def shuffle(i, j, mutation='none', left=0, right=0):
    n = i+j
    scale = math.factorial(n) % 2 if mutation == 'factorial_shuffle' else 1
    vector = set()
    if not scale:
        return vector
    for positions in itertools.combinations(range(n), i):
        chosen = set(positions)
        word = tuple(1 if k in chosen else 2 for k in range(n))
        xor_term(vector, (left, word, right))
    return vector


def bar_differential(vector):
    result = set()
    for left, word, right in vector:
        if not word:
            continue
        product = amul(left, word[0])
        if product is not None:
            xor_term(result, (product, word[1:], right))
        for k in range(len(word)-1):
            product = amul(word[k], word[k+1])
            if product is not None:
                xor_term(result, (left, word[:k]+(product,)+word[k+2:], right))
        product = amul(word[-1], right)
        if product is not None:
            xor_term(result, (left, word[:-1], product))
    return result


def shuffle_of_periodic_d(i, j, mutation):
    result = set()
    for present, next_i, next_j, variable in [(i, i-1, j, 1), (j, i, j-1, 2)]:
        if present:
            for term in shuffle(next_i, next_j, mutation, left=variable):
                xor_term(result, term)
            for term in shuffle(next_i, next_j, mutation, right=variable):
                xor_term(result, term)
    return result


def a_words(n):
    return list(itertools.product((1, 2, 3), repeat=n))


def cochain_basis(n, kind='B'):
    if n == 0:
        return ([('A', (), a) for a in range(4)] if kind != 'I' else []) + (
            [('K', (), 0)] if kind != 'A' else [])
    result = []
    if kind != 'I':
        result += [('A', word, a) for word in a_words(n) for a in range(4)]
    if kind != 'A':
        result += [('M', word+(m,), out) for word in a_words(n-1)
                   for m in range(2) for out in range(2)]
    return result


def relative_differential(n, kind, mutation):
    """Build directly by Hochschild terms, respecting all endpoint corners."""
    source = cochain_basis(n, kind)
    target = cochain_basis(n+1, kind)
    source_index = {term: i for i, term in enumerate(source)}
    target_index = {term: i for i, term in enumerate(target)}
    columns = [0]*len(source)

    def add(s, t):
        if s in source_index:
            columns[source_index[s]] ^= 1 << target_index[t]

    if kind != 'I':
        for word in a_words(n+1):
            for out in range(4):
                for a in range(4):
                    product = amul(word[0], a)
                    if product == out:
                        add(('A', word[1:], a), ('A', word, out))
                    product = amul(a, word[-1])
                    if product == out:
                        add(('A', word[:-1], a), ('A', word, out))
                for k in range(n):
                    product = amul(word[k], word[k+1])
                    if product is not None:
                        add(('A', word[:k]+(product,)+word[k+2:], out), ('A', word, out))
    if kind == 'A':
        return columns
    if n == 0:
        for m in range(2):
            for a in range(4):
                out = module_action(a, m, mutation)
                if out is not None:
                    add(('A', (), a), ('M', (m,), out))
            if mutation != 'omit_e_scalar':
                add(('K', (), 0), ('M', (m,), m))
        return columns
    for word in a_words(n):
        for m in range(2):
            target_word = word+(m,)
            for source_out in range(2):
                out = module_action(word[0], source_out, mutation)
                if out is not None:
                    add(('M', word[1:]+(m,), source_out), ('M', target_word, out))
            for k in range(n-1):
                product = amul(word[k], word[k+1])
                if product is not None:
                    for out in range(2):
                        add(('M', word[:k]+(product,)+word[k+2:]+(m,), out),
                            ('M', target_word, out))
            product = module_action(word[-1], m, mutation)
            if product is not None:
                for out in range(2):
                    add(('M', word[:-1]+(product,), out), ('M', target_word, out))
            for source_out in range(4):
                out = module_action(source_out, m, mutation)
                if out is not None:
                    add(('A', word, source_out), ('M', target_word, out))
    return columns


def field4_mul(a, b):
    # F_4 = F_2[z]/(z^2+z+1); no assumption that all scalars lie in F_2.
    product = 0
    while b:
        if b & 1:
            product ^= a
        a <<= 1
        if a & 4:
            a ^= 7
        b >>= 1
    return product


def rank4(columns, rows):
    pivots = {}
    for encoded in columns:
        v = [(encoded >> k) & 1 for k in range(rows)]
        for p in sorted(pivots, reverse=True):
            if v[p]:
                factor = v[p]
                v = [a ^ field4_mul(factor, b) for a, b in zip(v, pivots[p])]
        nonzero = [k for k, a in enumerate(v) if a]
        if nonzero:
            p = max(nonzero)
            inverse = next(a for a in range(1, 4) if field4_mul(a, v[p]) == 1)
            pivots[p] = [field4_mul(inverse, a) for a in v]
    return len(pivots)


def m4_mul(a, b):
    return (field4_mul(a[0], b[0]),
            field4_mul(a[0], b[1]) ^ field4_mul(a[1], b[0]))


def coefficient_operator(coefficient, vector):
    """The independently derived action on basis 1,x of M, over F4."""
    a, b = coefficient
    s, t = vector
    return (field4_mul(a, s), field4_mul(b, s) ^ field4_mul(a, t))


def main(mutation):
    if mutation == 'characteristic_three':
        # In char 3, s^2=(l+r)^2=2lr is nonzero. The constant differential fails.
        require((2 % 3) == 0, 'periodic differential square is 2*l*r in characteristic 3')
    matrices = [bimodule_matrix(n) for n in range(11)]
    ranks = complex_check(matrices, [16*(n+1) for n in range(11)], 4, 'P')
    require(ranks == [8*n+4 for n in range(11)], 'P rank pattern')
    DETAILS['P_ranks_through_d10'] = ranks
    tensor = [tensor_matrix(n, mutation) for n in range(11)]
    t_ranks = complex_check(tensor, [8*(n+1) for n in range(11)], 2, 'P tensor M')
    DETAILS['P_tensor_M_ranks_through_d10'] = t_ranks
    q = [q_matrix(n, mutation) for n in range(11)]
    q_ranks = complex_check(q, [4]*11, 2, 'Q')
    require(q_ranks == [2]*11, 'Q ranks')
    for n in range(11):
        j = comparison(n, mutation)
        if n == 0:
            require([apply(tensor[0], c) for c in j] == q[0], 'j augmentation')
        else:
            require([apply(tensor[n], c) for c in j]
                    == [apply(comparison(n-1, mutation), c) for c in q[n]],
                    'pure-y comparison chain identity at degree ' + str(n))
        for i in range(n+1):
            for coefficient in range(4):
                actual = cochain_on_tensor(n, i, coefficient, j[0], mutation)
                expected = 0 if i > 0 or coefficient & 2 else 1 << coefficient
                require(actual == expected,
                        'chi normalization at degree ' + str(n) + ', i=' + str(i)
                        + ', coefficient=' + str(coefficient))
    for n in range(1, 11):
        for i in range(n+1):
            j = n-i
            require(bar_differential(shuffle(i, j, mutation))
                    == shuffle_of_periodic_d(i, j, mutation),
                    'shuffle chain identity at (' + str(i) + ',' + str(j) + ')')
    for n in range(11):
        for i in range(n+1):
            sorted_word = (1,)*i+(2,)*(n-i)
            for k in range(n+1):
                value = sum(word == sorted_word for _, word, _ in shuffle(k, n-k, mutation)) % 2
                require(value == (i == k), 'ordered cup has no factorial/binomial factor')
    DETAILS['comparison_and_cup_degrees'] = list(range(11))
    complexes = {}
    bases = {}
    ranks = {}
    for kind in ['A', 'I', 'B']:
        complexes[kind] = [relative_differential(n, kind, mutation) for n in range(5)]
        bases[kind] = [cochain_basis(n, kind) for n in range(6)]
        ranks[kind] = [rank2(d) for d in complexes[kind]]
        for n in range(4):
            require(all(apply(complexes[kind][n+1], column) == 0
                        for column in complexes[kind][n]), kind + ': cochain d^2=0')
    for n in range(5):
        bindex = {basis: k for k, basis in enumerate(bases['B'][n])}
        aindex = {basis: k for k, basis in enumerate(bases['A'][n])}
        bnext = {basis: k for k, basis in enumerate(bases['B'][n+1])}
        anext = {basis: k for k, basis in enumerate(bases['A'][n+1])}
        projection_next = [1 << anext[b] if b in anext else 0 for b in bases['B'][n+1]]
        for basis, k in bindex.items():
            expected = complexes['A'][n][aindex[basis]] if basis in aindex else 0
            require(apply(projection_next, complexes['B'][n][k]) == expected,
                    'coefficient restriction is chain projection')
        for k, basis in enumerate(bases['I'][n]):
            include_next = [1 << bnext[b] for b in bases['I'][n+1]]
            require(complexes['B'][n][bindex[basis]]
                    == apply(include_next, complexes['I'][n][k]),
                    'coefficient-I subcomplex agrees with independent construction')
    dimensions = {}
    for kind in ['A', 'I', 'B']:
        dimensions[kind] = [len(bases[kind][n])-ranks[kind][n]
                            -(ranks[kind][n-1] if n else 0) for n in range(5)]
    require(dimensions['A'] == [4, 8, 12, 16, 20], 'HH(A) dimensions')
    require(dimensions['I'] == [0, 1, 2, 2, 2], 'HH(B,I) scalar quotient exception')
    require(dimensions['B'] == [3, 6, 10, 14, 18], 'HH(B) dimensions and degree-zero exception')
    DETAILS['direct_relative_cohomology_dimensions'] = dimensions
    for kind in ['A', 'I', 'B']:
        for n in range(3):
            require(rank4(complexes[kind][n], len(bases[kind][n+1])) == ranks[kind][n],
                    'F4 relative rank consistency')
    for n in range(5):
        rows = 2 if n == 0 else 8*n
        require(rank4(tensor[n], rows) == t_ranks[n], 'F4 tensor rank consistency')
    require(field4_mul(2, 2) == 3, 'non-F2 coefficient is exercised')
    for a, b in itertools.product(range(4), repeat=2):
        for c, d in itertools.product(range(4), repeat=2):
            # Compare polynomial coefficient multiplication with composition of
            # characteristic action operators on each basis vector of M.
            product = m4_mul((a, b), (c, d))
            for vector in [(1, 0), (0, 1)]:
                composition = coefficient_operator((a, b), coefficient_operator((c, d), vector))
                require(composition == coefficient_operator(product, vector),
                        'F4 characteristic coefficient product versus operator composition')
    for n, m in [(0, 0), (1, 1), (3, 7), (8, 2)]:
        # Yoneda identity shifts on Q compose with no degree-dependent factor.
        for k in range(1, 11-n-m):
            require(q[k] == q[k+n] == q[k+m] == q[k+n+m],
                    'Yoneda identity-shift lifts commute with differentials')
    DETAILS['F4_checks'] = {'relative_differentials': [0, 1, 2],
                          'tensor_differentials': [0, 1, 2, 3, 4],
                          'all_F4_coefficient_pairs': 256,
                          'scalar_example': 'z^2=z+1, z is encoded by 2'}
    return DETAILS


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mutation', default='none', choices=[
        'none', 'trivial_module', 'swapped_module', 'omit_x_right',
        'zero_high_comparison', 'factorial_shuffle', 'omit_e_scalar',
        'characteristic_three'])
    args = parser.parse_args()
    result = {'mutation': args.mutation, 'optimized': not __debug__}
    try:
        result['details'] = main(args.mutation)
        result.update(status='pass', checks=CHECKS)
        print(json.dumps(result, sort_keys=True))
    except DiagnosticFailure as error:
        result.update(status='diagnostic_failure', checks=CHECKS,
                      exception=type(error).__name__, message=str(error))
        print(json.dumps(result, sort_keys=True))
        sys.exit(1)

#!/usr/bin/env python3
"""Exact checks for the explicitly normalized cardinality-adder family.

No optimization solver or floating-point arithmetic is used.  The general proof
is in PROOF.md; finite checks are regression controls, not a replacement for it.
"""
from collections import defaultdict
from fractions import Fraction as Q
from itertools import combinations, product
import json

checks = defaultdict(int)


def check(condition, label):
    if not condition:
        raise AssertionError(label)
    checks[label] += 1


def add(poly, mon, coeff):
    poly[mon] += coeff
    if not poly[mon]:
        del poly[mon]


def indicator_expansion(variables, values):
    p = {frozenset(): Q(1)}
    for v, b in zip(variables, values):
        nxt = defaultdict(Q)
        for mon, c in p.items():
            if b:
                add(nxt, mon | {v}, c)
            else:
                add(nxt, mon, c)
                add(nxt, mon | {v}, -c)
        p = dict(nxt)
    return p


def residual_values(kind):
    arity = 2 if kind == 'H' else 3
    return [(bits, sum(bits[:arity])-bits[arity]-2*bits[arity+1])
            for bits in product((0, 1), repeat=arity+2)]


def local_checks():
    out = {}
    for kind, target in [('H', 18), ('F', 36)]:
        arity = 2 if kind == 'H' else 3
        rows = residual_values(kind)
        p = defaultdict(Q)
        for bits, residual in rows:
            for mon, c in indicator_expansion(range(arity+2), bits).items():
                add(p, mon, residual*c)
        expected = {frozenset([j]): Q(1) for j in range(arity)}
        expected[frozenset([arity])] = Q(-1)
        expected[frozenset([arity+1])] = Q(-2)
        check(dict(p) == expected, 'local_residual_polynomial')
        check(sum(abs(r) for _, r in rows) == target, 'local_residual_mass')
        check(sum(r != 0 for _, r in rows) == (12 if kind == 'H' else 24), 'local_forbidden_count')
        for inputs in product((0, 1), repeat=arity):
            valid = [bits for bits, r in rows if bits[:arity] == inputs and r == 0]
            check(len(valid) == 1, 'local_unique_correct_output')
        out[kind] = {'tuple_count': len(rows), 'forbidden_count': sum(r != 0 for _, r in rows), 'mass': target}
    return out


def circuit(d):
    m = 1 << d
    nxt = m
    words = [[i] for i in range(m)]
    gates = []
    for level in range(1, d+1):
        new_words = []
        for a, b in zip(words[::2], words[1::2]):
            check(len(a) == len(b) == level, 'word_width')
            sums = []
            carry = None
            for j in range(level):
                z, t = nxt, nxt+1
                nxt += 2
                variables = (a[j], b[j], z, t) if j == 0 else (a[j], b[j], carry, z, t)
                check(len(set(variables)) == len(variables), 'gate_variables_distinct')
                gates.append(('H' if j == 0 else 'F', variables, 1 << j))
                sums.append(z)
                carry = t
            new_words.append(sums + [carry])
        words = new_words
    return m, nxt, gates, words[0]


def certificate(d):
    m, n, gates, root = circuit(d)
    r = m//2
    terms = []
    for i in range(m):
        terms.append((Q(1, r), (i,), (1,), 'input'))
    for kind, variables, weight in gates:
        for bits, residual in residual_values(kind):
            if residual:
                terms.append((Q(-weight*residual, r), variables, bits, 'gate'))
    for j, v in enumerate(root):
        bit = 1 if j == d-1 else 0
        epsilon = -1 if bit else 1
        terms.append((Q(-(1 << j)*epsilon, r), (v,), (1-bit,), 'root'))
    return m, n, gates, root, terms


def circuit_assignment(m, n, gates, inputs):
    vals = [None]*n
    vals[:m] = inputs
    for kind, variables, weight in gates:
        arity = 2 if kind == 'H' else 3
        number = sum(vals[v] for v in variables[:arity])
        vals[variables[arity]] = number % 2
        vals[variables[arity+1]] = number // 2
    check(all(v in (0, 1) for v in vals), 'complete_boolean_extension')
    return vals


def evaluate_monomial(variables, bits, vals):
    return int(all(vals[v] == bit for v, bit in zip(variables, bits)))


def check_family(d):
    m, n, gates, root, terms = certificate(d)
    check(n == 5*m-2*d-4, 'family_variable_count')
    check(len(gates) == 2*m-d-2, 'family_gate_count')
    check(sum(k == 'H' for k, _, _ in gates) == m-1, 'half_adder_count')
    check(sum(k == 'F' for k, _, _ in gates) == m-d-1, 'full_adder_count')
    check(len(terms) == 37*m-23*d-35, 'family_clause_count')
    check(all(len(vs) <= 5 for _, vs, _, _ in terms), 'bounded_clause_width')
    keys = [(vs, bits) for _, vs, bits, _ in terms]
    check(len(keys) == len(set(keys)), 'distinct_original_axioms')
    mass = sum(abs(c) for c, _, _, _ in terms)
    expected_mass = 72*d-102+Q(106, m)
    check(mass == expected_mass, 'certificate_mass')
    check(all(abs(c) <= 3 and (m//2) % c.denominator == 0 for c, _, _, _ in terms), 'coefficient_encoding_bounds')
    # Actually expand every displayed indicator in ordinary primary variables.
    # The result being exactly {empty monomial: 1} checks the entire identity.
    poly = defaultdict(Q)
    for coeff, variables, bits, _ in terms:
        for mon, c in indicator_expansion(variables, bits).items():
            add(poly, mon, coeff*c)
    check(dict(poly) == {frozenset(): Q(1)}, 'global_ordinary_polynomial_identity')
    # Negative control: delete an actual input-axiom contribution.
    damaged = defaultdict(Q, poly)
    first_coefficient, first_variables, first_bits, _ = terms[0]
    for mon, c in indicator_expansion(first_variables, first_bits).items():
        add(damaged, mon, -first_coefficient*c)
    check(dict(damaged) != {frozenset(): Q(1)}, 'deleted_input_term_rejected')
    if d <= 3:
        r = m//2
        for inputs in product((0, 1), repeat=m):
            vals = circuit_assignment(m, n, gates, list(inputs))
            root_number = sum((1 << j)*vals[v] for j, v in enumerate(root))
            check(root_number == sum(inputs), 'all_small_inputs_counted')
            gate_ok = all(evaluate_monomial(vs, bits, vals) == 0
                          for _, vs, bits, kind in terms if kind == 'gate')
            root_ok = all(evaluate_monomial(vs, bits, vals) == 0
                          for _, vs, bits, kind in terms if kind == 'root')
            check(gate_ok and root_ok == (sum(inputs) == r), 'exact_cardinality_semantics')
            val = sum(c*evaluate_monomial(vs, bits, vals) for c, vs, bits, _ in terms)
            check(val == 1, 'certificate_on_valid_circuit')
        for q in range(m-r+1):
            for forbidden in combinations(range(m), q):
                outside = [i for i in range(m) if i not in forbidden]
                chosen = set(outside[:r])
                vals = circuit_assignment(m, n, gates, [int(i in chosen) for i in range(m)])
                check(all(vals[i] == 0 for i in forbidden), 'hitting_witness_avoids_used_units')
                check(all(evaluate_monomial(vs, bits, vals) == 0
                          for _, vs, bits, kind in terms if kind != 'input'), 'hitting_witness_satisfies_other_axioms')
    return {'d': d, 'm': m, 'variables': n, 'clauses': len(terms),
            'fractional_certificate_mass': str(mass), 'support_integer_lower_bound': m//2+1}


def gadget_checks(k):
    n = 3+k
    b = 1 << k
    points = list(product((0, 1), repeat=n))
    axioms = []
    for y in product((0, 1), repeat=k):
        for i in range(3):
            a = [-1]*3+list(y)
            a[i] = 1
            axioms.append(tuple(a))
    axioms.append((1, 1, 1)+(-1,)*k)
    for i, j in combinations(range(3), 2):
        a = [-1]*n
        a[i] = a[j] = 0
        axioms.append(tuple(a))
    weakenings = [w for w in product((-1, 0, 1), repeat=n)
                  if any(all(a[j] == -1 or a[j] == w[j] for j in range(n)) for a in axioms)]
    dual = {p: (Q(0), Q(1, b), Q(1, 2), Q(-1, b))[sum(p[:3])] for p in points}
    for w in weakenings:
        value = sum(dual[p] for p in points if all(w[j] == -1 or w[j] == p[j] for j in range(n)))
        check(abs(value) <= 1, 'gadget_exact_dual_constraint')
    check(sum(dual.values()) == Q(3*b, 2)+2, 'gadget_dual_objective')
    for p in points:
        x1, x2, x3 = p[:3]
        fractional = (Q((1-x1)*(1-x2)+(1-x1)*(1-x3)+x1*(1-x2)*(1-x3)
                         -x1*x2*x3+x1+x2+x3, 2))
        integer = x1+(1-x1)*x2+(1-x1)*(1-x2)
        check(fractional == integer == 1, 'gadget_primal_identities')
    return {'selector_bits': k, 'axioms': len(axioms), 'weakenings': len(weakenings),
            'exact_real_mass': str(Q(3*b, 2)+2), 'exact_integer_mass_and_support': 2*b+1}


def padded_checks(m):
    r = m//2
    b = 1 << m
    residual_mass = 0
    for x in product((0, 1), repeat=m):
        h = sum(x)
        residual = Q(1)-Q(h, r)
        check(Q(h, r)+residual == 1, 'padded_identity')
        check(abs(residual) <= 1, 'padded_residual_bound')
        if h != r:
            residual_mass += abs(residual)
        else:
            check(residual == 0, 'padded_omitted_slice')
    mass = Q(m*b, r)+residual_mass
    check(mass <= 3*b, 'padded_mass_bound')
    return {'m': m, 'rational_certificate_mass': str(mass), 'integer_support_lower_bound': b*(m-r+1)}


def large_parameter_checks():
    out = []
    for d in range(1, 41):
        m = 1 << d
        direct_gate_mass = sum((m >> level)*(36*(1 << level)-54) for level in range(1, d+1))
        check(direct_gate_mass == 36*m*d-54*m+54, 'large_exact_mass_summation')
        mass = Q(m+direct_gate_mass+2*m-1, m//2)
        check(mass == 72*d-102+Q(106, m), 'large_exact_mass_formula')
        if d >= 11:
            check(m//2+1 > mass, 'strict_large_parameter_saving')
        if d in (11, 16, 24, 40):
            out.append({'d': d, 'm': m, 'fractional_upper_bound': str(mass),
                        'integer_lower_bound': m//2+1,
                        'ratio_lower_bound': str(Q(m//2+1)/mass)})
    return out


def main():
    report = {'arithmetic': 'Python integers and fractions.Fraction only',
              'local_gates': local_checks(),
              'large_parameter_formula_controls': large_parameter_checks(),
              'adder_families': [check_family(d) for d in range(1, 9)],
              'published_gadget_replications': [gadget_checks(k) for k in range(1, 5)],
              'padded_hamming_slice_controls': [padded_checks(m) for m in (2, 4, 6, 8)]}
    report['assertion_counts'] = dict(sorted(checks.items()))
    report['total_assertions'] = sum(checks.values())
    report['status'] = 'PASS'
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

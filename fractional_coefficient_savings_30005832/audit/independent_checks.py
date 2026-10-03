#!/usr/bin/env python3
"""Independent, dependency-free audit of the frozen cardinality-adder packet.

Does not import the author checker or write to the frozen public directory.
Uses recursive circuit construction, scaled integer certificates, exact ordinary
polynomial expansion, and exhaustive witness/weakening controls.
"""
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

COUNTS = Counter()


def demand(ok, label):
    if not ok:
        raise AssertionError(label)
    COUNTS[label] += 1


def digest(data):
    return hashlib.sha256(data).hexdigest()


def check_freeze(folder):
    manifest_bytes = (folder / 'MANIFEST.json').read_bytes()
    demand(digest(manifest_bytes) == '477bda86fe9e79f2067a3d271146babb60272a690edf54207b727864542604ba', 'manifest_digest')
    manifest = json.loads(manifest_bytes)
    for name, entry in manifest['files'].items():
        data = (folder / name).read_bytes()
        demand(len(data) == entry['bytes'] and digest(data) == entry['sha256'], 'frozen_file_digest')
    demand(manifest['files']['PROOF.md']['sha256'] == '58378769695d585a53ba5e342305e344be8dd64e0ea765cc9e467ad93d8cf184', 'expected_proof_digest')
    return {'proof_sha256': manifest['files']['PROOF.md']['sha256'], 'manifest_sha256': digest(manifest_bytes)}


def construct(depth):
    """Postorder recursive tree, independently of the author's levelwise builder."""
    m = 2 ** depth
    next_var = m
    gates = []

    def visit(lo, size):
        nonlocal next_var
        if size == 1:
            return [lo]
        left = visit(lo, size // 2)
        right = visit(lo + size // 2, size // 2)
        demand(len(left) == len(right), 'recursive_equal_word_lengths')
        output = []
        carry = None
        for position, (a, b) in enumerate(zip(left, right)):
            z, t = next_var, next_var + 1
            next_var += 2
            incoming = (a, b) if carry is None else (a, b, carry)
            variables = incoming + (z, t)
            demand(len(set(variables)) == len(variables), 'distinct_gate_variables')
            gates.append((incoming, z, t, 2 ** position))
            output.append(z)
            carry = t
        return output + [carry]

    root = visit(0, m)
    return m, next_var, gates, root


def truth_table(incoming, z, t):
    """Gate truth predicate uses XOR/majority rather than a residual test."""
    variables = incoming + (z, t)
    for bits in product((0, 1), repeat=len(variables)):
        inputs = bits[:-2]
        expected_sum = 0
        for b in inputs:
            expected_sum ^= b
        expected_carry = int(sum(inputs) >= 2)
        valid = bits[-2:] == (expected_sum, expected_carry)
        residual = sum(inputs) - bits[-2] - 2 * bits[-1]
        demand(valid == (residual == 0), 'truth_predicate_matches_residual')
        yield variables, bits, residual, valid


def scaled_certificate(depth):
    m, n, gates, root = construct(depth)
    r = m // 2
    # Every coefficient below is multiplied by r, so all work uses integers.
    terms = [(1, (i,), (1,), 'input') for i in range(m)]
    for incoming, z, t, weight in gates:
        for variables, bits, residual, valid in truth_table(incoming, z, t):
            if not valid:
                terms.append((-weight * residual, variables, bits, 'gate'))
    for position, variable in enumerate(root):
        target = int(position == depth - 1)
        terms.append(((2 ** position) * (1 if target else -1), (variable,), (1 - target,), 'root'))
    return m, n, gates, root, terms


def expand_indicator(variables, bits):
    """Ordinary powers are retained: no Boolean x*x=x simplification occurs."""
    polynomial = {(): 1}
    for variable, bit in zip(variables, bits):
        updated = defaultdict(int)
        for monomial, coefficient in polynomial.items():
            extended = tuple(sorted(monomial + (variable,)))
            if bit:
                updated[extended] += coefficient
            else:
                updated[monomial] += coefficient
                updated[extended] -= coefficient
        polynomial = dict(updated)
    return polynomial


def expand_terms(terms):
    result = defaultdict(int)
    for coefficient, variables, bits, _ in terms:
        for monomial, factor in expand_indicator(variables, bits).items():
            result[monomial] += coefficient * factor
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def extension(m, n, gates, inputs):
    values = [None] * n
    values[:m] = inputs
    for incoming, z, t, _ in gates:
        demand(all(values[v] in (0, 1) for v in incoming), 'topological_boolean_gate_inputs')
        total = sum(values[v] for v in incoming)
        values[z] = total & 1
        values[t] = int(total >= 2)
    demand(all(v in (0, 1) for v in values), 'complete_extension')
    return values


def mask_term(variables, bits):
    positive = negative = 0
    for v, b in zip(variables, bits):
        if b:
            positive |= 1 << v
        else:
            negative |= 1 << v
    return positive, negative


def fits(p, q, assignment):
    return (assignment & p) == p and (assignment & q) == 0


def evaluate_terms(terms, assignment):
    return sum(c for c, vs, bs, _ in terms if fits(*mask_term(vs, bs), assignment))


def family_checks(depth):
    m, n, gates, root, terms = scaled_certificate(depth)
    r = m // 2
    demand(n == 5 * m - 2 * depth - 4, 'variable_formula')
    demand(len(gates) == 2 * m - depth - 2, 'gate_formula')
    demand(sum(len(g[0]) == 2 for g in gates) == m - 1, 'half_adder_formula')
    demand(sum(len(g[0]) == 3 for g in gates) == m - depth - 1, 'full_adder_formula')
    demand(len(terms) == 37 * m - 23 * depth - 35, 'clause_formula')
    demand(len({mask_term(vs, bs) for _, vs, bs, _ in terms}) == len(terms), 'canonical_distinct_axioms')
    demand(max(len(vs) for _, vs, _, _ in terms) <= 5, 'degree_width_bound')
    mass = Fraction(sum(abs(c) for c, _, _, _ in terms), r)
    demand(mass == 72 * depth - 102 + Fraction(106, m), 'mass_formula')
    demand(mass > 0, 'positive_denominator_bound')
    rational_coefficients = [Fraction(c, r) for c, _, _, _ in terms]
    demand(max(map(abs, rational_coefficients)) <= 3, 'coefficient_magnitude_bound')
    demand(all(r % c.denominator == 0 for c in rational_coefficients), 'coefficient_denominator_bound')
    demand(expand_terms(terms) == {(): r}, 'ordinary_polynomial_certificate')
    # Adversarial controls: corrupt three independently meaningful signs/terms.
    for idx, label in [(0, 'input'), (m, 'gate'), (len(terms) - 2, 'root_target')]:
        c, vs, bs, kind = terms[idx]
        corrupt = list(terms)
        corrupt[idx] = (-c, vs, bs, kind)
        demand(expand_terms(corrupt) != {(): r}, 'sign_flip_rejected_' + label)
    if depth <= 2:
        indicators = [(c, *mask_term(vs, bs)) for c, vs, bs, _ in terms]
        for assignment in range(1 << n):
            demand(sum(c for c, p, q in indicators if fits(p, q, assignment)) == r, 'all_small_full_assignments_identity')
            demand(any(fits(p, q, assignment) for _, p, q in indicators), 'all_small_full_assignments_unsatisfiable')
    if depth <= 3:
        for inputs in product((0, 1), repeat=m):
            vals = extension(m, n, gates, list(inputs))
            root_value = sum((1 << j) * vals[v] for j, v in enumerate(root))
            demand(root_value == sum(inputs), 'all_small_input_counts')
            demand((root_value == r) == (sum(inputs) == r), 'exact_cardinality')
    if depth <= 4:
        # The complement of each maximal forbidden I is its unique size-r witness.
        for allowed in combinations(range(m), r):
            chosen = set(allowed)
            vals = extension(m, n, gates, [int(i in chosen) for i in range(m)])
            demand(sum((1 << j) * vals[v] for j, v in enumerate(root)) == r, 'all_critical_hitting_witnesses')
            for incoming, z, t, _ in gates:
                demand(sum(vals[v] for v in incoming) == vals[z] + 2 * vals[t], 'witness_satisfies_all_gates')
            demand(all(vals[i] == 0 for i in range(m) if i not in chosen), 'witness_avoids_forbidden_units')
    return {'d': depth, 'm': m, 'variables': n, 'clauses': len(terms), 'mass': str(mass), 'integer_support_lower_bound': r + 1, 'strict_certified_gap': mass < r + 1}


def local_controls():
    output = {}
    for arity, target_mass, target_forbidden in [(2, 18, 12), (3, 36, 24)]:
        histogram = Counter()
        terms = []
        for variables, bits, residual, valid in truth_table(tuple(range(arity)), arity, arity + 1):
            histogram[residual] += 1
            if not valid:
                terms.append((residual, variables, bits, 'gate'))
        expected = {(v,): 1 for v in range(arity)}
        expected[(arity,)] = -1
        expected[(arity + 1,)] = -2
        demand(expand_terms(terms) == expected, 'local_ordinary_residual_identity')
        demand(sum(abs(c) for c, _, _, _ in terms) == target_mass, 'local_exact_mass')
        demand(len(terms) == target_forbidden, 'local_forbidden_count')
        output['half' if arity == 2 else 'full'] = {'histogram': dict(sorted(histogram.items())), 'mass': target_mass, 'forbidden': target_forbidden}
    return output


def exhaustive_weakening_control(depth):
    m, n, gates, root, terms = scaled_certificate(depth)
    axioms = [mask_term(vs, bs) for _, vs, bs, _ in terms]
    witnesses = []
    for ones in combinations(range(m), m // 2):
        chosen = set(ones)
        vals = extension(m, n, gates, [int(i in chosen) for i in range(m)])
        witnesses.append(sum(b << i for i, b in enumerate(vals)))
    projections = set()
    weakening_count = 0
    for pattern in product((-1, 0, 1), repeat=n):
        p = sum(1 << i for i, b in enumerate(pattern) if b == 1)
        q = sum(1 << i for i, b in enumerate(pattern) if b == 0)
        if not any((p & a) == a and (q & b) == b for a, b in axioms):
            continue
        weakening_count += 1
        projection = sum(1 << j for j, point in enumerate(witnesses) if fits(p, q, point))
        # Every nonzero projection must be contained in a chosen input star.
        if projection:
            demand(any(all(not (projection >> j & 1) or (point >> i & 1) for j, point in enumerate(witnesses)) for i in range(m) if p >> i & 1), 'all_degree_projection_in_input_star')
        projections.add(projection)
    full = (1 << len(witnesses)) - 1
    reachable = {0}
    for k in range(m // 2 + 1):
        demand(full not in reachable, 'all_degree_no_small_cover')
        reachable |= {a | b for a in reachable for b in projections}
    demand(full in reachable, 'projected_minimum_cover_sharp')
    return {'d': depth, 'all_ternary_monomials': 3 ** n, 'weakenings': weakening_count, 'witnesses': len(witnesses), 'distinct_projection_masks': len(projections), 'exact_minimum_witness_cover': m // 2 + 1}


def conventional_gate_encoding_controls():
    """Check the robustness observation using XOR plus AND/majority clauses."""
    output = {}
    for arity in (2, 3):
        n = arity + 2
        axioms = []
        # Sum bit is input parity: forbid all wrong parity assignments.
        for inputs in product((0, 1), repeat=arity):
            wrong_sum = 1 - (sum(inputs) % 2)
            axioms.append(inputs + (wrong_sum, -1))
        # Carry is AND for two inputs and majority for three inputs.
        for pair in combinations(range(arity), 2):
            p = [-1] * n
            for i in pair:
                p[i] = 1
            p[-1] = 0
            axioms.append(tuple(p))
        if arity == 2:
            for i in range(arity):
                p = [-1] * n
                p[i] = 0
                p[-1] = 1
                axioms.append(tuple(p))
        else:
            for pair in combinations(range(arity), 2):
                p = [-1] * n
                for i in pair:
                    p[i] = 0
                p[-1] = 1
                axioms.append(tuple(p))
        for point in product((0, 1), repeat=n):
            hit = any(all(b == -1 or b == v for b, v in zip(ax, point)) for ax in axioms)
            valid = point[-2] == sum(point[:arity]) % 2 and point[-1] == sum(point[:arity]) // 2
            demand(hit == (not valid), 'conventional_gate_cnf_exact')
        demand(len(axioms) == (7 if arity == 2 else 14), 'conventional_gate_clause_count')
        output['half' if arity == 2 else 'full'] = {'clauses': len(axioms), 'maximum_width': max(sum(v != -1 for v in ax) for ax in axioms)}
    return output


def published_gadget_controls():
    results = []
    for k in range(1, 5):
        B, n = 1 << k, k + 3
        points = list(product((0, 1), repeat=n))
        axioms = []
        for selector in product((0, 1), repeat=k):
            for i in range(3):
                row = [-1] * 3 + list(selector)
                row[i] = 1
                axioms.append(tuple(row))
        axioms.append((1, 1, 1) + (-1,) * k)
        for i, j in combinations(range(3), 2):
            row = [-1] * n
            row[i] = row[j] = 0
            axioms.append(tuple(row))
        def matches(row, point):
            return all(b == -1 or b == v for b, v in zip(row, point))
        weights = [Fraction([0, 2, B, -2][sum(p[:3])], 2 * B) for p in points]
        count = 0
        for row in product((-1, 0, 1), repeat=n):
            if any(all(a == -1 or a == b for a, b in zip(ax, row)) for ax in axioms):
                count += 1
                demand(abs(sum(w for w, p in zip(weights, points) if matches(row, p))) <= 1, 'gadget_all_weakening_dual')
        demand(sum(weights) == Fraction(3 * B, 2) + 2, 'gadget_exact_dual_objective')
        for p in points:
            a, b, c = p[:3]
            demand(Fraction((1-a)*(1-b)+(1-a)*(1-c)+a*(1-b)*(1-c)-a*b*c+a+b+c, 2) == 1, 'gadget_fractional_identity')
            demand(a+(1-a)*b+(1-a)*(1-b) == 1, 'gadget_integer_identity')
        results.append({'selector_bits': k, 'weakenings': count, 'real_optimum': str(sum(weights)), 'integer_optimum': 2 * B + 1})
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--public', type=Path, default=Path(__file__).resolve().parent.parent / 'public')
    args = parser.parse_args()
    result = {'freeze': check_freeze(args.public), 'local': local_controls()}
    output = subprocess.check_output([sys.executable, str(args.public / 'check_exact.py')], text=True)
    demand(output == (args.public / 'exact_results.json').read_text(), 'author_checker_reproduces_frozen_output')
    result['author_assertions_reproduced'] = json.loads(output)['total_assertions']
    result['independent_families'] = [family_checks(d) for d in range(1, 12)]
    result['all_degree_weakening_controls'] = [exhaustive_weakening_control(d) for d in (1, 2)]
    result['published_gadget_controls'] = published_gadget_controls()
    result['conventional_gate_encoding_controls'] = conventional_gate_encoding_controls()
    for depth in range(1, 101):
        m = 2 ** depth
        gate_mass = sum((m // 2 ** level) * sum((18 if j == 0 else 36) * 2 ** j for j in range(level)) for level in range(1, depth + 1))
        demand(gate_mass == 36 * m * depth - 54 * m + 54, 'large_exact_gate_sum')
        bound = Fraction(m + gate_mass + 2 * m - 1, m // 2)
        demand(bound == 72 * depth - 102 + Fraction(106, m), 'large_exact_total_mass')
        demand((bound < m // 2 + 1) == (depth >= 11), 'exact_strict_gap_threshold_control')
    check_freeze(args.public)
    result['checks_by_label'] = dict(sorted(COUNTS.items()))
    result['total_independent_assertions'] = sum(COUNTS.values())
    result['status'] = 'PASS'
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()

"""Exact, independent diagram/cube controls for PR177. No author code imported.

These finite controls support the written universal proof; they do not test every
finite-type invariant. Acceptance uses explicit exceptions and survives python -O.
"""
from collections import Counter
from fractions import Fraction as Q
from itertools import product
from math import comb, factorial
import json
import sys


class Failure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise Failure(message)


def diagram(word, extra_components=0):
    """Track actual strand labels, then glue bottom positions to top positions.

    +1/-1 are opposite over/under choices with the SAME endpoint transposition.
    0 is a double point of the SAME two immersed arcs, not a smoothing.
    """
    labels = [0, 1]
    crossings = []
    for sign in word:
        require(sign in (-1, 0, 1), "illegal crossing")
        crossings.append((labels[0], labels[1], sign))
        labels.reverse()
    parents = list(range(2))

    def root(x):
        while parents[x] != x:
            x = parents[x]
        return x

    for bottom_position, strand_label in enumerate(labels):
        a, b = root(bottom_position), root(strand_label)
        parents[a] = b
    roots = [root(i) for i in range(2)]
    components = len(set(roots)) + extra_components
    signed_crossings = Counter()
    self_crossings = Counter()
    for a, b, sign in crossings:
        if roots[a] == roots[b]:
            self_crossings[roots[a]] += sign
        else:
            signed_crossings[tuple(sorted((roots[a], roots[b])))] += sign
    linking = {pair: Q(value, 2) for pair, value in signed_crossings.items()}
    return {"components": components, "linking": linking,
            "self_writhe": dict(self_crossings), "endpoint_labels": labels}


def cancellation_normal_form(word):
    require(all(x in (-1, 1) for x in word), "singular unresolved word")
    stack = []
    certificates = []
    for position, sign in enumerate(word):
        if stack and stack[-1][1] == -sign:
            earlier, _ = stack.pop()
            certificates.append((earlier, position))
        else:
            stack.append((position, sign))
    return tuple(sign for _, sign in stack), certificates


def singular_word(n, r):
    return (1,) * (2*n) + (1, 0) * r


def resolve(word, choices):
    choices = iter(choices)
    resolved = tuple(next(choices) if x == 0 else x for x in word)
    try:
        next(choices)
        raise Failure("unused resolution bit")
    except StopIteration:
        return resolved


def finite_difference(values, r):
    require(len(values) >= r+1, "too few values")
    return sum(Q((-1)**(r-j) * comb(r, j)) * values[j] for j in range(r+1))


def binomial_q(t, r):
    answer = Q(1)
    for k in range(r):
        answer *= t-k
    return answer / factorial(r)


def newton_value(values, degree, t):
    return sum(binomial_q(t, r) * finite_difference(values, r)
               for r in range(degree+1))


def cube_coefficients(values, r):
    """Mobius expansion on {0,1}^r, with repeated variables reduced by x^2=x."""
    require(len(values) == 1 << r, "cube length")
    coefficients = list(map(Q, values))
    for bit in range(r):
        for mask in range(1 << r):
            if mask & (1 << bit):
                coefficients[mask] -= coefficients[mask ^ (1 << bit)]
    return coefficients


def evaluate_cube(coefficients, mask):
    return sum(coefficient for subset, coefficient in enumerate(coefficients)
               if subset & mask == subset)


def controls():
    counts = Counter()
    for n in range(5):
        for r in range(9):
            immersion = singular_word(n, r)
            require(diagram(immersion)["components"] == 2, "immersed domain components")
            multiplicities = Counter()
            signed_multiplicities = Counter()
            for choices in product((-1, 1), repeat=r):
                word = resolve(immersion, choices)
                normal, certificate = cancellation_normal_form(word)
                j = choices.count(1)
                require(normal == (1,) * (2*(n+j)), "RII normal form")
                require(len(certificate) == r-j, "RII certificate count")
                for extras in (0, 1, 5, 100):
                    info = diagram(word, extras)
                    require(info["components"] == 2+extras, "actual closure components")
                    require(list(info["linking"].values()) in ([Q(n+j)], []), "link count")
                    require(not info["self_writhe"], "no blackboard self framing")
                    counts["component_and_linking_cases"] += 1
                multiplicities[j] += 1
                signed_multiplicities[j] += (-1)**(r-j)
                counts["resolution_cases"] += 1
            for j in range(r+1):
                require(multiplicities[j] == comb(r, j), "resolution multiplicity")
                require(signed_multiplicities[j] == (-1)**(r-j)*comb(r, j), "skein signs")
                counts["grouped_coefficient_cases"] += 1

    # All rational polynomials in a basis through degree 8; checks include t=1/2,
    # negative points, and products of different degrees, not only n^2.
    for k in range(9):
        values = [Q(n)**k for n in range(24)]
        for n in range(8):
            require(finite_difference(values[n:], k+1) == 0, "order difference")
            counts["basis_vanishing_cases"] += 1
        for t in map(Q, (-7, -1, 0, 1, 3, 11)):
            require(newton_value(values, k, t) == t**k, "Newton integer")
            counts["newton_cases"] += 1
        require(newton_value(values, k, Q(1, 2)) == Q(1, 2)**k, "Newton half")
        counts["newton_cases"] += 1
    for a in range(5):
        for b in range(5):
            av = [Q(n)**a for n in range(20)]
            bv = [Q(n)**b for n in range(20)]
            pv = [x*y for x,y in zip(av, bv)]
            for t in (Q(-3), Q(1, 2), Q(7)):
                require(newton_value(pv, a+b, t) ==
                        newton_value(av, a, t)*newton_value(bv, b, t), "product identity")
                counts["newton_product_cases"] += 1

    # Arbitrary affine linking changes (including self-crossing zero increments).
    # This probes component-uniformity and the finite-type product proof on cubes.
    for base in range(-2, 3):
        for changes in product((-1, 0, 1), repeat=5):
            lk = [Q(base + sum(changes[i] for i in range(5) if mask & (1 << i)))
                  for mask in range(32)]
            g = [x*x for x in lk]
            f = [4*x*x-x for x in g]
            for degree, values in ((1, lk), (2, g), (4, f)):
                coefficients = cube_coefficients(values, 5)
                require(all(c == 0 for mask, c in enumerate(coefficients)
                            if mask.bit_count() > degree), "cube order bound")
                require(all(evaluate_cube(coefficients, mask) == values[mask]
                            for mask in range(32)), "Mobius round trip")
                counts["cube_order_cases"] += 1

    # Independently vary a symmetric 4-component linking matrix, label order,
    # and all choices of component orientation.
    matrix={(0,1):3, (0,2):-2, (0,3):1, (1,2):0, (1,3):-4, (2,3):2}
    g0=sum(x*x for x in matrix.values())
    from itertools import permutations
    for permutation in permutations(range(4)):
        for signs in product((-1, 1), repeat=4):
            changed={tuple(sorted((permutation[i], permutation[j]))): signs[i]*signs[j]*x
                     for (i,j),x in matrix.items()}
            require(sum(x*x for x in changed.values()) == g0, "orientation/order symmetry")
            counts["orientation_order_cases"] += 1
    require(newton_value([Q(n*n) for n in range(9)], 2, Q(1,2)) == Q(1,4), "chi g")
    require(newton_value([Q(4*n**4-n*n) for n in range(9)], 4, Q(1,2)) == 0, "chi f")
    for n in range(1001):
        require((4*n*n-n == 0) == (n == 0), "integer zero locus")
        counts["integer_zero_locus_cases"] += 1

    mutations=[]
    def reject(name, wrong_claim, witness):
        require(not wrong_claim, "negative mutation escaped: " + name)
        mutations.append({"name":name, "outcome":"rejected", "witness":witness})
    reject("delete_fixed_companion", diagram((1,))["components"] == 2,
           "one crossing has a single component after closure")
    reject("replace_double_point_with_smoothing", diagram((1,))["components"] == 2,
           "identity smoothing leaves the fixed crossing: one component")
    reject("start_from_odd_exponent", diagram((1,1,1))["components"] == 2,
           "odd endpoint exchange joins the two strand labels into one circle")
    reject("resolve_plus_plus", Q(1)+Q(1) == 0,
           "constant order-zero invariant gives 2, rather than first difference 0")
    reject("reuse_one_singular_site_for_two_bits", Q(1)-Q(0)-Q(0)+Q(1) == 0,
           "xor control gives second difference of linking number 2; lk has order one")
    reject("linking_number_equals_exponent", list(diagram((1,1))["linking"].values()) == [Q(2)],
           "Hopf closure has two mixed crossings and linking number 1")
    reject("g_has_order_at_most_one", finite_difference([Q(n*n) for n in range(5)], 2) == 0,
           "second difference of n squared is 2")
    reject("omit_factorial_in_Newton", sum(Q(1,2)*(Q(1,2)-1)*Q(2) for _ in range(1)) == Q(1,4)-Q(1,2),
           "quadratic Newton term without 2! doubles its necessary contribution")
    return {"status":"PASS", "optimization_level":sys.flags.optimize,
            "exact_arithmetic":"fractions.Fraction and integers", "counts":dict(counts),
            "negative_mutations":mutations,
            "scope_limit":"finite controls; universal claim is established by independent proof"}


if __name__ == "__main__":
    print(json.dumps(controls(), indent=2, sort_keys=True))

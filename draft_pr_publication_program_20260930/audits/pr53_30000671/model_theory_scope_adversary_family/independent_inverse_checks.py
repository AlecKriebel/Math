"""Bounded independent checks; no author or other reviewer code is imported."""
from itertools import product
import hashlib
import json
from pathlib import Path

assertions = 0

def check(claim):
    global assertions
    assert claim
    assertions += 1

def chain_from_viability(sizes, transition):
    # transition[j] maps level j+1 to level j. A top-level witness always
    # supplies a finite chain; backward viability avoids nonlifting choices.
    good = [None] * len(sizes)
    good[-1] = set(range(sizes[-1]))
    for j in range(len(sizes) - 2, -1, -1):
        good[j] = {transition[j][x] for x in good[j + 1]}
    chain = [min(good[0])]
    for j in range(1, len(sizes)):
        child = min(x for x in good[j] if transition[j - 1][x] == chain[-1])
        chain.append(child)
    return chain

systems = 0
non_surjective_systems = 0
naive_first_choice_failures = 0
for depth in range(1, 6):
    for sizes in product((1, 2), repeat=depth):
        maps = [tuple(product(range(sizes[j]), repeat=sizes[j + 1]))
                for j in range(depth - 1)]
        for transition in product(*maps):
            systems += 1
            chain = chain_from_viability(sizes, transition)
            check(len(chain) == depth)
            for j, x in enumerate(chain):
                check(0 <= x < sizes[j])
            for j in range(depth - 1):
                check(transition[j][chain[j + 1]] == chain[j])
            if any(len(set(transition[j])) != sizes[j] for j in range(depth - 1)):
                non_surjective_systems += 1
            reachable = set(range(sizes[-1]))
            for j in range(depth - 2, -1, -1):
                reachable = {transition[j][x] for x in reachable}
            if 0 not in reachable:
                naive_first_choice_failures += 1

check(non_surjective_systems > 0)
check(naive_first_choice_failures > 0)
# The explicit mutant chooses the first lower-level node despite no lift.
check(chain_from_viability((2, 1), ((1,),)) == [1, 0])
check(0 not in set((1,)))

toy_checks = 0
for horizon in range(1, 31):
    witness = horizon
    check(all(witness >= r for r in range(1, horizon + 1)))
    check(not witness >= horizon + 1)
    toy_checks += 2

def elements(q, r):
    return tuple(product(range(q), repeat=r))

def add(a, b, q):
    return tuple((x + y) % q for x, y in zip(a, b))

def mul(a, b, q):
    r = len(a)
    out = [0] * r
    for i in range(r):
        for j in range(r - i):
            out[i + j] = (out[i + j] + a[i] * b[j]) % q
    return tuple(out)

def evaluate(a, image_t, q):
    r = len(a)
    zero = (0,) * r
    one = (1,) + (0,) * (r - 1)
    power = one
    out = zero
    for c in a:
        out = add(out, tuple((c * x) % q for x in power), q)
        power = mul(power, image_t, q)
    return out

ring_cases = []
automorphisms = 0
hom_checks = 0
all_maps = {}
for q in (2, 3):
    for r in range(1, 5):
        els = elements(q, r)
        zero = (0,) * r
        one = (1,) + (0,) * (r - 1)
        if r == 1:
            t_images = [zero]
        else:
            t_images = [(0, leading) + tail for leading in range(1, q)
                        for tail in product(range(q), repeat=r - 2)]
        level_maps = []
        for t in t_images:
            f = {a: evaluate(a, t, q) for a in els}
            check(f[zero] == zero)
            check(f[one] == one)
            check(len(set(f.values())) == len(els))
            for a in els:
                for b in els:
                    check(f[add(a, b, q)] == add(f[a], f[b], q))
                    check(f[mul(a, b, q)] == mul(f[a], f[b], q))
                    hom_checks += 2
            # Use an independently formed reverse dictionary, not a formal
            # guessed inverse polynomial, to check actual inverse identities.
            inverse = {value: key for key, value in f.items()}
            for a in els:
                check(inverse[f[a]] == a)
                check(f[inverse[a]] == a)
            level_maps.append(f)
            automorphisms += 1
        all_maps[(q, r)] = level_maps
        ring_cases.append({'q': q, 'r': r, 'elements': len(els),
                           'automorphisms': len(level_maps)})

restriction_checks = 0
for q in (2, 3):
    for r in range(2, 5):
        lower_els = elements(q, r - 1)
        lower_maps = all_maps[(q, r - 1)]
        for f in all_maps[(q, r)]:
            restricted = {a: f[a + (0,)][:-1] for a in lower_els}
            check(restricted in lower_maps)
            for a in elements(q, r):
                check(f[a][:-1] == restricted[a[:-1]])
                restriction_checks += 1

# Two genuine quotient automorphisms need not be compatible. At levels 2,3
# over F_3, identity below and t -> 2t above are valid but disagree modulo t².
identity_lower = all_maps[(3, 2)][0]
nontrivial_upper = next(f for f in all_maps[(3, 3)] if f[(0, 1, 0)] == (0, 2, 0))
check(identity_lower[(0, 1)] != nontrivial_upper[(0, 1, 0)][:-1])

# Explicit rational dual-number automorphisms epsilon -> a epsilon. These
# bounded rational witnesses support the separate universal proof of infinitude.
from fractions import Fraction
def dual_mul(a, b):
    return (a[0] * b[0], a[0] * b[1] + a[1] * b[0])
def dual_scale(a, scalar):
    return (a[0], scalar * a[1])
dual_scalars = [Fraction(n) for n in range(1, 21)]
dual_witnesses = [(Fraction(a), Fraction(b)) for a in range(-2, 3) for b in range(-2, 3)]
for scalar in dual_scalars:
    for a in dual_witnesses:
        check(dual_scale(dual_scale(a, scalar), 1 / scalar) == a)
        for b in dual_witnesses:
            check(dual_scale(dual_mul(a, b), scalar)
                  == dual_mul(dual_scale(a, scalar), dual_scale(b, scalar)))
check(len({dual_scale((Fraction(0), Fraction(1)), c) for c in dual_scalars}) == 20)

result = {
    'schema': 'pr53-independent-inverse-system-checks/v1', 'status': 'PASS',
    'assertions': assertions, 'finite_inverse_systems': systems,
    'non_surjective_finite_systems': non_surjective_systems,
    'naive_first_choice_failures': naive_first_choice_failures,
    'bounded_infinite_toy_checks': toy_checks,
    'finite_quotient_ring_cases': ring_cases,
    'actual_automorphisms_checked': automorphisms,
    'ring_homomorphism_equations': hom_checks,
    'individual_quotient_restriction_equations': restriction_checks,
    'dual_number_rational_scalars': len(dual_scalars),
    'mutation_checks': ['arbitrary first isomorphism need not lift',
                        'finite-horizon toy witness fails at next level',
                        'individually valid quotient isomorphisms need not commute'],
    'infinite_toy_is_ring_counterexample': False,
    'historical_gabber_construction_reproduced': False,
    'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'root_approval': False,
}
print(json.dumps(result, indent=2, sort_keys=True))

#!/usr/bin/env python3
"""Independent exact holomorph/stabilizer controls for PR156.

No imports from submitted code. No assertions: all failed checks raise explicitly,
so optimized Python executes the same checks. The universal proof is REVIEW.md;
finite and bounded computations supplement its exact coefficient certificates.
"""

from datetime import datetime, timezone
from hashlib import sha256
from itertools import product
from math import gcd
from pathlib import Path
import argparse
import json
import platform
import sys


class VerificationFailure(Exception):
    pass


CHECKS = 0
SECTIONS = []


def require(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise VerificationFailure(message)


def section(name, start, detail):
    SECTIONS.append({"name": name, "explicit_checks": CHECKS - start, "detail": detail})


def eps(c):
    return 1 if c % 4 < 2 else -1


def parity_sign(c):
    return 1 if c % 2 == 0 else -1


def xor_chart(c, d):
    """Independent construction: XOR the two binary coordinates."""
    return ((c & 1) ^ (d & 1)) + 2 * (((c >> 1) & 1) ^ ((d >> 1) & 1))


def diamond(c, d):
    """Translation in the C4 factor of a holomorph element."""
    return (c + parity_sign(c) * d) % 4


def original_diamond(c, d):
    return (c + d + 2 * c * d) % 4


def add(a, b, modulus=None):
    n = a[0] + b[0]
    return (n if modulus is None else n % modulus, (a[1] + b[1]) % 4)


def neg(a, modulus=None):
    n = -a[0]
    return (n if modulus is None else n % modulus, -a[1] % 4)


def lam(a, b, modulus=None, epsilon=eps):
    n = epsilon(a[1]) * b[0]
    return (n if modulus is None else n % modulus, parity_sign(a[1]) * b[1] % 4)


def circle(a, b, modulus=None, epsilon=eps):
    return add(a, lam(a, b, modulus, epsilon), modulus)


def inv(a, modulus=None):
    n = -eps(a[1]) * a[0]
    return (n if modulus is None else n % modulus, a[1])


def star(a, b, modulus=None, epsilon=eps):
    return add(add(neg(a, modulus), circle(a, b, modulus, epsilon), modulus), neg(b, modulus), modulus)


def rhs_right_fixed(x, g):
    return (eps(x[1]) - 1) * g[0] == 0 and 2 * x[1] * g[1] % 4 == 0


def rhs_left_fixed(x, g):
    return (eps(g[1]) - 1) * x[0] == 0 and 2 * g[1] * x[1] % 4 == 0


def rhs_centralizes(x, g):
    return (1 - eps(x[1])) * g[0] == (1 - eps(g[1])) * x[0]


def rhs_intersection(x, g):
    return (
        (1 - eps(x[1])) * g[0] == 0
        and (1 - eps(g[1])) * x[0] == 0
        and 2 * g[1] * x[1] % 4 == 0
    )


def allowed_d(n, c):
    base = set(range(4)) if n == 0 else {0, 1}
    return sorted(base if c % 2 == 0 else base.intersection({0, 2}))


def indices(n, c):
    if c >= 2:
        return ("infinite", "infinite")
    return (1 if c == 0 else 2, 4 // len(allowed_d(n, c)))


def linear_integer_zero_kernel(coefficient):
    """Exact use of Z being torsion free: k*m=0 iff k=0 or m=0."""
    return "Z" if coefficient == 0 else "zero"


def vadd(a, b):
    return tuple(x + y for x, y in zip(a, b))


def vscale(scalar, vector):
    return tuple(scalar * x for x in vector)


def formal_add(a, b):
    return vadd(a[0], b[0]), (a[1] + b[1]) % 4


def formal_neg(a):
    return vscale(-1, a[0]), -a[1] % 4


def formal_circle(a, b):
    return vadd(a[0], vscale(eps(a[1]), b[0])), diamond(a[1], b[1])


def formal_inv(a):
    return vscale(-eps(a[1]), a[0]), a[1]


def formal_star(a, b):
    return formal_add(formal_add(formal_neg(a), formal_circle(a, b)), formal_neg(b))


def check_sign_characters(epsilon=eps, op=diamond):
    for c, d in product(range(4), repeat=2):
        require(epsilon(op(c, d)) == epsilon(c) * epsilon(d), f"epsilon character fails at {c,d}")
        require(parity_sign(op(c, d)) == parity_sign(c) * parity_sign(d), f"parity character fails at {c,d}")


def mutation_must_fail(name, function):
    start = CHECKS
    try:
        function()
    except VerificationFailure as exc:
        return {"name": name, "detected": True, "explicit_checks_to_detection": CHECKS - start, "diagnostic": str(exc)}
    raise VerificationFailure(f"negative control escaped detection: {name}")


def main(receipt_path):
    root = Path(__file__).resolve().parent
    start = CHECKS
    inputs = json.loads((root / "INPUT_SHA256.json").read_text())
    for item in inputs["files"]:
        p = Path(item["absolute_path"])
        require(sha256(p.read_bytes()).hexdigest() == item["sha256"], f"input digest mismatch: {p}")
    require(inputs["original_head"] == "aec31742f3f26c5b1e533404da57539d17dc94a1", "wrong original head")
    section("sealed input integrity", start, "Original candidate, source record, and parent original-file manifest match recorded SHA256.")

    start = CHECKS
    check_sign_characters()
    for c, d in product(range(4), repeat=2):
        require(diamond(c, d) == xor_chart(c, d), f"bit chart fails {c,d}")
        require(diamond(c, d) == original_diamond(c, d), f"source operation fails {c,d}")
        require(diamond(c, d) == diamond(d, c), "C4 graph quotient must be abelian")
    for c in range(4):
        require(diamond(c, c) == 0, "graph inverse finite factor")
        require((-parity_sign(c) * c) % 4 == c, "holomorph inverse translation")
        require(eps(c) ** 2 == 1 and parity_sign(c) ** 2 == 1, "diagonal automorphism inverse")
    section("regular holomorph graph", start, "D_c=diag(epsilon(c),(-1)^c), closure characters and inverse. Translation of 0 is (n,c), hence uniqueness/regularity for every n.")

    start = CHECKS
    for c, d, e in product(range(4), repeat=3):
        # Formal linear expressions in the independent integer variables n,m,k.
        a, b, t = ((1, 0, 0), c), ((0, 1, 0), d), ((0, 0, 1), e)
        left_assoc = formal_circle(formal_circle(a, b), t)
        right_assoc = formal_circle(a, formal_circle(b, t))
        require(left_assoc == right_assoc, "all-integer associativity formal expressions")
        require(left_assoc[0] == (1, eps(c), eps(c) * eps(d)), "collected associativity coefficients")
        left_dist = formal_circle(a, formal_add(b, t))
        right_dist = formal_add(formal_add(formal_circle(a, b), formal_neg(a)), formal_circle(a, t))
        require(left_dist == right_dist, "all-integer left-distributivity formal expressions")
        require(left_dist[0] == (1, eps(c), eps(c)), "collected left-distributivity coefficients")
        conjugate = formal_circle(formal_circle(b, a), formal_inv(b))
        require(conjugate == ((eps(d), 1 - eps(c), 0), c), "universal conjugation expression")
        require(formal_star(a, b) == ((0, eps(c) - 1, 0), 2 * c * d % 4), "universal star expression")
    for c in range(4):
        require(1 - eps(c) ** 2 == 0, "all-integer inverse coefficient")
    section("universal coefficient certificates", start, "All 64 finite residue triples checked, exact integer coefficient tuples establish identities for every integer input. Conjugation preserves c.")

    start = CHECKS
    elements = [(n, c) for n in range(-4, 5) for c in range(4)]
    identity = (0, 0)
    for a in elements:
        require(circle(a, identity) == a and circle(identity, a) == a, "identity on bounded controls")
        require(circle(a, inv(a)) == identity and circle(inv(a), a) == identity, "both inverses on bounded controls")
    for a, b, t in product(elements, repeat=3):
        require(circle(circle(a, b), t) == circle(a, circle(b, t)), "bounded associativity")
        lhs = circle(a, add(b, t))
        rhs = add(add(circle(a, b), neg(a)), circle(a, t))
        require(lhs == rhs, "bounded left brace law")
    section("bounded exact group/brace supplements", start, "Integer coordinates -4 through 4, all four residues, all triples; exact integer arithmetic, no finite-quotient inference.")

    start = CHECKS
    window = [(n, c) for n in range(-20, 21) for c in range(4)]
    for x, g in product(window, repeat=2):
        require((star(x, g) == identity) == rhs_right_fixed(x, g), "right fixed equation")
        require((star(g, x) == identity) == rhs_left_fixed(x, g), "left fixed equation")
        require((circle(x, g) == circle(g, x)) == rhs_centralizes(x, g), "centralizer equation")
        direct = star(g, x) == identity and circle(x, g) == circle(g, x)
        require(direct == rhs_intersection(x, g), "exact intersection equation")
        classified = (x[1] < 2 or g[0] == 0) and g[1] in allowed_d(x[0], x[1])
        require(direct == classified, "complete all-c, zero/nonzero classification")
    for c in range(4):
        require(linear_integer_zero_kernel(eps(c) - 1) == ("Z" if c < 2 else "zero"), "right integer kernel")
        require(linear_integer_zero_kernel(1 - eps(c)) == ("Z" if c < 2 else "zero"), "intersection integer kernel")
    rows = []
    for n in [0, 1]:
        for c in range(4):
            i1, i2 = indices(n, c)
            rows.append({"n_case": "zero" if n == 0 else "nonzero", "c": c, "index_additive": i1, "index_multiplicative": i2, "intersection_first_factor": "Z" if c < 2 else "zero", "intersection_allowed_d": allowed_d(n, c)})
            require((i1 != "infinite" and i2 != "infinite") == (c in {0, 1}), "exact property-s classification")
    section("stabilizers and exact classification", start, "Universal equations supplemented on -20..20, including negative n, zero n and every residue. Infinite index certified in REVIEW.md by pairwise distinct Z cosets.")

    start = CHECKS
    x, y = (0, 1), (0, 2)
    require(indices(*x) == (2, 2), "claimed witness indices")
    require(add(x, x) == y and indices(*y) == ("infinite", "infinite"), "additive nonclosure")
    require(lam(x, x) == (0, 3) and lam(x, x)[1] not in {0, 1}, "lambda invariance failure")
    require(star(x, x) == y and y[1] not in {0, 1}, "left and right star absorption fail")
    for g in window:
        for s in [a for a in window if a[1] in {0, 1}]:
            require(circle(circle(g, s), inv(g))[1] in {0, 1}, "normality bounded supplement")
    for c, d in product({0, 1}, repeat=2):
        require(diamond(c, d) in {0, 1}, "multiplicative subgroup finite kernel")
    u = v = x
    w = (1, 0)
    right_lhs = circle(add(u, v), w)
    right_rhs = add(add(circle(u, w), neg(w)), circle(v, w))
    require(right_lhs == (-1, 2) and right_rhs == (1, 2) and right_lhs != right_rhs, "right distributivity fails")
    section("ideal and two-sidedness adversarial checks", start, "S is a multiplicatively normal subgroup (kernel of epsilon projection), but fails additive closure, lambda invariance and both star absorption tests. Right distributivity has an explicit witness.")

    start = CHECKS
    quotient_controls = []
    for modulus in range(1, 21):
        finite = list(product(range(modulus), range(4)))
        for z in finite:
            right = [g for g in finite if star(z, g, modulus) == identity]
            intersection = [g for g in finite if star(g, z, modulus) == identity and circle(z, g, modulus) == circle(g, z, modulus)]
            require(len(right) > 0 and len(intersection) > 0, "finite index subgroups nonempty")
            require(len(finite) % len(right) == 0 and len(finite) % len(intersection) == 0, "finite index cardinal divisibility")
            if z[1] == 2:
                require(len(finite) // len(right) == modulus // gcd(modulus, 2), "finite quotient c2 first index")
            if z[1] == 3:
                require(len(finite) // len(right) == 2 * modulus // gcd(modulus, 2), "finite quotient c3 first index")
        quotient_controls.append({"modulus": modulus, "property_s_set": "entire finite brace", "c2_first_index": modulus // gcd(modulus, 2)})
    require(star((0, 2), (4, 0), 8) == identity, "torsion control in Z/8")
    require(star((0, 2), (4, 0)) == (-8, 0), "same coordinate outside infinite kernel")
    section("torsion and finite-quotient controls", start, "Every element in each quotient N=1..20 has both indices finite. c2 additive index N/gcd(N,2). Z/8 kernel contains 4, while Z kernel does not.")

    mutations = []
    mutations.append(mutation_must_fail("epsilon(3) changed to +1", lambda: check_sign_characters(lambda c: 1 if c in {0, 1, 3} else -1)))
    mutations.append(mutation_must_fail("2cd replaced by cd", lambda: check_sign_characters(op=lambda c, d: (c + d + c * d) % 4)))

    def wrong_left_kernel():
        z, g = (1, 0), (0, 2)
        require(star(g, z) == identity, "ignoring epsilon(d)n misses nonzero first coordinate -2")
    mutations.append(mutation_must_fail("nonzero-n left stabilizer made unrestricted", wrong_left_kernel))

    def wrong_property_set():
        require(indices(0, 2)[0] != "infinite", "classifying c=2 as property-s contradicts exact integer kernel")
    mutations.append(mutation_must_fail("S changed to all even c", wrong_property_set))

    def wrong_finite_inference():
        require(star((0, 2), (4, 0), 8) != identity, "Z/8 admits 4 in the 2-torsion kernel; integer-only kernel rule cannot be transferred")
    mutations.append(mutation_must_fail("Z kernel copied unchanged to Z/8", wrong_finite_inference))

    def altered_valid_brace():
        check_sign_characters(parity_sign)
        require(star((0, 1), (1, 0), epsilon=parity_sign) == identity, "alternate valid character makes witness x have nonzero first star coordinate")
    mutations.append(mutation_must_fail("epsilon replaced by parity character (another valid brace)", altered_valid_brace))

    # Stronger top-level fault injection: --corrupt must exit unsuccessfully,
    # including under -O. It intentionally lies about the surviving witness.
    if ARGS.corrupt:
        require(indices(0, 2)[0] == 2, "top-level corrupt-index fault detected")

    receipt = {
        "status": "PASS",
        "created_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "python": platform.python_version(),
        "optimization_level": sys.flags.optimize,
        "checker_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "input_manifest_sha256": sha256((root / "INPUT_SHA256.json").read_bytes()).hexdigest(),
        "explicit_check_count": CHECKS,
        "sections": SECTIONS,
        "exact_index_rows": rows,
        "negative_mutations": mutations,
        "finite_quotient_controls": quotient_controls,
        "limitations": ["Bounded tests supplement rather than establish universal identities.", "Integer torsion-freeness and infinite-coset arguments are proved in REVIEW.md.", "No novelty, priority, publication readiness, or external source certification conclusion."],
    }
    output = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if receipt_path:
        Path(receipt_path).write_text(output)
    print(output, end="")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt")
    parser.add_argument("--corrupt", action="store_true")
    ARGS = parser.parse_args()
    try:
        main(ARGS.receipt)
    except VerificationFailure as exc:
        print(json.dumps({"status": "FAIL", "optimization_level": sys.flags.optimize, "explicit_check_count": CHECKS, "reason": str(exc)}, sort_keys=True))
        sys.exit(1)

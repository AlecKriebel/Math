"""Fresh reviewer-2 arithmetic and pinned-source consistency checks."""
import hashlib
import itertools
import json
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
COMPANION = "Commuting-Division-Coefficient-Forms-and-the-Artinian-Eisenbud-Green-Harris-Conjecture-September-23-2026"

def convolution(a, q, h, modulus):
    return [sum(a[j] * q[i-j] for j in range(min(i, len(a)-1)+1)) % modulus
            for i in range(h+1)]

def has_bad_constant(a, p, v, h):
    modulus = p**v
    def extend(prefix):
        i = len(prefix)
        if i == h+1:
            return True
        known = sum(a[j] * prefix[i-j] for j in range(1, min(i, len(a)-1)+1))
        for coeff in range(modulus):
            if (a[0] * coeff + known) % modulus == 0:
                if extend(prefix + [coeff]):
                    return True
        return False
    return any(a[0] * q0 % modulus == 0 and extend([q0])
               for q0 in range(1, modulus))

tested = 0
for p, v, nu in itertools.product((2, 3), (1, 2), range(3)):
    modulus = p**v
    h = v*nu
    for a in itertools.product(range(modulus), repeat=nu+2):
        if any(a[j] % p for j in range(nu)) or a[nu] % p == 0:
            continue
        assert not has_bad_constant(a, p, v, h), (p, v, nu, a)
        tested += 1

threshold_examples = []
for p, v, nu in itertools.product((2, 3, 5), (2, 3), (1, 2, 3)):
    h = v*nu-1
    a = [p] + [0]*(nu-1) + [1]
    q = [0]*(h+1)
    for j in range(v):
        q[j*nu] = (-1)**j*p**(v-1-j)
    assert convolution(a, q, h, p**v) == [0]*(h+1)
    assert q[0] % (p**v)
    threshold_examples.append([p, v, nu, h])

orders = 0
from math import comb
for b, p in itertools.product(range(2, 81), (2, 3, 5, 7, 11, 13)):
    power = 1
    rest = b
    while rest % p == 0:
        rest //= p
        power *= p
    coeff = [(-1)**j * comb(b, j+1) % p for j in range(b)]
    assert next(j for j, c in enumerate(coeff) if c) == power-1
    orders += 1

geometry = 0
for h, s, r in itertools.product(range(2, 25), range(31), range(3, 10)):
    M = 2*h+4*s+10
    kappa = M+2*h
    c = M-2*s+1
    d = M*r-s
    assert 2*s+kappa-1 <= 2*M-2
    assert kappa <= 2*c-2
    assert d >= c
    geometry += 1

manifest = json.loads((PROJECT / "receipts/pinned_sources.json").read_text())
hashes = {}
for relative, expected in manifest["sha256"].items():
    if COMPANION not in relative or "/09-" in relative or relative.endswith("paper.pdf"):
        continue
    data = (PROJECT / relative).read_bytes()
    actual = hashlib.sha256(data).hexdigest()
    assert actual == expected, relative
    upstream_path = Path("/Users/alec/Desktop/math/preprints") / COMPANION / relative.split(COMPANION + "/", 1)[1]
    assert upstream_path.read_bytes() == data, str(upstream_path)
    hashes[relative] = actual

result = {
    "p_adic_all_A_countersearch_cases": tested,
    "sharpness_examples_below_threshold": threshold_examples,
    "A_b_Frobenius_orders": orders,
    "topology_range_cases": geometry,
    "pinned_source_and_actual_clone_match": hashes,
    "scope": "Finite arithmetic falsification checks; not a formalization of the theorem.",
}
out = Path(__file__).with_name("review_2_index_checks.json")
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({k: v for k, v in result.items() if k != "pinned_source_and_actual_clone_match"}))

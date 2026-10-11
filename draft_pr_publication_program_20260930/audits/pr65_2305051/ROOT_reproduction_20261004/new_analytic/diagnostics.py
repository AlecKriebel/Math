"""Independent bounded checks. These are diagnostics, not the universal proof."""
import cmath
import fractions
import hashlib
import itertools
import json
import math
import pathlib

OUT = pathlib.Path(__file__).resolve().parent

def children(left, middle, right):
    if middle == 0:
        return (0, 0, 0, 0)
    first = 1 if left >= middle else -1
    fourth = 1 if right > middle else -1
    for second, third in itertools.product((-1, 1), repeat=2):
        if first + second + third + fourth == 0:
            return tuple(middle + d for d in (first, second, third, fourth))
    raise AssertionError("No admissible pair")

def refine(v):
    return [a for j in range(len(v)) for a in children(v[j-1], v[j], v[(j+1) % len(v)])]

v = [1]
stages = []
for n in range(9):
    assert len(v) == 4**n
    assert sum(v) == len(v)
    assert min(v) >= 0 and max(v) <= n+1
    assert max(abs(v[j] - v[(j+1) % len(v)]) for j in range(len(v))) <= 2
    stages.append({"n": n, "N": len(v), "total": sum(v), "min": min(v), "max": max(v),
                   "nonzero": sum(a > 0 for a in v),
                   "sha256_integer_list": hashlib.sha256(json.dumps(v, separators=(",", ":")).encode()).hexdigest()})
    nv = refine(v)
    for j, value in enumerate(v):
        chunk = nv[4*j:4*j+4]
        assert sum(chunk) == 4*value
        assert all(a == 0 for a in chunk) if value == 0 else sorted(a-value for a in chunk) == [-1,-1,1,1]
    v = nv

local_cases = 0
for left, a, b, right in itertools.product(range(13), repeat=4):
    if max(abs(left-a), abs(a-b), abs(b-right)) > 2:
        continue
    ca, cb = children(left, a, b), children(a, b, right)
    assert min(ca + cb) >= 0
    assert abs(ca[-1] - cb[0]) <= 2
    local_cases += 1

# Exact rational second differences of H_n at sampled positions and scales.
# Dyadic samples across grid endpoints and circular origin include h << cell width.
v = [1]
zyg = []
Fraction = fractions.Fraction
for n in range(6):
    N = len(v)
    prefix = [0]
    for a in v:
        prefix.append(prefix[-1] + a-1)
    def H(x):
        x %= 1
        q = x*N
        j = q.numerator // q.denominator
        return Fraction(prefix[j], N) + (q-j)*Fraction(v[j]-1, N)
    largest = Fraction(0)
    count = 0
    for x in [Fraction(k, 37) for k in range(37)] + [Fraction(k, N) for k in range(min(N, 64))]:
        for h in [Fraction(1, d) for d in (2, 4, 7, 16, 31, 64, 257, 1024, 4096)]:
            ratio = abs(H(x+h)+H(x-h)-2*H(x))/h
            largest = max(largest, ratio)
            count += 1
    zyg.append({"n": n, "count": count, "max_sampled_second_difference_over_h": str(largest), "less_than_24": largest <= 24})
    v = refine(v)

# A required negative control: F_0 = (zeta+z)/(zeta-z), zeta=-1,
# so its Bloch expression on z=-r is 2*(1+r)/(1-r), diverging.
atomic_control = [{"r": r, "F0_Bloch_expression": 2*(1+r)/(1-r)} for r in (.5, .9, .99, .999, .9999)]
K = 12*math.pi*(math.pi**2+1)
result = {"status": "bounded_diagnostic_only_not_proof", "independent_implementation": True,
          "max_stage": 8, "stages": stages, "local_cases_0_to_12": local_cases,
          "sampled_Zygmund_Hn": zyg, "atomic_approximant_negative_control": atomic_control,
          "universal_bound_from_written_derivation": {"K": K, "Bloch_seminorm_upper_bound_20K": 20*K}}
(OUT / "DIAGNOSTIC_RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))

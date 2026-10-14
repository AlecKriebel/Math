"""Exact, independent arithmetic controls for the scope audit; no source mutation.

The all-real flow and asymptotic statements are proved in REPORT.md. Rational
controls below are reproducible falsification checks, not substitutes for them.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import datetime
import hashlib
import json

HERE = Path(__file__).resolve().parent
ORIGINAL = HERE.parent / "original_head_authentication_20261006"
count = 0


def require(value, reason):
    global count
    if not value:
        raise ValueError(reason)
    count += 1


def pin(path):
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def amplitude(s):
    return -(s - 1) * (s - 4) / (1 + s * s)


def amplitude_derivative(s):
    return (5 + 6 * s - 5 * s * s) / (1 + s * s) ** 2


def exterior_sums(rates):
    # Maximize over every coordinate blade, not a copied sorting calculation.
    return [max(sum(c, Q(0)) for c in combinations(rates, k)) for k in range(1, 6)]


def dimension(sums):
    nonnegative = [k for k, value in enumerate([Q(0)] + sums) if value >= 0]
    j = max(nonnegative)
    if j == 5:
        return Q(5)
    numerator = Q(0) if j == 0 else sums[j - 1]
    next_rate = sums[j] - numerator
    require(next_rate < 0, "pointwise dimension denominator")
    return Q(j) + numerator / (-next_rate)


source = json.loads((ORIGINAL / "SOURCE_STATEMENT.json").read_text())
require(source["id"] == 4900006, "problem id")
require(source["problem_number"] == "AMR-048-0006", "problem number")
require(source["statement"] == "For a smooth dissipative dynamical system with a global attractor, is the supremum of the local Lyapunov dimension on the attractor attained at an equilibrium or at an unstable periodic orbit contained in the attractor?", "literal immutable target")

candidate = ORIGINAL / "original_attempt" / "COUNTEREXAMPLE.md"
require(pin(candidate)["sha256"] == "a9ea8220014aed7c082c995023a3bc7cdd10014544a85376d99267d908323266", "candidate identity")
pdfs = {
    "eden1989.pdf": "e01e97ad093660750078ceec33acbeccaa67af3c62437086e48182a34e9f7078",
    "parker_goluskin_v2.pdf": "c8e53fbd26bd51b270deb81cf318161cb14f260ab827a0996d401fee899c6e7c",
    "kuznetsov_mokaev2018.pdf": "ed0ca54b5839cad99c88295b5b1a77bdeb6b7563bb8d2c7ccd412160bee7c168",
}
for name, expected in pdfs.items():
    require(pin(HERE / "private_primary_sources" / name)["sha256"] == expected, "primary PDF identity: " + name)

# The following cleared identities also have all-real nonnegative proofs in the
# report. Wide exact controls include the relevant endpoints and large radii.
controls = sorted({Q(i, 97) for i in range(1941)} | {Q(0), Q(1), Q(4)} | {Q(10**k) for k in range(7)})
for s in controls:
    f = amplitude(s)
    fp = amplitude_derivative(s)
    denominator = (1 + s * s) ** 2
    require(f + 4 == (3 * s * s + 5 * s) / (1 + s * s), "lower amplitude identity")
    require(Q(3, 2) - f == (Q(5, 2) * (s - 1) ** 2 + 3) / (1 + s * s), "upper amplitude identity")
    numerator = 5 * ((s - 1) ** 2 + s * s + s**4) + 3 * (s * s - 1) ** 2 + 10 * s**3
    require(8 - 2 * s * fp == numerator / denominator, "divergence identity")
    require(numerator >= 0, "nonnegative divergence certificate")
    require(Q(-4) <= f <= Q(3, 2), "amplitude control")
    require(2 * f + 2 * s * fp <= 11, "oscillator divergence control")
require(amplitude(Q(0)) == -4, "origin rate")
require(amplitude(Q(1)) + 2 * amplitude_derivative(Q(1)) == 3, "radius one radial rate")
require(amplitude(Q(4)) + 8 * amplitude_derivative(Q(4)) == Q(-24, 17), "radius two radial rate")

types = {"O": [Q(-4), Q(-4)], "U": [Q(3), Q(0)], "S": [Q(0), Q(-24, 17)]}
expected = {"OO": Q(0), "OU": Q(11, 4), "OS": Q(1), "UO": Q(11, 4), "UU": Q(203, 50), "US": Q(6827, 1700), "SO": Q(1), "SU": Q(6827, 1700), "SS": Q(2)}
table = {}
for left, right in product(types, repeat=2):
    key = left + right
    rates = types[left] + types[right] + [Q(-100)]
    sums = exterior_sums(rates)
    ky = dimension(sums)
    fixed = 4 + sums[3] / (sums[3] - sums[4])
    require(ky == expected[key], "pointwise dimension: " + key)
    require(sums[3] - sums[4] == 100, "fixed denominator: " + key)
    require(ky <= Q(203, 50) and fixed <= Q(203, 50), "global upper control: " + key)
    require((ky == Q(203, 50)) == (key == "UU"), "pointwise unique maximum type")
    require((fixed == Q(203, 50)) == (key == "UU"), "fixed-index unique maximum type")
    positive_indices = [k + 1 for k, value in enumerate(sums) if value > 0]
    if key in ["OO", "OS", "SO", "SS"]:
        require(positive_indices == [], "strict-positive zero-case index is empty")
    if key == "UU":
        require(max(positive_indices) == 4, "strict-positive torus index")
    if key in ["OU", "UO"]:
        require(max(positive_indices) == 2, "strict-positive unstable-circle index")
    table[key] = {"rates_unsorted": list(map(str, rates)), "leading_exterior_sums": list(map(str, sums)), "pointwise_dimension": str(ky), "fixed_j4_expression": str(fixed), "strict_positive_partial_sum_indices": positive_indices}

maxs = [max(Q(v["leading_exterior_sums"][k]) for v in table.values()) for k in range(5)]
require(maxs == list(map(Q, [3, 6, 6, 6, -94])), "global fixed index")
for key in ["OO", "OU", "OS", "UO", "SO"]:
    require(Q(table[key]["pointwise_dimension"]) < Q(203, 50), "all equilibrium/periodic pointwise candidates")
    require(Q(table[key]["fixed_j4_expression"]) < Q(203, 50), "all equilibrium/periodic fixed candidates")

# Hypothesis falsification controls: if the angular ratio is rational, a torus
# period exists, so the aperiodicity premise is essential. This does not claim
# robustness or genericity of the irrational-ratio example.
for p, q in [(1, 1), (2, 1), (3, 2), (7, 5)]:
    require(Q(q) * Q(p, q) == p, "rational-frequency periodic control")

result = {
    "schema": "pr111-independent-primary-scope-controls/v1",
    "completed_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "actual_pid": __import__("os").getpid(),
    "all_pass": True,
    "checks": count,
    "program_pin": pin(Path(__file__)),
    "candidate_pin": pin(candidate),
    "input_source_pin": pin(ORIGINAL / "SOURCE_STATEMENT.json"),
    "primary_pdf_pins": [pin(HERE / "private_primary_sources" / name) for name in pdfs],
    "ordered_type_table": table,
    "global_partial_sum_suprema": list(map(str, maxs)),
    "global_fixed_index": 4,
    "mandatory_source_correction": "Kuznetsov-Mokaev2018 printed equation5 uses strictly positive partial sums without specifying empty-index/zero-exponent conventions. Do not attribute the nonnegative-index OS=1 and SS=2 values to that printed formula. The torus and unstable-circle positive-leading cases agree.",
    "scope": "Literal imported assertion and later unrestricted Parker-Goluskin equation18 assertion; historical and strange/typical refinements are excluded.",
    "finite_controls_limit": "Global attraction, completeness, irrationality, derivative limits and directional exterior-norm reasoning are analytic deductions in REPORT.md, not inferred from finite controls.",
}
(HERE / "INDEPENDENT_SCOPE_CHECKS.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"all_pass": True, "checks": count, "actual_pid": result["actual_pid"]}))

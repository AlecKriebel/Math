"""Independent exact controls for the earlier Fourier/Dirichlet implication.

No candidate or external-paper program is imported. The analytic Fourier identity,
Holder inequality, and orthogonality argument are supplied in REPORT.md.
"""
from fractions import Fraction as F
from math import comb, factorial
import hashlib
import json
from pathlib import Path

CHECKS = []


def require(condition, label):
    if not condition:
        raise RuntimeError(label)
    CHECKS.append(label)


def mul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def power(a, n):
    out = [F(1)]
    for _ in range(n):
        out = mul(out, a)
    return out


def integrate(a, upper=F(1)):
    return sum(x * upper ** (i + 1) / (i + 1) for i, x in enumerate(a))


def iid_by_binomial(n):
    result = F(0)
    for k in range(n + 1):
        mass = [F(0)] * k + [F(comb(n, k))]
        mass = mul(mass, power([F(1), F(-1)], n - k))
        moment = power([F(k, n), F(-1)], 4)
        result += integrate(mul(mass, moment))
    return result


def energy(n):
    counts = [0] * (2 * n - 1)
    for a in range(n):
        for b in range(n):
            counts[a + b] += 1
    return sum(x * x for x in counts)


def bound(n, pi_upper):
    return F(2 * n * n + 1, 48 * n ** 3) / pi_upper ** 4


def iid(n):
    return F(3 * n - 1, 30 * n ** 3)


if __name__ == "__main__":
    for n in range(1, 81):
        require(energy(n) == F(2 * n ** 3 + n, 3), "orthogonality-energy-n=" + str(n))
    for n in range(1, 16):
        explicit = sum(a + b == c + d
                       for a in range(n) for b in range(n)
                       for c in range(n) for d in range(n))
        require(explicit == energy(n), "quadruple-enumeration-n=" + str(n))
    for n in range(1, 19):
        require(iid_by_binomial(n) == iid(n), "iid-binomial-beta-n=" + str(n))
    require(energy(3) == 19, "three-point-energy-is19")
    require(iid(3) == F(4, 405), "candidate-iid-three-point")
    require(bound(1000, F(4)) > iid(1000), "explicit-counterexample-n1000-pi-less4")
    require(bound(234, F(22, 7)) > iid(234), "sharper-counterexample-n234-pi-less22over7")
    # With pi^4 < U, a common positive denominator reduces the comparison to
    # 30(2n^2+1) - 48 U (3n-1)>0. Check shifted polynomial coefficients,
    # proving every real n>=234 after substituting n=234+t, t>=0.
    u = F(22, 7) ** 4
    n0 = 234
    shifted = [30 * (2 * n0 * n0 + 1) - 48 * u * (3 * n0 - 1),
               120 * n0 - 144 * u, F(60)]
    require(all(x > 0 for x in shifted), "all-n-ge234-positive-shifted-polynomial")
    # Independently integrate circular gap powers for the later preprint's
    # n=3 proof: gaps are z,z,1-2z on [0,1/2], reflected on the upper half.
    s2 = 2 * integrate([F(1), F(-4), F(6)], F(1, 2))
    s3 = 2 * integrate([F(1), F(-6), F(12), F(-6)], F(1, 2))
    phi1, phi2 = s2 / 2, s2 - s3 / 3
    require(s2 == F(1, 2), "later-preprint-gap-square-integral")
    require(s3 == F(5, 16), "later-preprint-gap-cube-integral")
    require(phi1 == F(1, 4), "later-preprint-phi1")
    require(phi2 == F(19, 48), "later-preprint-phi2")
    later_excess = F(4, 9) * (F(2, 5) - phi2)
    require(later_excess == F(1, 540), "later-preprint-exact-negative-margin")
    require(iid(3) + later_excess == F(19, 1620), "later-preprint-full-target-value")
    # Negative controls deliberately reject tempting law/normalization errors.
    negative_controls = {
        "replace-energy-with-iid-triple": energy(3) != 3 ** 2,
        "omit-normalization-n4": F(energy(3), 16) != F(energy(3), 16 * 3 ** 4),
        "Fourier-bound-alone-atn3-provesfailure": bound(3, F(22, 7)) <= iid(3),
        "replace-phi2-by-iid": phi2 != F(2, 5),
        "use-n233-as-certified-threshold": bound(233, F(22, 7)) <= iid(233),
    }
    for name, condition in negative_controls.items():
        require(condition, "negative-control:" + name)
    here = Path(__file__).resolve().parent
    out = {
        "status": "PASS", "check_count": len(CHECKS), "negative_controls": negative_controls,
        "implementation": "independent Python standard library, exact Fraction arithmetic, no asserts",
        "energy_identity": "(2n^3+n)/3", "fourier_lower_bound": "(2n^2+1)/(48*pi^4*n^3)",
        "iid_moment": "(3n-1)/(30*n^3)",
        "n1000_pi4_margin": str(bound(1000, F(4)) - iid(1000)),
        "n234_pi22over7_margin": str(bound(234, F(22, 7)) - iid(234)),
        "n234_shifted_positive_coefficients": [str(x) for x in shifted],
        "post_pr_phi2": str(phi2), "post_pr_excess": str(later_excess),
        "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "checks": CHECKS,
    }
    print(json.dumps(out, indent=2, sort_keys=True))

"""Independent finite algebra/asymptotic checks; these do not replace the proof."""
from fractions import Fraction
import json
import math
from pathlib import Path


def log_moment(n, q):
    alpha = (n - 2) / 2
    return (math.lgamma(alpha + 1) + math.lgamma(q / 2 + 1)
            - math.lgamma(q / 2 + alpha + 1))


def eigen_product(n, m):
    value = Fraction((-1) ** m, 1)
    for j in range(m):
        value *= Fraction(2 * j + 1, n - 1 + 2 * j)
    return value


def log_eigen(n, k):
    m = k / 2
    return (math.lgamma((n - 1) / 2) + math.lgamma(m + .5)
            - .5 * math.log(math.pi) - math.lgamma(m + (n - 1) / 2))


def log_lower_ratio(n, p, k, a=.5):
    return (math.log((k + n - 2) / (2 * k))
            + ((p - 1) / p) * math.log(1 - a)
            + log_moment(n, 2 * k) - log_eigen(n, k)
            - log_moment(n, p * (k - 1)) / p)


checks = []
for n in range(2, 13):
    for m in range(1, 30):
        product = float(abs(eigen_product(n, m)))
        ratio = math.exp(log_eigen(n, 2 * m))
        assert math.isclose(product, ratio, rel_tol=3e-13)
        if n == 2:
            assert product == 1
        if n == 4:
            assert eigen_product(n, m) == Fraction((-1) ** m, 2 * m + 1)
checks.append({"check": "exact product vs gamma formula", "cases": 319,
               "status": "passed", "circle_modulus": 1})

rates = []
for n in (3, 4, 5, 8, 12):
    for p in (1., 1.1, 1.5, 2., math.pi, 10., 100.):
        k0, k1 = 10000, 100000
        slope = (log_lower_ratio(n, p, k1) - log_lower_ratio(n, p, k0)) / math.log(k1/k0)
        alpha = (n - 2) / 2
        expected = alpha / p
        # The nonintegral p cases exercise the real-order expression unchanged.
        assert abs(slope - expected) < .003
        rates.append({"n": n, "p": p, "expected_exponent": expected,
                      "finite_range_log_slope": slope,
                      "lower_bound_at_k_100000": math.exp(log_lower_ratio(n, p, k1))})

# The explicit lower bound's asymptotic positive constant for amplitude a=.5.
constants = []
for n in (3, 4, 8):
    for p in (1., 2., math.pi, 100.):
        alpha = (n-2)/2
        c_lambda = math.gamma(alpha+.5) * (2**alpha) / math.sqrt(math.pi)
        constant = (.5 * (.5 ** ((p-1)/p)) *
                    (math.gamma(alpha+1) ** (1-1/p)) *
                    ((p/2) ** (alpha/p)) / c_lambda)
        k = 100000
        scaled = math.exp(log_lower_ratio(n, p, k) - alpha/p*math.log(k))
        assert math.isclose(constant, scaled, rel_tol=.0005)
        constants.append({"n": n, "p": p, "predicted_constant": constant,
                          "scaled_lower_bound": scaled})

out = {"purpose": "sanity checks of authored derivation, not proof of Wasserstein values",
       "checks": checks, "rates": rates, "asymptotic_constants": constants,
       "limitations": ["Computes the proved lower bound, not the optimal transport ratio.",
                       "Finite computations cannot establish a limit or historical priority.",
                       "No p=infinity conclusion is inferred."]}
Path(__file__).with_name("MECHANISM_CHECKS.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps({"status": "passed", "exact_cases": 319,
                  "real_p_rate_cases": len(rates), "constant_cases": len(constants)}))

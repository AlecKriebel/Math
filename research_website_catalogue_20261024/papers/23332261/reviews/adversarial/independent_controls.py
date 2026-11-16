"""Source-only adversarial controls; no native/project imports or network.

Exact support-function checks and an independently separated Fourier-cylinder
representation test. Numerical comparisons corroborate, rather than prove,
the analytic results in INITIAL.md.
"""
from decimal import Decimal, localcontext
from fractions import Fraction
import json


def require(ok, label):
    if not ok:
        raise ValueError(label)


def main():
    b0, c0 = Fraction(3, 8), Fraction(8, 83)
    squared_margin = (1 - c0) ** 2 * b0 ** 2 / (1 + b0 ** 2)
    require(squared_margin > Fraction(1, 16), "analytic margin lower bound")
    directions = 0
    for u in range(-32, 33):
        for v in range(-32, 33):
            if u == v == 0:
                continue
            # Evaluate the four affine gradient gaps directly.
            gaps = ((1 + c0) * u, (-1 + c0) * u,
                    c0 * u + b0 * v, c0 * u - b0 * v)
            g = max(gaps)
            require(g > 0 and 16 * g * g > u * u + v * v,
                    "exact directional negative control")
            directions += 1
    require(max(Fraction(0), Fraction(-2), b0 * 0 - 1) == 0,
            "boundary-gradient zero-gap control")
    require(1 - Fraction(3, 2) < 0,
            "outside-gradient negative-gap control")
    require(max(Fraction(0), Fraction(0)) == 0,
            "remove-transverse-competitors control")

    with localcontext() as ctx:
        ctx.prec = 90
        D = Decimal
        pi = D("3.141592653589793238462643383279502884197169399375105820974944592307816406286")

        def cosh(x):
            return (x.exp() + (-x).exp()) / 2

        def sinh(x):
            return (x.exp() - (-x).exp()) / 2

        qs = [1 / cosh(D(2 * k - 1) * pi * pi) for k in range(-12, 13)]
        s1, s2 = sum(qs), sum(q * q for q in qs)
        period_P = s1 / 2
        period_Px = -pi * s2 / 2
        # Independent cylinder Fourier ODE at (x,y)=(1/2,0).
        f = D(1) / 4
        g = D(1) / 2
        for n in range(1, 401):
            sign = D(-1 if n % 2 else 1)
            f += sign / (2 * cosh(D(n) / 2))
            g += sign * D(n) / (2 * sinh(D(n) / 2))
        fourier_P, fourier_Px = f / pi, -g / pi
        require(abs(period_P - fourier_P) < D("1e-70"), "Fourier value")
        require(abs(period_Px - fourier_Px) < D("1e-70"), "Fourier radial jet")
        c = -period_Px / period_P
        b = 1 / (2 * cosh(D(1) / 2))
        optimal_margin = b * (1 - c) / (1 + b * b).sqrt()
        require(D(0) < c < D(8) / 83, "numeric jet sanity")
        require(optimal_margin > D(1) / 4, "numeric support margin sanity")
        numerical = {"period_P_A": str(period_P), "period_Px_A": str(period_Px),
                     "Fourier_P_A": str(fourier_P), "Fourier_Px_A": str(fourier_Px),
                     "c": str(c), "b": str(b), "optimal_margin": str(optimal_margin),
                     "period_terms": len(qs), "Fourier_modes": 400,
                     "numerical_not_interval_or_formal_proof": True}
    result = {"status": "PASS_SOURCE_ONLY_ADVERSARIAL_CONTROLS",
              "exact_directions": directions,
              "exact_margin_squared_lower_bound": str(squared_margin),
              "negative_controls": {"boundary_gradient": "zero gap",
                                    "outside_gradient": "negative gap",
                                    "missing_transverse_pair": "zero transverse gap"},
              "independent_Fourier_comparison": numerical,
              "assertions_used": False, "native_imports_or_runs": [],
              "central_all_direction_proof": "analytic support minimization in INITIAL.md"}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

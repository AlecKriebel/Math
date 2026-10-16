#!/usr/bin/env python3
"""Independent CAS certificates. No imports from either frozen verifier.

All arithmetic is symbolic or exact over QQ(i). `require` remains active
under optimized Python. Finite checks supplement the universal arguments.
"""
import argparse
import json
from itertools import product

import sympy as s


def require(condition, message):
    if not condition:
        raise ValueError(message)


def iszero(expr):
    return s.expand(expr) == 0


def signature(expr, x):
    p = s.Poly(expr, x, extension=s.I)
    if p.is_zero:
        return "ALL_C"
    if p.degree() == 0:
        return "EMPTY"
    return p.sqf_part().monic().as_expr()


def implies_on_fiber(source, target, x):
    sig = signature(source, x)
    if sig == "ALL_C":
        return iszero(target)
    if sig == "EMPTY":
        return True
    return s.Poly(target, x, extension=s.I).rem(s.Poly(sig, x, extension=s.I)).is_zero


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inject-fault", choices=["polynomial_factorial", "lambda_relation"])
    args = parser.parse_args()
    x, z, z0, b = s.symbols("x z z0 b")
    lam, t = s.symbols("lambda t")
    stats = {}
    # Focused mutation probes avoid repeating the full unmodified control box.
    if args.inject_fault == "lambda_relation":
        bad_relation = s.Poly(lam**2-s.Rational(1,2),lam)
        require(s.Poly(lam**3+lam/2,lam).rem(bad_relation).is_zero,
                "injected positive lambda relation is false")

    # Symbolic parameters b,z0 establish the identity for complex parameters,
    # without choosing or numerically approximating the roots of a fiber.
    for k in range(2, 15):
        denom = s.factorial(k) + (1 if args.inject_fault == "polynomial_factorial" else 0)
        f = b * (z-z0)**k / denom
        fp = s.diff(f, z)
        require(iszero(s.diff(f, z, k)-b), f"kth-derivative identity k={k}")
        require(iszero(fp - b*(z-z0)**(k-1)/s.factorial(k-1)), f"first derivative k={k}")
        require(s.degree(f, z) == k and s.degree(fp, z) == k-1, f"degrees k={k}")
        require(iszero(f.subs(z,z0)) and iszero(fp.subs(z,z0)), f"zero k={k}")
        # f'/b-1 has exactly k-1 roots and no repeated root in C.
        fiber = s.Poly(x**(k-1)-s.factorial(k-1), x)
        require(s.gcd(fiber, fiber.diff()).degree() == 0, f"squarefree b-fiber k={k}")
    stats["symbolic_complex_parameter_family_orders"] = [2,14]

    # Non-monomial complex-coefficient box: use a CAS squarefree support,
    # not the rational coefficient-array code in either original verifier.
    count = sharing = passed = implications = 0
    values = [-1, 0, s.I]
    for degree in range(1,5):
        for low in product(values, repeat=degree):
            for lead in [s.Integer(1), s.I]:
                f = sum(c*x**j for j,c in enumerate(low)) + lead*x**degree
                fp = s.diff(f,x)
                count += 1
                for a in [0,1,s.I]:
                    if signature(f-a,x) != signature(fp-a,x):
                        continue
                    sharing += 1
                    require(a == 0, "nonzero-a polynomial H1")
                    require(s.degree(signature(f,x),x) == 1, "multiple root supports")
                    for k in range(2,7):
                        fk = s.diff(f,x,k)
                        for bv in [1,s.I,2,6,24]:
                            actual = implies_on_fiber(fp-bv,fk-bv,x)
                            expected = degree == k and iszero(fk-bv)
                            require(actual == expected, f"classification: {f},a={a},b={bv},k={k}")
                            implications += 1
                            passed += int(actual)
    stats["gaussian_coefficient_box"] = {"polynomials":count,"H1_pairs":sharing,
        "H2_checks":implications,"admissible":passed,"degree_range":[1,4]}

    # Exact, non-real translations and scales; nearby wrong coefficients,
    # derivative orders, and orders beyond the degree must all be rejected.
    monomial = positives = negatives = 0
    for n in range(2,9):
        for bv in [s.I,1+s.I,s.Rational(2,3)-s.I/5]:
            for shift in [s.I,2-s.I]:
                for correct_scale in [True,False]:
                    scale = bv/s.factorial(n) * (1 if correct_scale else 2)
                    f = scale*(x-shift)**n
                    fp = s.diff(f,x)
                    require(signature(f,x) == signature(fp,x), "translated H1")
                    for k in range(2,11):
                        actual = implies_on_fiber(fp-bv,s.diff(f,x,k)-bv,x)
                        expected = k == n and correct_scale
                        require(actual == expected, "Gaussian monomial order or coefficient")
                        monomial += 1
                        positives += int(actual)
                        negatives += int(not actual)
    stats["gaussian_translated_monomials"] = {"checks":monomial,"positive":positives,"negative":negatives}

    # These special branches distinguish empty fibers from ALL_C. They also
    # test b=0 as a deliberate out-of-scope value, exposing its necessity.
    boundaries = 0
    for const in [0,1,s.I]:
        for av in [0,1,s.I]:
            actual = signature(const-av,x) == signature(-av,x)
            expected = (const == 0) if av == 0 else (const != av)
            require(actual == expected, "constant H1")
            require(implies_on_fiber(-s.I,-s.I,x), "constant H2 vacuity")
            boundaries += 1
    for slope in [1,s.I]:
        for av in [0,1,s.I]:
            require(signature(slope*x+1-av,x) != signature(slope-av,x), "linear H1")
            boundaries += 1
    require(signature(0,x) == "ALL_C" and signature(1,x) == "EMPTY", "identity sentinel")
    require(implies_on_fiber(s.diff(x**3,x),s.diff(x**3,x,2),x), "out-of-scope b=0 boundary")
    require(not implies_on_fiber(s.diff(x**3,x)-1,s.diff(x**3,x,2)-1,x), "b!=0 negative")
    # H1 ignores multiplicities but CM does not: inspect the exact orders.
    require(s.Poly(x**2/2,x).terms()[0][0][0] == 2, "quadratic order")
    require(s.Poly(s.diff(x**2/2,x),x).terms()[0][0][0] == 1, "derivative order")
    require(signature(x**2/2,x) == signature(x,x), "quadratic IM")
    require(signature(x**2/2,x) != signature(x-1,x), "invalid additive shift")
    stats["constant_and_linear_boundary_cases"] = boundaries

    trans = 0
    for k in range(3,46):
        # Differentiate the actual composition exp(lambda*z), not theta arrays.
        actual_derivative = s.diff((s.exp(lam*z)-1)**2,z,k).expand()
        closed = lam**k*(2**k*s.exp(2*lam*z)-2*s.exp(lam*z))
        require(iszero(actual_derivative-closed), f"transcendental derivative k={k}")
        q = -s.Rational(1,2**(k-1)-2)
        if args.inject_fault == "lambda_relation":
            q = -q
        relation = s.Poly(lam**(k-1)-q,lam)
        residual_at_half = lam**k*(2**(k-2)-1)+lam/2
        require(s.Poly(residual_at_half,lam).rem(relation).is_zero, f"lambda quotient k={k}")
        fp_minus_b = 2*lam*t*(t-1)+lam/2
        require(iszero(fp_minus_b-2*lam*(t-s.Rational(1,2))**2), "b-fiber factorization")
        residual = q*(2**k*t*t-2*t)+s.Rational(1,2)
        require(iszero(residual.subs(t,s.Rational(1,2))), "value implication")
        require(not iszero(s.diff(residual,t).subs(t,s.Rational(1,2))), "simple higher derivative b-point")
        require(not s.Poly(residual,t).rem(s.Poly((t-s.Rational(1,2))**2,t)).is_zero,
                "reject multiplicity-dominating implication")
        require(not iszero(residual_at_half.subs(lam,1)), "lambda=1 negative control")
        trans += 1
    require(iszero((4*t*t-2*t).subs(t,s.Rational(1,2))), "k=2 derivative at half")
    require(not iszero(lam/2), "k=2 obstruction lambda!=0")
    stats["transcendental_orders"] = {"count":trans,"range":[3,45]}
    # Root-proposed routine scaling corollary, separate from frozen claims.
    # Let B be an arbitrary specified nonzero complex value and A=-2*B/lambda.
    B,A = s.symbols("B A")
    scaled_fp_minus_B = (2*A*lam*t*(t-1)-B).subs(A,-2*B/lam)
    require(iszero(scaled_fp_minus_B-2*(-2*B/lam)*lam*(t-s.Rational(1,2))**2),
            "arbitrary-b scaled factorization")
    for k in range(3,16):
        q = -s.Rational(1,2**(k-1)-2)
        value_minus_B = A*lam*q*(2**(k-2)-1)-B
        require(iszero(value_minus_B.subs(A,-2*B/lam)), "arbitrary-b scaled value")
    stats["root_proposed_routine_scaling_corollary_orders"] = [3,15]
    print(json.dumps({"status":"PASS","arithmetic":"SymPy exact symbolic polynomials and QQ(i)",
        "sympy_version":s.__version__,"checks":stats,
        "scope":"Mathematical certificates only; no source interpretation or novelty decision",
        "limits":"Finite controls accompany the universal proof in INDEPENDENT_DERIVATION.md"},
        indent=2,sort_keys=True))


if __name__ == "__main__":
    main()

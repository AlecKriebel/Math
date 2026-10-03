#!/usr/bin/env python3
"""Independent exact controls for the frozen polar-zonoid partial note.

No remote reads and no writes to the public package. Requires installed SymPy.
The cube density is recomputed by a cardinal B-spline recurrence rather than
the public alternating-sum implementation. Transform constants are recomputed
by exact Funk--Hecke moments rather than assuming the differential identity.
"""
from fractions import Fraction as F
from functools import lru_cache
from math import comb, factorial
from pathlib import Path
import argparse
import hashlib
import json

import sympy as s

HERE = Path(__file__).resolve().parent
PUBLIC = HERE.parents[1] / "public"


@lru_cache(None)
def uniform_sum_density(n, twice_x):
    """Density for n independent Uniform[0,1] variables at x=twice_x/2."""
    x = F(twice_x, 2)
    if n == 1:
        return F(0 <= x < 1)
    if x < 0 or x > n:
        return F(0)
    return (x * uniform_sum_density(n - 1, twice_x)
            + (n - x) * uniform_sum_density(n - 1, twice_x - 2)) / (n - 1)


def cube_controls():
    # Independent exact convolution of Rademacher variables for gamma.
    walk = {0: 1}
    results = {}
    for n in range(1, 65):
        nxt = {}
        for position, weight in walk.items():
            for step in (-1, 1):
                nxt[position + step] = nxt.get(position + step, 0) + weight
        walk = nxt
        if n < 3:
            continue
        gamma = F(sum(abs(k) * v for k, v in walk.items()), n)
        assert gamma == 2 * comb(n - 1, (n - 1) // 2)
        density = uniform_sum_density(n, n)
        assert density > 0
        diagonal_F = 1 / (2 ** (n - 1) * density)
        denominator = sum((-1) ** j * comb(n, j) * (n - 2*j) ** (n - 1)
                          for j in range(n // 2 + 1))
        assert diagonal_F == F(factorial(n - 1), denominator)
        witness = 2**n * diagonal_F - gamma * n / 2**(n - 1)
        assert witness == 0 if n == 4 else witness < 0
        results[str(n)] = str(witness)
    assert results["3"] == "-1/3"
    public = json.loads((PUBLIC / "exact_results.json").read_text())
    for n, value in public["cube_sample_values"].items():
        assert results[n] == value
    # For |x| >= |y| >= |z|, the four diagonal forms reduce to two cases.
    # This proves P(x)=4 max(2 ||x||_infinity - ||x||_1, 0) in dimension 3.
    x, y, z = s.symbols("x y z", real=True)
    first_three = (x+y+z) + (x+y-z) + (x-y+z)
    dominant = s.expand(2*(first_three + x-y-z) - 4*(x+y+z))
    nondominant = s.expand(2*(first_three - x+y+z) - 4*(x+y+z))
    assert dominant == 4*(x-y-z)
    assert nondominant == 0
    return {"dimensions": [3, 64], "all_witnesses": results,
            "three_dimensional_polynomial": "4*max(2*max(abs(x))-sum(abs(x)),0)"}


def beta_abs_moment(j, b):
    # Integral from -1 to 1 of |t| t^(2j) (1-t^2)^(b-1) dt.
    # u=t^2 gives Beta(j+1,b)=j!/[b(b+1)...(b+j)].
    return s.factorial(j) / s.prod(b+k for k in range(j+1))


def transform_controls():
    t = s.symbols("t", real=True)
    count = 0
    for n in range(3, 13):
        m = n-1
        alpha = s.Rational(n-2, 2)
        for degree in range(0, 31, 2):
            poly = s.Poly(s.gegenbauer(degree, alpha, t), t)
            pole_value = poly.eval(1)
            # Divide both transform eigenvalues by A=area(S^(n-2)).
            r = poly.eval(0) / pole_value
            c = sum(coefficient * beta_abs_moment(power[0]//2, s.Rational(m, 2))
                    for power, coefficient in poly.terms()) / pole_value
            c = s.factor(c)
            assert c != 0 and r != 0
            eigenvalue = -degree*(degree+n-2)
            assert s.simplify((eigenvalue+m)*c - 2*r) == 0
            # f_s=m/(A+s*A*r*q). C^-1 eigenvalue is 1/(A*c).
            # mu'_0/mu_0 = -2r/(m*c), independently from the moment integrals.
            ratio = -2*r/(m*c)
            assert s.simplify(ratio - (degree*(degree+n-2)-m)/s.Integer(m)) == 0
            if n == 4:
                assert r == s.Rational((-1)**(degree//2), degree+1)
            if degree == 0:
                assert c == s.Rational(2, m)
            count += 1
    # S^3 direct zonal inversion: R[t^(2j)](s)=4*pi*(1-s^2)^j/(2j+1).
    # 1/(4*pi) d/dt[t*f(sqrt(1-t^2))] must recover t^(2j).
    for j in range(16):
        f_composed = 4*s.pi*t**(2*j)/s.Integer(2*j+1)
        assert s.diff(t*f_composed, t)/(4*s.pi) == t**(2*j)
    # Ball radial function 1: rho_IB=4*pi/3; C[1]=8*pi/3.
    ball_density = (3/(4*s.pi))/(8*s.pi/3)
    assert ball_density == 9/(32*s.pi**2)
    return {"funk_hecke_dimension_degree_pairs": count,
            "dimensions": [3, 12], "even_degrees": [0, 30],
            "S3_radon_inverse_monomials": 16,
            "S3_unit_ball_generating_density": str(ball_density)}


def flat_cap_controls():
    t, b, h = s.symbols("t b h", positive=True)
    # Integrate H'=b^3/t^3 with the arbitrary boundary value H(1)=h.
    H = h + b**3*(1-t**-2)/2
    assert s.simplify(s.diff(H,t) - b**3/t**3) == 0
    G = s.diff(t**2/H, t)
    jet = s.factor((s.diff(G,t)-G).subs(t,1))
    assert jet == 2*b**6/h**3
    density = 3/(32*s.pi**2)*((1-t*t)*s.diff(G,t,2)-3*t*s.diff(G,t)+3*G)
    endpoint = s.factor(density.subs(t,1))
    assert endpoint == -9*b**6/(16*s.pi**2*h**3)
    return {"Gprime_minus_G_at_1": str(jet), "generating_density_at_1": str(endpoint),
            "sign": "strictly negative for all b>0 and h>0"}


def cylinder_controls():
    t, z = s.symbols("t z", positive=True)
    rho_lower = (1-t*t)**s.Rational(-1,2)
    rho_upper = 1/t
    switch = s.sqrt(2)/2
    # Exact antiderivatives are checked by differentiation, then evaluated.
    lower_h_primitive = t/s.sqrt(1-t*t)
    lower_k_primitive = t**3/(3*(1-t*t)**s.Rational(3,2))
    upper_h_primitive = -1/(4*t**4)+1/(2*t*t)
    upper_k_primitive = -1/(2*t*t)
    pairs = [(lower_h_primitive, rho_lower**5*(1-t*t)),
             (lower_k_primitive, rho_lower**5*t*t),
             (upper_h_primitive, rho_upper**5*(1-t*t)),
             (upper_k_primitive, rho_upper**5*t*t)]
    for primitive, integrand in pairs:
        assert s.simplify(s.diff(primitive,t)-integrand) == 0
    h_lower = s.simplify(lower_h_primitive.subs(t,switch)-lower_h_primitive.subs(t,0))
    k_lower = s.simplify(lower_k_primitive.subs(t,switch)-lower_k_primitive.subs(t,0))
    h_upper = s.simplify(upper_h_primitive.subs(t,1)-upper_h_primitive.subs(t,switch))
    k_upper = s.simplify(upper_k_primitive.subs(t,1)-upper_k_primitive.subs(t,switch))
    assert (h_lower,h_upper,k_lower,k_upper) == (1,s.Rational(1,4),s.Rational(1,3),s.Rational(1,2))
    h, k = h_lower+h_upper, k_lower+k_upper
    assert h == s.Rational(5,4) and k == s.Rational(5,6)
    assert h-2*k*k == -s.Rational(5,36)
    return {"h": str(h), "k": str(k), "h_r1_minus_2k2": str(h-2*k*k),
            "antiderivative_checks": 4}


def frozen_manifest_control():
    manifest = json.loads((PUBLIC/"FROZEN_AUTHOR_MANIFEST.json").read_text())
    for entry in manifest["public_files"]:
        data = (PUBLIC/entry["name"]).read_bytes()
        assert len(data) == entry["bytes"]
        assert hashlib.sha256(data).hexdigest() == entry["sha256"]
    return {"all_six_manifest_entries_match": True}


def main():
    global PUBLIC
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--author-dir", type=Path, default=PUBLIC,
                        help="Directory containing the frozen author files")
    PUBLIC = parser.parse_args().author_dir.resolve()
    result = {"status": "PASS", "arithmetic": "exact rational and symbolic; no numerical sampling",
              "cube": cube_controls(), "transforms_and_harmonic_derivative": transform_controls(),
              "flat_cap": flat_cap_controls(), "cylinder": cylinder_controls(),
              "frozen_package": frozen_manifest_control(),
              "scope": "Calculation audit only. Full genericity target remains unresolved."}
    output = json.dumps(result,indent=2)+"\n"
    (HERE/"independent_results.json").write_text(output)
    print(output,end="")


if __name__ == "__main__":
    main()

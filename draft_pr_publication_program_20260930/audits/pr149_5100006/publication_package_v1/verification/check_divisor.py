#!/usr/bin/env python3
"""Independent adversarial diagnostics; no submission code is imported.

Exact checks use Fraction cosets. Complex diagnostics use the standard-library
theta-series definition of Jacobi functions, rather than the submitted verifier.
Numerical agreement is supplementary, never the proof of all-period constancy.
"""

import sys
if sys.flags.optimize:
    raise RuntimeError("Run these diagnostic checks without Python optimization (-O).")

from collections import Counter
from fractions import Fraction
import cmath
import json
import math
from pathlib import Path


def exact_coset_check(m, tau):
    # Coordinates are divided by 2K; imaginary p cancels in comparisons.
    delta = Fraction(tau, m)
    v = delta / 2
    poles = Counter((-j * delta) % 1 for j in range(m))
    zeros = Counter()
    for sign in [-1, 1]:
        zeros.update((Fraction(1, 2) + sign * v - j * delta) % 1
                     for j in range(m))
    return poles, zeros


def complete_K(k):
    a, b = 1.0, math.sqrt((1-k) * (1+k))
    for _ in range(80):
        an, bn = (a+b)/2, math.sqrt(a*b)
        if abs(an-bn) < 1e-15 * an:
            return math.pi / (2*an)
        a, b = an, bn
    raise ArithmeticError("AGM did not converge")


def theta(n, z, q):
    if n in [1, 2]:
        result = 0j
        for j in range(100):
            coeff = 2 * q ** ((j+0.5)**2)
            if coeff == 0.0:
                break
            result += coeff * ((-1)**j * cmath.sin((2*j+1)*z)
                               if n == 1 else cmath.cos((2*j+1)*z))
        return result
    result = 1+0j
    for j in range(1, 100):
        coeff = 2 * q ** (j*j)
        if coeff == 0.0:
            break
        result += coeff * ((-1)**j if n == 4 else 1) * cmath.cos(2*j*z)
    return result


class Jacobi:
    def __init__(self, k):
        self.k = k
        self.K = complete_K(k)
        self.Kp = complete_K(math.sqrt((1-k)*(1+k)))
        self.q = math.exp(-math.pi*self.Kp/self.K)
        self.t2, self.t3, self.t4 = [theta(n, 0, self.q) for n in [2,3,4]]

    def scd(self, u):
        z = math.pi*u/(2*self.K)
        den = theta(4, z, self.q)
        return (self.t3/self.t2 * theta(1,z,self.q)/den,
                self.t4/self.t2 * theta(2,z,self.q)/den,
                self.t4/self.t3 * theta(3,z,self.q)/den)


def norm(fn, u, delta, m):
    result = 1+0j
    for j in range(m):
        result *= fn(u+j*delta)
    return result


def main():
    exact_cases = 0
    primitive_stars = 0
    even_failures = 0
    for m in range(3, 102):
        for tau in range(1,m):
            if math.gcd(tau,2*m) != 1:
                continue
            poles, zeros = exact_coset_check(m,tau)
            assert len(poles) == m and set(poles.values()) == {1}
            if m % 2:
                assert zeros == Counter({p:2 for p in poles})
                exact_cases += 1
                primitive_stars += tau > 1
            else:
                assert not (poles.keys() & zeros.keys())
                even_failures += 1

    numeric = []
    for k in [0.01, 0.3, 0.7, 0.99, 0.9999]:
        J = Jacobi(k)
        for m,tau in [(3,1),(5,1),(5,3),(7,5),(11,9),(25,23)]:
            v, delta = J.K*tau/m, 2*J.K*tau/m
            sv,cv,dv = J.scd(v)
            a, b, c = (dv/cv).real, (math.sqrt(1-k*k)/cv).real, k
            ratio = (c/a)**2
            F = lambda u: 1 - ratio*J.scd(u)[0]**2
            phases = [0, 0.193*J.K, 0.739*J.K,
                      0.251*J.K+0.127j*J.Kp,
                      0.691*J.K+0.333j*J.Kp]
            reference = norm(F,0,delta,m)
            # Limit at the double pole from independent leading coefficients.
            h_plus, h_minus = (m+1)//2, (m-1)//2
            derivative_magnitude = 2*(1-k*k)*sv*dv/(a*a*cv**3)
            pole_limit = derivative_magnitude**2/(a*a)
            for j in range(1,m):
                if j not in [h_plus,h_minus]:
                    pole_limit *= 1-1/(a*a*J.scd(j*delta)[0]**2)
            pole_limit_error = abs(pole_limit-reference)
            max_difference = max(abs(norm(F,u,delta,m)-reference)
                                 for u in phases)
            zero_residual = max(abs(F(1j*J.Kp+J.K+sgn*v))
                                for sgn in [-1,1])
            # Directly compare the original 2m positive-distance products.
            real_focal_errors = []
            for u in phases[:3]:
                pp = math.prod(a+c*J.scd(u+j*delta)[0].real
                               for j in range(2*m)) / a**(2*m)
                pm = math.prod(a-c*J.scd(u+j*delta)[0].real
                               for j in range(2*m)) / a**(2*m)
                real_focal_errors += [abs(pp-reference), abs(pm-reference)]
            # Independently reconstruct caustic chord tangency from theta data.
            t = 0.311*J.K
            st,ct,_ = J.scd(t)
            line_errors = []
            for z in [t-v,t+v]:
                sz,cz,_ = J.scd(z)
                x,y = -a*sz,b*cz
                line_errors.append(abs(-st*x+ct*y/math.sqrt(1-k*k)-1))
            numeric.append({"k":k,"m":m,"tau":tau,
                            "norm_max_absolute_error":max_difference,
                            "zero_max_absolute_error":zero_residual,
                            "focal_max_absolute_error":max(real_focal_errors),
                            "chord_tangency_max_error":max(line_errors),
                            "regularized_pole_limit_error":pole_limit_error,
                            "normalized_constant_real":reference.real})
            assert max_difference < 2e-9
            assert zero_residual < 2e-8
            assert max(real_focal_errors) < 2e-9
            assert max(line_errors) < 2e-9
            assert pole_limit_error < 2e-8

    # Two adversarial controls outside the exact theorem's primitive parity.
    # N=4 cannot have the required divisor cancellation.
    # A primitive triangle repeated twice has stated N=6 but remains period 3.
    controls=[]
    J=Jacobi(0.7)
    for n,tau,label in [(4,1,"primitive_N4"),(3,1,"primitive_N3_repeated_twice")]:
        v=2*J.K*tau/n
        delta=2*v
        _,cv,dv=J.scd(v)
        a=(dv/cv).real
        vals=[]
        count=n if n==4 else 2*n
        for u in [0,0.311*J.K,0.733*J.K]:
            vals.append(math.prod(1+(0.7/a)*J.scd(u+j*delta)[0].real
                                  for j in range(count)))
        controls.append({"label":label,"normalized_focal_products":vals,
                         "range":max(vals)-min(vals)})
        assert max(vals)-min(vals) > 1e-5

    result={"status":"PASS with scoped boundary controls",
            "exact_primitive_odd_m_cases":exact_cases,
            "exact_primitive_star_cases":primitive_stars,
            "even_m_disjoint_divisor_controls":even_failures,
            "theta_diagnostics":numeric,"outside_scope_controls":controls,
            "interpretation":"Exact coset arithmetic checks finite cases. The accompanying manuscript focal_product_period_criterion.tex (and separately deposited PDF) establishes every admissible period. Theta diagnostics are floating-point supplementary evidence, not validated numerics or proof."}
    Path(__file__).with_name("independent_results.json").write_text(
        json.dumps(result,indent=2)+"\n")
    print(json.dumps({"status":result["status"],
                      "exact_primitive_odd_m_cases":exact_cases,
                      "exact_primitive_star_cases":primitive_stars,
                      "even_m_disjoint_divisor_controls":even_failures,
                      "theta_diagnostic_cases":len(numeric),
                      "max_norm_error":max(x["norm_max_absolute_error"] for x in numeric),
                      "max_zero_error":max(x["zero_max_absolute_error"] for x in numeric),
                      "outside_scope_controls":controls},indent=2))


if __name__ == "__main__":
    main()

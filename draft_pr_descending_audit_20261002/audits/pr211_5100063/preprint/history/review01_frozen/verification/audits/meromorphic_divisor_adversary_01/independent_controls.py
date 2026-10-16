#!/usr/bin/env python3
"""Separately authored controls, after the frozen independent derivation.

Exact identities/lattice enumeration are checkable finite controls. All complex
floating-point tests below are diagnostics, not a proof of the universal claim.
No submitted or inherited Python module is imported or read.
"""
from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
import sys
import sympy as S
import mpmath as M

BASE = Path(__file__).parent
OUTPUT = BASE / "CONTROL_RESULTS.json"


def symbolic_controls():
    k, h, C, d, s, x, y, alpha, kc = S.symbols("k h C d s x y alpha kc")
    q, t = 1-h*h, h*h
    W = 1-k*k*t*t
    U = 1-2*k*k*t+k*k*t*t
    V = 1-2*t+k*k*t*t
    T = 1-k*k*t*s*s
    H1 = d+k*C*s
    L0 = (U*U-k*k*V*V*t)/d
    L1 = (V*V-U*U*t)/C
    H2 = L0+k*L1*s
    rules = [(x, 1-s*s), (y, 1-k*k*s*s),
             (C, q), (d, 1-k*k*t), (kc, 1-k*k)]

    def reduced(expr):
        num = S.cancel(expr).as_numer_denom()[0]
        num = S.expand(num)
        for z, z2 in rules:
            num = S.rem(num, z*z-z2, z)
        return S.factor(num)

    sm = (s*C*d-h*x*y)/T
    sp = (s*C*d+h*x*y)/T
    cm = (x*C+s*y*h*d)/T
    cp = (x*C-s*y*h*d)/T
    A, B, c = alpha*d*d/q, alpha*kc/q, alpha*k
    det = ((-A*sm-c)*B*cp-(-A*sp-c)*B*cm)/2
    distance = (-A*s-c)**2+(B*x)**2
    Z = W*W-4*k*k*t*t*q*d*d
    D3, C3 = U*W-2*k*k*t*q*V, V*W-2*t*d*d*U
    checks = {
        "focal_distance_factorization": distance-alpha**2/q**2*(1+k*s)*(U+k*V*s),
        "inverse_edge_determinant": det-alpha*B*h*d*y*H1/(C*T),
        "first_distance_pair": (1+k*sm)*(1+k*sp)-H1**2/T,
        "second_distance_pair": (U+k*V*sm)*(U+k*V*sp)-H1*H2/T,
        "triple_dn_polynomial": U*U-k*k*V*V*t-d*d*D3,
        "triple_cn_polynomial": V*V-U*U*t-q*C3,
        "second_fiber_at_first_root": L0-d*L1/C-4*(1-k*k)*t*d*W,
        "real_positivity_gap": L0**2-k*k*L1**2-(1-k*k)*Z**2,
    }
    out = {name: str(reduced(expr)) for name, expr in checks.items()}
    assert all(v == "0" for v in out.values()), out
    return out


def mod(x, period):
    return x % period


def lattice_controls():
    cases = 0
    branch = []
    for N in range(3, 102, 2):
        for tau in range(1, (N+1)//2):
            if math.gcd(N, tau) != 1:
                continue
            cases += 1
            v, delta = Fraction(2*tau, N), Fraction(4*tau, N)
            ap, am = mod(3+v, 4), mod(3-v, 4)
            bp, bm = mod(3+3*v, 4), mod(3-3*v, 4)
            assert ap != am
            assert {ap, am}.isdisjoint({bp, bm})
            assert (3*v) % 2 != 1  # cn(3v) cannot vanish
            assert (2*v) % 2 != 1  # cn(2v), hence V, cannot vanish
            if bp == bm:
                branch.append([N, tau])
                assert (N, tau) == (3, 1)
            tz = {mod(v,4), mod(-v,4), mod(2+v,4), mod(2-v,4)}
            assert {bp,bm}.isdisjoint(tz)
            plus = [mod(ap-j*delta, 4) for j in range(N)]
            minus = [mod(am-j*delta, 4) for j in range(N)]
            assert len(set(plus)) == N and len(set(minus)) == N
            assert set(plus) == set(minus)
            assert all(mod(bp-j*delta,4) in plus for j in range(N))
            assert all(mod(bm-j*delta,4) in plus for j in range(N))
            L = Fraction(4,N)
            assert mod(Fraction(2)-L/2, L) == 0
    assert branch == [[3,1]]
    return {"odd_primitive_pairs_tested": cases, "max_N": 101,
            "only_coalescent_second_fiber": branch,
            "finite_control_not_substitute_for_universal_argument": True}


def numeric_controls():
    M.mp.dps = 90
    eps = M.mpf("1e-17")
    errors = {}
    positive_min = M.inf
    residual_min = M.inf
    cases = []

    def record(name, value):
        errors[name] = max(errors.get(name, M.mpf(0)), abs(value))

    for kval in ["0.1", "0.55", "0.93"]:
        for N, tau in [(3,1),(5,1),(5,2),(7,3),(9,4),(11,4),(15,7),(25,12)]:
            k = M.mpf(kval)
            m, kc = k*k, M.sqrt(1-k*k)
            K, Kc = M.ellipk(m), M.ellipk(1-m)
            p = 1j*Kc
            v, delta, L = 2*K*tau/N, 4*K*tau/N, 4*K/N
            sn = lambda u: M.ellipfun("sn", u, m)
            cn = lambda u: M.ellipfun("cn", u, m)
            dn = lambda u: M.ellipfun("dn", u, m)
            h, C, d = sn(v), cn(v), dn(v)
            t,q = h*h,C*C
            U,V,W = 1-2*m*t+m*t*t,1-2*t+m*t*t,1-m*t*t
            L0,L1 = (U*U-m*V*V*t)/d,(V*V-U*U*t)/C
            Z = W*W-4*m*t*t*q*d*d
            alpha = M.mpf("1.3")
            A,B,c = alpha*d*d/q,alpha*kc/q,alpha*k
            C0 = B*h*d*q**4/(alpha**3*C)
            def E(u):
                su = sn(u)
                return C0*dn(u)*(1-m*t*su*su)/((d+k*C*su)**2*(L0+k*L1*su))
            def F(u):
                return M.fsum(E(u+j*delta) for j in range(N))
            def Q(u):
                return -A*sn(u), B*cn(u)
            def direct_edge(u):
                xm,ym = Q(u-v)
                xp,yp = Q(u+v)
                xm,xp=xm-c,xp-c
                dm,dp=xm*xm+ym*ym,xp*xp+yp*yp
                return (xm*yp-xp*ym)/(2*dm*dp)
            testu = M.mpf("0.231")*K+M.mpf("0.173")*p
            record("edge_formula", (direct_edge(testu)-E(testu))/(1+abs(E(testu))))
            record("real_period_E", (E(testu+4*K)-E(testu))/(1+abs(E(testu))))
            record("imaginary_antiperiod_E", (E(testu+2*p)+E(testu))/(1+abs(E(testu))))
            record("correct_dn_real_period", dn(testu+2*K)-dn(testu))
            record("quarter_shift_sn", sn(K+p+testu)-dn(testu)/(k*cn(testu)))
            record("quarter_shift_cn", cn(K+p+testu)+1j*kc/(k*cn(testu)))
            record("quarter_shift_dn", dn(K+p+testu)-1j*kc*sn(testu)/cn(testu))
            r,R = 3*K+p,3*K+p+v
            record("reflection_E", (E(2*r-testu)+E(testu))/(1+abs(E(testu))))
            record("reduced_real_period_F", (F(testu+L)-F(testu))/(1+abs(F(testu))))
            record("imaginary_antiperiod_F", (F(testu+2*p)+F(testu))/(1+abs(F(testu))))
            expected_a2 = 1j*C0*V/(4*kc**5*h**3*C*d*W)
            for sign in [1,-1]:
                point = r+sign*v
                measured = eps**2*(E(point+eps)+E(point-eps))/2
                record("quadratic_coefficient", (measured-sign*expected_a2)/(1+abs(expected_a2)))
            for j in range(N):
                point = R-j*delta
                measured = eps**2*(F(point+eps)+F(point-eps))/2
                record("cyclic_quadratic_cancellation", measured/(1+abs(expected_a2)))
            residual = eps*(F(R+eps)-F(R-eps))/2
            residual_min=min(residual_min,abs(residual))
            for point,ratio in [(p,-1j*k),(2*K+p,1j*k),(3*p,1j*k),(2*K+3*p,-1j*k)]:
                expected = -C0*t/(k*C*C*L1)*ratio
                measured = (E(point+eps)+E(point-eps))/2
                record("common_pole_removability", (measured-expected)/(1+abs(expected)))
            record("half_period_zero", F(R+L/2)/(1+abs(F(0))))
            realF = F(M.mpf("0.367")*K)
            assert abs(M.im(realF)) < M.mpf("1e-75") and M.re(realF)>0
            positive_min=min(positive_min,M.re(realF))
            product = F(0)*F(L/2)
            for u in [testu,M.mpf("0.37")*K,M.mpf("1.11")*K]:
                record("constant_shifted_product", (F(u)*F(u+L/2)-product)/(1+abs(product)))
                record("original_opposite_shift", (F(u+2*K)-F(u+L/2))/(1+abs(F(u))))
            if N == 3:
                b=K+p
                expected=-2j*C0*q/(Z*kc*(d+C)**2)
                measured=eps*(E(b+eps)-E(b-eps))/2
                record("N3_coalescent_simple_residue", (measured-expected)/(1+abs(expected)))
            cases.append({"k":kval,"N":N,"tau":tau})
    limits = {name: (M.mpf("1e-29") if name in {
        "quadratic_coefficient", "cyclic_quadratic_cancellation",
        "common_pole_removability", "N3_coalescent_simple_residue"} else M.mpf("1e-65"))
        for name in errors}
    for name, val in errors.items():
        assert val < limits[name], (name,M.nstr(val,15))
    return {"status":"diagnostics passed; not universal proof", "dps":M.mp.dps,
            "eps":str(eps),"cases":cases,
            "max_errors":{name:M.nstr(val,15) for name,val in errors.items()},
            "min_sampled_real_F":M.nstr(positive_min,15),
            "min_sampled_simple_residue_abs":M.nstr(residual_min,15)}


def main():
    result = {"python":sys.version.split()[0],"sympy":S.__version__,
              "mpmath":M.__version__,
              "independence":"No inherited review/checker/module read or imported.",
              "derivation_sha256":hashlib.sha256((BASE/"INDEPENDENT_DERIVATION.md").read_bytes()).hexdigest(),
              "symbolic_zero_controls":symbolic_controls(),
              "rational_lattice_controls":lattice_controls(),
              "numerical_diagnostics":numeric_controls()}
    OUTPUT.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"symbolic":len(result["symbolic_zero_controls"]),
                      "lattice_pairs":result["rational_lattice_controls"]["odd_primitive_pairs_tested"],
                      "numeric_cases":len(result["numerical_diagnostics"]["cases"]),
                      "max_numeric_errors":result["numerical_diagnostics"]["max_errors"]},indent=2))


if __name__ == "__main__":
    main()

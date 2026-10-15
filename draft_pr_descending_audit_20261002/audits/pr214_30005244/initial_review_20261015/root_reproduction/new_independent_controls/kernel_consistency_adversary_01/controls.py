#!/usr/bin/env python3
"""Independent controls. Exact algebra/finite shell identities certify only
those identities; floating point tables illustrate, and do not prove, limits.
No candidate/author program is imported or executed. Writes only given output.
"""
import argparse
import json
import math
import platform
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import sympy as sp


def exact_controls():
    r = sp.symbols('r', positive=True)
    k = sp.symbols('k')
    g = sp.exp(sp.I*k*r)/(4*sp.pi*r)
    ci = sp.simplify(-sp.diff(g,r)/r-k*k*g)
    ce = sp.simplify(-sp.diff(g,r,2)+sp.diff(g,r)/r)
    expected_i = sp.exp(sp.I*k*r)*(1-sp.I*k*r-k*k*r*r)/(4*sp.pi*r**3)
    expected_e = sp.exp(sp.I*k*r)*(k*k*r*r+3*sp.I*k*r-3)/(4*sp.pi*r**3)
    assert sp.simplify(ci-expected_i) == 0
    assert sp.simplify(ce-expected_e) == 0
    ri = sp.series(ci-1/(4*sp.pi*r**3), r, 0, 2)
    re = sp.series(ce+3/(4*sp.pi*r**3), r, 0, 2)
    assert sp.simplify(ri.removeO().coeff(r,-1)+k*k/(8*sp.pi)) == 0
    assert sp.simplify(re.removeO().coeff(r,-1)+k*k/(8*sp.pi)) == 0
    assert sp.simplify(ri.removeO().coeff(r,0)+sp.I*k**3/(6*sp.pi)) == 0
    assert sp.simplify(re.removeO().coeff(r,0)) == 0
    assert sp.simplify(2*sp.pi**sp.Rational(3,2)/(3*sp.gamma(sp.Rational(3,2)))-4*sp.pi/3) == 0
    # For each squared-radius shell, sum the integer numerator q I -3 j j^T.
    # Its exact vanishing implies all radial-weighted shell controls, without
    # irrational denominators or rounded summation.
    qmax = 512
    b = math.isqrt(qmax)
    shells = defaultdict(lambda: [[0]*3 for _ in range(3)])
    counts = defaultdict(int)
    for x in range(-b,b+1):
        for y in range(-b,b+1):
            for z in range(-b,b+1):
                j = [x,y,z]
                q = x*x+y*y+z*z
                if not 0 < q <= qmax:
                    continue
                counts[q] += 1
                for a in range(3):
                    for c in range(3):
                        shells[q][a][c] += (q if a == c else 0)-3*j[a]*j[c]
    assert all(not any(v for row in mat for v in row) for mat in shells.values())
    # Exact h^3 K0(hj)=K0(j) with rational h and translation cancellation.
    h = sp.Rational(2,7)
    a = sp.Matrix([sp.Rational(1,3),sp.Rational(-7,5),sp.Rational(9,2)])
    m, n = sp.Matrix([2,-1,5]), sp.Matrix([-3,4,1])
    displacement = (a+h*m)-(a+h*n)
    assert displacement == h*(m-n)
    def static(v):
        q = (v.T*v)[0]
        return (q*sp.eye(3)-3*v*v.T)/(4*sp.pi*q**sp.Rational(5,2))
    assert sp.simplify(h**3*static(displacement)-static(m-n)) == sp.zeros(3)
    return dict(radial_derivative_identity=True,
                remainder_I_series=str(ri), remainder_eeT_series=str(re),
                source_nu3='4*pi/3',
                exact_shells_checked=len(shells), squared_radius_max=qmax,
                shell_numerator_sums_zero=True, exact_translated_h_scaling=True)


def static_gaussian_controls():
    # D applied at zero to phi(y)=y_1^2 exp(-|y|^2) e1 has first component
    # (4pi)^-1 [4pi/3-3*(4pi/5)] * integral_0^infty r exp(-r^2)dr = -2/15.
    rows = []
    for h in [0.5,0.25,0.125,0.0625]:
        b = math.ceil(6/h)
        t = np.arange(-b,b+1,dtype=float)*h
        yz = t[:,None]**2+t[None,:]**2
        total = 0.0
        for x in t:
            q = x*x+yz
            mask = q>0
            val = np.zeros_like(q)
            val[mask] = (q[mask]-3*x*x)*x*x*np.exp(-q[mask])/(4*np.pi*q[mask]**2.5)
            total += float(val.sum())*h**3
        rows.append(dict(h=h,lattice_value=total,continuum_value=-2/15,
                         absolute_error=abs(total+2/15)))
    return rows


def centers(n):
    indices = np.stack(np.meshgrid(np.arange(n),np.arange(n),np.arange(n),indexing='ij'),axis=-1).reshape(-1,3)
    return (indices+0.5)/n, indices


def remainder(d, k):
    q = np.sum(d*d,axis=-1)
    rr = np.sqrt(q)
    nonzero = rr>0
    safe = np.where(nonzero,rr,1.0)
    t = k*safe
    exp = np.exp(1j*t)
    aa = (exp*(1-1j*t-t*t)-1)/(4*np.pi*safe**3)
    bb = (exp*(t*t+3j*t-3)+3)/(4*np.pi*safe**3)
    ee = d[..., :,None]*d[...,None,:]/safe[...,None,None]**2
    ans = aa[...,None,None]*np.eye(3)+bb[...,None,None]*ee
    return np.where(nonzero[...,None,None],ans,0)


def dynamic_nested_controls():
    rows = []
    for k in [1.7+0j,1.2-0.8j,0j]:
        for n in [2,4,6,8]:
            fine, indices = centers(2*n)
            coarse_at_fine = (indices//2+0.5)/n
            total = 0.0
            diagonal_total = 0.0
            for start in range(0,len(fine),48):
                sl = slice(start,min(start+48,len(fine)))
                fine_kernel = remainder(fine[sl,None,:]-fine[None,:,:],k)
                coarse_kernel = remainder(coarse_at_fine[sl,None,:]-coarse_at_fine[None,:,:],k)
                diff = fine_kernel-coarse_kernel
                total += float(np.sum(np.abs(diff)**2))
                same_coarse = np.all((indices[sl,None,:]//2)==(indices[None,:,:]//2),axis=-1)
                diagonal_total += float(np.sum(np.abs(fine_kernel[same_coarse])**2))
            weight = (1/(2*n))**6
            rows.append(dict(k=[k.real,k.imag],coarse_n=n,fine_n=2*n,
                             hs_difference=math.sqrt(total*weight),
                             fine_mass_in_omitted_coarse_blocks=diagonal_total*weight))
    return rows


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output',required=True)
    args = p.parse_args()
    result = dict(timestamp_utc=datetime.now(timezone.utc).isoformat(),
                  executable_versions=dict(python=platform.python_version(),numpy=np.__version__,sympy=sp.__version__),
                  exact=exact_controls(),static_gaussian=static_gaussian_controls(),
                  dynamic_nested=dynamic_nested_controls(),
                  limitation='Numerical tables are illustration only; proofs are in the independent reconstruction/report.')
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()

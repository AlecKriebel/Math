#!/usr/bin/env python3
"""Supplemental independent symbolic identities. Requires SymPy (audited at 1.14.0).

No author code is imported. Exact finite/rational certification is separately
portable in independent_controls.py. Analytic domains and limit reasoning are
spelled out in AUDIT.md; symbolic simplification alone is not that reasoning.
"""
import json
import sympy as s

CHECKS = []
def identity(actual, expected, name):
    if s.simplify(actual-expected) != 0:
        raise AssertionError(name)
    CHECKS.append(name)

def main():
    a, b, c, t, e, M = s.symbols('a b c t epsilon M', positive=True)
    n = s.symbols('n', integer=True, positive=True)
    mean = (a-b)/(s.log(a)-s.log(b))
    da, db = s.diff(mean, a), s.diff(mean, b)
    z = s.log(a)-s.log(b)
    identity(da, 1/z-(a-b)/(a*z*z), 'logmean first derivative')
    identity(db, -1/z+(a-b)/(b*z*z), 'logmean second derivative')
    identity(a*da+b*db, mean, 'logmean Euler homogeneity')
    identity(s.limit(mean, a, b), b, 'logmean diagonal extension')
    identity(s.limit(da, a, b), s.Rational(1,2), 'first derivative diagonal extension')
    identity(s.limit(db, a, b), s.Rational(1,2), 'second derivative diagonal extension')
    q = 2/(n*(n-1))
    th = mean.subs({a:t,b:1})
    d1, d2 = da.subs({a:t,b:1}), db.subs({a:t,b:1})
    A = (n-1)*q*th/n
    B = (n-1)*q*(s.Rational(1,2)*(d1*q*(n-1)*(1-t)+d2*q*(t-1))+th*n*q)/n
    R = (n+(t+n-2-(n-1)/t)/s.log(t))/(n*(n-1))
    identity(B/A, R, 'one-card formula for symbolic n and t')
    identity(s.limit(R, t, 1), n*q, 'one-card removable singularity at one')
    identity(s.limit(s.diff(R, t), t, 1), q*(2-n)/4, 'one-card linear perturbation coefficient')
    root_form = n/(n-1)+2*(n-2+1/s.sqrt(n))/((n-1)*s.log(n))
    identity(n*R.subs(t,s.sqrt(n)), root_form, 'sqrt-n simplified asymptotic expression')
    identity(s.limit(root_form, n, s.oo), 1, 'sqrt-n upper-test asymptotic limit')
    # Build the full six-state K3,3 calculation from its directed generator.
    rho = [e,e,e,1,e*e,e*e]
    logs = [-M,-M,-M,0,-2*M,-2*M]
    psi = [1,1,1,0,2,2]
    neighbors = [list(range(3,6))]*3+[list(range(3))]*3
    lr = [sum((rho[j]-rho[i] for j in neighbors[i]), s.S.Zero)/3 for i in range(6)]
    lp = [sum((psi[j]-psi[i] for j in neighbors[i]), s.S.Zero)/3 for i in range(6)]
    action = density = gradient = on = s.S.Zero
    for i in range(6):
        for j in neighbors[i]:
            l = logs[i]-logs[j]
            th = (rho[i]-rho[j])/l
            d1 = 1/l-(rho[i]-rho[j])/(rho[i]*l*l)
            d2 = -1/l+(rho[i]-rho[j])/(rho[j]*l*l)
            g = psi[j]-psi[i]
            action += th*g*g/36
            density += (d1*lr[i]+d2*lr[j])*g*g/72
            gradient -= th*g*(lp[j]-lp[i])/36
            on += (d1-d2)*(rho[j]-rho[i])*g*g/216+th*g*g/54
    full = density+gradient
    Z = 1+2*e*M-e*e
    identity(action, (1-e)*(1+2*e)/(6*M), 'local S3 action for arbitrary epsilon')
    identity(on/action, Z/(6*e*M), 'local S3 diagonal ratio for arbitrary epsilon')
    identity((full-on)/action, Z/(3*M*(1+2*e)), 'local S3 off-diagonal ratio for arbitrary epsilon')
    identity(full/action, (1+4*e)*Z/(6*e*M*(1+2*e)), 'local S3 full ratio for arbitrary epsilon')
    off = s.factor((full-on)/action).subs(M,-s.log(e))
    fullr = s.factor(full/action).subs(M,-s.log(e))
    identity(s.limit(off,e,0,dir='+'),0,'local off-diagonal limit')
    if s.limit(fullr,e,0,dir='+') != s.oo:
        raise AssertionError('local full ratio limit')
    CHECKS.append('local full ratio diverges to positive infinity')
    if s.limit(s.factor(on/action).subs(M,-s.log(e)), e, 0, dir='+') != s.oo:
        raise AssertionError('local diagonal ratio limit')
    CHECKS.append('local diagonal ratio diverges to positive infinity')
    ell = s.symbols('ell', positive=True)
    aw = (4496*ell+135)/(18*ell)
    bw = (251392*ell*ell+480*ell+6075)/(1152*ell*ell)
    identity(s.Rational(9,10)*aw-bw,
             (37888*ell*ell+36480*ell-30375)/(5760*ell*ell),
             'witness gap simplification')
    return {'status':'passed','symbolic_assertions':len(CHECKS),'checks':CHECKS,
            'sympy_version':s.__version__,'author_code_imported':False,
            'all_density_or_all_n_optimum_certified':False}

if __name__ == '__main__':
    print(json.dumps(main(),indent=2,sort_keys=True))

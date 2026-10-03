#!/usr/bin/env python3
"""Independent exact algebra controls. This is not a proof checker for IMCF.
Requires Python 3 and SymPy. No data files, network, current-directory state,
or assertions (which python -O would suppress) are used.
"""
import json
import sys
import sympy as sp


def main():
    if len(sys.argv) != 1:
        raise SystemExit('Usage: python independent_controls.py')
    labels = []
    def equal(label, a, b=0):
        residual = sp.simplify(sp.expand(a - b))
        if residual != 0:
            raise RuntimeError('%s: nonzero residual %s' % (label, residual))
        labels.append(label)

    r, c, K, x, t, A0 = sp.symbols('r c K x t A0', positive=True)
    P = sp.Poly(4*sp.pi*r**2-sp.Rational(4,3)*sp.pi*c*r**3, r)
    equal('01 ball-energy derivative', P.diff().as_expr(), 4*sp.pi*r*(2-c*r))
    equal('02 critical-radius energy', P.eval(2/c), sp.Rational(16,3)*sp.pi/c**2)
    equal('03 negative endpoint', P.eval(4/c), -sp.Rational(64,3)*sp.pi/c**2)
    Q = sp.Poly(K*x*x-c*x**3, x)
    root = 2*K/(3*c)
    equal('04 volume-root stationarity', Q.diff().eval(root))
    equal('05 profile critical value', Q.eval(root), 4*K**3/(27*c**2))
    # These ratios explicitly separate the dimensional constants from K^3=36*pi.
    equal('06 width normalization', sp.cancel(Q.eval(root)/K**3)*36*sp.pi,
          16*sp.pi/(3*c*c))
    equal('07 critical-volume normalization', sp.cancel(root**3/K**3)*36*sp.pi,
          32*sp.pi/(3*c**3))
    equal('08 zero-energy volume', Q.eval(K/c))
    area = A0*sp.exp(t)
    radius = sp.sqrt(area/(4*sp.pi))
    H = 2/radius
    equal('09 equality radial-coordinate metric', (1/H**2)/sp.diff(radius,t)**2, 1)
    equal('10 area-power evolution', sp.diff(area**sp.Rational(3,2),t),
          sp.Rational(3,2)*area**sp.Rational(3,2))

    # Recompute cone scalar curvature from the metric/Christoffel/Ricci definitions,
    # rather than insert the warped-product scalar formula being checked.
    theta, phi = sp.symbols('theta phi', real=True)
    a = sp.Function('a')(theta)
    coordinates = [r,theta,phi]
    g = sp.diag(1,r*r,r*r*a*a)
    inverse = g.inv()
    n = 3
    Gamma = [[[sp.simplify(sum(inverse[k,l]*(
        sp.diff(g[l,j],coordinates[i])+sp.diff(g[l,i],coordinates[j])-
        sp.diff(g[i,j],coordinates[l])) for l in range(n))/2)
        for j in range(n)] for i in range(n)] for k in range(n)]
    Ric = [[sp.simplify(sum(
        sp.diff(Gamma[k][i][j],coordinates[k])-
        sp.diff(Gamma[k][i][k],coordinates[j])+
        sum(Gamma[k][k][l]*Gamma[l][i][j]-
            Gamma[k][j][l]*Gamma[l][i][k] for l in range(n))
        for k in range(n))) for j in range(n)] for i in range(n)]
    scalar = sp.simplify(sum(inverse[i,j]*Ric[i][j]
                              for i in range(n) for j in range(n)))
    fiber_scalar = -2*sp.diff(a,theta,2)/a
    equal('11 cone scalar from Christoffel symbols', scalar, (fiber_scalar-2)/r**2)
    equal('12 global profile deficit factorization', Q.eval(root)-Q.as_expr(),
          c*(x-root)**2*(x+K/(3*c)))

    # Four additional local/constant controls, independent of the author program.
    G, R, B, J = sp.symbols('gradlogH2 R tracefreeA2 integralH2')
    # Here every symbol denotes the corresponding surface integral.
    # I' = -2G - 2B - 2Ric, Gauss gives 2Ric=R-8*pi-B+J/2 on S^2.
    Iprime = -2*G-2*B-(R-8*sp.pi-B+J/2)
    equal('13 spherical Geroch integrand cancellation',
          (16*sp.pi-J)/2-Iprime, 2*G+R+B)
    equal('14 Holder-to-isoperimetric constant',
          (sp.Rational(3,2)*sp.sqrt(16*sp.pi))**2, 36*sp.pi)
    equal('15 cone is flat for round fiber', scalar.subs(a,sp.sin(theta)).doit(), 0)
    # eps_j=1/(j*q_j^5), |x| <= (6/5)*q_j on each transplant ball.
    # The worst k<=3 is bounded by a fixed constant/(j*q_j^2).
    j,q = sp.symbols('j q', positive=True)
    equal('16 weighted-third-derivative decay exponent', q**3/(j*q**5), 1/(j*q**2))
    print(json.dumps({'status':'PASS','checks':len(labels),'labels':labels,
        'scope':'Exact algebra and local tensor-formula controls only. No computational claim about theorem validity, metric construction, topology, flow regularity, or width strictness.',
        'required_dependency':'sympy'},indent=2))

if __name__ == '__main__':
    main()

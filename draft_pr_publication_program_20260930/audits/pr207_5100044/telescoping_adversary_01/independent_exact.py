"""Independent reconstruction; no imports or execution of the submitted checker."""
import sys
sys.path.insert(0, '/Users/alec/Library/Python/3.11/lib/python/site-packages')
import sympy as z
import json
from pathlib import Path

k, h, r, cv, dv, cc, dd, kp, al = z.symbols('k h r cv dv cc dd kp al')
t = h*h
q = 1-t
U = 1-2*k*k*t+k*k*t*t
V = 1-2*t+k*k*t*t
W = 1-k*k*t*t
Den = 1-k*k*t*r*r
relations = [(cv, cv*cv+h*h-1), (dv, dv*dv+k*k*h*h-1),
             (cc, cc*cc+r*r-1), (dd, dd*dd+k*k*r*r-1),
             (kp, kp*kp+k*k-1)]
checks = {}
def reduce_num(expr):
    num = z.cancel(expr).as_numer_denom()[0]
    for variable, relation in relations:
        num = z.rem(num, relation, variable)
    return z.factor(num)
def check(name, expr):
    residual = reduce_num(expr)
    checks[name] = {'passed': residual == 0, 'residual': str(residual)}
    if residual != 0:
        raise AssertionError((name, residual))

a, b, c = al*dv/cv, al*kp/cv, al*k
sp, sm = (r*cv*dv+h*cc*dd)/Den, (r*cv*dv-h*cc*dd)/Den
cp, cm = (cc*cv-r*dd*h*dv)/Den, (cc*cv+r*dd*h*dv)/Den
dp, dm = (dd*dv-k*k*r*cc*h*cv)/Den, (dd*dv+k*k*r*cc*h*cv)/Den
det = lambda p, y: p[0]*y[1]-p[1]*y[0]
pm, pp = (-a*sm,b*cm), (-a*sp,b*cp)
fm, fp = (pm[0]-c,pm[1]), (pp[0]-c,pp[1])
dprod = (a+c*sm)*(a+c*sp)
dprod_claim = al**2*(1+k*r)*(U+k*V*r)/(q*Den)
fdet_claim = 2*al*b*h*dv*dd*(1+k*r)/Den
C = b*h*dv*q*q/al**3
E = C*dd*Den/((1+k*r)*(U+k*V*r)**2)
check('confocal_axes', a*a-b*b-c*c)
check('focal_distance_squared', (-a*r-c)**2+b*b*cc*cc-(a+c*r)**2)
check('double_cn', (cv*cv-h*h*dv*dv)/W-V/W)
check('double_dn', (dv*dv-k*k*h*h*cv*cv)/W-U/W)
check('UV_difference', U-V-2*t*(1-k*k))
check('UV_norm', U*U-k*k*V*V-(1-k*k)*W*W)
check('focal_distance_product', dprod-dprod_claim)
check('focal_endpoint_determinant', det(fm,fp)-fdet_claim)
check('ordinary_endpoint_determinant', det(pm,pp)-2*a*b*h*cv*dd/Den)
check('endpoint_dn_sum', dm+dp-2*dd*dv/Den)
check('inverse_side_half_cross', fdet_claim/(2*dprod_claim*dprod_claim)-E)
H = U*U-k*k*V*V*r*r
Bnorm = (1-k*k*t*r*r)*(U*U+k*k*V*(V+2*U)*r*r)/(dd*H*H)
check('antipodal_pair', E+E.subs(r,-r)-2*C*Bnorm)

# Rebuild reciprocal shifts directly from the dn addition formula.
sd, cd, dD = 2*h*cv*dv/W, V/W, U/W
DX = 1-k*k*r*r*sd*sd
dplus = (dd*dD-k*k*r*cc*sd*cd)/DX
dminus = (dd*dD+k*k*r*cc*sd*cd)/DX
check('reciprocal_symmetric_shift', 1/dplus+1/dminus-2*W*U*dd/H)
check('reciprocal_antisymmetric_shift', 1/dplus-1/dminus-2*k*k*sd*cd*W*W*r*cc/H)

# Derive the decomposition by solving coefficient equations, rather than
# copying the submitted B,D expressions. Use abstract U,V before specializing.
uu,vv,ww,tt,x = z.symbols('uu vv ww tt x')
HH = uu*uu-k*k*vv*vv*x
target = (1-k*k*tt*x)*(uu*uu+k*k*vv*(vv+2*uu)*x)
aa, bb, gg = z.symbols('aa bb gg')
ansatz = aa*HH*HH + bb*(1-k*k*x)*HH + gg*(1-k*k*x)*(uu*uu+(k*k*vv*vv-2*uu*uu)*x)
sol = z.solve(z.Poly(target-ansatz,x).all_coeffs(),(aa,bb,gg),dict=True)[0]
check('independently_reconstructed_polynomial_identity', target-ansatz.subs(sol))
check('solved_a0', sol[aa]-(1-tt)/(uu-vv)**2)
closed_a2 = (vv*vv-uu*uu*tt)/(4*h*cv*dv*(uu*uu-k*k*vv*vv)*(uu-vv))
check('solved_derivative_coefficient', sol[gg]-4*k*k*h*cv*dv*vv*closed_a2)
lam = U*(k**4*t**3+k**4*t*t-5*k*k*t+k*k+2)/(2*(1-k*k)**2*W**3)
special = {uu:U,vv:V,ww:W,tt:t}
check('solved_cyclic_coefficient', (sol[aa]+sol[bb]/(ww*uu)).subs(special)-lam)
check('derivative_numerator', (1-2*x)*HH+2*k*k*vv*vv*x*(1-x)-(uu*uu+(k*k*vv*vv-2*uu*uu)*x))
check('N4_decomposition_a0', sol[aa].subs(vv,0)-(1-tt)/uu**2)
check('N4_decomposition_b0', sol[bb].subs(vv,0)-tt)
check('N4_decomposition_d0', sol[gg].subs(vv,0))
check('N4_a2_finite', closed_a2.subs(vv,0)+tt/(4*h*cv*dv*uu))

out = {'all_passed': all(c['passed'] for c in checks.values()),
       'check_count': len(checks), 'checks': checks,
       'independently_solved_coefficients': {str(j):str(z.factor(v)) for j,v in sol.items()},
       'method':'Exact polynomial remainders in the Jacobi quadrics, and independent coefficient-system solution.',
       'sympy_version':z.__version__}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))

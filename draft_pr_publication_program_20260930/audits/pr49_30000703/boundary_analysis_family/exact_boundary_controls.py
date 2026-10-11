"""Independent exact boundary, sign and scope controls; no proof by sampling."""
from pathlib import Path
import json
import sympy as s
checks = {}
def ck(name, value):
    assert __debug__ and bool(value), name
    checks[name] = 'PASS'
r, a = s.symbols('r a', positive=True)
z = s.symbols('z')
x, y = s.symbols('x y', real=True)
Z = x+s.I*y
for k in range(2,23):
    phi = k*r**(k-1)/sum(r**(2*j) for j in range(k))
    ck('power_formula_'+str(k), s.cancel(phi-k*r**(k-1)*(1-r*r)/(1-r**(2*k))) == 0)
    ck('power_limit_'+str(k), s.limit(phi,r,1) == 1)
    ck('power_positive_normal_'+str(k), s.diff(z**k,z).subs(z,1) == k)
    ck('power_boundary_defining_ratio_'+str(k), s.limit((1-r**(2*k))/(1-r*r),r,1) == k)
    ck('power_taylor_coefficient_'+str(k), s.expand((1+z)**k).coeff(z,1) == k)
C = (1-Z)/(1+Z)
ck('cayley_positive_realpart',s.factor(s.re(C)-(1-x*x-y*y)/((1+x)**2+y*y)) == 0)
ck('cayley_circle_reflection',s.cancel((1-1/z)/(1+1/z)+(1-z)/(1+z)) == 0)
u = s.symbols('u', positive=True)
for av in [s.Rational(1,20),s.Rational(1,7),s.Rational(2,5),s.Rational(1,2),s.Integer(1),s.Rational(3,2),s.Integer(3),s.Integer(7)]:
    f = s.exp(-av*(1-z)/(1+z))
    ck('exponential_value_'+str(av),f.subs(z,1) == 1)
    ck('exponential_normal_'+str(av),s.diff(f,z).subs(z,1) == av/2)
    ck('exponential_distortion_'+str(av),s.cancel((2*av*u*s.exp(-av*u)/(1-s.exp(-2*av*u))-av*u/s.sinh(av*u)).rewrite(s.exp)) == 0)
    ck('exponential_unrestricted_scalar_limit_'+str(av),s.limit(av*u/s.sinh(av*u),u,0) == 1)
    ck('exponential_defining_ratio_'+str(av),s.limit((1-s.exp(-2*av*(1-r)/(1+r)))/(1-r*r),r,1) == av/2)
    ck('exponential_Hopf_sign_'+str(av),s.diff(-av*(1-r)/(1+r),r).subs(r,1) == av/2)
# Complex rotations check the coefficient at a general boundary point and
# the sign of local boundary orientation; no alpha=1 or global degree claim.
for k in [1,2,3,5,9]:
    for xi in [s.Integer(1),s.I,-s.Integer(1),s.Rational(3,5)+s.I*s.Rational(4,5)]:
        for eta in [s.Integer(1),s.I,s.Rational(5,13)+s.I*s.Rational(12,13)]:
            f = eta*(z/xi)**k
            derivative = s.diff(f,z).subs(z,xi)
            ck('general_boundary_coefficient_'+str((k,xi,eta)),s.simplify(s.conjugate(eta)*xi*derivative) == k)
# Möbius examples validate the unrestricted defining ratio exactly, including
# small/large positive derivatives and zeros strictly inside the disk.
for av in [s.Rational(-4,5),s.Rational(-1,2),s.Integer(0),s.Rational(1,3),s.Rational(4,5)]:
    T = (Z-av)/(1-av*Z)
    one_minus = s.factor(1-T*s.conjugate(T))
    expected = (1-av**2)*(1-x*x-y*y)/((1-av*x)**2+av**2*y*y)
    ck('automorphism_disk_defining_'+str(av),s.factor(one_minus-expected) == 0)
    Tr = (z-av)/(1-av*z)
    alpha = (1+av)/(1-av)
    ck('automorphism_normal_'+str(av),s.diff(Tr,z).subs(z,1) == alpha)
    ck('automorphism_ratio_'+str(av),s.limit((1-Tr.subs(z,r)**2)/(1-r*r),r,1) == alpha)
    ck('automorphism_positive_'+str(av),alpha > 0)
# The positive harmonic barrier has inward derivative m/(a log 2).
t,m,b = s.symbols('t m b',positive=True)
barrier = m*s.log(b/(b-t))/s.log(2)
ck('barrier_boundary_value',barrier.subs(t,0) == 0)
ck('barrier_inward_derivative',s.diff(barrier,t).subs(t,0) == m/(b*s.log(2)))
ck('barrier_inner_value',s.simplify(barrier.subs(t,b/2)-m) == 0)
# Triangle propagation at exact radii with positive strict margins.
for j in range(1,21):
    delta = s.Rational(1,j)
    for ratio in [s.Rational(1,4),s.Rational(1,3),s.Rational(2,5)]:
        ck('point_arc_margin_'+str((j,ratio)),ratio*delta+delta/2 < delta)
# A weaker angular hypothesis has an explicit counterexample to reflection.
W = s.symbols('W')
F = W+a*s.log(1+W)
ck('weaker_halfplane_derivative',s.diff(F,W) == 1+a/(1+W))
for av in [s.Rational(1,5),s.Rational(1,2),s.Integer(1),s.Integer(3)]:
    radial = x*(1+av/(1+x))/(x+av*s.log(1+x))
    ck('weaker_radial_limit_'+str(av),s.limit(radial,x,s.oo) == 1)
    tangential_squared = (4+y*y+4*av+av*av)/(4+y*y)/(1+av*s.log(4+y*y)/2)**2
    ck('weaker_tangential_limit_'+str(av),s.limit(tangential_squared,y,s.oo) == 0)
    fp = 1+av/(2+s.I*y)
    ck('weaker_tangential_derivative_norm_'+str(av),s.factor(fp*s.conjugate(fp)-(4+y*y+4*av+av*av)/(4+y*y)) == 0)
# Cayley converts strict positive real part to strict disk modulus <1.
R,I = s.symbols('R I',real=True)
h = (R+s.I*I-1)/(R+s.I*I+1)
ck('halfplane_to_disk_defining',s.factor(1-h*s.conjugate(h)-4*R/((R+1)**2+I**2)) == 0)
result = {'schema':'pr49-independent-boundary-exact-controls/v1','passed':len(checks),'failed':0,'sympy_version':s.__version__,'checks':checks,'scope':'Independent exact analytic-example, normal-sign, defining-function and quantifier controls. Universal proofs are in BOUNDARY_PROOF.md; the central published arc theorem is imported explicitly. Finite checks do not establish the reflection theorem.'}
Path(__file__).with_name('EXACT_BOUNDARY_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))

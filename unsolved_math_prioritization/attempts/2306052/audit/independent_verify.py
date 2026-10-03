#!/usr/bin/env python3
"""Independent exact controls for the Rubel partial-results packet.

Uses SymPy for symbolic expansion and exact real-root isolation. Does not import
or execute the packet verifier. Run from this directory or pass --output PATH.
These finite checks do not prove the analytic statements or resolve Problem 6.52.
"""
import argparse
import json
from collections import Counter
from fractions import Fraction
import sympy as S

records = []

def check(category, name, condition):
    if not bool(condition):
        raise AssertionError(f'{category}: {name}')
    records.append((category, name))

def eq(name, lhs, rhs):
    check('original_polynomial_controls', name, S.expand(lhs-rhs) == 0)

z, a, w, t, y, s, x, v = S.symbols('z a w t y s x v')
R = S.Rational
N = 2*z*(1+z)
# Independent symbolic engine, rather than the submitted sparse-polynomial code.
eq('Cayley numerator', (1+z)**2-(1+z)*(1-z), N)
eq('half-slope endpoint', N+(1+z)*(1-z)**2/2, (1+z)**3/2)
eq('target -a', N+a*(1+z)*(1-z)**2,
   (1+z)*(a*z**2+(2-2*a)*z+a))
eq('monic half-plane equation', (t**2-t-w)*(t+1)+a*(t-1),
   t**3+(a-w-1)*t-a-w)
eq('double-root cusp', (y-s)**2*(y+2*s), y**3-3*s**2*y+2*s**3)
eq('Cayley metric', (x+1)**2+v**2-((x-1)**2+v**2), 4*x)

base_controls = [
    ('cluster interior', R(1,2)-R(3,8)>0),
    ('cluster contains zeros', R(1,4)<R(3,8)),
    ('cluster margin', R(3,8)**2-R(1,4)**2==R(5,64)),
    ('separated interior', R(1,2)-R(1,8)>0),
    ('separated margin', R(1,8)*(2*R(1,4)-R(1,8))==R(3,64)),
    ('common margin', R(3,64)<R(5,64)),
    ('critical preimage', (R(1,2)-1)/(R(1,2)+1)==R(-1,3)),
    ('critical value', R(1,2)**2-R(1,2)==R(-1,4)),
]
for name, condition in base_controls:
    check('original_rational_constants', name, condition)

for k in range(-20,21):
    r = Fraction(k,4)
    al = (1+3*r*r)/2
    be = r**3
    delta = lambda ar: (2*ar-1)**3-27*be**2
    for suffix, test in [
        ('boundary', delta(al)==0),
        ('root sum', r+r-2*r==0),
        ('root product', r*r*(-2*r)==-2*be),
        ('outside', delta(al-Fraction(1,10))<0),
        ('inside', delta(al+Fraction(1,10))>0),
    ]:
        check('original_cusp_controls', f'{k}: {suffix}', test)

samples = [
    (0,0,False), (R(1,100),0,False), (-10,0,False), (0,10,False),
    (R(1,2),0,True), (1,0,True), (2,1,True), (2,-1,True), (2,2,False),
]
for n,(al,be,bad) in enumerate(samples):
    check('original_named_samples', str(n), bool((2*al-1)**3>=27*be**2)==bad)

for j in range(-15,16):
    for k in range(-15,16):
        al,be=Fraction(j,32),Fraction(k,32)
        if al*al+be*be < Fraction(1,4):
            check('original_half_disk_controls', f'{j},{k}', (2*al-1)**3<27*be**2)

original_count=len(records)
if original_count != 1021:
    raise AssertionError(f'Original-control count {original_count}, expected 1021')

# Additional adversarial algebraic checks.
Q=t**3+(a-w-1)*t-a-w
Nz=S.expand(N+a*z*(1-z)**2-w*(1-z)**2)
extras = [
    ('no denominator-root cancellation for nonzero a', S.expand(Q.subs(t,-1)+2*a)==0),
    ('a=0 factorization', S.expand(Q.subs(a,0)-(t+1)*(t**2-t-w))==0),
    ('no z=1 solution', S.expand(Nz.subs(z,1))==4),
    ('homogeneous change of variable', S.cancel((t+1)**3*Nz.subs(z,(t-1)/(t+1))-4*Q)==0),
    ('uniform monic leading coefficient', S.Poly(Q,t).LC()==1),
    ('vanishing root sum', S.Poly(Q,t).coeff_monomial(t**2)==0),
    ('real cubic discriminant', S.discriminant(y**3-x*y+2*v,y)==4*x**3-108*v**2),
    ('critical preimage derivative', S.simplify(S.diff(N/(1-z)**2,z).subs(z,-R(1,3)))==0),
]
for name,test in extras:
    check('additional_algebraic_controls',name,test)

# Exact isolation of all real roots with multiplicity, not floating-point roots
# or direct re-evaluation of the claimed discriminant sign alone.
for jp in range(-8,13):
    p=R(jp,2)
    for kb in range(-12,13):
        beta=R(kb,4)
        poly=S.Poly(y**3-p*y+2*beta,y)
        real_multiplicity=sum(mult for interval,mult in poly.intervals())
        expected=bool(p**3>=27*beta**2)
        check('additional_exact_root_isolations',f'p={p}, beta={beta}',
              (real_multiplicity==3)==expected)

# Nonzero cusp parameters need not be captured by the preceding rational grid.
for k in range(-20,21):
    r=R(k,4)
    p=3*r*r
    beta=r**3
    real_multiplicity=sum(mult for _,mult in S.Poly(y**3-p*y+2*beta,y).intervals())
    check('additional_cusp_root_isolations',str(k),real_multiplicity==3)
    zs=(S.I*r-1)/(S.I*r+1)
    check('additional_boundary_preimages',str(k),S.simplify(zs*S.conjugate(zs))==1)

counts=dict(sorted(Counter(category for category,_ in records).items()))
result={
    'status':'PASS',
    'independent_implementation':True,
    'submitted_verifier_imported':False,
    'original_exact_controls_reproduced':original_count,
    'additional_exact_controls':len(records)-original_count,
    'total_exact_controls':len(records),
    'category_counts':counts,
    'sympy_version':S.__version__,
    'root_isolation_method':'SymPy exact rational real-root isolation; multiplicities included',
    'scope':'Finite algebraic controls only. The analytic arguments are audited separately in AUDIT.md; this is not a formal proof of them or a resolution of the universal question.'
}
output=json.dumps(result,indent=2,sort_keys=True)+'\n'
parser=argparse.ArgumentParser()
parser.add_argument('--output')
args=parser.parse_args()
if args.output:
    with open(args.output,'w',encoding='utf-8') as f:
        f.write(output)
print(output,end='')

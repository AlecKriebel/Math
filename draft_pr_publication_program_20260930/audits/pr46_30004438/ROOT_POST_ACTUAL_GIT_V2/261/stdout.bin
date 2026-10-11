#!/usr/bin/env python3
"""Finite exact adversarial controls; the universal proof is in the report."""
import json
import sympy as s

z = s.symbols('z')
checks = {}
def ck(name, value):
    if not bool(value):
        raise AssertionError(name)
    checks[name] = 'PASS'

def compose(P, Q, p, q, d):
    pp = s.Poly(sum(p.nth(j) * P.as_expr()**j * Q.as_expr()**(d-j) for j in range(d+1)), z)
    qq = s.Poly(sum(q.nth(j) * P.as_expr()**j * Q.as_expr()**(d-j) for j in range(d+1)), z)
    return pp, qq

for d in range(2, 8):
    r = s.Integer(d+1)
    c = s.Rational(1, 10*d)
    B = r + sum(c/(r-j) for j in range(1, d+1))
    f = s.cancel(B + sum(c/(j-z) for j in range(1, d+1)))
    p, q = [s.Poly(v,z) for v in s.fraction(f)]
    ck(f'own_d{d}_degree', max(p.degree(),q.degree()) == d)
    ck(f'own_d{d}_coprime', s.gcd(p,q).degree()==0)
    ck(f'own_d{d}_fixed_r', f.subs(z,r)==r)
    mu = s.diff(f,z).subs(z,r)
    ck(f'own_d{d}_strict_attraction', 0 < mu <= s.Rational(1,10))
    # M f M^-1, M(z)=-1/(z-r), M^-1(z)=r-1/z.
    g = s.cancel(-1/(f.subs(z,r-1/z)-r))
    gp,gq = [s.Poly(v,z) for v in s.fraction(g)]
    poly,rem = s.div(gp,gq)
    ck(f'own_d{d}_conjugate_degree', gp.degree()==d and gq.degree()==d-1)
    ck(f'own_d{d}_conjugate_coprime', s.gcd(gp,gq).degree()==0)
    ck(f'own_d{d}_conjugate_linear_part', poly.degree()==1 and poly.nth(1)==1/mu and poly.nth(1)>1)
    ck(f'own_d{d}_conjugate_poles_real_simple', gq.count_roots(-s.oo,s.oo)==d-1 and s.gcd(gq,gq.diff()).degree()==0)
    ck(f'own_d{d}_all_fixed_roots_real', (p-s.Poly(z,z)*q).count_roots(-s.oo,s.oo)==d+1)
    if d<=3:
        P,Q = p,q
        for n in range(1,4):
            e=d**n
            F=P-s.Poly(z,z)*Q
            ck(f'own_d{d}_period_divides_{n}_degree', F.degree()==e+1)
            ck(f'own_d{d}_period_divides_{n}_all_real', F.count_roots(-s.oo,s.oo)==e+1)
            if n<3:
                P,Q=compose(P,Q,p,q,d)

# Link the candidate's actual product family to the independently derived mechanism.
# For x>=0, f'_d(x)=f_d(x) sum 1/((x+2j-1)(x+2j)).
for d in range(2,9):
    f=s.prod((z+2*j-1)/(z+2*j) for j in range(1,d+1))
    rhs=f*sum(1/((z+2*j-1)*(z+2*j)) for j in range(1,d+1))
    ck(f'candidate_d{d}_derivative_identity', s.cancel(s.diff(f,z)-rhs)==0)
    ck(f'candidate_d{d}_positive_fixed_bracket', f.subs(z,0)>0 and f.subs(z,1)<1)
    bound=sum(s.Rational(1,(2*j-1)*(2*j)) for j in range(1,d+1))
    ck(f'candidate_d{d}_uniform_derivative_bound', 0<bound<1)
    p=s.Poly(s.prod(z+2*j-1 for j in range(1,d+1)),z)
    q=s.Poly(s.prod(z+2*j for j in range(1,d+1)),z)
    ck(f'candidate_d{d}_same_negative_residue_sign', all(p.eval(-2*j)/q.diff().eval(-2*j)<0 for j in range(1,d+1)))

# Falsify three tempting overstatements exactly, including nonreal attracting cycles.
h=(z*z-1)/(2*z)
ck('H_selfmap_not_sufficient_nonreal_fixed', s.cancel(h.subs(z,s.I))==s.I and s.cancel(h.subs(z,-s.I))==-s.I)
ck('nonreal_basin_superattracting_fixed', s.diff(h,z).subs(z,s.I)==0)
k=-h
ck('halfplane_swap_not_sufficient_nonreal_2cycle', s.cancel(k.subs(z,s.I))==-s.I and s.cancel(k.subs(z,-s.I))==s.I)
ck('nonreal_2cycle_superattracting', s.diff(k,z).subs(z,s.I)==0)
a,c=s.symbols('a c',positive=True)
family=a*z-c/z
ck('neutral_boundary_fixed_equation', s.cancel(family-z-((a-1)*z*z-c)/z)==0)
ck('neutral_boundary_arbitrarily_small_bad_perturbation', s.cancel((s.Rational(99,100)*z-1/z).subs(z,10*s.I))==10*s.I)
u,v=s.symbols('u v',real=True)
ck('imaginary_growth_identity', s.simplify(s.im(a*(u+s.I*v)-c/(u+s.I*v))-v*(a+c/(u*u+v*v)))==0)

print(json.dumps({'sympy_version':s.__version__,'passed':len(checks),'failed':0,'checks':checks,
 'scope':'Exact finite controls for independent H-selfmap/attracting-boundary proof. No finite computation establishes the all-period theorem.'},indent=2))

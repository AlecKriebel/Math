#!/usr/bin/env python3
"""Exact finite controls for the boundary-frequency packet; standard library only.

These checks supplement, and do not certify, the analytic proofs or imported
theorems. Explicit exceptions remain active under python -O.
"""
from fractions import Fraction as F
from itertools import product
import json

counts = {}

def check(category, condition):
    if not condition:
        raise ArithmeticError('Failed exact control: ' + category)
    counts[category] = counts.get(category, 0) + 1

# Laurent polynomials in x,t, represented by {(x exponent,t exponent): coefficient}.
def clean(p):
    return {k: F(v) for k, v in p.items() if v}

def add(*ps):
    q = {}
    for p in ps:
        for k, v in p.items():
            q[k] = q.get(k, F(0)) + v
    return clean(q)

def scale(p, c):
    return clean({k: c*v for k, v in p.items()})

def mul(p, q):
    r = {}
    for (a,b), v in p.items():
        for (c,d), w in q.items():
            k = (a+c,b+d)
            r[k] = r.get(k, F(0)) + v*w
    return clean(r)

def deriv(p, var):
    q = {}
    for k, v in p.items():
        e = k[var]
        if e:
            kk = list(k)
            kk[var] -= 1
            q[tuple(kk)] = v*e
    return clean(q)

def lap(p):
    return add(deriv(deriv(p,0),0), deriv(deriv(p,1),1))

def dotgrad(p,q):
    return add(*(mul(deriv(p,i),deriv(q,i)) for i in (0,1)))

t = {(0,1): F(1)}
inv_t = {(0,-1): F(1)}

for ax in range(7):
    for at in range(-3,9):
        v = {(ax,at): F(1)}
        lifted = add(lap(v),scale(mul(inv_t,deriv(v,1)),2))
        check('strong_lift_laurent_identity', lap(mul(t,v)) == mul(t,lifted))
        # The claimed intertwining is special to three radial variables.
        if at:
            for radial_dim in (1,2,4,5):
                wrong = add(lap(v),scale(mul(inv_t,deriv(v,1)),radial_dim-1))
                check('wrong_radial_dimension_negative', lap(mul(t,v)) != mul(t,wrong))

for ax,at,bx,bt in product(range(5), range(1,6), range(5), range(5)):
    h={(ax,at):F(1)}
    a={(bx,bt):F(1)}
    lhs=add(dotgrad(h,mul(t,a)),scale(mul(mul(t,t),dotgrad(mul(h,inv_t),a)),-1))
    check('weak_lift_total_derivative', lhs == deriv(mul(h,a),1))

# Wrong sign in the integration-by-parts correction is detected.
h={(0,2):F(1)}; a={(0,3):F(1)}
lhs=add(dotgrad(h,mul(t,a)),scale(mul(mul(t,t),dotgrad(mul(h,inv_t),a)),-1))
check('weak_lift_sign_negative', lhs != scale(deriv(mul(h,a),1),-1))

# Exact cone eigenvalue shift, including the sharp endpoint and angular harmonicity.
for d in range(3,41):
    for alpha in (F(k,2) for k in range(2,25)):
        beta=alpha-1
        check('spherical_shift', alpha*(alpha+d-2)-beta*(beta+d) == d-1)
    gamma=F(5,2)
    check('hemisphere_minmax_endpoint', F(3,2)*(F(3,2)+d)+(d-1) == gamma*(gamma+d-2))
    check('additive_gap_not_threshold', gamma-2 == F(1,2) and gamma-2 != gamma)
    for rho_degree in (F(1,2),F(1),F(3,2),F(2),F(5,2)):
        check('planar_polar_harmonic_coefficient', rho_degree*(rho_degree-1)+rho_degree-rho_degree**2 == 0)

# Degree-three scalar diagnostic: t(x^2-t^2/3) is harmonic.
P={(2,1):F(1),(0,3):F(-1,3)}
check('literal_gap_polynomial_diagnostic', lap(P)=={})

# Matrix commutant checks. Q is symmetric and commutes with three 90-degree
# rotations on the final three coordinates. The expected commutant is diag(A,cI3).
def rank_and_basis(rows, n):
    basis={}
    for row in rows:
        r=[F(a) for a in row]
        for p,b in sorted(basis.items()):
            if r[p]:
                c=r[p]
                r=[x-c*y for x,y in zip(r,b)]
        nz=next((j for j,x in enumerate(r) if x),None)
        if nz is not None:
            c=r[nz]
            basis[nz]=[x/c for x in r]
    return basis

def implied(row,basis):
    r=[F(a) for a in row]
    for p,b in sorted(basis.items()):
        if r[p]:
            c=r[p]
            r=[x-c*y for x,y in zip(r,b)]
    return not any(r)

for m in range(1,9):
    n=m+3
    variables=[(i,j) for i in range(n) for j in range(i,n)]
    index={ij:k for k,ij in enumerate(variables)}
    def qi(i,j):
        return index[tuple(sorted((i,j)))]
    rotations=[]
    for a,b in ((m,m+1),(m,m+2),(m+1,m+2)):
        R=[[int(i==j) for j in range(n)] for i in range(n)]
        R[a][a]=R[b][b]=0; R[a][b]=-1; R[b][a]=1
        rotations.append(R)
    rows=[]
    for R in rotations:
        for i,j in product(range(n),repeat=2):
            row=[F(0)]*len(variables)
            for k in range(n):
                row[qi(i,k)]+=R[k][j]
                row[qi(k,j)]-=R[i][k]
            rows.append(row)
    basis=rank_and_basis(rows,len(variables))
    check('rotation_commutant_dimension', len(basis)==len(variables)-(m*(m+1)//2+1))
    for i in range(m):
        for j in range(m,n):
            row=[F(0)]*len(variables); row[qi(i,j)]=1
            check('rotation_cross_block_zero',implied(row,basis))
    for i,j in ((m,m+1),(m,m+2),(m+1,m+2)):
        row=[F(0)]*len(variables);row[qi(i,j)]=1
        check('rotation_normal_offdiagonal_zero',implied(row,basis))
        row=[F(0)]*len(variables);row[qi(i,i)]=1;row[qi(j,j)]=-1
        check('rotation_normal_diagonal_equal',implied(row,basis))
check('rank_two_excludes_normal_three_space',3>2)

# Tree interpolation in exact arithmetic. Vertex represented canonically by (0,0).
points=[(0,F(0))]+[(i,r) for i in range(1,4) for r in (F(1,2),F(1),F(2))]
def td(a,b):
    return abs(a[1]-b[1]) if a[0]==b[0] else a[1]+b[1]
def geodesic(a,b,s):
    if a[0]==b[0]:
        r=(1-s)*a[1]+s*b[1]
        return (a[0],r) if r else (0,F(0))
    c=(1-s)*a[1]-s*b[1]
    return (a[0],c) if c>0 else (b[0],-c) if c<0 else (0,F(0))
times=(F(0),F(1,4),F(1,2),F(3,4),F(1))
for a,b in product(points,repeat=2):
    for s,tau in product(times,repeat=2):
        check('tree_constant_speed',td(geodesic(a,b,s),geodesic(a,b,tau))==abs(s-tau)*td(a,b))
    for c,d in product(points,repeat=2):
        s=F(1,2)
        check('tree_midpoint_lipschitz',td(geodesic(a,b,s),geodesic(c,d,s))<=F(1,2)*(td(a,c)+td(b,d)))

# Product slab threshold, with pi^2 treated as the positive unit of scaling.
for N in range(2,16):
    for Delta in (F(1,3),F(1),F(7,2),F(11)):
        threshold=F(N*(N*N-1),1)/Delta
        def horizontal_minus_slab(L_squared):
            return Delta-F(N*(N*N-1),1)/L_squared
        check('product_threshold_equality',horizontal_minus_slab(threshold)==0)
        check('product_long_slab_strict_improvement',horizontal_minus_slab(2*threshold)>0)
        check('product_short_slab_no_improvement',horizontal_minus_slab(threshold/2)<0)

# Finite Parseval controls for the thin-domain transverse gap. Factors pi^2 cancel.
for coeffs in product((F(-1),F(0),F(1,2),F(1)),repeat=5):
    norm=sum(c*c for c in coeffs)
    energy=sum((k+1)**2*c*c for k,c in enumerate(coeffs))
    tail=sum(c*c for c in coeffs[1:])
    exact=sum(((k+1)**2-1)*c*c for k,c in enumerate(coeffs))
    check('transverse_parseval_identity',energy-norm==exact)
    check('transverse_gap_three',energy-norm>=3*tail)
check('transverse_gap_cannot_be_four',F(4)-F(1)<4)

# The separated radial ODE and Bessel coefficient recurrence, all rational.
gamma=F(5,2)
for d in range(3,31):
    a=F(d-2,2);nu=gamma+a;angular=gamma*(gamma+d-2)
    check('bessel_order',nu==F(d+3,2))
    check('radial_ground_exponent',nu-a==gamma)
    check('radial_angular_constant',nu*nu-a*a==angular)
    for lam in (F(1),F(2,3),F(11,4)):
        coefficient=F(1)
        for k in range(1,13):
            new=-lam*coefficient/(4*k*(nu+k))
            exponent=gamma+2*k
            ode_factor=exponent*(exponent+d-2)-angular
            check('bessel_series_recurrence',ode_factor*new+lam*coefficient==0)
            check('wrong_bessel_order_negative',ode_factor*(-lam*coefficient/(4*k*(nu+1+k)))+lam*coefficient!=0)
            coefficient=new

print(json.dumps({'status':'PASS','exact_predicates':sum(counts.values()),'categories':counts,
                  'scope':'Finite algebraic controls only; not a formal proof or a spectral global-minimality certificate.'},
                 indent=2,sort_keys=True))

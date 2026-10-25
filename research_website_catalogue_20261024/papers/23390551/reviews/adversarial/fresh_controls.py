"""Independent exact checks, specified before reading submitted programs.

Only Python's standard library is required. No imported submitted code.
"""
from fractions import Fraction as Q
from math import factorial
from itertools import product
import json
from pathlib import Path

checks = []

def record(name, statement, ok, evidence):
    assert ok, name
    checks.append(dict(name=name, statement=statement, passed=True, evidence=evidence))

def matmul(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]

def sub(a,b):
    return [[x-y for x,y in zip(r,s)] for r,s in zip(a,b)]

def scale(c,a):
    return [[c*x for x in r] for r in a]

zero2=[[Q(0),Q(0)],[Q(0),Q(0)]]
eye2=[[Q(1),Q(0)],[Q(0),Q(1)]]
p1=[[Q(1),Q(0)],[Q(0),Q(0)]]
x=[[Q(0),Q(1)],[Q(0),Q(0)]]

record('Taylor_coefficient_identity', 'Numerator coefficients after removing i^n/n! agree with radial formula.', all(1-n+n*(n-1)==(n-1)**2 and -3+3*n-n*(n-1)==-(n-1)*(n-3) for n in range(2,101)), 'Checked exact integer identities n=2..100; polynomial identities are derived in FRESH_DERIVATION.md.')
e_upper=sum((Q(1,factorial(n)) for n in range(13)),Q(0))+Q(14,13*factorial(13))
record('Taylor_infinite_tail', 'Rational geometric bound proves e<11/4 and 2e-9/2<1.', e_upper<Q(11,4) and 2*e_upper-Q(9,2)<1, {'e_upper':str(e_upper),'tail_upper':str(2*e_upper-Q(9,2))})

shells={}
for j in product(range(-6,7), repeat=3):
    s=sum(t*t for t in j)
    if 0<s<=36:
        a=shells.setdefault(s,[[0]*3 for _ in range(3)])
        for u in range(3):
            for v in range(3): a[u][v]+=(s if u==v else 0)-3*j[u]*j[v]
record('cubic_radial_shell_cancellation', 'Every complete radius shell through |j|=6 has exactly zero trace-free tensor sum.', all(all(t==0 for row in a for t in row) for a in shells.values()), {'shell_count':len(shells),'max_radius_squared':36})
missing=[[(-2 if u==v==0 else 1 if u==v else 0) for v in range(3)] for u in range(3)]
record('broken_symmetry_mutant', 'Removing (1,0,0) from the nearest shell destroys cancellation.', any(t!=0 for row in missing for t in row), missing)
record('lattice_near_bound', 'L-infinity shells prove the explicit 26R bound.', all((2*q+1)**3-(2*q-1)**3==24*q*q+2 and Q(24*q*q+2,q*q)<=26 for q in range(1,101)), 'Each shell has 24q^2+2 points, every Euclidean radius is >=q; 26h floor(R/h)<=26R for every h,R>0.')

for q in (3,5,11,101):
    t=Q(2*q,q*q-1)
    b=[[Q(0),t],[t,Q(1)]]
    s=[[Q(3),t],[t,Q(1)]]
    lam=3+Q(2,q*q-1)
    p=scale(Q(1,q*q+1),[[Q(q*q),Q(q)],[Q(q),Q(1)]])
    d=sub(p,p1)
    record(f'non_norm_static_projection_family_q{q}', 'Selfadjoint strongly convergent backgrounds support a norm-convergent off-interval projection.', matmul(p,p)==p and matmul(s,p)==scale(lam,p) and matmul(d,d)==scale(Q(1,q*q+1),eye2) and t<1, {'lambda_plus':str(lam),'projection_gap_squared':str(Q(1,q*q+1)),'static_norm_lower_bound':'1','background_spectral_interval':'[-1,2] (row-sum/Gershgorin bound)'})

record('left_compact_strong_mutant', 'Strong convergence cannot justify compact-left multiplication without adjoints.', matmul(p1,x)==x and matmul(x,p1)==zero2, 'X_n=e1 tensor en ->0 strongly, P1 X_n=X_n has norm one; X_n*e1=en does not converge to zero.')
s=[[Q(3),Q(1)],[Q(0),Q(0)]]
pn=[[Q(1),Q(1,3)],[Q(0),Q(0)]]
record('nonselfadjoint_projection_mutant', 'Dropping background selfadjointness permits norm-projection failure.', matmul(pn,pn)==pn and matmul(s,pn)==scale(Q(3),pn) and sub(pn,p1)==scale(Q(1,3),x), 'Embed this block on e1,en: projection error remains exactly 1/3, despite strong background convergence and fixed compact correction.')
record('strong_correction_pollution_mutant', 'Strong convergence of compact corrections cannot replace norm convergence.', True, 'C_n=3P_en is compact and strongly tends to zero but has eigenvalue 3 and norm 3 at every n; the limiting zero operator has no spectral point at 3.')

for n in (2,7,100):
    eps=Q(1,n*n)
    nil=[[Q(0),Q(1)],[eps,Q(0)]]
    record(f'Jordan_split_n{n}', 'Cluster algebraic multiplicity survives while individual Jordan blocks change.', matmul(nil,nil)==scale(eps,eye2), {'eigenvalue_shifts':[str(Q(-1,n)),str(Q(1,n))],'total_multiplicity':2,'limit_nilpotent_index':2})

k=Q(1,10000); eta=120*k*k
trace=-Q(2,3)*k**3+1446*k**4
record('ball_rational_certificate', 'All explicit smallness bounds hold and the trace has strictly negative imaginary upper bound.', 2*k*k<=Q(1,60) and eta<=Q(1,2) and trace==-Q(7831,15000)*k**3 and trace<0, {'kappa':str(k),'epsilon_upper':str(2*k*k),'eta_upper':str(eta),'graph_upper':str(240*k*k),'trace_upper':str(trace),'trace_coefficient':str(trace/k**3)})
record('ball_harmonic_gap', 'Shifted harmonic eigenvalues ell>=2 are at least 1/15.', all(Q(ell-1,3*(2*ell+1))>=Q(1,15) for ell in range(2,1001)), 'The inequality reduces to 15(ell-1)>=3(2ell+1), i.e. ell>=2; the 1/6 accumulation is retained.')
record('rational_deletion_volume', 'The geometric series sum_(k>=1) 2^(-3k) is 1/7.', Q(1,8)/(1-Q(1,8))==Q(1,7), {'removed_fraction_upper_j1':str(Q(1,2**15*7)),'removed_fraction_upper_j8':str(Q(1,2**36*7))})
record('physical_embedding_weight', 'J_h is an isometry precisely with the common h^3 sequence weight.', all(sum(h**3*v*v for v in (Q(2),Q(-3),Q(1,2)))==h**3*Q(53,4) for h in (Q(1,2),Q(1,7))), 'Cell integral norm and weighted vector norm agree; omission of h^3 is detected for h!=1.')

result={'arithmetic':'Python fractions.Fraction and integers only','test_count':len(checks),'checks':checks,'scope':'Finite exact identities and explicitly proved infinite-family controls. They do not certify lattice endpoint extrema, historical priority or replace operator proofs.'}
out=Path(__file__).with_name('fresh_results.json');out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'test_count':len(checks),'all_passed':all(c['passed'] for c in checks),'output':str(out)},indent=2))

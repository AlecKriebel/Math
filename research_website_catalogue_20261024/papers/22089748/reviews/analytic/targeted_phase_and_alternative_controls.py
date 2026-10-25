#!/usr/bin/env python3
"""Bounded independent check of a reported identity and existing alternative proof.

No published helper imported; no replacement proof or repaired source generated.
"""
from pathlib import Path
from datetime import datetime, timezone
from fractions import Fraction as F
from math import comb
from itertools import combinations
import hashlib, json, sympy as s

out={'utc':datetime.now(timezone.utc).isoformat(),'checks':[]}
def ck(ok, label):
    if not ok: raise AssertionError(label)
    out['checks'].append(label)

# Eq.35 is a scalar binomial identity, independent of any numerical solve.
cases=[]
for N in (3,4,5,24,40,288):
    omega=lambda j:F(comb(N-2,j-1),2**(N-1)*(N+1))
    qb=lambda k:F(comb(N-3,k-2),2**(N-2)*(N+1))
    Y=lambda k:F(2*(k+1),3*k*(k-1))
    coefficient=lambda j:F(4*(j+2),3*(j+1)*(N-2))
    actual=sum(Y(k)*qb(k) for k in range(2,N))
    printed=sum(coefficient(j)*omega(j) for j in range(1,N-1))
    shifted=sum(coefficient(j)*omega(j+1) for j in range(1,N-1))
    ck(actual==shifted, f'Yq equals shifted binomial sum N={N}')
    ck(all(qb(k)==F(2*(k-1),N-2)*omega(k) for k in range(2,N)),f'q/omega exact N={N}')
    cases.append({'N':N,'Yq':str(actual),'printed_sum':str(printed),'difference':str(actual-printed)})
ck(cases[4]['difference']=='549755813107/501063941451939840','reported N40 counterexample independently authenticated')
out['eq35_counterexamples']=cases

# Existing forward-chain proof: reconstruct the interface of the displayed
# H polynomial to the stated curvature inequality, without importing verifier.
n,k,q=s.symbols('n k q', integer=True, positive=True)
def Q(i):return 4*i*(i-1)*(n-i)*(n-i-1)/(n*(n-1)*(n-2)*(n-3))
def O(i):return 2*i*(n-i)*(n-i-1)/(n*(n-1)*(n-2))
def I(i):return 2*i*(i-1)*(n-i)/(n*(n-1)*(n-2))
def w(h):return (n+k+h-n*2**(h+1)*q)/((k+h)*(n-k-h))
def p(i):return 2*(n-1)**2/(n+i-1)**2
def r(i):return 2*(n-1)**2/(n+i-2)**2
def d(h):return (n+k+h-1)/((n-1)*s.Integer(2)**h)
ell=2*(w(0)*(p(k)+r(k))*Q(k)+w(-1)*p(k-1)*(-Q(k-1)+2*O(k-1))+w(1)*r(k+1)*(-Q(k+1)+2*I(k+1)))
bar=s.Rational(21,20)*(n+k)/(4*n-2*k)*2*(n-1)*(n+k)/((n+k-1)*(n+k-2))
Dprev=w(-1)*(4*(n-1)**3*d(-1)*O(k-1)/(n+k-2)**3+4*(n-1)**3*d(-2)*I(k-1)/(n+k-3)**3)
j=k-1
C=j**3+3*j*j*n-3*j*j+3*j*n*n-10*j*n+6*j+n**3-7*n*n+12*n-6
A0=k*n-3*k+n*n-3*n+3
B0=k*k+2*k*n-6*k+n*n-4*n+5
H=20*(n+k-1-n*q)*C*(2*n-k)*(n-3)*(n+k-1)**2-21*n*(n-1)*(n+k)**2*(A0-q*B0)*(n+k-3)**2
ratio=s.factor(s.cancel((Dprev-ell*bar)/H))
ck(s.cancel(Dprev-ell*bar-ratio*H)==0,'alternative H is exactly the curvature-comparison numerator')
ck(s.cancel(ratio-4*(n-1)/(5*n*(n-3)*(n-2)*(2*n-k)*(n+k-3)**2*(n+k-2)**2*(n+k-1)**2))==0,'alternative H prefactor has displayed positive factorization')
out['alternative_H_prefactor_without_positive_rho_squared_2_power']=str(ratio)

# Check the averaging identities on multiple independent row-balanced symmetric
# directions, by literal enumeration of all subsets (not the reduced formula).
for nn in range(4,10):
    directions=[]
    for scale in (1,2):
        delta=[[0]*nn for _ in range(nn)]
        for aa,bb,v in [(0,1,1),(1,2,-1),(2,3,1),(3,0,-1)]:
            delta[aa][bb]=delta[bb][aa]=v
        if nn>=5 and scale==2:
            for aa,bb,v in [(1,2,2),(2,3,-2),(3,4,2),(4,1,-2)]:
                delta[aa][bb]+=v; delta[bb][aa]+=v
        directions.append(delta)
    for ix,delta in enumerate(directions):
        ck(all(sum(row)==0 for row in delta),f'fresh balanced direction n{nn}#{ix}')
        edge=sum(delta[a][b]**2 for a in range(nn) for b in range(a+1,nn))
        for kk in range(1,nn):
            sums=[0,0,0]
            for subset in combinations(range(nn),kk):
                ss=set(subset);ys=[sum(delta[v][u] for u in ss) for v in range(nn)]
                cut=sum(ys[v] for v in range(nn) if v not in ss)
                sums[0]+=cut*cut;sums[1]+=sum(ys[v]**2 for v in range(nn) if v not in ss);sums[2]+=sum(ys[v]**2 for v in ss)
            observed=[s.Rational(z,comb(nn,kk)*edge) for z in sums]
            expected=[s.cancel(expr.subs({n:nn,k:kk})) for expr in (Q(k),O(k),I(k))]
            ck(observed==expected,f'alternative cut-square identities n{nn}k{kk}#{ix}')

out['status']='PASS (identity error confirmed; existing alternative proof interfaces corroborated)'
out['scope']='Eq35 is disproved. The alternative proof is already published support, not a repair. This check does not prove or disprove the standalone A31 inequality.'
out['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
Path(__file__).with_name('targeted_phase_and_alternative_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'checks':len(out['checks']),'H_prefactor':str(ratio)}))

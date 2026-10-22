#!/usr/bin/env python3
"""Finite exact controls only; the infinite statements are proved in PROOF.md."""
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path
import json

counts = {}
def check(group, condition):
    counts[group] = counts.get(group, 0) + 1
    if not condition:
        raise AssertionError((group, counts[group]))

# Koopman/Cesaro identities on uniform cycles. These finite controls do not
# stand in for weak compactness or prove the general Hilbert-space theorem.
for q in range(2, 13):
    u = [F((i*i+3*i+7) % 17 - 8, i+1) for i in range(q)]
    phi = [u[(i+1)%q]-u[i] for i in range(q)]
    for N in range(1, 25):
        def S(n, i): return sum((phi[(i+j)%q] for j in range(n)), F(0))
        A = [sum((S(n,i) for n in range(1,N+1)),F(0))/N for i in range(q)]
        for i in range(q):
            check('telescoping_cycle', S(N,i) == u[(i+N)%q]-u[i])
            check('cesaro_cycle', A[i]-A[(i+1)%q] == phi[i]-S(N,(i+1)%q)/N)
        check('mean_zero_cycle', sum(phi)==0)
        check('norm_bound_cycle', sum(S(N,i)**2 for i in range(q)) <= 4*sum(v*v for v in u))

# Genuine one-sided Bernoulli cylinder calculations. The probability space
# here is modeled through sufficiently long finite-word marginals.
for width in range(1,5):
    def u(word):
        index=sum(bit << j for j,bit in enumerate(word[:width]))
        return F((index*index+3*index) % 11 - 5,3)
    u2=sum((u(w)**2 for w in product((0,1), repeat=width)),F(0))/2**width
    for n in range(1,7):
        norm2=F(0)
        for word in product((0,1), repeat=width+n):
            s=sum((u(word[j+1:])-u(word[j:]) for j in range(n)),F(0))
            check('bernoulli_telescope', s==u(word[n:])-u(word))
            norm2+=s*s
        norm2/=2**(width+n)
        check('bernoulli_norm_bound',norm2<=4*u2)

# Exact geometric moments, with no finite-tail approximation.
M=[1]
for j in range(1,9):
    M.append(sum(comb(j,i)*M[i] for i in range(j)))
    check('moment_recursion',2*M[j]==sum(comb(j,i)*M[i] for i in range(j+1)))
check('geometric_moments',M[:5]==[1,1,3,13,75])
check('centered_transfer_variance',M[4]-M[2]**2==66)
# e^(k^2)/2^(k+1) >= e^(k^2-k-1), since log2 < 1.
# The exponent tends to +infinity analytically; these are controls only.
for k in range(3,100):
    check('exp_obstruction_growth',k*k-k-1>0 and ((k+1)**2-(k+1)-1)>(k*k-k-1))

# Algebraic sign/centering controls, using u=k log2 and e^a=2^aindex.
# These arrays are local cocycle data, not an assertion of invariant models.
for v in range(-5,6):
    for w in range(-5,6):
        for d in (F(3,2),F(2),F(5,3)):
            for aindex in (-2,0,3):
                geometric=d**2
                J=F(2)**(aindex+w-v)*geometric
                rho=F(2)**(-v); rho_f=F(2)**(-w)
                check('conformal_sign',J*rho_f/rho==F(2)**aindex*geometric)
                if v!=w:
                    wrong=J*(F(2)**w)/(F(2)**v)
                    check('wrong_sign_rejected',wrong!=F(2)**aindex*geometric)

# Integer walk defining the Moran set. Adjacent interval ratios are rational.
b=[0]; peaks=[]; troughs=[]
for j in range(1,41):
    while b[-1]<j: b.append(b[-1]+1)
    peaks.append(len(b)-1)
    while b[-1]>-j: b.append(b[-1]-1)
    troughs.append(len(b)-1)
    check('moran_stage_endpoint',len(b)-1==2*j*j+j)
    check('moran_peak_value',b[peaks[-1]]==j)
    check('moran_trough_value',b[troughs[-1]]==-j)
for n in range(1,len(b)):
    ratio=F(1,4)*F(4,3)**(b[n]-b[n-1])
    check('moran_ratio',ratio in (F(1,3),F(3,16)))
    check('moran_separation',1-2*ratio>=ratio)
    check('moran_sublinear_control',b[n]**2<=n)
for j,(p,t) in enumerate(zip(peaks,troughs),1):
    # Squared half-dimensional cover cost and squared density upper bound.
    check('moran_cover_cost',F(4,3)**b[t]==F(3,4)**j)
    check('moran_density_control',9*F(4,3)**(-b[p])==9*F(3,4)**j)
    if j>1: check('moran_cover_decreasing',F(3,4)**j<F(3,4)**(j-1))

# Explicit finite interval geometry, built independently of the ball estimate.
intervals=[(F(0),F(1))]
for n in range(1,9):
    ell=F(1,4)**n*F(4,3)**b[n]
    nxt=[]
    for a,z in intervals: nxt.extend(((a,a+ell),(z-ell,z)))
    intervals=sorted(nxt)
    check('moran_interval_count',len(intervals)==2**n)
    for i,(a,z) in enumerate(intervals):
        check('moran_interval_length',z-a==ell)
        if i: check('moran_interval_gap',a-intervals[i-1][1]>=ell)

report={
 'status':'PASS',
 'arithmetic':'Python standard-library integers and fractions; no floating point',
 'checks':counts,
 'total_assertions':sum(counts.values()),
 'geometric_moments_0_to_8':M,
 'binary_transfer_mean':0,
 'binary_transfer_L2_norm_squared':66,
 'uniform_partial_sum_squared_bound':264,
 'moran_stages_checked':40,
 'moran_last_level_checked':len(b)-1,
 'scope':'Finite controls support exact identities only. Infinite proofs, source applicability, and the unresolved holomorphic implication are not mechanically certified.'
}
s=json.dumps(report,indent=2,sort_keys=True)+'\n'
if __name__=='__main__':
    import sys
    if '--write' in sys.argv: Path(__file__).with_name('verification_results.json').write_text(s)
    else:
        expected=Path(__file__).with_name('verification_results.json')
        if expected.exists():
            if expected.read_text()!=s: raise AssertionError('Committed results differ from recomputation')
    print(s,end='')

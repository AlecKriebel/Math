#!/usr/bin/env python3
"""Independent finite controls. These do not mechanically prove the infinite claims."""
from fractions import Fraction as Q
from math import comb
from itertools import product
from pathlib import Path
import json
import sys

counts = {}
def check(group, test):
    counts[group] = counts.get(group, 0) + 1
    if not test:
        raise AssertionError((group, counts[group]))

def plus(a,b):
    size=max(len(a),len(b))
    return [(a[i] if i<len(a) else Q(0))+(b[i] if i<len(b) else Q(0)) for i in range(size)]
def scale(a,c): return [x*c for x in a]
def shift(a,n=1): return [Q(0)]*n+a
def equal(a,b): return all(x==0 for x in plus(a,scale(b,-1)))
def norm2(a): return sum((x*x for x in a),Q(0))

# The orthonormal one-bit Walsh coordinates e_j on the ONE-SIDED fair shift
# obey U e_j=e_(j+1). Coefficient shifts model a genuine nonsurjective isometry,
# not a periodic truncation. All arrays have zero invariant constant component.
for width in range(1,13):
    u=[Q((-1)**j*(j+2),j+1) for j in range(width)]
    phi=plus(shift(u),scale(u,-1))
    check('one_sided_isometry', norm2(shift(u))==norm2(u))
    partial=[]; average=[]
    for n in range(1,41):
        partial=plus(partial,shift(phi,n-1))
        average=plus(average,partial)
        A=scale(average,Q(1,n))
        check('one_sided_telescope',equal(partial,plus(shift(u,n),scale(u,-1))))
        check('one_sided_cesaro',equal(plus(A,scale(shift(A),-1)),plus(phi,scale(shift(partial),Q(-1,n)))))
        check('one_sided_norm_bound',norm2(partial)<=4*norm2(u))
        check('one_sided_cesaro_remainder',norm2(scale(shift(partial),Q(1,n)))==norm2(partial)/n**2)
check('isometry_not_surjective', shift([Q(1)])[0]==0 and [Q(1)][0]!=0)

# Genuine Bernoulli branch Jacobians, using a positive one-coordinate density.
# On cylinder [b,c], m(TA)=p_c and J_m=1/p_b. The image/source ratio for
# nu=rho*m is therefore rho_c/(p_b*rho_b). No holomorphic realization asserted.
for p in [Q(1,5),Q(1,3),Q(1,2),Q(3,4)]:
    weights=[p,1-p]
    for rho in [[Q(1,2),Q(3)],[Q(2),Q(1,4)],[Q(1),Q(1)]]:
        total=sum(weights[b]*rho[b] for b in (0,1))
        for b,c in product((0,1),repeat=2):
            source=weights[b]*weights[c]*rho[b]
            target=weights[c]*rho[c]
            jac=Q(1)/weights[b]*rho[c]/rho[b]
            check('branch_change_of_density',jac*source==target)
            check('normalization_preserves_jacobian',(target/total)/(source/total)==jac)
            for e_a in [Q(1,4),Q(1),Q(8)]:
                geom=jac/e_a
                check('centering_factor_retained',e_a*geom*source==target)
                if e_a!=1:
                    check('dropping_nonzero_center_rejected',geom*source!=target)

# Independent exact geometric law moment recurrence plus explicit covariance.
M=[Q(1)]
for j in range(1,5): M.append(sum(Q(comb(j,i))*M[i] for i in range(j)))
check('run_length_moments',M==[1,1,3,13,75])
check('run_length_transfer_variance',M[4]-M[2]**2==66)
for n in range(1,101):
    early=sum(Q(k*k,2**(k+1)) for k in range(n))
    joint=3*early+Q(1,2**n)*(n*n*M[2]+2*n*M[3]+M[4])
    covariance=joint-9
    check('exact_run_length_covariance',covariance==Q(20*n+66,2**n))
    exact_norm=2*(M[4]-joint)
    check('exact_run_length_sum_norm',exact_norm==132-Q(20*n+66,2**(n-1)))
    check('sharper_binary_bound',0<exact_norm<132<264)

# Derive the Moran walk directly from stage coordinates, not iterative walking.
# Stage j starts after 2(j-1)^2+(j-1) steps; the peak index is 2j^2-j.
b=[0]
for j in range(1,61):
    start=len(b)-1
    peak=2*j*j-j
    end=2*j*j+j
    check('stage_length_formula',end-start==4*j-1)
    for n in range(start+1,end+1):
        value=-(j-1)+(n-start) if n<=peak else j-(n-peak)
        b.append(value)
        check('walk_sublinearity',value*value<=n)
        check('walk_unit_steps',abs(b[-1]-b[-2])==1)
    check('peak_trough_indices',b[peak]==j and b[end]==-j)
    check('critical_cost_squared',Q(4,3)**b[end]==Q(3,4)**j)
    check('good_density_squared',9*Q(4,3)**(-b[peak])==9*Q(3,4)**j)

# Explicit cylinders through level 9. Adjacent gaps >= ell establish the
# stated ball-overlap bound; checking first-to-fourth gaps gives direct
# protection against four level-n cylinders meeting a diameter-2ell ball.
intervals=[(Q(0),Q(1))]
for n in range(1,10):
    ell=Q(1,4)**n*Q(4,3)**b[n]
    intervals=sorted([z for a,c in intervals for z in [(a,a+ell),(c-ell,c)]])
    check('cylinder_count',len(intervals)==2**n)
    for i,(a,c) in enumerate(intervals):
        check('cylinder_length',c-a==ell)
        if i:check('cylinder_separation',a-intervals[i-1][1]>=ell)
        if i>=3:check('ball_cannot_meet_four_cylinders',a-intervals[i-3][1]>2*ell)

result={
    'status':'PASS',
    'arithmetic':'Exact integers and fractions; standard library only',
    'counts':counts,
    'total_assertions':sum(counts.values()),
    'independent_binary_identity':'||S_n phi||_2^2 = 132 - 2^(1-n)(20n+66), n>=1',
    'scope':'Finite identities and construction controls only. Weak compactness, measure-theoretic limits, source applicability, and the general holomorphic problem are not mechanically certified.'
}
text=json.dumps(result,indent=2,sort_keys=True)+'\n'
if __name__=='__main__':
    target=Path(__file__).with_name('AUDIT_RESULTS.json')
    if '--write' in sys.argv: target.write_text(text)
    elif target.read_text()!=text: raise AssertionError('Independent results changed')
    print(text,end='')

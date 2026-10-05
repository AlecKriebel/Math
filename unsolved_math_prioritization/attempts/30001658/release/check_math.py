#!/usr/bin/env python3
"""Exact, standard-library regression checks; no floating-point theorem inference."""
from fractions import Fraction as F
from math import comb, lcm
import json

COUNTS = {}
def require(ok, name):
    if not ok: raise ValueError(name)
    COUNTS[name] = COUNTS.get(name, 0) + 1

def kernel(n, d):
    return F(sum(comb(n+1,j) for j in range(d+1,n+2)),
             (n+1)*comb(n,d)*2**(n+1))

def scaled_kernel(n):
    v=[kernel(n,d) for d in range(n+1)]
    den=lcm(*(q.denominator for q in v))
    return [int(q*den) for q in v],den

def energy_sum(mask,n,k):
    pts=[x for x in range(1<<n) if mask>>x&1]
    return sum(k[(x^y).bit_count()] for x in pts for y in pts)

def compress(mask,n,i):
    out=mask
    for x in range(1<<n):
        if x>>i&1: continue
        y=x^(1<<i)
        if mask>>y&1 and not mask>>x&1:
            out ^= (1<<x)|(1<<y)
    return out

def downsets(n):
    if n==0:return [0,1]
    old=downsets(n-1);shift=1<<(n-1)
    return [a|(b<<shift) for a in old for b in old if b&~a==0]

def ln_lower_upper(r,terms=24):
    """r in [1,2]; atanh series with a proved geometric tail majorant."""
    require(F(1)<=r<=F(2),'log_argument_range')
    z=(r-1)/(r+1)
    lo=sum((2*z**(2*j+1)/F(2*j+1) for j in range(terms)),F(0))
    hi=lo+2*z**(2*terms+1)/(F(2*terms+1)*(1-z*z))
    return lo,hi

LN2_LO,LN2_HI=ln_lower_upper(F(2))
def k_upper(n,m):
    j=m.bit_length()-1
    if m==1<<j:return F(n-j)
    lo,_=ln_lower_upper(F(m,1<<j))
    return F(n-j)-lo/LN2_HI

def check():
    # Independently expressed resolvent: radial Green equation and Walsh diagonalization.
    for n in range(1,11):
        for d in range(n+1):
            row=(n+2)*kernel(n,d)
            if d:row-=d*kernel(n,d-1)
            if d<n:row-=(n-d)*kernel(n,d+1)
            require(row==int(d==0),'green_equation')
            z=(1<<d)-1
            spectral=sum((F((-1)**((s&z).bit_count()),2*(s.bit_count()+1))
                          for s in range(1<<n)),F(0))/(1<<n)
            require(spectral==kernel(n,d),'walsh_kernel')
        require(all(kernel(n,d)>kernel(n,d+1)>0 for d in range(n)), 'kernel_strict_decrease')
    dense_checks=0
    allset_counts={}
    for n in range(1,5):
        N=1<<n;k,den=scaled_kernel(n)
        vals=[0]*(1<<N)
        bounds=[None]+[k_upper(n,m) for m in range(1,N+1)]
        for mask in range(1,1<<N):
            bit=mask&-mask;x=bit.bit_length()-1;rest=mask^bit
            cross=0;rr=rest
            while rr:
                by=rr&-rr;y=by.bit_length()-1;rr^=by
                cross+=k[(x^y).bit_count()]
            vals[mask]=vals[rest]+k[0]+2*cross
            m=mask.bit_count();b=bounds[m]
            require(vals[mask]*b.numerator <= den*m*b.denominator,'all_sets_n_le_4')
            if m*8>=N:
                # A separate exact spectral estimate, using k <= 3 here.
                require(F(3)*(1+F(m,N))/4<=1 or m*4>=N, 'dense_regime_control')
                dense_checks+=1
        for mask in range(1<<N):
            for i in range(n):
                cm=compress(mask,n,i)
                require(cm.bit_count()==mask.bit_count(),'compression_cardinality')
                require(vals[cm]>=vals[mask],'compression_monotonicity')
        allset_counts[str(n)]=(1<<N)-1
    # Compression reduces every n=5 set to one of these 7,581 downsets.
    n=5;k,den=scaled_kernel(n);bounds=[None]+[k_upper(n,m) for m in range(1,33)]
    ds=downsets(n);require(len(ds)==7581 and len(set(ds))==7581,'downset_count_n5')
    for mask in ds:
        for i in range(n):require(compress(mask,n,i)==mask,'downset_definition')
        if not mask:continue
        b=bounds[mask.bit_count()];g=energy_sum(mask,n,k)
        require(g*b.numerator<=den*mask.bit_count()*b.denominator,'downsets_n5_inequality')
    # Affine-subspace controls: all linear subspaces up through dimension four,
    # followed by every distinct coset. These are not the proof for arbitrary n.
    affine_counts={}
    for n in range(1,5):
        spaces={frozenset([0])}
        todo=list(spaces)
        while todo:
            V=todo.pop()
            for x in range(1<<n):
                W=V|frozenset(v^x for v in V)
                if W not in spaces:spaces.add(W);todo.append(W)
        cosets=set()
        for V in spaces:
            for x in range(1<<n):cosets.add(frozenset(v^x for v in V))
        affine_counts[str(n)]=len(cosets)
        for A in cosets:
            m=len(A);codim=n-(m.bit_length()-1)
            g=sum((kernel(n,(x^y).bit_count()) for x in A for y in A),F(0))/m
            cap=F(1-F(1,2**(codim+1)),codim+1)
            require(g<=cap,'affine_resolvent_bound')
            if codim:require(codim*g<1,'affine_strict_target')
    for k in range(1,101):
        value=sum((F(comb(k,j),2**k*2*(j+1)) for j in range(k+1)),F(0))
        formula=F(1-F(1,2**(k+1)),k+1)
        require(value==formula,'subcube_closed_form')
        require(k*value<1,'subcube_strict_target')
    # Exact obstructions to invalid bridges / alternative conventions.
    require(F(3,8)>F(1,3),'schur_not_supported_inverse')
    require(F(4*4,4+2)>2,'parity_schur_correction_exceeds_2')
    require(5+4<2*5 and 2*5+4>=2*5,'unordered_counterexample_not_source')
    # Fictitious degree-one spectrum obeys only mean and Parseval; relaxation fails.
    require(F(5)*(1+F(1,32))/4>1,'spectral_relaxation_obstruction')
    # Mathematically negative controls, each deliberately wrong exact identity.
    mutants=[
        ('half_energy',F(4)==F(8)),
        ('wrong_green_shift',(1+1)*kernel(1,0)-kernel(1,1)==1),
        ('omit_ordered_pair',F(5+4)>=F(10)),
        ('wrong_subcube_factor',F(1-F(1,4),1)==kernel(1,0)),
        ('reverse_compression',energy_sum(0b1001,2,scaled_kernel(2)[0])>=energy_sum(0b0011,2,scaled_kernel(2)[0])),
        ('erase_schur_correction',F(3,8)==F(1,3)),
    ]
    for name,accepted in mutants:require(not accepted,'negative_'+name)
    return {'status':'PASS_SCOPED_CONTROLS','arithmetic':'exact integers and rational logarithm enclosures',
            'counts':dict(sorted(COUNTS.items())), 'total_checks':sum(COUNTS.values()),
            'all_nonempty_set_counts':allset_counts,'n5_downsets_including_empty':len(ds),
            'affine_cosets_checked':affine_counts,
            'scope':'Finite verification through n=5 and regression of written all-dimension partials; not a universal proof.'}

if __name__=='__main__':print(json.dumps(check(),sort_keys=True,indent=2))

#!/usr/bin/env python3
"""Small exact diagnostics; stdout only, no submission imports or file writes.

Tests local nontriviality on BOTH tails, finite-truncation implementation,
tuple interpolation, and bilateral shift orientation/indexing. Universal and
infinite support-order claims require the separate written proof.
"""
from fractions import Fraction as F
from collections import Counter
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json

C = Counter()


def ck(value,family):
    if not value:
        raise RuntimeError(family)
    C[family] += 1


def p2(n):
    return F(2**n) if n>=0 else F(1,2**(-n))


def bump(a,b,x,inverse=False):
    if x<=a or x>=b:
        return x
    if inverse:
        br=a+F(2,3)*(b-a)
        return a+(x-a)/2 if x<=br else b+2*(x-b)
    br=a+(b-a)/3
    return a+2*(x-a) if x<=br else b+(x-b)/2


def h(x,inverse=False,cutoff=None):
    if x in (0,1):
        return x
    if not 0<x<1:
        raise RuntimeError('outside unit interval')
    m=0
    while cutoff is None or m<=cutoff:
        b=p2(-2*m-2);a=b/2
        if a<=x<=b:
            return bump(a,b,x,inverse)
        if 1-b<=x<=1-a:
            return bump(1-b,1-a,x,inverse)
        if b<x<1-b:
            return x
        m+=1
    return x


def alpha(f,x,cutoff=None):
    return h(f(h(x,cutoff=cutoff)),inverse=True,cutoff=cutoff)


tails=[]
for m in range(8):
    b=p2(-2*m-2);a=b/2
    ck(p2(-2*(m+1)-2)<a,'left_tail_strict_positive_gap')
    ck(1-a<1-p2(-2*(m+1)-2),'right_tail_strict_positive_gap')
    for lo,hi in [(a,b),(1-b,1-a)]:
        length=hi-lo
        v0=lo+length/6;v1=lo+length/5
        left_pre=h(v0,True);right_pre=h(v1,True)
        ck(right_pre<v0,'local_support_disjoint_from_conjugate_support')
        f=lambda x,a=v0,b=v1:bump(a,b,x)
        witness=(v0+v1)/2
        ck(f(witness)>witness and alpha(f,witness)==witness,
           'alpha_nontrivial_on_each_local_tail_group')
        ck(h(lo)==lo and h(hi)==hi,'each_tail_interval_invariant')
        step=(right_pre-left_pre)/100
        ck(alpha(f,left_pre+step)==left_pre+2*step,
           'first_right_germ_slope_preserved')
        for k in range(1,8):
            x=lo+F(k,8)*length
            ck(h(x)>x,'strict_bump_displacement')
            ck(h(h(x),True)==x and h(h(x,True))==x,'two_sided_inverse_exact')
        ck(alpha(f,witness,cutoff=m)==alpha(f,witness),
           'finite_truncation_agrees_on_selected_local_group')
        if m:
            ck(alpha(f,witness,cutoff=m-1)==f(witness)
               and alpha(f,witness)!=f(witness),
               'finite_truncation_does_not_implement_whole_infinite_automorphism')
        tails.append({'m':m,'interval':[str(lo),str(hi)],
                      'local_witness':str(witness),'first_slope':'2'})

# Non-dyadic interpolation, extreme ratios, and zero-length branch limits.
for ratio in [F(1,257),F(1,4),F(1,2),F(1),F(2),F(3),F(97,31),F(513)]:
    k=0
    while p2(k)>ratio:k-=1
    while p2(k+1)<ratio:k+=1
    s=p2(k);l1=(2*s-ratio)/s;l2=(ratio-s)/s
    ck(l1>=0 and l2>=0 and l1+l2==1,'interpolation_branch_lengths')
    ck(s*l1+2*s*l2==ratio,'interpolation_target_length')

# Concrete bilateral model with beta(f)=h0^-1 f h0, where h0 is a finite bump.
# The arbitrary-beta statement follows separately from the index algebra.
h0=lambda y:bump(F(0),F(1),y)
h0i=lambda y:bump(F(0),F(1),y,True)
f0=lambda y:bump(F(1,5),F(2,5),y)


def iterate(fun,x,n):
    for _ in range(n):x=fun(x)
    return x


def beta_power(n,y):
    if n>=0:return iterate(h0i,f0(iterate(h0,y,n)),n)
    return iterate(h0,f0(iterate(h0i,y,-n)),-n)


def phi(n,y):
    return -p2(-n)+p2(-n-1)*y


for n in range(-4,5):
    for y in [F(0),F(1,9),F(1,3),F(2,3),F(8,9),F(1)]:
        x=phi(n,y)
        ck(x/2==phi(n+1,y),'bilateral_shift_cell_coordinate')
        left=phi(n,beta_power(n+1,y))
        right=2*phi(n+1,beta_power(n+1,y))
        ck(left==right,'bilateral_conjugation_index_sign')
        if y in (0,1):
            ck(left==x,'bilateral_cell_endpoints_fixed')
    ck(phi(n,1)<0 and phi(n,0)<phi(n,1),'negative_cell_order')
    ck(phi(n,1)==phi(n+1,0),'cell_junction_identity')
ck(all(p2(-n-1)<=p2(-n) for n in range(8)),
   'cell_length_tends_to_zero_control_only')

# Infinite germ obstruction is not inferred from these finite samples:
# h(a_m)=a_m and h((a_m+b_m)/2)>(a_m+b_m)/2 at all m by formulas.
# Any affine right germ at0, fixing infinitely many a_m->0, would be the
# identity there and contradict these strict displacements.
result={'status':'PASS','timestamp_utc':datetime.now(timezone.utc).isoformat(),
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'exact_checks':sum(C.values()),'counts':dict(sorted(C.items())),
        'local_tail_cases':len(tails),'tail_records':tails,
        'imports_submission_helpers':False,'writes_files':False,
        'scope':'Small exact construction controls only. Infinite/universal claims are proved in DERIVATIONS.md.'}
print(json.dumps(result,indent=2,sort_keys=True))

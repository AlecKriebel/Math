"""Independent exact finite controls for the rational-orbit packet.
No imports or execution of the packet's mathematical checker; no asymptotic certification.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import gcd
import json

class AuditFailure(Exception):
    pass

checks=Counter()
def check(value,label):
    if not value:
        raise AuditFailure(label)
    checks[label]+=1

def orbit(a,b,r,s,L):
    vals=[]
    an=1
    for n in range(L+1):
        bk=1
        for k in range(L+1):
            vals.append((r*an*bk)%s)
            bk=bk*b%s
        an=an*a%s
    return vals

def cover(xs,delta):
    """Dynamic program over all consecutive blocks with diameter <= delta."""
    xs=sorted(set(xs));d=[0]+[len(xs)+1]*len(xs)
    for j in range(1,len(xs)+1):
        for i in range(j-1,-1,-1):
            if xs[j-1]-xs[i]>delta:break
            d[j]=min(d[j],d[i]+1)
    return d[-1]

def order(a,q):
    if q==1:return 1
    z=a%q;h=1
    while z!=1:
        z=z*a%q;h+=1
        if h>q:raise AuditFailure('order did not terminate')
    return h

def run():
    checks.clear()
    # Every subset of each tiny prime grid, exact threshold endpoints included.
    for p in (3,5,7):
        deltas={Fraction(1,100),Fraction(1,3),Fraction(p-1,2*p)}
        for k in range(1,(p+1)//2):
            deltas.add(Fraction(k,p));deltas.add(Fraction(k,p)-Fraction(1,p*101))
        for mask in range(1,1<<p):
            U=[j for j in range(p) if mask>>j&1];T=len(U)
            for delta in sorted(deltas):
                Es=[]
                for r in range(1,p):
                    X=[Fraction(r*u%p,p) for u in U]
                    E=sum(min(abs(x-y),1-abs(x-y))<=delta for x in X for y in X)
                    Es.append(E)
                    check(E*cover(X,delta)>=T*T,'collision_cover')
                target=T*(p-1)+2*(p*delta.numerator//delta.denominator)*T*(T-1)
                check(sum(Es)==target,'collision_mean')
                for eta in (Fraction(1,2),Fraction(1,3),Fraction(2,3)):
                    mean=Fraction(target,p-1)
                    bad=sum(E>mean/eta for E in Es)
                    check(bad<=eta*(p-1),'markov_integer_bound')
    pairs=((2,3),(4,7),(4,6),(6,10),(8,9))
    for a,b in pairs:
        for s in range(2,101):
            if gcd(a*b,s)!=1:continue
            L=0
            while (a*b)**(L+1)<s:L+=1
            for r in range(1,s):
                if gcd(r,s)!=1:continue
                xs=orbit(a,b,r,s,L)
                check(len(set(xs))==(L+1)**2,'unit_injectivity')
                check((len(set(orbit(a,b,r,s,1)))==1)==((a-1)%s==0 and (b-1)%s==0),'singleton_iff')
        # Rational-neighborhood identities, with nontrivial signed wraparound.
        for q in range(1,10):
            if gcd(a*b,q)!=1:continue
            oa,ob=order(a,q),order(b,q);h=oa*ob//gcd(oa,ob)
            for u in range(q):
                for s in (101,211):
                    for r in {max(1,u*s//q),min(s-1,u*s//q+1)}:
                        if gcd(r,s)!=1:continue
                        eps=Fraction(r,s)-Fraction(u,q)
                        if not eps:continue
                        check(abs(eps)>=Fraction(1,q*s),'rational_difference_grid')
                        for n in range(3):
                            for k in range(3):
                                factor=pow(a,h*n)*pow(b,h*k)
                                lhs=(factor*Fraction(r,s))%1
                                rhs=(Fraction(u,q)+factor*eps)%1
                                check(lhs==rhs,'bounded_rational_identity')
    # Independent amplification tests using rational deltas, not floating logarithms.
    for a,b in pairs:
        for s in (101,211,1009,10007):
            if gcd(s,a*b)!=1:continue
            L0=0
            while (a*b)**(2*(L0+1))<s:L0+=1
            for r in {1,s//3,s//2,s-1}:
                if gcd(r,s)!=1:continue
                B=sorted(set(orbit(a,b,r,s,L0)))
                if len(B)<2:continue
                gap,x,y=min((v-u,u,v) for u,v in zip(B,B[1:]))
                d=Fraction(gap,s)
                check(Fraction(1,s)<=d<=Fraction(1,len(B)-1),'minimum_gap_bounds')
                for delta in (Fraction(1,1000),Fraction(1,10000),Fraction(1,s.bit_length()**4)):
                    j=0
                    while pow(a,j)*d<4*delta:j+=1
                    j0=j;ts=[]
                    while pow(a,j)*d<=Fraction(1,4):
                        ts.append((j,pow(a,j)*d));j+=1
                    if not ts:continue
                    H=L0+ts[-1][0]
                    A=set(orbit(a,b,r,s,H))
                    for e,t in ts:
                        xx=x*pow(a,e,s)%s;yy=y*pow(a,e,s)%s
                        check(xx in A and yy in A and Fraction((yy-xx)%s,s)==t,'amplification_membership')
                    for (_,u),(_,v) in combinations(ts,2):
                        check(min(v-u,1-(v-u))>2*delta,'amplification_strict_packing')
                    K=cover([Fraction(z,s) for z in A],delta)
                    check(K*K>=len(ts),'difference_cover_square')
                    check(pow(a,j0)*d<=max(d,4*a*delta),'first_expansion_upper_bound')
    # Cancellation verified as equality of rational probability coefficients.
    for a,b in pairs:
        for s in (11,17,25,35,61,101):
            if gcd(s,a*b)!=1:continue
            for L in range(5):
                den=(L+1)**2;raw=Counter(orbit(a,b,1,s,L))
                for g,other in ((a,b),(b,a)):
                    pushed=Counter()
                    for z,c in raw.items():pushed[g*z%s]+=c
                    boundary=Counter()
                    for k in range(L+1):
                        boundary[pow(g,L+1,s)*pow(other,k,s)%s]+=1
                        boundary[pow(other,k,s)]-=1
                    diff={z:pushed[z]-raw[z] for z in set(raw)|set(pushed)|set(boundary)}
                    check(all(diff[z]==boundary[z] for z in diff),'empirical_coefficient_identity')
                    check(Fraction(sum(abs(v) for v in diff.values()),den)<=Fraction(2,L+1),'empirical_tv')
    for a in range(2,8):
        for m in range(2,31):
            s=a**m-1;xs=[Fraction(a**j,s) for j in range(m)]
            check({(a*x)%1 for x in xs}==set(xs),'single_generator_invariant')
            for ell in range(1,m):
                q=a**ell;observed=Counter((q*x).numerator//(q*x).denominator for x in xs)
                want=Counter({0:m-ell});want.update({a**t:1 for t in range(ell)})
                check(observed==want,'single_generator_partition_counts')
                check(cover(xs,Fraction(1,q))<=ell+1,'single_generator_cover')
    # Half-open atom occupancy at closed interval endpoints: at most two.
    for q in range(1,30):
        for j in range(4*q):
            left=Fraction(j,4*q);right=min(Fraction(1),left+Fraction(1,q))
            pts={left,right}|{Fraction(k,q) for k in range(q) if left<=Fraction(k,q)<=right}
            atoms={int(q*x) for x in pts if x<1}
            check(len(atoms)<=2,'closed_interval_partition_occupancy')
    false_claims={
      'finite_fixed_witness_extends_to_s9':len(set(orbit(4,7,1,9,1)))==1,
      'all_numerators_without_unit':len(set(orbit(2,3,7,35,1)))==4,
      'dependent_bases_still_square':len(set(orbit(2,4,1,101,2)))==9,
      'finite_empirical_measure_is_exactly_invariant':Counter(2*z%101 for z in orbit(2,3,1,101,2))==Counter(orbit(2,3,1,101,2)),
      'source_representative_condition_is_invariant':(3**2<1)==(3**2<13),
      'sparse_orbit_has_same_coarse_entropy':len(Counter(int(2*x) for x in [Fraction(2**j,2**10-1) for j in range(10)]))==10,
      'support_cover_forces_entropy_lower_bound':False,
    }
    # An explicit low-entropy weighting on a two-point well-separated support.
    # H(eps,1-eps) <= eps*log(1/eps)+eps < 15 eps < 1/2 < log 2.
    # Here log(10**6)<14 and log 2>1/2 are elementary analytic bounds.
    check(cover([Fraction(0),Fraction(1,2)],Fraction(1,4))==2,'entropy_counterexample_support')
    false_claims['support_cover_forces_entropy_lower_bound']=15*Fraction(1,10**6)>=Fraction(1,2)
    try:
        Fraction(0,0)
        false_claims['collision_quotient_defined_for_empty_set']=True
    except ZeroDivisionError:
        false_claims['collision_quotient_defined_for_empty_set']=False
    for name,value in false_claims.items():check(not value,'wrong_claim_rejected:'+name)
    return {'status':'PASS','checks':sum(checks.values()),'families':dict(sorted(checks.items())),
      'limits':'Independent finite exact-arithmetic controls; no verification of asymptotic thresholds, external Baker theorem, universal openness, or proof syntax.'}

if __name__=='__main__':
    try:print(json.dumps(run(),sort_keys=True,indent=2))
    except AuditFailure as exc:
        print('FAILED: '+str(exc));raise SystemExit(2)

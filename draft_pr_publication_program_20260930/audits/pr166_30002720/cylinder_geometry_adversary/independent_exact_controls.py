#!/usr/bin/env python3
"""Independent rational cylinder and stopped-cost controls; not a limit proof."""
from fractions import Fraction as Q
from itertools import product, combinations
from math import isqrt
import json,sys
q=Q(3,4); r=Q(1,4)

def word_probability(word):
    if not word: return Q(1)
    ans=Q(1,2)
    for a,b in zip(word,word[1:]): ans*=q if a==b else r
    return ans

def interval(word):
    # Build conditional intervals directly, without the rank-sum formula.
    lo=Q(0); hi=Q(1); prev=None
    for digit in word:
        zero_share=Q(1,2) if prev is None else (q if prev==0 else r)
        split=lo+(hi-lo)*zero_share
        if digit==0: hi=split
        else: lo=split
        prev=digit
    return lo,hi

def rank_left(word):
    return sum((word_probability(word[:i]+(0,)) for i,b in enumerate(word) if b),Q(0))

def decode(u,depth):
    lo=Q(0); hi=Q(1); out=[]; prev=None
    for _ in range(depth):
        z=Q(1,2) if prev is None else (q if prev==0 else r)
        split=lo+(hi-lo)*z
        b=0 if u<split else 1
        if b==0: hi=split
        else: lo=split
        out.append(b);prev=b
    return tuple(out)

def sparse(depth):
    return tuple(int(isqrt(i)**2==i and isqrt(i)>=2) for i in range(1,depth+1))

def prefix_mass_sum(prefix):
    total=Q(1); mass=Q(1)
    for i,b in enumerate(prefix):
        mass*=Q(1,2) if i==0 else (q if b==prefix[i-1] else r)
        total+=mass
    return total

def endpoint_mean(prefix,terminal):
    # All prefixes through prefix, followed by the first tail transition
    # and the stationary self-transition geometric series.
    ans=prefix_mass_sum(prefix)
    if not prefix: return ans+Q(1,2)/(1-q)
    return ans+word_probability(prefix)*(q if prefix[-1]==terminal else r)/(1-q)

def radix_select(items,k):
    # Direct recursion on the bucket currently containing the selected item.
    if len(items)<=1: return 0
    zero=[s[1:] for s in items if s[0]==0]
    one=[s[1:] for s in items if s[0]==1]
    return len(items)+(radix_select(zero,k) if k<=len(zero) else radix_select(one,k-len(zero)))

def prefix_cost(items,target):
    ans=0
    for d in range(len(target)+1):
        count=sum(s[:d]==target[:d] for s in items)
        if count<=1: return ans
        ans+=count
    raise AssertionError('Inputs not distinguished by finite control depth')

checks={}; mutation=[]
words_tested=0
for d in range(13):
    last=Q(0)
    for w in product((0,1),repeat=d):
        lo,hi=interval(w)
        assert lo==last and hi-lo==word_probability(w) and lo==rank_left(w)
        if d: assert decode((lo+hi)/2,d)==w
        assert hi-lo <= (Q(1) if d==0 else Q(1,2)*q**(d-1))
        last=hi; words_tested+=1
    assert last==1
checks['cylinder_partition_words']=words_tested
rows=[]
for j in range(2,51):
    W=sparse(j*j-1); P=word_probability(W); K=j//2
    flips=sum(a!=b for a,b in zip(W,W[1:])); keeps=len(W)-1-flips
    formula=Q(1,2)*r**(2*j-4)*q**(j*j-2*j+2)
    assert flips==2*j-4 and keeps==j*j-2*j+2 and W[-1]==0 and P==formula
    C=prefix_mass_sum(W)
    A=endpoint_mean(W+(0,),1); B=endpoint_mean(W+(1,),0)
    assert A==C+Q(3,2)*P and B==C+Q(1,2)*P and A-B==P
    tau=interval(W+(1,))[0]
    rank_sum=sum((q*word_probability(sparse(i*i-1)) for i in range(2,j+1)),Q(0))
    assert tau==rank_sum
    lc=interval(W+(0,)+(1,)*K);rc=interval(W+(1,)+(0,)*K)
    assert lc[1]==tau and rc[0]==tau
    assert lc[1]-lc[0]==P*q**K/4 and rc[1]-rc[0]==P*q**K/12
    next_prefix=W+(1,)+(0,)*(2*j)
    near=interval(next_prefix)
    assert near[0]==tau and near[1]-near[0]==P*q**(2*j)/12
    w=P*q**j
    assert (w<min(lc[1]-lc[0],rc[1]-rc[0]))==(j>=17)
    # Sum twenty future square contributions and independently enclose all
    # remaining contributions using decreasing exact ratios.
    partial=sum((q*word_probability(sparse(i*i-1)) for i in range(j+1,j+21)),Q(0))
    first=q*word_probability(sparse((j+1)*(j+1)-1))
    upper=first/(1-r*r*q**(2*j+1))
    assert Q(0)<partial<upper<P*q**(2*j)/12
    assert first==P*q**(2*j)/16
    for d in (0,1,3,j*j-1,j*j,j*j+2*j):
        pref=sparse(d);lo,hi=interval(pref)
        # Two actual future 1s and at least one intervening zero prove
        # interiority of finite rank approximations once past the prefix.
        vlong=sparse(max(d+10,(j+2)*(j+2)+1))
        rr=rank_left(vlong)
        assert lo<rr<hi
    rows.append({'j':j,'changes':flips,'preservations':keeps,'P':str(P),'tau':str(tau),'jump_over_P':str((A-B)/P),'left_length_over_P':str((lc[1]-lc[0])/P),'right_length_over_P':str((rc[1]-rc[0])/P),'window_inside_both':j>=17})
checks['square_indices']=len(rows)
# Check exact stopped cost on all subsets of at most four distinct 4-bit words.
universe=list(product((0,1),repeat=4));cases=0
for n in range(1,5):
    for items in combinations(universe,n):
        for k,target in enumerate(items,1):
            assert radix_select(items,k)==prefix_cost(items,target)
            cases+=1
checks['recursive_stopped_cost_rank_cases']=cases
# Deliberate erroneous conventions must be detected by these exact controls.
W=sparse(3);P=word_probability(W)
assert P!=Q(1,2)*q**3
mutation.append({'mutation':'count initial symbol as a transition','witness':'j=2, W=000','correct':str(P),'mutated':str(Q(1,2)*q**3),'detected':True})
correct_jump=endpoint_mean(W+(0,),1)-endpoint_mean(W+(1,),0)
wrong_jump=P*(q-r)/(1-q)
assert correct_jump!=wrong_jump
mutation.append({'mutation':'omit first terminal switch in endpoint sums','witness':'j=2','correct_jump':str(correct_jump),'mutated_jump':str(wrong_jump),'detected':True})
assert interval(W+(1,))[0]!=interval(W)[0]+P*r
mutation.append({'mutation':'use transition-to-one mass as rank increment','witness':'j=2','correct_boundary':str(interval(W+(1,))[0]),'mutated_boundary':str(interval(W)[0]+P*r),'detected':True})
assert interval(W+(0,))[1]-interval(W+(0,))[0]!=P/4
mutation.append({'mutation':'apply left local length formula at K=0','witness':'j=2,K=0 (outside actual K_j>=1 assumption)','correct_length':str(P*q),'mutated_length':str(P/4),'detected':True})
items=((0,0,0,0),(0,0,0,1));correct=radix_select(items,1)
assert correct==8 and correct!=6
mutation.append({'mutation':'omit empty-prefix/root charge','witness':'0000,0001;rank1','correct_cost':correct,'mutated_cost':6,'detected':True})
assert radix_select(((0,0,0,0),),1)==0
mutation.append({'mutation':'continue charging after singleton','witness':'one input; any four symbols','correct_cost':0,'mutated_finite_depth_cost':4,'detected':True,'infinite_version':'diverges'})
# Independent exact conservative bound on the analytic cost-band error.
# For j>=2: log n<=3(j^2+j), H<=91j^2, sqrt(2log n)<=3j.
# Hence E/P <= q^floor(j/2)+546j^3q^j+182j^2q^(4j)+91j^2q^(2j)+2q^(10j).
j=100
band_error=q**(j//2)+546*j**3*q**j+182*j**2*q**(4*j)+91*j**2*q**(2*j)+2*q**(10*j)
assert band_error<Q(1,8)
# Each polynomial*exponential term decreases thereafter; direct rational ratios.
for power,expo in [(3,1),(2,4),(2,2)]:
    assert Q(j+1,j)**power*q**expo<1
checks['all_j_ge_100_conservative_band_error_bound']={'j100_exact':str(band_error),'j100_float_for_display':float(band_error),'strictly_below':'1/8','monotonicity_ratios_verified_at_100':True,'proof_required':'Ratios decrease for larger j; q^floor(j/2) is nonincreasing.'}
# Fixed-rank rational enclosure using fifty square contributions.
tau50=sum((q*word_probability(sparse(i*i-1)) for i in range(2,51)),Q(0))
first51=q*word_probability(sparse(51*51-1));tail_upper=first51/(1-r*r*q**101)
checks['t_enclosure']={'lower':str(tau50),'upper':str(tau50+tail_upper),'float_for_display':float(tau50),'strictly_inside_0_1':True,'finite_enclosure_not_identity_with_t':True}
result={'kind':'independent exact finite controls and all-index bound diagnostics','author_verifier_read':False,'checks':checks,'rows':rows,'negative_mutations':mutation,'negative_mutations_detected':len(mutation),'finite_computations_are_not_asymptotic_proof':True}
json.dump(result,sys.stdout,indent=2);print()

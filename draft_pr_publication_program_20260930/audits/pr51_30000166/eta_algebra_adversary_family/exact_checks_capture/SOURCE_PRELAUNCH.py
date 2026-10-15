#!/usr/bin/env python3
"""Independent bounded eta-product checks; no imported submitted helper.
Exact Euler recurrence, generalized-binomial product, hook enumeration and
provably complete finite theta sublevels. Standard library only.
"""
from collections import Counter
from fractions import Fraction
from itertools import product
from math import comb, gcd
import hashlib,json
from pathlib import Path

ASSERTIONS=Counter()
def check(condition,family):
    if not condition: raise AssertionError(family)
    ASSERTIONS[family]+=1

def prime_factorization(n):
    ps={};d=2
    while d*d<=n:
        if n%d==0:
            ps[d]=0
            while n%d==0: n//=d;ps[d]+=1
        d+=1
    if n>1: ps[n]=1
    return ps

def mobius(n):
    ps=prime_factorization(n)
    return 0 if any(v>1 for v in ps.values()) else (-1)**len(ps)
def totient(n):
    z=n
    for p in prime_factorization(n): z=z//p*(p-1)
    return z

def divisor_list(n): return [d for d in range(1,n+1) if n%d==0]

def eta_exponents(n,H):
    # Derived after the Mobius sum is evaluated, independently of divisor loop.
    return [0]+[totient(n)*int(k%n==0)-int(gcd(n,k)==1) for k in range(1,H+1)]

def recurrence(exps,H):
    # q F'/F = sum_m b_m q^m; m a_m = sum_j b_j a_(m-j).
    b=[0]*(H+1)
    for d in range(1,H+1):
        for m in range(d,H+1,d): b[m]-=d*exps[d]
    a=[1]
    for n in range(1,H+1):
        s=sum(b[j]*a[n-j] for j in range(1,n+1))
        check(s%n==0,'Euler exact integer division')
        a.append(s//n)
    return a

def binomial_product(exps,H):
    a=[1]+[0]*H
    for k in range(1,H+1):
        e=exps[k]
        if e==0: continue
        cs=([(-1)**j*comb(e,j) for j in range(min(e,H//k)+1)] if e>0 else
            [comb(-e+j-1,j) for j in range(H//k+1)])
        a=[sum(cs[j]*a[m-k*j] for j in range(min(len(cs)-1,m//k)+1)) for m in range(H+1)]
    return a

def convolution(a,b,H): return [sum(a[j]*b[i-j] for j in range(i+1)) for i in range(H+1)]

def partitions(n,maximum=None):
    if n==0: yield ();return
    if maximum is None: maximum=n
    for a in range(min(n,maximum),0,-1):
        for rest in partitions(n-a,a): yield (a,)+rest

def hooks(part):
    return [row-j+sum(int(k>j) for k in part[i+1:]) for i,row in enumerate(part) for j in range(row)]

def qform(ns):
    a=len(ns)
    return sum(a*x*(x-1)//2+i*x for i,x in enumerate(ns))

def theta(a,M,r,H):
    # Q >= a |n_i|(|n_i|-1)/2, so a coordinate outside this box
    # cannot appear at degree <= H after e >= (M-r)Q is proved.
    B=1
    while (M-r)*a*B*(B-1)//2<=H: B+=1
    out=[0]*(H+1);points=0
    for ns0 in product(range(1-B,B),repeat=a-1):
        ns=ns0+(-sum(ns0),)
        if abs(ns[-1])>=B: continue
        Q=qform(ns)
        for j in range(a):
            e=M*Q+r*(a*ns[j]+j)
            check(e>=0,'Theta specialized nonnegative exponent')
            if e<=H: out[e]+=1
        points+=1
    return out,B,points

def theta_product_exponents(a,M,r,H):
    # C = E(q^M) E(q^(aM))^(a-2) [q^(ar);q^(aM)]/[q^r;q^M].
    return [0]+[int(k%M==0)+(a-2)*int(k%(a*M)==0)
        +int(k%(a*M)==a*r)+int(k%(a*M)==a*(M-r))
        -int(k%M==r)-int(k%M==M-r) for k in range(1,H+1)]

H=144
normalization=[]
for n in range(1,361):
    es=eta_exponents(n,H)
    direct=[0]+[totient(n)*int(k%n==0)-sum(mobius(d) for d in divisor_list(n) if k%d==0) for k in range(1,H+1)]
    check(es==direct,'Mobius vs gcd product exponents')
    cs=recurrence(es,H)
    check(all(c>=0 for c in cs),'All-N finite eta positivity')
    if n<=45 or n in (60,72,105,120,180,210,225,300,360):
        check(cs==binomial_product(es,H),'Independent coefficient algorithms')
    A=Fraction(n*totient(n)-sum(d*mobius(d) for d in divisor_list(n)),24)
    check(A>=0,'Eta leading exponent nonnegative')
    check(sum(d*mobius(d) for d in divisor_list(n))==__import__('functools').reduce(lambda x,p:x*(1-p),prime_factorization(n),1),'Leading shift prime product')
    if n<=12: normalization.append({'N':n,'A_numerator':A.numerator,'A_denominator':A.denominator,'first_12_coefficients':cs[:12]})
    if n==1:
        check(cs==[1]+[0]*H,'N=1 exact boundary');continue
    ps=prime_factorization(n);p=2 if n%2==0 else min(ps);alpha=ps[p]
    M=n//p**alpha;t=p**(alpha-1);n0=p*M
    check(M%2==1 and gcd(M,p)==1 and n==p**alpha*M,'All integer split')
    lifted=[0]+[eta_exponents(n0,H)[k]+totient(n0)*(t*int(k%n==0)-int(k%n0==0)) for k in range(1,H+1)]
    check(es==lifted,'Prime power lift exponents')
    if M>1:
        rs=[r for r in range(1,(M+1)//2) if gcd(r,M)==1]
        check(2*len(rs)==totient(M),'Odd residue pair coverage')
        rhs=[0]+[sum((2*p-2)*int(k%n0==0)+int(k%n0==p*r)+int(k%n0==p*(M-r))-int(k%M==r)-int(k%M==M-r) for r in rs) for k in range(1,H+1)]
        check(rhs==eta_exponents(n0,H),'D-product exact factor exponents')
    else:
        check(eta_exponents(p,H)==[0]+[p*int(k%p==0)-1 for k in range(1,H+1)],'Prime core reduction')

# Independent hook tests include composite t and t=1, not only prime cores.
core_cases=[]
for t in range(1,11):
    bound=22
    expected=[sum(all(h%t for h in hooks(part)) for part in partitions(n)) for n in range(bound+1)]
    es=[0]+[t*int(k%t==0)-1 for k in range(1,bound+1)]
    check(recurrence(es,bound)==expected,'Direct partition hook core identity')
    core_cases.append({'t':t,'degree':bound,'coefficients':expected})

# Supplemental exact lattice diagnostics. The universal symbolic derivation
# is written in PROOF_AUDIT.md rather than inferred from this finite lattice.
for a in range(2,8):
    for ns0 in product(range(-2,3),repeat=min(a-1,3)):
        # Cover high dimensions without pretending an exhaustive lattice proof.
        ns=ns0+(0,)*(a-1-len(ns0))+(-sum(ns0),)
        Q=qform(ns)
        check(Q>=0,'Lattice Q nonnegative diagnostic')
        for i,x in enumerate(ns):
            c=a*x*(x-1)//2+i*x
            check(c>=a*abs(x)*(abs(x)-1)//2,'Coordinate sublevel lower bound')
        for j in range(a):
            tr=list(ns[1:]+ns[:1])
            if j: tr[j-1]+=1;tr[-1]-=1
            check(sum(tr)==0,'T_j lattice preservation')
            check(qform(tr)-Q==a*ns[j]+j,'T_j exact difference')
            for M,r in ((2,1),(5,1),(5,4),(7,3)):
                check(M*Q+r*(a*ns[j]+j)==(M-r)*Q+r*qform(tr),'Specialization convex decomposition')

cases=[]
for a in (2,3,4,5):
    for M in range(2,9):
        for r in range(1,M):
            bound=32
            coeffs,B,points=theta(a,M,r,bound)
            prod=recurrence(theta_product_exponents(a,M,r,bound),bound)
            check(coeffs==prod,'Complete finite theta identity')
            # D includes the independently verified core factor at base q^M.
            core=recurrence([0]+[a*int(k%(a*M)==0)-int(k%M==0) for k in range(1,bound+1)],bound)
            ds=convolution(coeffs,core,bound)
            de=[0]+[(2*a-2)*int(k%(a*M)==0)+int(k%(a*M)==a*r)+int(k%(a*M)==a*(M-r))-int(k%M==r)-int(k%M==M-r) for k in range(1,bound+1)]
            check(ds==recurrence(de,bound) and min(ds)>=0,'D positive factor identity')
            cases.append({'a':a,'M':M,'r':r,'degree':bound,'exclusive_coordinate_bound':B,'enumerated_lattice_points':points,'coefficient_sha256':hashlib.sha256(json.dumps(coeffs,separators=(',',':')).encode()).hexdigest()})

# Falsifiers show the controls detect the exact sign/exponent mistakes most
# likely to arise during transcription. They are not broader impossibility claims.
mutants=[]
for name,a,M,r in [('missing E(q^M)',3,5,2),('wrong a-2 exponent',4,7,3),('one missing bracket residue',2,3,1),('unscaled numerator residue',3,5,1)]:
    es=theta_product_exponents(a,M,r,32)
    if name=='missing E(q^M)':
        es=[v-int(k%M==0) if k else 0 for k,v in enumerate(es)]
    elif name=='wrong a-2 exponent':
        es=[v+int(k%(a*M)==0) if k else 0 for k,v in enumerate(es)]
    elif name=='one missing bracket residue':
        es=[v-int(k%(a*M)==a*(M-r)) if k else 0 for k,v in enumerate(es)]
    else:
        es=[v-int(k%(a*M)==a*r)+int(k%(a*M)==r) if k else 0 for k,v in enumerate(es)]
    good,_,_=theta(a,M,r,32);bad=recurrence(es,32)
    first=next((i for i,(x,y) in enumerate(zip(good,bad)) if x!=y),None)
    check(first is not None,'Deliberate mutation rejected')
    mutants.append({'name':name,'a':a,'M':M,'r':r,'first_difference':first,'theta_coefficient':good[first],'mutant_coefficient':bad[first]})

result={'status':'PASS','assertions':sum(ASSERTIONS.values()),'by_family':dict(ASSERTIONS),'eta_N_range':[1,360],'eta_degree':H,'theta_case_count':len(cases),'theta_cases':cases,'core_cases':core_cases,'normalization_small_cases':normalization,'mutants':mutants,'limitation':'Finite exact controls and complete degree-bounded theta enumeration. Universal proof and imported classical core/theta identities are separately audited in PROOF_AUDIT.md; neither finite counts nor floating point nor modular/Sturm certification prove positivity.'}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':result['status'],'assertions':result['assertions'],'by_family':result['by_family'],'theta_case_count':len(cases),'mutants':mutants},indent=2,sort_keys=True))

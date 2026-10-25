"""Independent prime-polynomial truth and adversarial boundary controls.

Only the explicitly labeled implementation-under-test calls use the supplied
modules. Truth computations below use separate integer polynomial arithmetic,
trial division, and an explicit F9 model. No prior checker is imported.
"""
from pathlib import Path
from itertools import product
from collections import Counter
from math import comb
import sys, json, hashlib, datetime

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'published_code'))
import finite_fields as ff
import sparse_cartier as sc
C=Counter(); negative={}; samples=[]
def check(ok,label):
    if not ok: raise AssertionError(label)
    C[label]+=1
def trim(f,p):
    f=[x%p for x in f]
    while f and f[-1]==0: f.pop()
    return tuple(f)
def mul(f,g,p):
    h=[0]*(len(f)+len(g)-1) if f and g else []
    for i,a in enumerate(f):
        for j,b in enumerate(g):h[i+j]=(h[i+j]+a*b)%p
    return trim(h,p)
def div(f,g,p):
    f=list(trim(f,p));g=trim(g,p);q=[0]*max(0,len(f)-len(g)+1)
    while len(f)>=len(g) and f:
        j=len(f)-len(g);a=f[-1]*pow(g[-1],-1,p)%p;q[j]=a
        for k,b in enumerate(g):f[j+k]=(f[j+k]-a*b)%p
        while f and f[-1]==0:f.pop()
    return trim(q,p),tuple(f)
def power(f,e,p):
    out=(1,)
    while e:
        if e&1:out=mul(out,f,p)
        e//=2
        if e:f=mul(f,f,p)
    return out
def irr(f,p):
    if len(f)<2:return False
    return all(div(f,g+(1,),p)[1] for d in range(1,(len(f)-1)//2+1)
               for g in product(range(p),repeat=d))
def valuation(f,g,p):
    e=0
    while len(f)>=len(g):
        q,r=div(f,g,p)
        if r:break
        e+=1;f=q
    return e
def fact(f,p):
    unit=f[-1];left=trim([a*pow(unit,-1,p) for a in f],p);out={}
    for d in range(1,len(left)):
        if len(left)==1:break
        for c in product(range(p),repeat=d):
            g=c+(1,)
            if not irr(g,p):continue
            e=valuation(left,g,p)
            if e:
                out[g]=e
                left,r=div(left,power(g,e,p),p)
                check(not r,'trial_division_reconstruction')
    check(left==(1,),'trial_factorization_exhausted')
    return unit,out

for p,maximum in [(2,7),(3,4),(5,3)]:
    K=ff.FiniteField(p,(0,1))
    for degree in range(maximum+1):
        for low in product(range(p),repeat=degree):
            f=low+(1,);unit,want=fact(f,p)
            terms=[(i,a) for i,a in enumerate(f) if a]
            got,audit=sc.factor_sparse(K,terms)
            actual={tuple(x[0] for x in g):e for g,e in got.factors}
            check(actual==want and got.unit==(unit,),'complete_sparse_vs_independent_trial_factorization')
            D=sum(len(g)-1 for g in want);b=max(1,degree.bit_length());t=len(terms)
            check(len(audit['levels'])<=b,'actual_descent_count_bound')
            for k,level in enumerate(audit['levels']):
                check(level['denominator_degree']<=k*D,'actual_denominator_growth_bound')
                check(level['visible_degree']<=(k+1)*D,'actual_visible_oracle_degree_bound')
                check(level['residue_product_degree']<=max(0,t-1)*(k+1)*D,
                      'actual_residue_product_sparse_bound')
            if degree:
                for g,e in want.items():
                    value=sc.quotient_multiplicity(K,sc.normalized_sparse(K,terms),K.poly(g))
                    check(value==e,'quotient_trie_vs_independent_repeated_division')

# Exhaustive integer valuations cover the carry that makes floor(e_F/p) wrong.
carry=None
for p in [2,3,5,11,101]:
    for eu in range(102):
        for ev in range(eu+1):
            eh=eu//p-ev//p;ef=eu-ev;r=eu%p-ev%p
            check(eh>=0 and r+p*eh==ef,'signed_carry_exact_multiplicity')
            check(ef>0 or eh==0,'radical_containment_from_integer_valuations')
            if eh!=ef//p and carry is None:carry={'p':p,'eU':eu,'eV':ev,'eF':ef,'eH':eh,'signed_residue':r}
check(carry is not None,'naive_floor_descent_negative_control');negative['carry']=carry

# Direct dense algebra for one Cartier step on arbitrary polynomial quotients.
for p in [2,3,5]:
    roots=list(range(1,p))[:2]
    gs=[((-a)%p,1) for a in roots]
    for exps in product(range(5),repeat=2*len(gs)):
        ef,ev=exps[:len(gs)],exps[len(gs):]
        F=V=AU=AV=HU=HV=(1,)
        for g,fv,vv in zip(gs,ef,ev):
            F=mul(F,power(g,fv,p),p);V=mul(V,power(g,vv,p),p)
            AU=mul(AU,power(g,(fv+vv)%p,p),p)
            AV=mul(AV,power(g,vv%p,p),p)
            HU=mul(HU,power(g,(fv+vv)//p,p),p)
            HV=mul(HV,power(g,vv//p,p),p)
        U=mul(F,V,p);unew=trim(U[::p],p);W=trim(AU[::p],p);vnew=mul(W,HV,p)
        check(unew==mul(W,HU,p),'direct_Cartier_pullout')
        H,remainder=div(HU,HV,p)
        check(not remainder and div(unew,vnew,p)==(H,()),'new_denominator_divides_new_numerator')
        DF=sum(1 for e in ef if e);v=len(V)-1
        check(len(vnew)-1<=v+DF,'direct_denominator_degree_invariant')
        check(len(unew)-1<=(len(U)-1)//p,'numerator_numeric_degree_shrinks')

# Large-characteristic, huge-exponent tests must not invoke a numeric-p oracle.
p=2**127-1;K=ff.FiniteField(p,(0,1))
def forbid_oracle(p,f):raise AssertionError('unexpected prime-oracle use in one-factor fixture')
for k in [1,3,8]:
    s=p**k
    small=power((p-2,1),5,p);sparse={}
    for j,c in enumerate(small):
        if c:sparse[j+7]=(-6*c)%p;sparse[j+s+7]=(3*c)%p
    got,audit=sc.factor_sparse(K,sparse.items(),prime_oracle=forbid_oracle)
    check(dict(got.factors)=={K.poly((0,1)):7,K.poly((p-2,1)):s+5}
          and got.unit==K.element(3),'large_binary_characteristic_and_exponents')
    check(len(audit['levels'])<=k+1,'large_characteristic_uses_digit_levels')
    samples.append({'p_bits':p.bit_length(),'exponent_bits':(s+12).bit_length(),
                    'terms':len(sparse),'D':2,'levels':len(audit['levels'])})

# F9 is modeled independently as a+b*z, z^2=-1 over F3.
def eadd(a,b):return ((a[0]+b[0])%3,(a[1]+b[1])%3)
def eneg(a):return ((-a[0])%3,(-a[1])%3)
def emul(a,b):return ((a[0]*b[0]-a[1]*b[1])%3,(a[0]*b[1]+a[1]*b[0])%3)
def epow(a,n):
    b=(1,0)
    while n:
        if n&1:b=emul(a,b)
        n//=2
        if n:a=emul(a,a)
    return b
K=ff.FiniteField(3,(1,0,1));a=(1,1);scalar=(2,1)
for c in product(range(3),repeat=2):
    check(sc.coefficient_root(K,c)==epow(c,3),'inverse_Frobenius_against_independent_F9')
check(epow(a,3)!=a,'copying_extension_coefficients_negative_control')
for k in [1,4,30]:
    s=3**k;ap=epow(a,s)
    terms={0:emul(scalar,emul(a,ap)),1:emul(scalar,eneg(ap)),
           s:emul(scalar,eneg(a)),s+1:scalar}
    got,audit=sc.factor_sparse(K,terms.items())
    check(got.unit==scalar and dict(got.factors)=={(eneg(a),K.one):s+1},
          'extension_sparse_descent_known_factor_truth')
    samples.append({'field':'F9','exponent_bits':(s+1).bit_length(),'terms':4,'D':1,
                    'levels':len(audit['levels'])})

# A long zero Taylor prefix is not an exact logarithmic-derivative certificate.
K=ff.FiniteField(2,(0,1));audit=[]
G=sc.logarithmic_denominator(K,{0:K.one,16:K.one,17:K.one},audit)
check(not audit[0]['accepted'] and len(G)-1==17,'false_Pade_prefix_rejected')
# Keeping exponent residues modulo alpha's multiplicative order destroys valuation.
check(sc.quotient_multiplicity(K,{0:K.one,1024:K.one},K.poly((1,1)))==1024,
      'integer_exponent_information_retained')
negative['exponent_reduction']='At alpha=1, replacing exponents0 and1024 by residues modulo1 turns a nonzero polynomial with valuation1024 into zero.'

print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'status':'PASS','assertions':sum(C.values()),'families':dict(C),'samples':samples,
 'negative_controls':negative,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'limits':'Finite exact truth/control tests. Calls under test import supplied core modules; independent truth uses separately written prime polynomial arithmetic and F9 model. No asymptotic complexity or upstream theorem certification.'},indent=2))

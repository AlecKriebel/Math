#!/usr/bin/env python3
"""Independent exact checks. No author imports, network, or PDF dependencies.
Run with Python 3 + SymPy. See AUDIT.md for proofs and scope.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib, json, platform
import sympy as s

RESULT = {}
# First establish the frozen bytes, when the original author packet is adjacent.
root=Path(__file__).resolve().parent.parent
manifest=root/'author'/'MANIFEST.json'
if manifest.exists():
    expected='6c1444e73c64c5b5a2e9eaebda234d3befb997fbf209c7522377c02b0c4bbf4a'
    assert hashlib.sha256(manifest.read_bytes()).hexdigest()==expected
    entries=json.loads(manifest.read_text())['files']
    for e in entries:
        data=(manifest.parent/e['path']).read_bytes()
        assert len(data)==e['bytes']
        assert hashlib.sha256(data).hexdigest()==e['sha256'], e['path']
    RESULT['frozen_manifest_and_files']=len(entries)

# Sparse Laurent polynomials: exponents ordered (p,q,u1,u2,u3).
Z=(0,0,0,0,0)
def add(*polys):
    d=defaultdict(int)
    for poly in polys:
        for ex,co in poly.items(): d[ex]+=co
    return {ex:co for ex,co in d.items() if co}
def mul(a,b):
    d=defaultdict(int)
    for ea,ca in a.items():
        for eb,cb in b.items():d[tuple(x+y for x,y in zip(ea,eb))]+=ca*cb
    return {ex:co for ex,co in d.items() if co}
def term(ex,co=1):return {tuple(ex):co}
def monshift(poly,ex,co=1):return mul(poly,term(ex,co))
D1=mul({Z:1,(1,0,0,0,0):-1},{Z:1,(-1,1,0,0,0):-1})
D2=mul({Z:1,(1,-1,0,0,0):-1},{Z:1,(0,1,0,0,0):-1})
# Transcribed monomials from the repaired common numerator.
HIGH=[((1,1,1),1),((0,2,0),-1),((0,0,2),-1)]
LOW=[((1,-1,-1),1),((-1,1,-1),1),((-1,-1,1),1),((-2,0,0),-1)]
def A(r):
    if r>0: return {(i,j,0,0,0):-1 for i in range(r) for j in range(r-i)}
    return {(-i,-j,0,0,0):-1 for i in range(1,-r) for j in range(1,-r-i+1)}
def original_ratio_numerator(flux):
    # Direct chart substitution, independently of the finite-triangle formula.
    sl={};vir={}
    for high, terms in [(True,HIGH),(False,LOW)]:
        for u,co in terms:
            r=sum(a*b for a,b in zip(u,flux))
            ps,qs=(1,1) if high else (0,0)
            pv,qv=(2,0) if high else (0,0)
            sl=add(sl,term((ps+r,qs,*u),co),term((ps,qs,*u),-co))
            vir=add(vir,term((pv,qv+r,*u),co),term((pv,qv,*u),-co))
    return add(mul(sl,D2),mul(vir,D1))
def finite_ratio_character(flux):
    ans={}
    for u,co in HIGH:
        r=sum(a*b for a,b in zip(u,flux))
        ans=add(ans,monshift(A(r-1),(2,1,*u),co))
    for u,co in LOW:
        r=sum(a*b for a,b in zip(u,flux))
        ans=add(ans,monshift(A(r),(0,0,*u),co))
    return ans
def euler(poly,weights):
    ans=F(1)
    for ex,co in poly.items():
        wt=sum(a*b for a,b in zip(ex,weights))
        assert wt, ('unexpected zero test weight',ex,weights)
        ans*=wt**(-co)
    return ans
def triangle(r,x,e1,e2):
    ans=F(1)
    points=((i,j) for i in range(r) for j in range(r-i)) if r>0 else ((-i,-j) for i in range(1,-r) for j in range(1,-r-i+1))
    for i,j in points:ans*=x-i*e1-j*e2
    return ans
def BFT(m,n,l,mu,nu,la,K):
    t=lambda r,x: triangle(r,x,F(1),-1/K)
    expo=(l-m+n)*(l-m+n+1)//2 + 2*n*(m-n)*(2*(m-n)-1)
    value=F(-1 if expo%2 else 1)
    for r,x in [(-l-m-n,-(2+la+mu+nu)/(2*K)),(-l+m-n,-(la-mu+nu)/(2*K)),(-l-m+n,-(la+mu-nu)/(2*K)),(l-m-n,-(-la+mu+nu)/(2*K))]:value*=t(r,x)
    for r,x in [(-2*l,-(la+1)/K),(-2*m,-(mu+1)/K),(-2*n,-(nu+1)/K)]:value/=t(r,x)
    return value
def N(l,la,K):return triangle(-2*l,-la/K,F(1),-1/K)/triangle(-2*l,-(la+1)/K,F(1),-1/K)

count=0
parameters=[(F(19,7),F(31,23),F(37,29),F(41,31)),(F(-17,5),F(43,37),F(47,41),F(53,43))]
for flux in product(range(-4,5),repeat=3):
    finite=finite_ratio_character(flux)
    assert original_ratio_numerator(flux)==mul(finite,mul(D1,D2)),flux
    l,n,m=flux
    for K,la,nu,mu in parameters:
        actual=euler(finite,(F(1),-K,la/2,nu/2,mu/2))
        target=(-1 if (l+m)%2 else 1)*BFT(m,n,l,mu,nu,la,K)/N(l,la,K)
        assert actual==target,(flux,K)
        count+=1
RESULT['independent_formal_character_triples']=9**3
RESULT['independent_exact_E_vs_source_BFT_comparisons']=count
# Sewing directly from the Laurent characters, not the author's triangle ratio.
K,la,mu1,mu2=parameters[0]
mu3,mu4=F(59,47),F(61,53)
for j in range(-8,9):
    first=euler(finite_ratio_character((0,0,j)),(F(1),-K,mu1/2,mu2/2,la/2))
    second=euler(finite_ratio_character((j,0,0)),(F(1),-K,la/2,mu3/2,mu4/2))
    coef=BFT(j,0,0,la,mu2,mu1,K)*BFT(0,0,j,mu4,mu3,la,K)/N(j,la,K)
    assert first*second==coef,j
RESULT['independent_Laurent_sewings']=17
# A check designed to fail if one follows printed B.7 instead of the repaired order.
l,n,m=0,1,0
actual=euler(finite_ratio_character((l,n,m)),(F(1),-K,la/2,mu2/2,mu1/2))
wrong=BFT(m,n,l,mu2,mu1,la,K)/N(l,la,K)
assert actual!=wrong and actual!=-wrong
RESULT['printed_B7_mu_nu_swap_witness_ratio']=str(actual/wrong)

p,q,u,v,w=s.symbols('p q u v w')
def c(kind,p,q,u,v,w,printed=False):
    a=u*v*w-u*u-v*v if printed and kind=='S' else u*v*w-v*v-w*w
    b=u/v/w+v/u/w+w/u/v-u**-2
    return ((p*p*q if kind=='S' else p*p*q*q)*a+b)/((1-p)*(1-q))
raw=s.factor(c('S',p,q,u,v,w,True)-c('S',p,q/p,u,v,w,True)-c('V',p/q,q,u,v,w))
assert s.cancel(raw+p*p*q*(u*u-w*w)/((p-q)*(q-1)))==0
assert raw.subs({p:2,q:3,u:5,v:7,w:11})==-576
assert s.cancel(c('S',p,q,u,v,w)-c('S',p,q/p,u,v,w)-c('V',p/q,q,u,v,w))==0
RESULT['printed_B10_residual']=str(raw)
rev=c('S',p,q/p,u*p,v,w)+c('V',p/q,q,u,v,w*q)-c('S',p,q/p,u,v,w)-c('V',p/q,q,u,v,w)
residue=s.factor(s.cancel((p-q)*rev).subs(q,p))
assert residue!=0
RESULT['printed_B6_reversed_flux_pole_coefficient']=str(residue)
# A symbolic recurrence proves the first finite-character identity for all integers.
x,y=s.symbols('x y') # x=p^r, y=q^r
DD1=(1-p)*(1-q/p);DD2=(1-p/q)*(1-q)
step=p**0*x*(p-1)/DD1+y*(q-1)/DD2
assert s.cancel(step-(q*y-p*x)/(p-q))==0
assert s.cancel(q/p*(x-1)/DD1+(y-1)/DD2-q*((x/p-1)/DD1+(y/q-1)/DD2))==0
RESULT['arbitrary_integer_character_recurrence_algebra']=True
l,n,m=s.symbols('l n m',integer=True)
d=lambda r:r*(r+1)/2
sigma=d(l-n-m)+d(-l+n-m)+d(-l-n+m)-d(-2*l)
sgn=d(l-m+n)+2*n*(m-n)*(2*(m-n)-1)
even=-l*(l+1)+m*(m-1)+n*(n-1)-2*l*n-2*n*(m-n)*(2*(m-n)-1)
assert s.expand(sigma-sgn-l-m-even)==0
assert s.expand(d(-l-n-m)+d(l-n-m)+d(-l+n-m)+d(-l-n+m)-d(-2*l)-d(-2*n)-d(-2*m))==0
RESULT['all_integer_sign_parity_and_scaling']=True
K,h,j=s.symbols('K h j')
H=lambda x,k:x*(x+2)/(4*k)
bb=-K/(K+1);Pb=-(h+1)*bb/(2*K)
assert s.factor(H(h+2*j,K+1)-H(h,K+1)-2*j*Pb-j*j*bb)==j*j
assert s.factor(H(h,K+1)+(1-(h+1)**2)*(-1/(K*(K+1)))/4-H(h,K))==0
wrong=s.factor(H(h+2*j,K+1)-H(h,K+1)-j*(h+1)/K+j*j*(K+1)/K-j*j)
assert wrong.subs({K:2,h:0,j:1})==F(2,3)
RESULT['coset_grade_and_base_weight']=True
RESULT['printed_OWR_grade_residual']=str(wrong)
# Explicit exceptional locus: nonzero norms cannot be dropped from hypotheses.
num=K-h-1;den=K-h-2
assert num.subs(h,K-1)==0 and den.subs(h,K-1)!=0
assert den.subs(h,K-2)==0 and num.subs(h,K-2)!=0
RESULT['norm_N1_zero_and_pole_loci']='zero at lambda=K-1; pole at lambda=K-2'
print(json.dumps({'status':'PASS_PARTIAL','python':platform.python_version(),'sympy':s.__version__,'checks':RESULT,'scope':'Independent finite-character, coefficient, and sewing audit. Published Eq.4.59 is an input. No certification of convention-specific gauge partition functions or singular analytic limits.'},indent=2))

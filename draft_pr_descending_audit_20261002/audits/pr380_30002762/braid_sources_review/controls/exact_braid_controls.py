"""Independent faithful Artin-action controls, authored before candidate access.
No candidate imports, tables, or precomputed outcomes. Python standard library only.
An automorphism is the tuple of reduced free words which are its basis images.
Composition f*g is f after g, giving the conventional braid product.
These computations are finite corroboration; INDEPENDENT_NOTES gives universal K proof.
"""
from functools import lru_cache
from fractions import Fraction
import json

def reduce(w):
    s=[]
    for x in w:
        if s and s[-1]==-x:s.pop()
        else:s.append(x)
    return tuple(s)

def inverse_word(w):return tuple(-x for x in reversed(w))

def substitute(f,w):
    out=[]
    for x in w:
        image=f[abs(x)-1] if x>0 else inverse_word(f[-x-1])
        for y in image:
            if out and out[-1]==-y:out.pop()
            else:out.append(y)
    return tuple(out)

def compose(f,g):return tuple(substitute(f,w) for w in g)
def identity(n):return tuple((i,) for i in range(1,n+1))

@lru_cache(None)
def generator(n,i):
    f=list(identity(n));j=abs(i)
    if i>0:f[j-1]=(j,j+1,-j);f[j]=(j,)
    else:f[j-1]=(j+1,);f[j]=(-(j+1),j,j+1)
    return tuple(f)

def action(n,w):
    f=identity(n)
    for i in w:f=compose(f,generator(n,i))
    return f

def power(f,k):
    assert k>=0
    r=identity(len(f))
    while k:
        if k&1:r=compose(r,f)
        f=compose(f,f);k//=2
    return r

def conjugate(t,x,ti):return compose(compose(t,x),ti)
def commute(x,y):return compose(x,y)==compose(y,x)

def torus_sign_at_minus_one(n,p):
    # GG2005 Prop5.1 exact Dedekind sum, root omega=-1 (theta=1/2).
    s=0
    for i in range(1,n):
        for j in range(1,p):
            v=Fraction(1,2)+Fraction(i,n)+Fraction(j,p)
            v=v%2
            s+=(1 if 0<v<1 else -1 if 1<v<2 else 0)
    return s

rows=[]
for K in range(9):
    n=3*(K+1);a=generator(n,1);b=generator(n,2);I=identity(n)
    delta=tuple(range(1,n));t=action(n,delta*3);ti=action(n,inverse_word(delta*3))
    assert compose(t,ti)==I==compose(ti,t)
    assert action(n,(1,2,1))==action(n,(2,1,2))
    tests=[]
    for k in range(1,K+1):
        tk=power(t,k);tik=power(ti,k)
        ak=conjugate(tk,a,tik);bk=conjugate(tk,b,tik)
        assert ak==generator(n,1+3*k),('shift a',K,k)
        assert bk==generator(n,2+3*k),('shift b',K,k)
        for u in (a,b):
            for v in (ak,bk):
                assert commute(u,v),('relator',K,k)
                tests.append(True)
    q=K+1;aq=conjugate(power(t,q),a,power(ti,q));bq=conjugate(power(t,q),b,power(ti,q))
    assert aq==a and bq==b
    assert not commute(a,bq),('omitted distance',K)
    assert not commute(a,b),('distance0',K)
    g=(-1,)*4+(2,1,1,2);Z=(1,2)*3
    assert action(n,g)==action(n,(-1,)*6+Z)
    assert commute(action(n,Z),a)
    # Unit mutation: shift only2indices; b meets shifted a at adjacent indices.
    wrong_t=action(n,delta*2);wrong_ti=action(n,inverse_word(delta*2))
    wrong_relation=not commute(b,conjugate(wrong_t,a,wrong_ti)) if K>=1 else None
    if K>=1:assert wrong_relation
    rows.append({'K':K,'strands':n,'four_pair_relators_checked':len(tests),'boundary_shift_checked':K>0,'omitted_distance':q,'omitted_relation_fails':True,'distance0_fails':True,'stride2_mutation_fails':wrong_relation,'detector_identity_checked':True})

# Exact signatures of central torus braids and two-strand generator powers.
# GG2005 sign convention is negative on positive torus braids. For every p,
# sigma(σ1^(p))=-(p-1); sigma((σ1σ2)^(3p))=-4p for positive integer p.
# The latter limit yields homogenized sigma(Z)=-4 without floating-point claims.
sig=[]
for p in range(1,41):
    s2=torus_sign_at_minus_one(2,p);s3=torus_sign_at_minus_one(3,3*p)
    assert s2==-(p-1)
    assert s3==-4*p
    sig.append({'p':p,'sign_sigma1_power':s2,'sign_Z_power':s3})
print(json.dumps({'representation':'faithful Artin automorphisms on the free group; exact reduced words','finite_relator_results':rows,'exact_torus_signature_sums':sig,'homogeneous_signature_detector':str(-6*Fraction(-1)+Fraction(-4)),'scope':'finite checks K=0..8, p=1..40; universal identities and limits are proved separately'},indent=2))

#!/usr/bin/env python3
"""Read-only audit of frozen packet plus independent exact stress controls.
No remote actions, third-party dependencies, floating point, or proof search.
"""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import permutations, product
from pathlib import Path
import json
import runpy

ROOT=Path(__file__).resolve().parent.parent
PUB=ROOT/'public'
EXPECTED='1bf1bf1b7bf7b1232a75bac9e742940a9fcbb52bbe27847a947a3c56226d4075'

def digest():
    fs=sorted(p for p in PUB.iterdir() if p.is_file())
    return len(fs),sha256(b''.join(p.name.encode()+b'\0'+sha256(p.read_bytes()).digest() for p in fs)).hexdigest()

def frozen_and_original():
    assert digest()==(15,EXPECTED)
    manifest=json.loads((PUB/'MANIFEST.json').read_text())
    for name,row in manifest['files'].items():
        b=(PUB/name).read_bytes()
        assert len(b)==row['bytes'] and sha256(b).hexdigest()==row['sha256']
    # Calling functions, not main(), avoids rewriting frozen verification.json.
    ns=runpy.run_path(str(PUB/'verify.py'),run_name='read_only_audit')
    actual={k:ns[f]() for k,f in [('torus','torus_controls'),('s3','s3_control'),('abelian','abelian_controls'),('cyclic','cyclic_cocycle_controls')]}
    assert actual==json.loads((PUB/'verification.json').read_text())['checks']
    assert digest()==(15,EXPECTED)
    return {'files':15,'packet_sha256':EXPECTED,'manifest_entries_checked':len(manifest['files']),'saved_verification_reproduced':True,'frozen_bytes_unchanged':True}

def cyclic_bar_chains():
    def clean(c):return Counter({k:v for k,v in c.items() if v})
    def basis(coef,t):
        return Counter({(coef,tuple(t)):1}) if 0 not in t else Counter()
    def add(out,c,mult=1):
        for k,v in c.items():out[k]+=mult*v
    def d(c,n):
        out=Counter()
        for (r,t),mult in c.items():
            add(out,basis((r+t[0])%n,t[1:]),mult)
            for j in range(len(t)-1):
                tt=t[:j]+((t[j]+t[j+1])%n,)+t[j+2:]
                add(out,basis(r,tt),mult*(-1)**(j+1))
            add(out,basis(r,t[:-1]),mult*(-1)**len(t))
        return clean(out)
    for n in range(2,32):
        f2=Counter();f3=Counter();Nf1=Counter();gf2=Counter()
        for j in range(n):
            add(f2,basis(0,(j,1)));add(f3,basis(0,(1,j,1)));add(Nf1,basis(j,(1,)))
            add(gf2,basis(1,(j,1)));add(gf2,basis(0,(j,1)),-1)
        assert d(f2,n)==clean(Nf1)
        assert d(f3,n)==clean(gf2)
        # Sum coefficients after trivial-module tensoring gives a cycle.
        triv=Counter()
        for (r,t),mult in d(f3,n).items():triv[t]+=mult
        assert not clean(triv)
    return {'cyclic_orders':list(range(2,32)),'free_bar_comparison_identities':60,'trivial_coefficient_cycles':30}

def exact_nonreal_torus():
    count=0;summary=[]
    for p in (3,5):
        labels=list(product(range(p),repeat=2))
        B=lambda a,b:(a[0]*b[1]+a[1]*b[0])%p
        # Integer numerator polynomials at zeta_p; equality iff all
        # coefficient differences agree, by the prime cyclotomic polynomial.
        def eq_poly(a,b):
            diff=[a[r]-b[r] for r in range(p)]
            return len(set(diff))==1
        def mon(e,m=1):
            c=[0]*p;c[e%p]=m;return c
        for j in labels:
            for k in labels:
                num=[0]*p
                for i in labels:num[(B(k,i)-B(i,j))%p]+=1
                assert eq_poly(num,mon(0,p*p if j==k else 0))
                count+=1
            for l in labels:
                for g in labels:
                    num=[0]*p
                    for i in labels:
                        rem=((g[0]-i[0])%p,(g[1]-i[1])%p)
                        num[(-B(i,j)-B(rem,l))%p]+=1
                    assert eq_poly(num,mon(-B(g,j),p*p if j==l else 0))
                    count+=1
        # epsilon(p_j)=1/p^2; positive sqrt=1/p. Both are exact.
        assert Fraction(1,p)**2==Fraction(1,p*p)
        summary.append({'prime':p,'rank':p*p,'has_nonselfdual_labels':True,'counit_weight':str(Fraction(1,p*p))})
    return {'tests':summary,'exact_S_and_idempotent_coefficient_checks':count}

def groupoid_normalization():
    G=list(permutations(range(3)));I=(0,1,2)
    mul=lambda a,b:tuple(a[b[i]] for i in range(3))
    inv=lambda a:tuple(a.index(i) for i in range(3))
    def power(a,n):
        r=I
        for _ in range(n):r=mul(r,a)
        return r
    out=[]
    for n in range(1,13):
        eligible={a for a in G if power(a,n)==I};unseen=set(eligible);weighted=Fraction(0);orbits=0
        while unseen:
            a=next(iter(unseen));orbit={mul(mul(h,a),inv(h)) for h in G};unseen-=orbit
            cent=sum(mul(h,a)==mul(a,h) for h in G)
            weighted+=Fraction(1,cent);orbits+=1
        assert weighted==Fraction(len(eligible),6)
        out.append({'n':n,'weighted_value':str(weighted),'unweighted_orbits':orbits})
    assert out[1]['weighted_value']=='2/3' and out[1]['unweighted_orbits']==2
    return {'S3_lens_space_checks':out,'S3_value':'1/6'}

def coboundary_lens_control():
    tests=0
    for p in (2,3,5,7,11,13,17,19,23,29):
        # An arbitrary deterministic normalized 2-cochain in exponent form.
        beta=lambda a,b:(a*b*(a+2*b+1))%p
        db=lambda a,b,c:(beta(b,c)-beta((a+b)%p,c)+beta(a,(b+c)%p)-beta(a,b))%p
        for x in range(p):
            assert sum(db(x,j*x%p,x) for j in range(p))%p==0
            for u in range(p):
                s=sum((u*x*((j*x%p+x)//p)+db(x,j*x%p,x)) for j in range(p))%p
                assert s==u*x*x%p;tests+=1
    return {'coboundary_modified_lens_exponent_checks':tests}

if __name__=='__main__':
    result={'status':'PASS','scope':'Verification only; original converse remains unresolved.','frozen':frozen_and_original(),'independent_controls':{'bar_chains':cyclic_bar_chains(),'nonreal_torus':exact_nonreal_torus(),'groupoid':groupoid_normalization(),'coboundary_lens':coboundary_lens_control()}}
    assert digest()==(15,EXPECTED)
    out=Path(__file__).with_name('independent_verification.json');out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))

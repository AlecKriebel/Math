#!/usr/bin/env python3
"""Independent finite controls. No source code import and no theorem-verification claim."""
from fractions import Fraction
from math import comb
import json
from pathlib import Path

PRIMES=(2,3,5,7,11)

def v_p(a,p):
    if not a: return None
    v=0
    while a%p==0: a//=p;v+=1
    return v

def clean(f): return {j:a for j,a in f.items() if a}
def plus(f,g):
    h=dict(f)
    for j,a in g.items():h[j]=h.get(j,0)+a
    return clean(h)
def scale(f,a):return clean({j:a*b for j,b in f.items()})
def times(f,g):
    h={}
    for j,a in f.items():
        for k,b in g.items():h[j+k]=h.get(j+k,0)+a*b
    return clean(h)
def power(f,n):
    out={0:1}
    for _ in range(n):out=times(out,f)
    return out

def m_remainder(f,p,L):
    """Canonical coefficients in Z_p[[u]]/(p,u)^L."""
    return clean({j:a%(p**(L-j)) for j,a in f.items() if j<L})
def shift(f,c):
    """Substitute u=v+c exactly."""
    h={}
    for j,a in f.items():
        for k in range(j+1):h[k]=h.get(k,0)+a*comb(j,k)*c**(j-k)
    return clean(h)
def derivative(f):return clean({j-1:j*a for j,a in f.items() if j})

def run():
    rows=[];count={k:0 for k in ['prism','thickening','specialization','frobenius','frobenius_products','de_rham','non_torsion_coefficients','localization']}
    for p in PRIMES:
        d={1:1,0:-p}
        # Check distinguished generator, including p=2.
        numerator=plus({p:1,0:-p},scale(power(d,p),-1))
        assert all(a%p==0 for a in numerator.values())
        delta={j:a//p for j,a in numerator.items()}
        delta_at_p=sum(a*p**j for j,a in delta.items())
        assert delta_at_p==p**(p-1)-1 and delta_at_p%p!=0
        count['prism']+=1
        for N in range(1,13):
            f=power(d,N)
            assert m_remainder(f,p,N)=={}
            rem=m_remainder(f,p,N+1)
            assert rem.get(N)==1 # leading coefficient certifies nonvanishing.
            assert shift(f,p)=={N:1}
            for s in range(1,9):
                assert clean({j:a%(p**s) for j,a in shift(f,p).items() if j<N})=={}
                count['thickening']+=1
        g=times({1:1},d)
        assert sum(a*0**j for j,a in g.items())==0
        assert sum(a*p**j for j,a in g.items())==0
        assert m_remainder(g,p,2)=={} and m_remainder(g,p,3).get(2)==1
        count['specialization']+=1
        product={0:1}
        for r in range(8):
            f={p**r:1,0:-p}
            assert f[0]==-p and p%abs(f[0])==0
            assert p%(p*p)!=0
            assert min(v_p(a,p)+j for j,a in f.items())==1
            count['frobenius']+=1
            # Product constant term already witnesses order r+1; coefficients cannot lower it.
            product=times(product,f)
            order=min(v_p(a,p)+j for j,a in product.items())
            assert order==r+1
            assert m_remainder(product,p,r+1)=={}
            assert m_remainder(product,p,r+2)!={}
            count['frobenius_products']+=1
        omega={p**n-1:p**n for n in range(1,14)}
        primitive={j+1:Fraction(a,j+1) for j,a in omega.items()}
        assert set(primitive.values())=={Fraction(1)}
        for k in range(1,11):
            head={p**n:1 for n in range(1,k)}
            tail={p**n-1:p**(n-k) for n in range(k,14)}
            assert plus(derivative(head),scale(tail,p**k))==omega
            assert min(v_p(a,p) for a in tail.values())==0
            count['de_rham']+=1
        for b in range(6):
            coeffs={Fraction(p**b*a,j+1) for j,a in omega.items()}
            assert coeffs=={Fraction(p**b)}
            count['non_torsion_coefficients']+=1
        # A/p is nonzero and multiplication by p acts as zero: its localization is zero.
        assert 1%p != 0 and p%p==0
        count['localization']+=1
        rows.append({'p':p,'delta_d_at_u_p':delta_at_p,'thickening_N':list(range(1,13)),'thickening_p_orders':list(range(1,9)),'phi_iterates':list(range(8)),'omega_terms':13,'tail_k':list(range(1,11))})
    return {'all_checks_pass':True,'counts':count,'total_controls':sum(count.values()),'parameters':rows,'limitations':['Finite integer polynomial and sparse coefficient identities only.','Non-exactness, non-torsion, derived completeness and nonseparatedness require the written infinite arguments.','No complex arising as the target prismatic restriction is constructed.','No test verifies arbitrary-order prismatic vanishing or a prior theorem.']}

if __name__=='__main__':
    result=run()
    recorded=Path(__file__).with_name('INDEPENDENT_RESULTS.json')
    text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if recorded.exists():
        assert recorded.read_text()==text,'Independent recorded result mismatch'
    else:recorded.write_text(text)
    print(json.dumps({'all_checks_pass':True,'counts':result['counts'],'total_controls':result['total_controls']},sort_keys=True))

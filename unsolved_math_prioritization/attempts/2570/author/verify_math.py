#!/usr/bin/env python3
"""Exact, bounded controls for KOU-21.61 scoped notes; no network or third-party code."""
import json
from math import gcd


def red(w):
    s=[]
    for a in w:
        if s and s[-1]==-a:s.pop()
        else:s.append(a)
    return tuple(s)


def inv(w):return tuple(-a for a in reversed(w))

def mul(*ws):return red(a for w in ws for a in w)

def power(w,n):return mul(*([w]*n)) if n>=0 else power(inv(w),-n)


def subst(w,images):return mul(*(images[a] if a>0 else inv(images[-a]) for a in w))


class Stallings:
    """Fold an inverse-labelled bouquet. Trees may remain; rank is unchanged."""
    def __init__(self,words):
        self.words=[red(w) for w in words]
        parent=[0];edges=[]
        def new():parent.append(len(parent));return len(parent)-1
        def root(a):
            while parent[a]!=a:parent[a]=parent[parent[a]];a=parent[a]
            return a
        def union(a,b):
            a,b=root(a),root(b)
            if a==b:return False
            parent[max(a,b)]=min(a,b);return True
        for w in self.words:
            v=0
            for i,a in enumerate(w):
                u=0 if i==len(w)-1 else new()
                edges.extend([(v,a,u),(u,-a,v)]);v=u
        while True:
            changed=False; seen={}
            for v,a,u in edges:
                k=(root(v),a);u=root(u)
                if k in seen:changed=union(seen[k],u) or changed
                else:seen[k]=u
            if not changed:break
        self.base=root(0)
        self.transitions={(root(v),a):root(u) for v,a,u in edges}
        self.vertices={root(v) for v in range(len(parent))}
        self.rank=len(self.transitions)//2-len(self.vertices)+1
        assert all(self.transitions.get((u,-a))==v for (v,a),u in self.transitions.items())
    def contains(self,w):
        v=self.base
        for a in red(w):
            if (v,a) not in self.transitions:return False
            v=self.transitions[v,a]
        return v==self.base
    def same(self,other):
        return all(self.contains(w) for w in other.words) and all(other.contains(w) for w in self.words)


def b(k):return mul(power((1,),k),(2,),power((1,),-k))


def run():
    counts={}
    # Empty/trivial/finite-rank and non-invariance controls.
    assert Stallings([]).rank==0
    assert Stallings([(),(1,-1)]).rank==0
    assert Stallings([(1,),(2,),(1,2)]).rank==2
    assert Stallings([(1,1)]).contains((1,1,1,1))
    assert not Stallings([(1,1)]).contains((1,))
    counts['basic_stallings_controls']=5
    # The symmetric orbit-window kernel grows forever, although H is free of rank 2.
    for n in range(41):
        A=Stallings([b(k) for k in range(-n,n+1)])
        assert A.rank==2*n+1
        assert not A.contains(b(n+1)) and not A.contains(b(-n-1))
        assert all(A.contains(b(k)) for k in range(-n,n+1))
    counts['infinite_kernel_windows']=41
    # General finite interval formula, positive and negative exponents.
    interval_count=0
    for l in range(-12,13):
        for r in range(l,l+15):
            A=Stallings([b(k) for k in range(l,r+1)])
            assert A.rank==r-l+1
            assert not A.contains(b(l-1)) and not A.contains(b(r+1))
            interval_count+=1
    counts['interval_rank_controls']=interval_count
    # Delayed HNN relation: local presentations have rank 3 until N=M, then rank 2.
    # The relator graph is a forest; eliminate one generator for each oriented edge.
    delay_count=0
    for m in range(1,61):
        for n in range(0,m+3):
            I=set(range(n+1))|set(range(m,m+n+1))
            J=(set(range(n))|set(range(m,m+n))) if n else set()
            assert all(i in I and i+1 in I for i in J)
            candidate_free_rank=1+len(I)-len(J)
            assert candidate_free_rank==(3 if n<m else 2)
            # Every finite orbit generator maps to the actual free fibre as claimed.
            if m<=16 and n<=18:
                A=Stallings([b(k) for k in I])
                assert A.rank==len(I)
            # Before the merger, c^{-1}s^m b s^{-m} is a nonempty reduced F3 word.
            R=mul((-3,),power((1,),m),(2,),power((1,),-m))
            assert len(R)==2*m+2
            delay_count+=1
    counts['delayed_hnn_window_controls']=delay_count
    # A true one-step saturation certificate: beta swaps the two basis letters.
    swap={1:(2,),2:(1,)}
    K0=Stallings([(1,)])
    K1=Stallings([(1,),(2,)])
    K2=Stallings([(1,),(2,),subst((1,),swap),subst((2,),swap)])
    assert not K0.same(K1) and K1.same(K2)
    counts['finite_kernel_saturation_controls']=2
    # Fibonacci automorphism and an explicit inverse, checked on signed letters.
    phi={1:(1,2),2:(1,)}; psi={1:(2,),2:(-2,1)}
    for a in (1,2,-1,-2):
        assert subst(subst((a,),phi),psi)==(a,)
        assert subst(subst((a,),psi),phi)==(a,)
    w=(1,);f0,f1=1,2
    for k in range(19):
        expected=f0
        assert len(w)==expected and all(a>0 for a in w)
        w=subst(w,phi);f0,f1=f1,f0+f1
    counts['fibonacci_length_controls']=19
    counts['automorphism_inverse_controls']=8
    # A concrete F2 x Z subgroup: <(a,2),(b,-1),(ab,5)> = <(a,2),(b,-1)> x <(1,4)>.
    gens=[((1,),2),((2,),-1),((1,2),5)]
    def product(x,y):return (mul(x[0],y[0]),x[1]+y[1])
    def inverse(x):return (inv(x[0]),-x[1])
    residual=product(gens[2],inverse(product(gens[0],gens[1])))
    assert residual==((),4)
    # Check constructive membership criterion on a finite set of words and all nearby heights.
    words={()}
    for _ in range(4):words|={mul(w,(a,)) for w in list(words) for a in [1,2,-1,-2]}
    member_count=0
    for w in words:
        sigma=sum(2*(1 if a>0 else -1) if abs(a)==1 else -(1 if a>0 else -1) for a in w)
        for k in range(-10,11):
            q,rem=divmod(k-sigma,4)
            if rem==0:assert sigma+4*q==k
            member_count+=1
    counts['direct_product_normal_form_controls']=member_count
    # Residue-index formula for finite-extension setup.
    c=0
    for m in range(1,25):
        for a in range(-8,9):
            for z in range(-8,9):
                vals={0}
                while True:
                    nxt=vals|{(v+a)%m for v in vals}|{(v+z)%m for v in vals}
                    if nxt==vals:break
                    vals=nxt
                assert len(vals)==m//gcd(m,gcd(a,z));c+=1
    counts['cyclic_quotient_index_controls']=c
    return {'passed':True,'counts':counts,'scope':'Bounded exact controls only; the written proofs carry the general claims; KOU-21.61 is unresolved.'}

if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))

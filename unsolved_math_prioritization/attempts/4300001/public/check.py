#!/usr/bin/env python3
"""Exact finite controls for PROOF.md, using only Python's standard library.

These controls do not prove arbitrary support exclusion, radical saturation,
or mixing. Those conclusions depend on the written proofs and cited theorem.
"""
import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

ASSERTIONS = 0

def ck(condition, message='control failed'):
    global ASSERTIONS
    ASSERTIONS += 1
    if not condition:
        raise AssertionError(message)

def clean(a, p=0):
    return {m: c % p if p else c for m, c in a.items() if (c % p if p else c)}

def add(a, b, p=0):
    r = Counter(a)
    for m, c in b.items(): r[m] += c
    return clean(r, p)

def scale(a, c, p=0): return clean({m:c*v for m,v in a.items()},p)

def mul(a, b, p=0):
    r = Counter()
    for (i,j), c in a.items():
        for (k,l), d in b.items(): r[(i+k,j+l)] += c*d
    return clean(r,p)

def power(a, n, p=0):
    r={(0,0):1}
    while n:
        if n&1: r=mul(r,a,p)
        a=mul(a,a,p);n//=2
    return r

def uni(cs): return {(i,0):c for i,c in enumerate(cs) if c}

def coeffs(a):
    if not a:return []
    assert all(j==0 for i,j in a)
    return [a.get((i,0),0) for i in range(max(i for i,j in a)+1)]

def rem(a,b,p):
    a=coeffs(clean(a,p)); b=coeffs(clean(b,p))
    while a and not a[-1]:a.pop()
    while a and len(a)>=len(b):
        c=a[-1]*pow(b[-1],-1,p)%p;d=len(a)-len(b)
        for j,v in enumerate(b):a[j+d]=(a[j+d]-c*v)%p
        while a and not a[-1]:a.pop()
    return uni(a)

def gcd(a,b,p):
    while b:a,b=b,rem(a,b,p)
    return scale(a,pow(coeffs(a)[-1],-1,p),p)

def deriv(a,axis,p=0):
    r={}
    for m,c in a.items():
        if m[axis]:
            n=list(m);n[axis]-=1;r[tuple(n)]=c*m[axis]
    return clean(r,p)

ONE={(0,0):1}; X={(1,0):1}; Y={(0,1):1}
A=uni([1,0,0,0,1]); B=uni([0,1,1,1])
C={(0,0):1,(0,2):1}
F=add(mul(A,C),mul(B,Y))
Q=uni([1,-1,1]); R=uni([2,3,2]); T=uni([2,-1,-1,-1,2])


def identity_controls():
    ck(len(F)==7)
    D=add(power(B,2),scale(power(A,2),-4))
    ck(D==scale(mul(mul(Q,R),T),-1),'integer discriminant factorization')
    ck(R==add(scale(Q,2),scale(X,5)))
    ck(T==add(mul(uni([-2,1,2]),Q),uni([4,-4])))
    D3=scale(mul(mul(power(uni([1,1]),2),uni([1,0,1])),uni([1,1,1,1,1])),-1)
    D5=mul(mul(uni([1,0,1]),power(uni([1,1]),2)),power(Q,2))
    ck(clean(D,3)==clean(D3,3))
    ck(clean(D,5)==clean(D5,5))
    ck(gcd(uni([1,0,1]),uni([1,1,1,1,1]),3)==ONE)
    ck(gcd(uni([1,0,1]),uni([1,1]),3)==ONE)
    ck(gcd(uni([1,0,1]),Q,5)==ONE)
    ck(gcd(uni([1,0,1]),uni([1,1]),5)==ONE)
    for p in [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101]:
        ck(gcd(A,B,p)==ONE)
    ck({(4-i,j):c for (i,j),c in F.items()}==F)
    ck({(i,2-j):c for (i,j),c in F.items()}==F)
    for p in [2,3,5,7]:
        ck(power(F,p,p)=={(p*i,p*j):c for (i,j),c in F.items()})
    W=mul(A,add(Y,ONE),2)
    ck(add(add(power(W,2,2),mul(B,W,2),2),mul(A,B,2),2)==mul(A,F,2))
    ck(deriv(F,0,2)==mul(Y,uni([1,0,1]),2))
    ck(deriv(F,1,2)==B)
    rnum=uni([1,0,1]);rden=uni([1,1,1])
    ck(add(rnum,rden,2)==X)
    ck(power(uni([1,1]),2,2)==rnum)
    for n in range(1,65):
        bn={(0,0):1,(n,0):1}
        ck((not rem(bn,uni([1,0,0,0,1]),2))==(n%4==0))
        ck((not rem(bn,uni([1,0,1]),2))==(n%2==0))
    # Deliberate scope control: a different defining polynomial has a
    # shorter relation after adjoining a radical, as in DM's example (1.4).
    U=uni([1,1,1])
    ck(power(U,3,2)==uni([1,1,0,1,0,1,1]))
    return {'discriminant_identity_over':'Z','gcd_sample_primes_through':101,
            'frobenius_primes':[2,3,5,7],'boundary_binomial_exponents_through':64,
            'limits':'Prime samples supplement the symbolic all-prime proof; they are not its basis.'}


def local_series_controls():
    # Bitsets encode polynomials over F_2 truncated modulo t^precision.
    precision=16;mask=(1<<precision)-1
    def m(a,b):
        out=0
        while b:
            if b&1:out^=a
            a<<=1;b>>=1
        return out&mask
    def pw(a,n):
        out=1
        while n:
            if n&1:out=m(out,a)
            a=m(a,a);n//=2
        return out
    def evalf(x,y):
        out=0
        for (i,j),c in F.items():out^=m(pw(x,i),pw(y,j))
        return out
    x=0;y=3  # y=1+t
    for degree in range(1,precision):
        if (evalf(x,y)>>degree)&1:x^=1<<degree
    ck(evalf(x,y)==0)
    ck((x&-x).bit_length()-1==2)
    xx=3;yy=0 # x=1+t
    for degree in range(1,precision):
        if (evalf(xx,yy)>>degree)&1:yy^=1<<degree
    ck(evalf(xx,yy)==0)
    ck((yy&-yy).bit_length()-1==4)
    return {'precision':precision,'x_at_y_1_plus_t_nonzero_degrees':[i for i in range(precision) if x>>i&1],
            'y_at_x_1_plus_t_nonzero_degrees':[i for i in range(precision) if yy>>i&1],
            'limits':'Finite series are consistency checks; smooth local rings prove the valuations.'}


def graph_controls():
    grid=list(itertools.product(range(4),repeat=2));accepted=0;forest=0;rect=0
    total=0
    for r in [4,5,6]:
        for supp in itertools.combinations(grid,r):
            total+=1
            xs=[s[0] for s in supp];ys=[s[1] for s in supp]
            if min(xs)==max(xs) or min(ys)==max(ys):continue
            faces=[[i for i,s in enumerate(supp) if s[axis]==value]
                   for axis,value in [(0,min(xs)),(0,max(xs)),(1,min(ys)),(1,max(ys))]]
            if any(len(v)!=2 for v in faces):continue
            accepted+=1
            edges={tuple(v) for v in faces};ck(len(edges)==4)
            adj=[set()for _ in supp]
            for a,b in edges:adj[a].add(b);adj[b].add(a)
            ck(max(map(len,adj))<=2)
            comps=[];todo=set(range(r))
            while todo:
                start=todo.pop();comp={start};stack=[start]
                while stack:
                    for v in adj[stack.pop()]:
                        if v not in comp:comp.add(v);todo.discard(v);stack.append(v)
                comps.append(comp)
            cycles=[c for c in comps if all(len(adj[v])==2 for v in c)]
            if not cycles:
                forest+=1;ck(len(comps)==r-4);ck(len(comps)<=2)
            else:
                rect+=1;ck(len(cycles)==1);ck(len(cycles[0])==4)
                corners={(min(xs),min(ys)),(min(xs),max(ys)),(max(xs),min(ys)),(max(xs),max(ys))}
                ck({supp[i]for i in cycles[0]}==corners)
                ck(all(len(c)==1 for c in comps if c!=cycles[0]))
    witness=[(0,0),(4,0),(0,2),(4,2),(1,1),(2,1)]
    ck(len({(a%2,b%2)for a,b in witness})==3)
    return {'grid':'{0,1,2,3}^2','support_sizes':[4,5,6],'supports_inspected':total,
            'all_four_extreme_lines_have_two_points':accepted,'forest_cases':forest,
            'rectangle_cycle_cases':rect,
            'limits':'Checks finite support geometry only, without asserting those sets are polynomial multiples.'}


def odd_congruence_controls():
    # Remainders in F_p[x,y]/(x^2+x+1,y^2+1) keep repeated roots at p=3.
    checked=0;vanishing=0
    for p in [3,5,7,11]:
        q=uni([1,1,1])
        for dx in range(25):
            xr=rem({(dx,0):1},q,p)
            for dy in range(13):
                sign=pow(p-1,dy//2,p);parity=dy%2
                for h in range(1,p):
                    # x^dx*y^dy + h. For dx=dy=0 this includes zero;
                    # it still satisfies all necessary congruences.
                    val={(i,parity):c*sign%p for (i,_),c in xr.items()}
                    val=add(val,{(0,0):h},p);checked+=1
                    if not val:
                        vanishing+=1;ck(dx%3==0);ck(dy%2==0)
                        ck(h==(-pow(p-1,dy//2,p))%p)
    return {'primes':[3,5,7,11],'x_exponent_difference_max':24,
            'y_exponent_difference_max':12,'binomials_inspected':checked,
            'vanishing_remainders':vanishing,
            'limits':'Tests necessary congruences; does not establish the existence of a six-term multiple.'}


def sparse_controls():
    results=[]
    for p,a,b in [(2,4,2),(3,3,1),(5,2,1),(7,2,1)]:
        mons=[(i,j)for j in range(b+1)for i in range(a+1)];n=len(mons)
        hist=Counter();count=0;best=100;first=None
        # Projective representatives: the first nonzero coefficient is 1.
        for k in range(n):
            for tail in itertools.product(range(p),repeat=n-k-1):
                cs=(0,)*k+(1,)+tail;h={m:c for m,c in zip(mons,cs) if c}
                g=mul(F,h,p);weight=len(g);hist[weight]+=1;count+=1
                ck(weight>=7,'unexpected small-support multiple in finite box')
                if weight<best:best=weight;first=[[i,j,c]for(i,j),c in sorted(h.items())]
        ck(count==(p**n-1)//(p-1));ck(best==7)
        results.append({'p':p,'multiplier_box':{'x_degree_at_most':a,'y_degree_at_most':b},
                        'projective_multipliers':count,'minimum_support':best,
                        'first_minimizer':first,'support_histogram':dict(sorted(hist.items()))})
    return {'results':results,'limits':'Exhaustive only in these small multiplier boxes, modulo nonzero scalar. No unbounded exponent, large-height, or all-prime exclusion follows.'}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',default='control-results.json')
    args=parser.parse_args()
    out={'identities':identity_controls(),'local_series':local_series_controls(),
         'geometry':graph_controls(),'odd_six_term_congruences':odd_congruence_controls(),
         'bounded_sparse_multiples':sparse_controls()}
    out['assertions_passed']=ASSERTIONS
    out['interpretation']='Finite exact controls supplement PROOF.md; the odd-prime six-term gap remains open in this attempt.'
    Path(args.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'assertions_passed':ASSERTIONS,'output':args.output},sort_keys=True))

if __name__=='__main__':main()

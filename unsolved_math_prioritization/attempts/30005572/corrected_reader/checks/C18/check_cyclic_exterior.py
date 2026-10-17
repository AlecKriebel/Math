"""Independent exact exterior-algebra audit of the finite averaging identities.
This is finite algebra verification, not a K-theory or specialization proof.
"""
from collections import defaultdict
import json

def add(*terms):
    out=defaultdict(int)
    for coefficient,term in terms:
        for key,value in term.items(): out[key]+=coefficient*value
    return {k:v for k,v in out.items() if v}

def wedge(a,b):
    out=defaultdict(int)
    for i,x in a.items():
        for j,y in b.items():
            if i<j: out[i,j]+=x*y
            elif i>j: out[j,i]-=x*y
    return {k:v for k,v in out.items() if v}

results=[]
for n in range(2,18):
    def h(a):
        a=min(a%n,(-a)%n)
        return {a:1} if a else {}
    def B(x,y):return add((1,h(x+y)),(1,h(x-y)))
    def phi(x,y,z):
        A,C,D=B(z,x),B(y,x),B(z,y)
        return add((1,wedge(A,C)),(1,wedge(C,D)),(1,wedge(D,A)))
    def M(a,b,c,d):return add((1,B(c,a)),(1,B(d,b)),(-1,B(c,b)),(-1,B(d,a)))
    def delta(a,b,c,d):return wedge(M(a,b,c,d),M(a,c,b,d))
    def psi(a,b):
        c=-a-b
        return add((1,wedge(h(a),h(b))),(1,wedge(h(b),h(c))),(1,wedge(h(c),h(a))))
    # All triples: exact n*phi=sum delta in the FREE exterior algebra.
    triple_checks=0; degenerate_checks=0
    delta_sums={}
    for a in range(n):
        for b in range(n):
            for c in range(n):
                S={}
                for d in range(n):
                    D=delta(a,b,c,d)
                    S=add((1,S),(1,D))
                    signs=[min(t%n,(-t)%n) for t in (a,b,c,d)]
                    if len(set(signs))<4:
                        degenerate_checks+=1
                        if D:raise RuntimeError(('nonzero degenerate delta',n,a,b,c,d,D))
                if add((1,S),(-n,phi(a,b,c))):raise RuntimeError(('averaged phi',n,a,b,c))
                delta_sums[a,b,c]=S
                triple_checks+=1
    # Every pair: independently form RHS of the explicit double-delta identity.
    pair_checks=0
    for a in range(n):
        for b in range(n):
            c=(-a-b)%n
            rhs={}
            for x in range(n):
                rhs=add((1,rhs),(4,delta_sums[x,(-b-x)%n,(a-x)%n]),
                  (-1,delta_sums[0,a,(c+2*x)%n]),
                  (-1,delta_sums[0,c,(b+2*x)%n]),
                  (-1,delta_sums[0,b,(a+2*x)%n]))
            if add((1,rhs),(-4*n*n,psi(a,b))):raise RuntimeError(('cyclic delta certificate',n,a,b))
            pair_checks+=1
    results.append({'n':n,'triple_checks':triple_checks,'pair_checks':pair_checks,'degenerate_delta_checks':degenerate_checks,'passed':True})
print(json.dumps({'convention':'even formal h; h(0)=0; exact free exterior algebra over Z','cyclic_cases':results,'all_passed':True},indent=2))

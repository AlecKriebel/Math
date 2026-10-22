#!/usr/bin/env python3
"""Exact supporting algebra. No numerical K2, geometric, or descent inference."""
from collections import defaultdict, deque
from functools import lru_cache
from itertools import product
from math import gcd, prod
import json


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def add(*vectors):
    d = defaultdict(int)
    for vector in vectors:
        for k, v in vector.items():
            d[k] += v
    return {k: v for k, v in d.items() if v}


def scale(c, vector):
    return {k: c*v for k, v in vector.items() if c*v}


def wedge(x, y):
    d = defaultdict(int)
    for a, u in x.items():
        for b, v in y.items():
            if a < b:
                d[(a,b)] += u*v
            elif b < a:
                d[(b,a)] -= u*v
    return {k: v for k, v in d.items() if v}


def check_cyclic(n):
    G = range(n)
    def h(x):
        k = min(x % n, (-x) % n)
        return {k:1} if k else {}
    @lru_cache(None)
    def B(x,y):
        return add(h(x+y),h(x-y))
    def M(a,b,c,d):
        return add(B(c,a),B(d,b),scale(-1,B(c,b)),scale(-1,B(d,a)))
    def psi(a,b):
        A,Bb,C=h(a),h(b),h(-a-b)
        return add(wedge(A,Bb),wedge(Bb,C),wedge(C,A))
    @lru_cache(None)
    def phi(x,y,z):
        A,Bb,C=B(z,x),B(y,x),B(z,y)
        return add(wedge(A,Bb),wedge(Bb,C),wedge(C,A))
    def delta(a,b,c,d):
        return wedge(M(a,b,c,d),M(a,c,b,d))
    @lru_cache(None)
    def D(a,b,c):
        # Actually sum every d, rather than substituting n*phi.
        return add(*(delta(a,b,c,d) for d in G))
    degenerate = 0
    for a,b,c,d in product(G,repeat=4):
        value = delta(a,b,c,d)
        require(value == add(phi(a,b,c),phi(c,d,a),phi(b,a,d),phi(d,c,b)),
                f"delta expansion {n} {(a,b,c,d)}")
        if len({min(t,(-t)%n) for t in (a,b,c,d)}) < 4:
            require(not value, f"degeneracy {n} {(a,b,c,d)}")
            degenerate += 1
    for a,b,c in product(G,repeat=3):
        require(D(a,b,c) == scale(n,phi(a,b,c)),f"single delta sum {n} {(a,b,c)}")
    for a,b in product(G,repeat=2):
        c=(-a-b)%n
        first=add(*(D(x,(-b-x)%n,(a-x)%n) for x in G))
        second=add(*(D(0,v,(u+2*x)%n) for u,v in ((c,a),(b,c),(a,b)) for x in G))
        require(add(scale(4,first),scale(-1,second)) == scale(4*n*n,psi(a,b)),
                f"explicit double-delta witness {n} {(a,b)}")
    result = {"n":n,"quadruples":n**4,"degenerate_quadruples":degenerate,
              "all_triangles_tested":n*n,"identities":"exact"}
    if n == 7:
        A,Bb,C={1:1},{2:1},{3:1}
        X=add(scale(-1,A),scale(3,Bb),scale(-2,C))
        Y=add(scale(2,A),Bb,scale(-3,C))
        Psi=add(wedge(A,Bb),wedge(Bb,C),wedge(C,A))
        require(wedge(X,Y)==scale(-7,Psi),"C7 primary wedge")
        require(Psi.get((1,2),0)%7==1,"C7 witness Psi")
        for a,b,c,d in product(G,repeat=4):
            require(delta(a,b,c,d).get((1,2),0)%7==0,"C7 functional")
        result["formal_seven_quotient"]="nonzero functional to Z/7 verified"
    return result


def check_orbits(m):
    remaining=set(product(range(m),repeat=2)); orbits=[]
    while remaining:
        root=min(remaining); orbit={root}; todo=deque([root])
        while todo:
            x,y=todo.popleft()
            for nxt in (((x+y)%m,y),(x,(y+x)%m)):
                if nxt not in orbit:
                    orbit.add(nxt);todo.append(nxt)
        contents={gcd(gcd(x,y),m) for x,y in orbit}
        require(len(contents)==1,f"content preserved m={m}")
        content=contents.pop()
        expected={(x,y) for x,y in product(range(m),repeat=2) if gcd(gcd(x,y),m)==content}
        require(orbit==expected,f"SL2 content orbit m={m} content={content}")
        remaining-=orbit;orbits.append((content,orbit))
    # Rational rank by integer Gaussian elimination, no floating arithmetic.
    import sympy as sp
    matrix=sp.Matrix([[sum(1 for x,yy in orbit if yy==y) for _,orbit in orbits] for y in range(m)])
    require(matrix.rank()==len(orbits),f"injective invariant marginal m={m}")
    return {"modulus":m,"orbit_count":len(orbits),"marginal_rank":matrix.rank()}


def local_matrix(Q,r):
    return [[(Q-1)*Q**(r-j-1) if j<k else (Q**(r-k) if j==k else 0)
             for j in range(r+1)] for k in range(r+1)]


def check_local_matrices():
    import sympy as sp
    outputs=[]
    for Q in (2,3,4,5,7,9,11,25):
        for r in range(1,5):
            M=sp.Matrix(local_matrix(Q,r)); det=int(M.det())
            require(det==Q**(r*(r+1)//2),f"local determinant Q={Q} r={r}")
            outputs.append({"Q":Q,"r":r,"determinant":det})
    A=sp.Matrix(local_matrix(4,2));B=sp.Matrix(local_matrix(9,1));C=sp.kronecker_product(A,B)
    require(C.det()==A.det()**B.rows * B.det()**A.rows,"CRT tensor determinant")
    return {"local_matrices":outputs,"CRT_product_determinant":int(C.det())}


def main():
    result={"cyclic_exterior_checks":[check_cyclic(n) for n in range(2,16)],
            "actual_elementary_orbits":[check_orbits(m) for m in (2,3,4,5,6,7,8,9,10,12,15,16,18,20,24,25)],
            "projection_matrices":check_local_matrices(),
            "scope":"Exact free-exterior and finite-cycle checks. No K2 nonvanishing, arithmetic descent, or homology calibration is inferred."}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=="__main__":
    main()

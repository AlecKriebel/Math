#!/usr/bin/env python3
"""Small exact algebra checks; no claim of a p-adic full-module computation."""
from fractions import Fraction as F
from itertools import combinations
import json
import sys

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def matmul(a, b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]

def rank(a):
    a = [[F(x) for x in row] for row in a]
    if not a:
        return 0
    r = 0
    for c in range(len(a[0])):
        p = next((i for i in range(r,len(a)) if a[i][c]), None)
        if p is None:
            continue
        a[r],a[p] = a[p],a[r]
        pivot = a[r][c]
        a[r] = [x/pivot for x in a[r]]
        for i in range(len(a)):
            if i != r:
                t = a[i][c]
                a[i] = [x-t*y for x,y in zip(a[i],a[r])]
        r += 1
        if r == len(a):
            break
    return r

def inverse(a):
    n=len(a)
    a=[[F(x) for x in row]+[F(i==j) for j in range(n)] for i,row in enumerate(a)]
    for c in range(n):
        p=next((i for i in range(c,n) if a[i][c]),None)
        require(p is not None,"singular chart matrix")
        a[c],a[p]=a[p],a[c]
        pivot=a[c][c]
        a[c]=[x/pivot for x in a[c]]
        for i in range(n):
            if i!=c:
                t=a[i][c]
                a[i]=[x-t*y for x,y in zip(a[i],a[c])]
    return [row[n:] for row in a]

def monomial_member(monomial,generators):
    return any(all(a>=b for a,b in zip(monomial,g)) for g in generators)

def main():
    require(len(sys.argv) in (1,3),"use --mutate NAME or no arguments")
    mutation=None
    if len(sys.argv)==3:
        require(sys.argv[1]=="--mutate","unknown option")
        mutation=sys.argv[2]
        require(mutation in {"split_jordan","merge_orbits","equal_fitting","drop_factor"},"unknown mutation")

    t=[[0,-4],[1,4]]
    if mutation=="split_jordan":
        t=[[2,0],[0,2]]
    nil=[[t[i][j]-2*int(i==j) for j in range(2)] for i in range(2)]
    require(matmul(nil,nil)==[[0,0],[0,0]],"Jordan square is nonzero")
    require(rank(nil)==1,"repeated-root quotient wrongly split")
    require(rank([[1,t[0][0]],[0,t[1][0]]])==2,"quotient is not cyclic")

    charts=[
        [[0,1,0],[0,0,1],[1,0,0]],
        [[1,0,0],[0,0,1],[0,1,0]],
        [[1,0,0],[0,1,0],[0,0,1]],
        [[1,1,0],[0,0,1],[1,0,0]],
        [[1,0,1],[0,1,0],[1,0,0]],
        [[1,0,0],[0,1,1],[0,1,0]],
    ]
    if mutation=="merge_orbits":
        charts[4]=charts[3]
    generators=[]
    for i,j in [(0,0),(0,1),(1,0),(1,1)]:
        e=[[0]*3 for _ in range(3)]
        e[i][j]=1
        generators.append(e)
    orbit_dimensions=[]
    signatures=[]
    for g in charts:
        gi=inverse(g)
        coefficient_matrices=[matmul(matmul(gi,e),g) for e in generators]
        rows=[[m[i][j] for m in coefficient_matrices] for i,j in [(1,0),(2,0),(2,1)]]
        orbit_dimensions.append(rank(rows))
        sig=[]
        for k in [1,2]:
            sig.extend([k-rank([g[2][:k]]), k-rank([g[0][:k],g[1][:k]])])
        signatures.append(tuple(sig))
    require(orbit_dimensions==[1,1,1,2,3,2],"incorrect orbit stabilizer dimensions")
    require(len(set(signatures))==6,"orbit signatures collide")

    i_generators=[(1,0),(0,1)]
    j_generators=[(2,0),(0,1)]
    if mutation=="equal_fitting":
        j_generators=i_generators
    require(monomial_member((1,0),i_generators),"u missing from I")
    require(not monomial_member((1,0),j_generators),"Fitting ideals wrongly identified")
    require(monomial_member((2,0),j_generators),"u squared missing from J")

    # Pure polynomial samples: if one X coordinate equals a listed beta,
    # product_a product_j (X_a-beta_j) has a zero factor. No assertion about
    # a representation layer, center action, or nilpotence is tested here.
    polynomial_cases=0
    for n in range(1,6):
        betas=list(range(2,n+3))
        roots=betas[1:] if mutation=="drop_factor" else betas
        for r in range(1,n+1):
            for subset in combinations(betas,r):
                xs=list(subset)+list(range(20,20+n-r))
                value=1
                for x in xs:
                    for b in roots:
                        value*=x-b
                require(value==0,"central support factor omitted")
                polynomial_cases+=1
    print(json.dumps({"status":"PASS","arithmetic":"exact rational/integer",
                      "orbit_dimensions":orbit_dimensions,
                      "polynomial_cases":polynomial_cases,
                      "p_adic_model_proved":False},sort_keys=True))

if __name__=="__main__":
    main()

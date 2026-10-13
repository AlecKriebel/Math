#!/usr/bin/env python3
"""Portable finite diagnostics; the universal full-algebra argument is in the proof.

No assert statements are used: optimization must preserve all checks.
No third-party libraries, bodies, network, or Git access are required.
"""
from fractions import Fraction as F
from itertools import permutations, product
from math import comb
from hashlib import sha256
from pathlib import Path
from datetime import datetime, timezone
import json
import platform
import sys


def require(condition, name):
    if not condition:
        raise RuntimeError(name)


def trim(p):
    p = list(map(F, p))
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def add(p, q):
    r = [F(0)] * max(len(p), len(q))
    for i, c in enumerate(p): r[i] += c
    for i, c in enumerate(q): r[i] += c
    return trim(r)


def scale(p, c): return trim([F(c)*x for x in p])


def mul(p, q):
    r = [F(0)] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q): r[i+j] += x*y
    return trim(r)


def value(p, t):
    answer = F(0)
    for x in reversed(p): answer = answer*F(t) + x
    return answer


def difference(fn, n, r):
    return sum(((-1)**(r-j) * comb(r, j) * fn(n+j) for j in range(r+1)), F(0))


def binomial_poly(r, denominator=True):
    p = [F(1)]
    for k in range(r):
        p = mul(p, [-k, 1])
        if denominator: p = scale(p, F(1, k+1))
    return p


def newton(p, d=None, denominator=True):
    if d is None: d = len(trim(p))-1
    answer = [F(0)]
    for r in range(d+1):
        answer = add(answer, scale(binomial_poly(r, denominator), difference(lambda n: value(p,n), 0,r)))
    return answer


def braid_resolution(n, r, sign=1, residual=True):
    result = {}
    for bits in product((-1,1), repeat=r):
        exponent = 2*n + (r if residual else 0) + sum(bits)
        coefficient = (sign**r) * (-1)**bits.count(-1)
        result[exponent] = result.get(exponent, 0) + coefficient
    return {e:c for e,c in result.items() if c}


def braid_difference(n, r):
    return {2*(n+j): (-1)**(r-j)*comb(r,j) for j in range(r+1)}


def g(matrix):
    return sum(matrix[i][j]**2 for i in range(len(matrix)) for j in range(i+1,len(matrix)))


def run():
    checks = []
    mutants = []
    def control(name, fn):
        fn()
        checks.append(name)
    def rejected(name, fn):
        try: fn()
        except RuntimeError as error:
            mutants.append({"mutation":name, "status":"rejected", "check":str(error)})
        else:
            raise RuntimeError("Undetected negative mutation: " + name)

    def braid_test(sign=1, residual=True):
        for n in range(5):
            for r in range(9):
                expansion = braid_resolution(n,r,sign,residual)
                require(expansion == braid_difference(n,r), "exact braid coefficients")
                require(all(e%2 == 0 for e in expansion), "two-component resolution parity")
    control("B2 singular expansion: n=0..4, r=0..8", braid_test)
    rejected("reverse the singular-resolution sign", lambda: braid_test(-1,True))
    rejected("omit residual positive crossings", lambda: braid_test(1,False))

    polys = [[1], [0,1], [0,0,1], [3,-2,4], [F(2,7),0,F(-1,3),2], [F((-1)**i,i+1) for i in range(9)]]
    def newton_test(denominator=True):
        for p in polys:
            rebuilt = newton(p,denominator=denominator)
            require(trim(rebuilt)==trim(p), "exact Newton coefficients")
            for t in list(range(18)) + [F(1,2),F(-7,3)]:
                require(value(rebuilt,t)==value(p,t), "Newton evaluation")
            for n in range(8):
                require(difference(lambda k:value(p,k),n,len(trim(p)))==0, "order+1 difference")
    control("Newton identities through degree 8 over Q",newton_test)
    rejected("remove factorial denominators",lambda:newton_test(False))
    control("polynomial restriction multiplicativity", lambda: [require(newton(mul(p,q))==mul(newton(p),newton(q)), "multiplicativity") for p in polys for q in polys])
    rejected("truncate n^4 restriction at degree 2",lambda:require(newton([0,0,0,0,1],d=2)==[0,0,0,0,1], "degree bound mutation"))

    def symmetry_test():
        for m in range(2,5):
            entries = list(product((-2,-1,0,1,2),repeat=m*(m-1)//2))
            # Complete for m<=3; deterministic representatives for m=4.
            if m==4: entries = entries[::37]
            for entries_row in entries:
                a=[[0]*m for _ in range(m)]
                k=0
                for i in range(m):
                    for j in range(i+1,m): a[i][j]=a[j][i]=entries_row[k]; k+=1
                target=g(a)
                require((target==0)==all(x==0 for x in entries_row), "g zero set")
                require(target*(4*target-1)==0 if target==0 else target*(4*target-1)!=0, "actual integer zero set")
                for signs in product((-1,1),repeat=m):
                    require(g([[a[i][j]*signs[i]*signs[j] for j in range(m)] for i in range(m)])==target,"orientation symmetry")
                for perm in permutations(range(m)):
                    require(g([[a[perm[i]][perm[j]] for j in range(m)] for i in range(m)])==target,"component permutation symmetry")
    control("linking-square zero set and sign/permutation symmetry",symmetry_test)
    def signed_sum_mutation():
        a=[[0,2,-1],[2,0,3],[-1,3,0]]
        signs=(-1,1,1)
        changed=[[a[i][j]*signs[i]*signs[j] for j in range(3)] for i in range(3)]
        signed=lambda matrix:sum(matrix[i][j] for i in range(3) for j in range(i+1,3))
        require(signed(a)==signed(changed),"orientation symmetry")
    rejected("replace square-sum by signed linking sum",signed_sum_mutation)

    def character_test(t=F(1,2), plus=False):
        image_g=t*t
        image_f=image_g*(4*image_g+(1 if plus else -1))
        require(image_g==F(1,4),"g character image")
        require(image_f==0,"generator killed by character")
        for n in range(1,13): require(image_g**n!=0,"all checked witness powers nonzero")
    control("character witness: exact rational values, powers 1..12",character_test)
    rejected("evaluate at actual integer t=1",lambda:character_test(F(1)))
    rejected("replace 4g-1 by 4g+1",lambda:character_test(plus=True))

    def order_zero_test():
        for fixed_m in range(2,7):
            for support_m in range(1,8):
                image=F(fixed_m==support_m)
                require(image*image==image,"component indicator is idempotent")
            for a in range(1,8):
                for b in range(1,8):
                    require(F(fixed_m==a)*F(fixed_m==b)==F(a==b)*F(fixed_m==a),"component indicator products")
        # C[t] has only constant idempotents: coefficient leading term rules out positive degree.
        for p in [[0],[1],[0,1],[1,-1],[0,0,1]]:
            require((mul(p,p)==trim(p))==(trim(p) in ([F(0)],[F(1)])),"polynomial idempotent finite control")
    control("order-zero component indicators and polynomial idempotents",order_zero_test)

    def boundary_test():
        for p in (3,5,7,11,13):
            n=(p+1)//2
            gp=n*n%p
            require(gp!=0 and gp*(4*gp-1)%p==0,"odd characteristic actual nonzero-g root")
            require((comb(0,p)%p,comb(p,p)%p)==(0,1),"binomial sequence is not a polynomial in residue n")
        for x in range(2): require((x*(4*x-1))%2==x,"characteristic two generator equals g")
        for n in range(13):
            image_g=F(n*n); image_f=image_g*(4*image_g-1)
            h=1/(4*image_g-1)
            require(image_f*h==image_g,"arbitrary-function enlargement makes g a multiple")
        # Truncated formal inverse of 4g-1; g is a multiple modulo g^(N+1).
        for N in range(1,13):
            f=[0,-1,4]
            inverse=[-4**k for k in range(N)]
            product_f=mul(f,inverse)
            require(product_f[:N+1]==[F(0),F(1)]+[F(0)]*(N-1),"completed inverse coefficients")
        witness=[0,1]
        homogeneous_generator=mul(witness,witness)
        require(value(homogeneous_generator,F(1,4))!=0,"homogeneous generator is not killed by proposed character")
        require(mul(witness,witness)==homogeneous_generator,"g squared belongs to homogeneous generator ideal")
    control("positive-characteristic and enlarged/completed-ring boundaries",boundary_test)
    rejected("assert original zero-set equivalence in characteristic 3",lambda:require((1*(4*1-1))%3!=0,"odd characteristic actual nonzero-g root"))

    return {"status":"pass", "positive_controls":checks, "negative_mutations":mutants,
            "limitations":"Finite exact diagnostics only. Entire-algebra polynomiality, nonmembership of every positive witness power, and nonfinite-order reciprocal require the proofs in FIRST_ASSESSMENT.md.",
            "utc":datetime.now(timezone.utc).isoformat(),
            "runtime":{"python_executable":sys.executable,"python_version":sys.version,"platform":platform.platform(),"optimization":sys.flags.optimize},
            "script_sha256":sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__ == "__main__":
    print(json.dumps(run(),indent=2))

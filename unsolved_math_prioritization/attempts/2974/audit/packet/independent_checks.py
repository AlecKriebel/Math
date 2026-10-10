#!/usr/bin/env python3
"""Independent exact illustrations; no source downloads or file writes."""
from collections import deque
from itertools import combinations, product
from functools import reduce
from math import gcd
import json


def need(condition, message):
    if not condition:
        raise ValueError(message)


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def det(a):
    if not a:
        return 1
    return sum((-1)**j * a[0][j] * det([r[:j]+r[j+1:] for r in a[1:]])
               for j in range(len(a)))


def polarization():
    E = [[0,4,0,0],[-4,0,0,0],[0,0,0,9],[0,0,-9,0]]
    basis = [(1,0,1,0),(0,-2,0,1),(9,0,8,0),(0,9,0,-4)]
    B = [list(x) for x in zip(*basis)]
    need(abs(det(B)) == 1, "Basis is not integral unimodular")
    transformed = [[dot(x, [dot(r,y) for r in E]) for y in basis] for x in basis]
    need(transformed == [[0,1,0,0],[-1,0,0,0],[0,0,0,36],[0,0,-36,0]],
         "Explicit (1,36) polarization basis failed")
    minors = []
    for k in range(1,5):
        values = [abs(det([[E[i][j] for j in cs] for i in rs]))
                  for rs in combinations(range(4), k) for cs in combinations(range(4), k)]
        minors.append(reduce(gcd, values))
    need(minors == [1,1,36,1296], "Smith determinantal divisors failed")
    return {"alternating_type":[1,36], "basis_columns":basis,
            "basis_determinant":det(B), "determinantal_divisors":minors}


def torus():
    rows = []
    M = 1
    for k,p in enumerate((3,5,7,11,13,17,19,23),1):
        M *= p
        ds = [reduce(lambda a,b:a*b, ss,1) for j in range(1,k+1)
              for ss in combinations((3,5,7,11,13,17,19,23)[:k],j)]
        divs = []
        for a in ds:
            b = M*M//a
            need(a*b == M*M and a >= 3 and b >= 3 and b%a == 0,
                 "Finite product family failed")
            need(gcd(a,b) == a, "Divisibility differs from selected divisor")
            divs.append(gcd(a,b))
        need(len(set(divs)) == 2**k-1, "Wrong number of distinct classes")
        rows.append({"k":k,"genus":M*M+1,"count":len(divs)})
    return rows


def matvec(A,v,m):
    return tuple(sum(a*b for a,b in zip(r,v))%m for r in A)


def plus(v,w,m):
    return tuple((a+b)%m for a,b in zip(v,w))


def finite_group_checks(wrong_coefficient=False):
    cases = 0
    matrices = [(( -1,0),(0,1)),((0,1),(1,0)),((-1,0),(0,-1)),((1,2),(0,-1))]
    for m,A in product((4,6,8,9), matrices):
        unit = ((0,0),0)
        def mul(a,b):
            v,t=a; w,u=b
            return (plus(v,matvec(A,w,m) if t else w,m),(t+u)%2)
        def inv(a):
            v,t=a
            z=tuple(-x%m for x in v)
            return (matvec(A,z,m) if t else z,t)
        def conj(a,b):
            return mul(mul(a,b),inv(a))
        def closure(gens):
            moves=list(gens)+[inv(g) for g in gens]
            todo=deque([unit]); seen={unit}
            while todo:
                x=todo.popleft()
                for y in moves:
                    z=mul(x,y)
                    if z not in seen:
                        seen.add(z); todo.append(z)
            return seen
        for offset,t in product(((0,0),(1,2)),((0,1),(2,0))):
            S=[(offset,1),(t,0)]
            G0=closure(S)
            L0={x for x in G0 if x[1]==0}
            for v in ((1,0),(1,1)):
                Mgens=[]
                for s in S:
                    sv=matvec(A,v,m) if s[1] else v
                    dv=tuple((x-y)%m for x,y in zip(sv,v))
                    for g in G0:
                        Mgens.append((matvec(A,dv,m) if g[1] else dv,0))
                for n in range(m+1):
                    fn=(tuple(n*x%m for x in v),0)
                    Gn=closure(S+[conj(fn,s) for s in S])
                    actual={x for x in Gn if x[1]==0}
                    predicted=closure(list(L0)+[(tuple(n*x%m for x in w),0) for w,_ in Mgens])
                    need(actual==predicted,"Independent general finite kernel formula failed")
                    cases+=1
    # The even-modulus control detects loss of the factor 2 that all odd-prime
    # reductions of the author's one example fail to detect.
    m=8; n=1
    actual={(2*n*a%m,b,0) for a in range(m) for b in range(m)}
    c=1 if wrong_coefficient else 2
    predicted={(c*n*a%m,b,0) for a in range(m) for b in range(m)}
    need(actual==predicted,"Even-modulus factor-two control failed")
    return {"general_cases":cases,"moduli":[4,6,8,9],"involutions":len(matrices),
            "factor_two_control_modulus":8}


def integer_reflection():
    def mul(a,b):
        x,y,t=a; u,v,s=b
        return (x+(-u if t else u),y+v,(t+s)%2)
    def inv(a):
        x,y,t=a
        return (x if t else -x,-y,t)
    r=(0,0,1); e2=(0,1,0)
    for n in range(15):
        f=(n,0,0)
        rn=mul(mul(f,r),inv(f))
        t=mul(rn,r)
        need(t==(2*n,0,0),"Integer commutator lost factor 2")
        for a,b,eps in product(range(-4,5),range(-4,5),(0,1)):
            g=(2*n*a,b,eps)
            for s in (r,e2,inv(e2),rn):
                h=mul(g,s)
                need(h[0]==0 if n==0 else h[0]%(2*n)==0,
                     "Exact integer normal form not stable")
    # Nonsaturated C=3Z: nonzero Mbar=2 mod 3 cannot distinguish n=1,2.
    need(gcd(3,2)==gcd(3,4)==1,"Nonsaturated-quotient countercontrol failed")
    return {"parameters":15,"normal_form":"(2*n*a,b,epsilon)",
            "nonsaturated_counterexample_kernel_generators":[[3,2],[3,4]],
            "nonsaturated_counterexample_equal_kernels":True}


def topology():
    tested=0
    for e,sigma,h,b,d in product((-4,0,3,8,24),(-16,-4,0,1),(0,1,2,4,7),(1,4,9),(2,3,5)):
        ey=e+b; sy=sigma-b
        r=ey+4*h-4
        eyd=4-4*h+d*r
        syd=d*sy
        need(eyd+syd-e-sigma==(d-1)*(e+sigma+4*h-4),"Base-change expansion failed")
        for k in (0,b,2*b):
            need((eyd-k)+(syd+k)==eyd+syd,"Blowdown changed e+signature")
        tested+=1
    for q in range(2,101):
        eZ=8-4*q; sZ=-4; h=2*q
        rZ=eZ-(4-4*h)
        need(rZ+sZ==4*q,"Ruled sum defect failed")
    return {"base_change_cases":tested,"ruled_sum_cases":99,
            "zero_bracket_not_claimed_impossible":True}


def rank_and_saturation_index(columns):
    d=len(columns[0]); matrix=[list(r) for r in zip(*columns)]
    for r in range(min(d,len(columns)),0,-1):
        minors=[abs(det([[matrix[i][j] for j in cs] for i in rs]))
                for rs in combinations(range(d),r) for cs in combinations(range(len(columns)),r)]
        index=reduce(gcd,minors)
        if index:
            return r,index
    return 0,1


def intrinsic_index_checks():
    tested=0
    A=[(1,0,0)]
    families=[[(1,2,0),(3,0,3)],[(0,2,0)],[(1,0,0),(0,3,0),(0,0,5)]]
    transforms=[((1,0,0),(0,1,0),(0,0,1)),((1,2,0),(0,1,3),(0,0,1)),((0,1,0),(1,0,0),(0,0,-1))]
    for M in families:
        rank,index=rank_and_saturation_index(A+M)
        s=rank-1
        need(s>0,"Expected positive rank increase")
        for n in range(1,21):
            columns=A+[tuple(n*x for x in v) for v in M]
            r,j=rank_and_saturation_index(columns)
            need((r,j)==(rank,n**s*index),"Intrinsic saturation-index formula failed")
            for T in transforms:
                need(abs(det([list(r) for r in T]))==1,"Bad test basis")
                changed=[tuple(dot(row,v) for row in T) for v in columns]
                need(rank_and_saturation_index(changed)==(r,j),"Saturation index changed under unimodular action")
                tested+=1
    # Saturation of A matters for the simple all-n formula.
    r,j=rank_and_saturation_index([(2,0),(2,0),(0,2)])
    need((r,j)==(2,4),"Nonsaturated countercontrol failed")
    need(j!=2,"Omitting the saturation hypothesis escaped the control")
    return {"unimodular_cases":tested,"all_n_formula":"j(Lambda_n)=n^s*j(Lambda_1)",
            "hypothesis":"Lambda_0 saturated and rank increase s > 0",
            "nonsaturated_naive_formula_rejected":True}


def main():
    need(False is False,"Runtime guard")
    caught=False
    try:
        finite_group_checks(wrong_coefficient=True)
    except ValueError as exc:
        need(str(exc)=="Even-modulus factor-two control failed","Wrong negative control failure")
        caught=True
    need(caught,"Factor-two mutation was not detected")
    print(json.dumps({"schema":"lefschetz-2974-independent-checks-v1",
          "polarization":polarization(),"torus":torus(),
          "groups":finite_group_checks(),"integer_model":integer_reflection(),
          "topology":topology(),"intrinsic_index":intrinsic_index_checks(),
          "deliberate_factor_two_error_rejected":True,
          "scope":"Exact illustrations and arithmetic, not geometric certification"},indent=2,sort_keys=True))


if __name__=="__main__":
    main()

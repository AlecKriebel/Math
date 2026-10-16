#!/usr/bin/env python3
"""Exact independent checks of the matrix-to-prior-Wiebe translation.

Python standard library only. The proof, not these finite cases, establishes
the general equivalence. Matrices are rational and conjugated into an arbitrary
common basis. No ideal generators or unit vector are supplied to recovery.
"""
from fractions import Fraction as F
from itertools import combinations, permutations, product
import json
from pathlib import Path


def zero(n, m=None):
    return [[F(0) for _ in range(n if m is None else m)] for _ in range(n)]


def identity(n):
    a = zero(n)
    for i in range(n):
        a[i][i] = F(1)
    return a


def mul(a, b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def add(a, b, c=F(1)):
    return [[x+c*y for x,y in zip(ar,br)] for ar,br in zip(a,b)]


def flat(a):
    return [x for row in a for x in row]


def columns(cols):
    return [list(row) for row in zip(*cols)]


def rref(a):
    a = [list(map(F, row)) for row in a]
    pivots = []
    r = 0
    for c in range(len(a[0])):
        p = next((i for i in range(r,len(a)) if a[i][c]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        t = a[r][c]
        a[r] = [x/t for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c]:
                t = a[i][c]
                a[i] = [x-t*y for x,y in zip(a[i],a[r])]
        pivots.append(c)
        r += 1
        if r == len(a):
            break
    return a, pivots


def rank(a):
    return len(rref(a)[1])


def kernel(a):
    rr, ps = rref(a)
    ans = []
    for f in range(len(a[0])):
        if f in ps:
            continue
        v = [F(0)]*len(a[0]); v[f] = F(1)
        for row,p in enumerate(ps):
            v[p] = -rr[row][f]
        ans.append(v)
    return ans


def solve(basis, target):
    rr, ps = rref([row+[t] for row,t in zip(columns(basis),target)])
    assert ps == list(range(len(basis))), "target not in independent basis span"
    return [rr[i][-1] for i in range(len(basis))]


def linear(coeff, mats):
    a = zero(len(mats[0]))
    for c,m in zip(coeff,mats):
        if c:
            a = add(a,m,c)
    return a


def inverse(a):
    n = len(a); e = identity(n)
    rr, ps = rref([row+er for row,er in zip(a,e)])
    assert ps == list(range(n))
    return [row[n:] for row in rr]


def conjugate(ms):
    n = len(ms[0]); s = identity(n)
    for i in range(n):
        for j in range(i+1,n):
            s[i][j] = F((i+j)%3-1)
    si = inverse(s)
    return [mul(mul(s,m),si) for m in ms]


def eval_monomial(exps, ms):
    a = identity(len(ms[0]))
    for e,m in zip(exps,ms):
        for _ in range(e):
            a = mul(a,m)
    return a


def recover(ms):
    """Recover an order ideal and its border generators from matrix evaluations."""
    n,d = len(ms[0]),len(ms)
    candidates = sorted((exps for exps in product(range(n),repeat=d)
                         if sum(exps) <= n-1), key=lambda e:(sum(e),e))
    order, mats, vecs = [], [], []
    for exps in candidates:
        m = eval_monomial(exps,ms); v = flat(m)
        if not vecs or rank(columns(vecs+[v])) > len(vecs):
            order.append(exps); mats.append(m); vecs.append(v)
    assert len(order) == n, "input must have regular-representation dimension"
    for e in order:
        for i,a in enumerate(e):
            if a:
                f = list(e); f[i] -= 1
                assert tuple(f) in order
    border = set()
    for e in order:
        for i in range(d):
            f = list(e); f[i] += 1
            if tuple(f) not in order:
                border.add(tuple(f))
    relations = []
    for b in sorted(border,key=lambda e:(sum(e),e)):
        coeff = solve(vecs,flat(eval_monomial(b,ms)))
        assert flat(add(eval_monomial(b,ms),linear(coeff,mats),F(-1))) == [F(0)]*(n*n)
        relations.append({"border":list(b),"basis_coefficients":[str(c) for c in coeff]})
    return order,mats,relations


def prior_wiebe(ms, basis, lam):
    """Present m_lambda B using all coefficient-kernel syzygies in B^d."""
    n,d = len(ms[0]),len(ms)
    ts = [add(m,identity(n),F(-l)) for m,l in zip(ms,lam)]
    e = columns([flat(mul(t,b)) for t in ts for b in basis])
    zs = kernel(e)
    w = [[linear(z[i*n:(i+1)*n],basis) for z in zs] for i in range(d)]
    for c in range(len(zs)):
        s = zero(n)
        for i in range(d):
            s = add(s,mul(ts[i],w[i][c]))
        assert not any(flat(s))
    tested, nonzero = 0,None
    for cs in combinations(range(len(zs)),d):
        delta = zero(n)
        for perm in permutations(range(d)):
            parity = sum(perm[i]>perm[j] for i in range(d) for j in range(i+1,d))%2
            term = identity(n)
            for i in range(d):
                term = mul(term,w[i][cs[perm[i]]])
            delta = add(delta,term,F(-1 if parity else 1))
        tested += 1
        if any(flat(delta)) and nonzero is None:
            nonzero = {"columns":list(cs),"rank_of_determinant_matrix":rank(delta)}
    return {"rank_of_coefficient_map":rank(e),"kernel_columns":len(zs),
            "minors_tested":tested,"is_local_ci":nonzero is not None,
            "first_nonzero_minor":nonzero}


def koszul(ms,lam):
    n,d = len(ms[0]),len(ms)
    ts = [add(m,identity(n),F(-l)) for m,l in zip(ms,lam)]
    d1 = [sum((t[i] for t in ts),[]) for i in range(n)]
    d2 = zero(d*n,len(list(combinations(range(d),2)))*n)
    for col,(i,j) in enumerate(combinations(range(d),2)):
        for r in range(n):
            for s in range(n):
                d2[i*n+r][col*n+s] = -ts[j][r][s]
                d2[j*n+r][col*n+s] = ts[i][r][s]
    r1 = rank(d1)
    r2 = rank(d2) if d>1 else 0
    return {"D1_rank":r1,"D2_rank":r2,"H1_dimension":d*n-r1-r2,
            "is_local_ci":r1==n-1 and d*n-r1-r2==d}


def truncated(bounds):
    bs = list(product(*(range(k) for k in bounds)))
    ms = [zero(len(bs)) for _ in bounds]
    for j,e in enumerate(bs):
        for i,k in enumerate(bounds):
            f = list(e); f[i]+=1
            if f[i]<k:
                ms[i][bs.index(tuple(f))][j] = F(1)
    return ms


def square_zero(d):
    ms = [zero(d+1) for _ in range(d)]
    for i in range(d): ms[i][i+1][0] = F(1)
    return ms


def gorenstein_non_ci():
    # Basis 1,x,y,z,xy, with z^2=xy and x^2=y^2=xz=yz=0.
    ms = [zero(5) for _ in range(3)]
    for i in range(3): ms[i][i+1][0]=F(1)
    ms[0][4][2]=F(1); ms[1][4][1]=F(1); ms[2][4][3]=F(1)
    return ms


def block_product(a,b,shift):
    n,m = len(a[0]),len(b[0]); ans=[]
    for i,(x,y) in enumerate(zip(a,b)):
        z=zero(n+m)
        for r in range(n):
            for s in range(n): z[r][s]=x[r][s]
        for r in range(m):
            for s in range(m): z[n+r][n+s]=y[r][s]+F(shift[i] if r==s else 0)
        ans.append(z)
    return ans


def main():
    j=truncated([4])[0]
    curved=[j,mul(j,j),mul(mul(j,j),j)]
    reduced=[[[F(point[i] if r==s else 0) for s,point in enumerate([(0,0,0),(1,2,3),(2,1,1)])]
              for r in range(3)] for i in range(3)]
    cases=[
        ("univariate_t3",truncated([3]),[(0,)],True),
        ("two_variable_rectangular_ci",truncated([2,3]),[(0,0)],True),
        ("two_variable_square_zero_non_ci",square_zero(2),[(0,0)],False),
        ("three_variable_curved_t4_affine_ci",curved,[(0,0,0)],True),
        ("three_variable_gorenstein_non_ci",gorenstein_non_ci(),[(0,0,0)],False),
        ("three_reduced_supports",reduced,[(0,0,0),(1,2,3),(2,1,1)],True),
        ("mixed_multiple_support_non_ci",block_product(truncated([2,2]),square_zero(2),(5,0)),[(0,0),(5,0)],False),
        ("multiple_nonreduced_ci",block_product(truncated([2,2]),truncated([2,1]),(5,0)),[(0,0),(5,0)],True),
    ]
    report=[]
    for name,ms,support,expected in cases:
        ms=conjugate(ms)
        assert all(mul(a,b)==mul(b,a) for a,b in combinations(ms,2))
        order,basis,relations=recover(ms)
        local=[]
        for lam in support:
            prior=prior_wiebe(ms,basis,lam); candidate=koszul(ms,lam)
            assert prior["is_local_ci"]==candidate["is_local_ci"]
            local.append({"lambda":list(lam),"prior_wiebe":prior,"candidate_koszul":candidate})
        actual=all(x["prior_wiebe"]["is_local_ci"] for x in local)
        assert actual==expected
        report.append({"name":name,"N":len(ms[0]),"d":len(ms),"order_ideal":[list(e) for e in order],
                       "border_relations":relations,"local_tests":local,"global_ci":actual})
    target=Path(__file__).with_name("translation_checks.json")
    target.write_text(json.dumps({"method":"matrix-algebra kernel to Wiebe Fitting minors",
                                  "arithmetic":"exact rational; standard library",
                                  "passed":len(report),"cases":report},indent=2)+"\n")
    print(json.dumps({"passed":len(report),"cases":[{"name":r["name"],"N":r["N"],"global_ci":r["global_ci"]} for r in report]},indent=2))


if __name__ == "__main__":
    main()

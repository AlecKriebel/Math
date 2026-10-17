#!/usr/bin/env python3
"""Exact finite illustrations, not a proof of any arithmetic cocycle residue."""
import itertools, json
from pathlib import Path


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def rank(a, p):
    a = [[x % p for x in row] for row in a]
    if not a:
        return 0
    r = 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        inv = pow(a[r][c], -1, p)
        a[r] = [x*inv % p for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c]:
                t = a[i][c]
                a[i] = [(x-t*y) % p for x,y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def induced_test(moduli, kappa, Q, psi_indices):
    """C=product Z/n; psi=(-1)^sum specified coordinates, an honest char."""
    for i in psi_indices:
        require(moduli[i] % 2 == 0, "quadratic character must be well-defined")
    elems = list(itertools.product(*[range(n) for n in moduli]))
    add = lambda a,b: tuple((x+y)%n for x,y,n in zip(a,b,moduli))
    zero = tuple(0 for _ in moduli)
    powers = [zero]
    while (v := add(powers[-1], kappa)) != zero:
        powers.append(v)
    f = len(powers)
    require(pow(Q, f, 5) == 1, "stabilizer character must respect its order")
    seen, reps, loc = set(), [], {}
    for x in elems:
        if x in seen:
            continue
        j = len(reps); reps.append(x)
        for t,k in enumerate(powers):
            y = add(x,k); seen.add(y); loc[y]=(j,t)
    d = len(reps)
    row_blocks, column_blocks = [], []
    psi = lambda g: pow(4, sum(g[i] for i in psi_indices), 5)
    for i,n in enumerate(moduli):
        g = tuple(int(j==i) for j in range(len(moduli)))
        mat = [[0]*d for _ in range(d)]
        for j,x in enumerate(reps):
            k,t=loc[add(g,x)]
            mat[k][j]=pow(Q,t,5)
        for j in range(d):
            mat[j][j]=(mat[j][j]-psi(g))%5
        row_blocks.extend(mat)
        column_blocks.extend([list(col) for col in zip(*mat)])
    inv_dim = d-rank(row_blocks,5)
    quotient_dim = d-rank(column_blocks,5)
    expected = int(psi(kappa)==Q%5)
    require(inv_dim == quotient_dim == expected, "induced invariant and coinvariant dimensions")
    return dict(C=moduli,kappa=kappa,Q_mod5=Q%5,f=f,induced_dimension=d,
                invariant_dimension=inv_dim,coinvariant_dimension=quotient_dim,
                psi_kappa=psi(kappa))


def congruence_check(ell, m, n, allowed_units):
    modulus=ell**m
    units={u % modulus for u in allowed_units}
    mats=[]
    for a,b,c,d in itertools.product(range(modulus),repeat=4):
        if c % (ell**min(n,m)) or (d-1) % (ell**min(n,m)):
            continue
        if (a*d-b*c)%modulus in units:
            mats.append((a,b,c,d))
    size=len(mats)
    k=size
    for p in {ell,2,3}:
        while k%p==0 and k:
            k//=p
    require(k==1, "congruence quotient has no forbidden prime divisor")
    return dict(ell=ell,m=m,n=n,unit_images=sorted(units),group_size=size,
                only_allowed_prime_factors=True)


def main():
    induced=[]
    # Include nonsemisimple C5 and C5 x C5 cases; psi comes from a C2 factor.
    for mods in [(2,), (2,5), (2,5,5), (4,), (4,5), (6,5)]:
        for kap in itertools.product(*[range(n) for n in mods]):
            for Q in range(1,5):
                f=1
                while any((f*x)%n for x,n in zip(kap,mods)):
                    f+=1
                if pow(Q,f,5)==1:
                    induced.append(induced_test(mods,kap,Q,[0]))
    congruences=[congruence_check(ell,m,n,units) for ell,m,n,units in
                 [(2,2,2,[1,-1]),(2,3,2,[1,-1]),(3,2,1,[1,-1]),
                  (3,2,2,[1,-1]),(5,2,1,[1,-1])]]
    # Every allowed scalar is killed mod5; t=2 mod25 has exactly one factor5.
    scalar_values={str(t): t**4-1 for t in [2,3,7,11,13]}
    require((2**4-1)%25 != 0 and all(v%5==0 for v in scalar_values.values()),
            "scalar fifth-divisibility and exact valuation")
    result={"status":"all checks passed","induced_cases":len(induced),
            "nonsemisimple_cases":sum(5 in x['C'] for x in induced),
            "induced_cases_detail":induced,"congruence_examples":congruences,
            "scalar_values":scalar_values,
            "actual_cocycle_evaluated":False,
            "scope":"finite group checks only; no continuity or integrality claim"}
    dest=Path(__file__).with_name('CHECK_RESULTS.json')
    dest.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='induced_cases_detail'},indent=2))

if __name__=='__main__': main()

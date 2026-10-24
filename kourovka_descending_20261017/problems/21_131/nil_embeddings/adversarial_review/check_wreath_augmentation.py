"""Finite sanity checks for Sections 1-2; proof remains in audit.md.

Run with Python 3; standard library only. All arithmetic is exact.
UT_3(F_p) uses (a,b,c) for the entries (1,2),(2,3),(1,3).
"""
from itertools import product
import json


def check_prime(p):
    group = list(product(range(p), repeat=3))
    ident = (0, 0, 0)
    def mul(g, h):
        a,b,c = g
        x,y,z = h
        return ((a+x)%p, (b+y)%p, (c+z+a*y)%p)
    def inv(g):
        a,b,c = g
        return (-a%p, -b%p, (-c+a*b)%p)
    def power(g, k):
        ans = ident
        for _ in range(k):
            ans = mul(ans, g)
        return ans
    wreath = {}
    for m in (p, p*p):
        admitted = 0
        rejected = 0
        for h in group:
            f = [power(h, i) for i in range(m)]
            # [f,t](i)=f(i)f(i-1)^{-1}, with i-1 cyclic.
            comm = [mul(f[i], inv(f[(i-1)%m])) for i in range(m)]
            equal = all(g == h for g in comm)
            admissible = power(h, m) == ident
            assert equal == admissible
            admitted += admissible
            rejected += not admissible
        wreath[str(m)] = {"valid_diagonal_commutators": admitted,
                          "correctly_rejected_wraparound": rejected}

    size = len(group)
    index = {g:i for i,g in enumerate(group)}
    table = [[index[mul(g,h)] for h in group] for g in group]
    def algebra_mul(v, w):
        ans = [0]*size
        for i,x in enumerate(v):
            if not x:
                continue
            for j,y in enumerate(w):
                if y:
                    k = table[i][j]
                    ans[k] = (ans[k]+x*y)%p
        return ans
    def basis(vectors):
        rows = {}
        for v in vectors:
            v = v[:]
            for k in sorted(rows):
                if v[k]:
                    factor = v[k]
                    v = [(a-factor*b)%p for a,b in zip(v, rows[k])]
            lead = next((i for i,x in enumerate(v) if x), None)
            if lead is not None:
                scale = pow(v[lead], -1, p)
                rows[lead] = [(scale*x)%p for x in v]
        return list(rows.values())
    augmentation = []
    for g in group[1:]:
        v = [0]*size
        v[index[g]] = 1
        v[index[ident]] = -1%p
        augmentation.append(v)
    current = basis(augmentation)
    dims = []
    while current:
        dims.append(len(current))
        current = basis([algebra_mul(v,w)
                         for v in current for w in augmentation])
        assert len(dims) <= size, "Nilpotence bound |P| failed"
    dims.append(0)
    assert dims[0] == size-1
    return {"p":p, "group_order":size, "wreath_checks":wreath,
            "augmentation_power_dimensions":dims,
            "nilpotence_index":len(dims)}


if __name__ == "__main__":
    print(json.dumps({"UT3_examples":[check_prime(2), check_prime(3)],
                      "scope":"finite sanity checks, not proof of the general claim"},
                     indent=2))

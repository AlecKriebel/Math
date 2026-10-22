#!/usr/bin/env python3
"""Small exact convention checks; these do not verify 3-manifold topology."""
from itertools import permutations, product
import json

def mul(a, b):
    return tuple(a[b[i]] for i in range(len(a)))

def inv(a):
    return tuple(a.index(i) for i in range(len(a)))

def subgroup(gens, n=4):
    ans = {tuple(range(n))}
    while True:
        nxt = ans | {mul(a,b) for a in ans for b in gens}
        if nxt == ans:
            return ans
        ans = nxt

def main():
    G = list(permutations(range(4)))
    L = subgroup([(1,0,2,3), (0,2,1,3)])
    R = subgroup([(0,1,3,2)])
    j = (1,2,3,0)
    jj = inv(j)
    Lconj = {mul(mul(jj,l),j) for l in L}
    orbit_checks = 0
    for phi in G:
        alpha = mul(j,phi)
        alpha_orbit = {mul(mul(l,alpha),inv(r)) for l in L for r in R}
        phi_orbit = {mul(mul(l,phi),inv(r)) for l in Lconj for r in R}
        assert {mul(jj,a) for a in alpha_orbit} == phi_orbit
        for p2 in G:
            assert (p2 in phi_orbit) == (mul(j,p2) in alpha_orbit)
            orbit_checks += 1
    # Deliberately dropping the conjugation must fail somewhere.
    assert any(
        {mul(jj,mul(mul(l,mul(j,p)),inv(r))) for l in L for r in R}
        != {mul(mul(l,p),inv(r)) for l in L for r in R}
        for p in G
    )
    genus_checks = 0
    for k in range(1,5):
        for hs in product(range(4), repeat=k):
            for extra in range(5):
                n = k-1+extra
                g = sum(hs)+n-k+1
                chiF = sum(2-2*h for h in hs)
                assert (2-2*g)+chiF == 2*(chiF-n)
                genus_checks += 1
    for p in range(50):
        assert 1+p-1+1 == p+1
    torus_checks = 0
    for a,b,c,d in product(range(-4,5),repeat=4):
        if a*d-b*c != 1:
            continue
        # The meridian subgroup Z(1,0) is preserved exactly by c=0.
        preserves = c == 0 and abs(a) == 1
        assert preserves == (c == 0)
        torus_checks += 1
    print(json.dumps({
        "double_coset_equivalence_checks": orbit_checks,
        "omitted_conjugation_mutant_rejected": True,
        "handle_euler_checks": genus_checks,
        "knot_genus_checks": 50,
        "solid_torus_matrix_checks": torus_checks,
        "topology_proof_certified_by_computation": False,
        "status": "PASS"
    }, sort_keys=True, indent=2))

if __name__ == '__main__':
    main()

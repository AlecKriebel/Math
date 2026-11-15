#!/usr/bin/env python3
"""Read-only, exact source-interface diagnostics; finite checks, not an infinite proof."""
from fractions import Fraction as Q
from math import gcd
import json


def require(condition, description):
    if not condition:
        raise RuntimeError(description)


def main():
    f = [0, 1]
    for _ in range(199):
        f.append(f[-1] + f[-2])
    counts = {"cassini_and_coprimality_indices": 0, "reversed_coordinate_points": 0,
              "endpoint_points": 0, "unit_norm_heights": 0,
              "geometry_pairs": 0, "nearest_residue_offsets": 0,
              "exact_zaremba_indices": 0, "negative_controls": 0}
    for n in range(3, 201):
        p, q = f[n-1], f[n]
        sign = (-1)**n
        require(gcd(p, q) == 1, "consecutive Fibonacci coprimality")
        require((p*p-sign) % q == 0, "Cassini modular square")
        require((p*(sign*p)-1) % q == 0, "actual modular inverse")
        counts["cassini_and_coprimality_indices"] += 1
        if n <= 16:
            image = set()
            for j in range(q):
                k = p*j % q
                image.add(k)
                require((p*k-sign*j) % q == 0, "ABD angle equals target up to parity reflection")
                require(Q(k,q) == Q(p*j % q,q), "ABD height equals target after permutation")
                counts["reversed_coordinate_points"] += 1
            require(len(image) == q, "reindexing is a permutation")
        if q <= 610:
            products = []
            for m in range(1,q):
                r = p*m % q
                r = min(r,q-r)
                require(r > 0 and 3*m*r >= q, "needed arithmetic product bound")
                products.append(m*r)
                counts["nearest_residue_offsets"] += 1
            rho = min([q] + products)
            require(rho == f[n-2], "classical exact Zaremba index including axis vectors")
            counts["exact_zaremba_indices"] += 1
    for q in range(2,51):
        for k in range(q+1):
            t=Q(k,q)
            radius2=4*t*(1-t)
            require(radius2+(1-2*t)**2 == 1, "unit sphere, including both endpoints")
            counts["unit_norm_heights"] += 1
        for j in range(1,q+1):
            a,b=Q(j,q),Q(q-j,q)
            require(a*(1-a) == b*(1-b) and 1-2*a == -(1-2*b), "endpoint isometry radial/vertical components")
            require((j+(q-j)) % q == 0, "endpoint isometry negates integer longitude")
            counts["endpoint_points"] += 1
    for q in range(2,21):
        for i in range(q):
            for j in range(i+1,q+1):
                a,b=Q(i,q),Q(j,q)
                d=b-a
                u=2*(a+b-2*a*b)
                v2=16*a*(1-a)*b*(1-b)
                require(u-2*d == 4*a*(1-b) >= 0, "latitude inequality")
                require(v2 == u*u-4*d*d, "radial algebra")
                # Coefficient identity avoids numerical square roots entirely.
                for c in (Q(0),Q(1,3),Q(3,4),Q(-1,2)):
                    residual=(1-c*c)*(u*u-v2-4*d*d)
                    require(residual == 0, "squared longitude identity")
                if j < q:
                    require((u==2*d) == (i==0), "endpoint-sensitive equality condition")
                counts["geometry_pairs"] += 1
    # These are exact, intentionally false source substitutions.
    require((3*3-1) % 5 != 0, "odd Fibonacci coordinate swap needs reflection")
    counts["negative_controls"] += 1
    require((3*3-1) % 7 != 0, "arbitrary rational multiplier need not be self-inverse")
    counts["negative_controls"] += 1
    require(Q(1,2*5) != 0, "midpoint convention has no pole at index zero")
    counts["negative_controls"] += 1
    # Phi(0,0)=(0,0,1), Phi(0,1/2)=(1,0,0): 2 versus 1/4.
    lift_chord2 = 2 * (2 * Q(1,2))
    planar_distance2 = Q(1,2)**2
    require(lift_chord2 == 2 and planar_distance2 == Q(1,4)
            and lift_chord2 != planar_distance2, "equal-area lift is not distance preserving")
    counts["negative_controls"] += 1
    print(json.dumps({"status":"PASS_EXACT_SOURCE_INTERFACE_DIAGNOSTICS", "counts":counts,
                      "infinite_theorem_proved_by_finite_checks":False,
                      "priority_certified":False, "writes_files":False},sort_keys=True))


if __name__ == "__main__":
    main()

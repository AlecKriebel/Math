"""Small witness audit written from the displayed matrices, without verifier reuse."""
from collections import Counter


def check(p, A, B, expected):
    I = (1, 0, 0, 1)
    Z = ((-1) % p, 0, 0, (-1) % p)

    def mul(a, b):
        x, y, z, w = a
        r, s, t, u = b
        return ((x*r+y*t) % p, (x*s+y*u) % p,
                (z*r+w*t) % p, (z*s+w*u) % p)

    def pow_(a, n):
        r = I
        for _ in range(n):
            r = mul(r, a)
        return r

    def group(gens):
        found, queue = {I}, [I]
        for a in queue:
            for b in gens:
                c = mul(a, b)
                if c not in found:
                    found.add(c)
                    queue.append(c)
        return found

    def order(a):
        r = I
        for n in range(1, 121):
            r = mul(r, a)
            if r == I:
                return n
        raise AssertionError(a)

    H = group((A, B))
    assert len(H) == expected
    assert all((a*d-b*c) % p == 1 for a, b, c, d in H)
    lines = [(1, t) for t in range(p)] + [(0, 1)]
    stabilizers = []
    for x, y in lines:
        stabilizer = {
            h for h in H
            if (x*(h[2]*x+h[3]*y)-y*(h[0]*x+h[1]*y)) % p == 0
        }
        stabilizers.append(stabilizer)
    if p == 29:
        assert pow_(A, 2) == pow_(B, 3) == pow_(mul(A, B), 5) == Z
        R = (A, (12, 24, 0, 17), (25, 3, 4, 4))
        assert R[1] == mul(mul(B, A), pow_(B, 2))
        assert R[2] == mul(mul(A, R[1]), pow_(mul(A, B), 2))
        assert all(r in H and pow_(r, 2) == Z for r in R)
        pairs = [group((R[j], R[k])) for j, k in ((1, 2), (0, 2), (0, 1))]
        assert [len(g) for g in pairs] == [8, 12, 20]
        assert [order(mul(R[j], R[k])) for j, k in ((1, 2), (0, 2), (0, 1))] == [4, 3, 10]
        assert pairs[0] & pairs[1] == group((R[2],))
        assert set.intersection(*pairs) == {I, Z}
        assert group(R) == H
        assert all(len(g) == 4 and any(order(h) == 4 for h in g) for g in stabilizers)

        # Lists (translation vector, linear matrix) for the three faithful witnesses.
        vadd = lambda x, y: tuple((a+b) % p for a, b in zip(x, y))
        lines_affine = []
        for direction, shift in (((1, 0), (0, 0)), ((0, 1), (0, 0)), ((1, 1), (2, 0))):
            W = [((t*direction[0]) % p, (t*direction[1]) % p) for t in range(p)]
            lines_affine.append({(v, I) for v in W} | {(vadd(v, shift), Z) for v in W})
        assert [len(g) for g in lines_affine] == [58, 58, 58]
        E = ((0, 0), I)
        assert lines_affine[0] & lines_affine[1] == {E, ((0, 0), Z)}
        assert lines_affine[0] & lines_affine[2] == {E, ((2, 0), Z)}
        assert lines_affine[1] & lines_affine[2] == {E, ((0, p-2), Z)}
        assert set.intersection(*lines_affine) == {E}
        print("p=29: all displayed matrix identities, pair orders, complement generation,")
        print("      pair intersections, thirty cyclic line stabilizers, and faithful witnesses pass.")
    else:
        C = (6, 10, 0, 2)
        assert C in H and order(C) == 10
        assert C in stabilizers[0] and C in stabilizers[4]
        assert group((pow_(C, 5),)) & group((pow_(C, 2),)) == {I}
        print("p=11: complement size 120, displayed C membership/order, and both eigenlines pass.")
    print("Line-stabilizer order distribution:", dict(sorted(Counter(map(len, stabilizers)).items())))


check(29, (0, 28, 1, 0), (2, 7, 12, 28), 120)
check(11, (0, 10, 1, 0), (0, 2, 5, 1), 120)

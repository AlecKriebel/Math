#!/usr/bin/env python3
"""Independent finite exact controls; not a proof or existence certificate."""
import json
import sys
from fractions import Fraction as Q

count = 0


def require(ok, label):
    global count
    if not ok:
        raise ValueError(label)
    count += 1


def main():
    if sys.argv[1:] == ["--negative-control"]:
        require(False, "intentional independent negative control")
    require(not sys.argv[1:], "unexpected arguments")
    # Unit directions via rational stereographic parametrization. For N=z*v,
    # the hyperbolic orthonormal-frame derivative matrix is
    # T=-v_z I + e_z v^T. These planes are not generally minimal.
    # This independently controls the signs in the full divergence identity.
    directions = 0
    for p in range(-3, 4):
        for q in range(-3, 4):
            d = Q(1+p*p+q*q)
            v = [2*Q(p)/d, 2*Q(q)/d, Q(p*p+q*q-1)/d]
            T = [[-v[2]*Q(i==j)+Q(i==2)*v[j] for j in range(3)] for i in range(3)]
            a = [Q(i==2)-v[2]*v[i] for i in range(3)]
            trace = sum(T[i][i] for i in range(3))
            trace_square = sum(T[i][j]*T[j][i] for i in range(3) for j in range(3))
            norm_square = sum(x*x for row in T for x in row)
            require(sum(x*x for x in v)==1, "unit rational direction")
            require(trace==-2*v[2], "mean curvature trace")
            require(trace_square==2*v[2]**2, "trace of derivative square")
            require(-2*a[2]==trace_square-2, "full divergence identity")
            require(norm_square==trace_square+sum(x*x for x in a), "acceleration norm distinction")
            require(sum(a[i]*v[i] for i in range(3))==0, "acceleration tangent")
            neg_a = [Q(i==2)-(-v[2])*(-v[i]) for i in range(3)]
            require(a==neg_a, "normal reversal invariance")
            directions += 1
    # The coordinate model for minimal vertical planes has v_z=0.
    for v in ([Q(1),Q(0),Q(0)], [Q(3,5),Q(4,5),Q(0)]):
        T = [[-v[2]*Q(i==j)+Q(i==2)*v[j] for j in range(3)] for i in range(3)]
        for X in ([-v[1],v[0],Q(0)],[Q(0),Q(0),Q(1)]):
            require(all(sum(T[i][j]*X[j] for j in range(3))==0 for i in range(3)), "zero plane shape operator")
    # All trace-free symmetric 2x2 matrices obey the shape relations.
    for p in range(-4,5):
        for q in range(-4,5):
            B = [[Q(p),Q(q)],[Q(q),Q(-p)]]
            s = sum(B[i][j]*B[j][i] for i in range(2) for j in range(2))
            determinant = B[0][0]*B[1][1]-B[0][1]*B[1][0]
            require(s==-2*determinant, "minimal shape trace determinant")
            require(-1+determinant==-1-s/2, "minimal leaf Gauss curvature")
    # Equality +1,-1 would force a flat principal frame by Codazzi, while
    # its Gauss curvature is -2. This checks the algebra, not that theorem.
    require(-1+Q(1)*Q(-1)==-2, "equality case negative Gauss curvature")
    # Delta_(H2) z^r = r(r-1) z^r; r=-1 supplies the plane lapse.
    require(Q(-1)*Q(-2)==2, "positive plane Jacobi lapse coefficient")
    print(json.dumps({"result":"PASS_INDEPENDENT_FINITE_CONTROLS","checks":count,
        "rational_unit_directions":directions,
        "scope":"Finite rational/algebraic controls only; not a foliation existence or nonexistence certificate"},sort_keys=True,indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("FAIL: "+str(exc),file=sys.stderr)
        sys.exit(1)

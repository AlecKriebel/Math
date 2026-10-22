#!/usr/bin/env python3
"""Supplementary exact computations, not a certificate of foliation existence."""
import json
import sys
import sympy as sp

checks = 0


def equal(actual, expected, label):
    global checks
    if sp.simplify(actual - expected) != 0:
        raise ValueError(f"FAILED: {label}: {actual} != {expected}")
    checks += 1


def main():
    if len(sys.argv) > 1:
        if sys.argv[1:] == ["--negative-control"]:
            equal(sp.Integer(1), sp.Integer(0), "intentional negative control")
        raise ValueError("Unexpected arguments")

    x, y, z = sp.symbols("x y z", positive=True)
    xyz = [x, y, z]
    g = sp.eye(3) / z**2
    inv = g.inv()
    Gamma = [[[sp.simplify(sum(inv[k, l] *
        (sp.diff(g[l, j], xyz[i]) + sp.diff(g[l, i], xyz[j])
         - sp.diff(g[i, j], xyz[l])) / 2 for l in range(3)))
        for j in range(3)] for i in range(3)] for k in range(3)]
    delta = lambda i, j: sp.Integer(i == j)
    for k in range(3):
        for i in range(3):
            for j in range(3):
                expected = (-delta(k, i)*delta(j, 2)
                            -delta(k, j)*delta(i, 2)
                            +delta(i, j)*delta(k, 2))/z
                equal(Gamma[k][i][j], expected, f"Christoffel {k}{i}{j}")

    def R(l, k, i, j):
        return sp.simplify(sp.diff(Gamma[l][j][k], xyz[i])
             - sp.diff(Gamma[l][i][k], xyz[j])
             + sum(Gamma[l][i][m]*Gamma[m][j][k]
                   - Gamma[l][j][m]*Gamma[m][i][k] for m in range(3)))

    for l in range(3):
        for k in range(3):
            for i in range(3):
                for j in range(3):
                    equal(R(l, k, i, j),
                          g[k, i]*delta(l, j)-g[k, j]*delta(l, i),
                          f"constant sectional curvature tensor {l}{k}{i}{j}")
    for k in range(3):
        for j in range(3):
            equal(sum(R(i, k, i, j) for i in range(3)), -2*g[k, j],
                  f"Ricci {k}{j}")

    N = sp.Matrix([z, 0, 0])
    deriv = sp.Matrix(3, 3, lambda j, i: sp.diff(N[j], xyz[i])
                  + sum(Gamma[j][i][k]*N[k] for k in range(3)))
    for tangent in (sp.Matrix([0, z, 0]), sp.Matrix([0, 0, z])):
        for j, value in enumerate(deriv*tangent):
            equal(value, 0, f"plane shape component {j}")
    a = sp.simplify(deriv*N)
    for j in range(3):
        equal(a[j], [0, 0, z][j], f"acceleration component {j}")
    div = lambda v: sp.simplify(sum(sp.diff(z**-3*v[i], xyz[i])
                                   for i in range(3))*z**3)
    equal(div(N), 0, "normal divergence")
    equal(div(a), -2, "acceleration divergence")
    u = 1/z
    equal(z**2*(sp.diff(u,y,2)+sp.diff(u,z,2)), 2*u, "plane Jacobi lapse")

    p,q,b,c = sp.symbols("p q b c", real=True)
    B = sp.Matrix([[p,q],[q,-p]])
    equal(sp.trace(B),0,"minimal trace")
    equal(sp.trace(B*B),2*(p*p+q*q),"shape norm")
    equal(B.det(),-(p*p+q*q),"shape determinant")
    T = sp.Matrix([[p,q,b],[q,-p,c],[0,0,0]])
    equal(sp.trace(T*T),sp.trace(B*B),"trace square has no acceleration term")
    equal(sum(v*v for v in T),sp.trace(B*B)+b*b+c*c,"full norm differs")
    A = sp.diag(1,-1)
    C = lambda w: sp.Matrix([[0,-w],[w,0]])
    d1 = C(b)*A-A*C(b)
    d2 = C(c)*A-A*C(c)
    for actual, expected in zip(d1[:,1],sp.Matrix([2*b,0])):
        equal(actual,expected,"first Codazzi side")
    for actual, expected in zip(d2[:,0],sp.Matrix([0,2*c])):
        equal(actual,expected,"second Codazzi side")
    equal(-1+A.det(),-2,"Gauss equality case")
    print(json.dumps({"checks":checks,"result":"PASS_EXACT_SUPPLEMENTARY_CALCULATIONS",
        "scope":"Coordinate and algebra identities only; no geometric existence certificate",
        "sympy_version":sp.__version__},sort_keys=True,indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAIL: {exc}",file=sys.stderr)
        sys.exit(1)

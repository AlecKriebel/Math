#!/usr/bin/env python3
"""Small exact checks for KP-1.30. No network or third-party knot dataset.

Requires Python 3 and SymPy (tested with 1.14.0). This is a transparent
cube-of-resolutions calculation for closures of positive two-strand braids,
plus algebraic obstruction examples. It is not a search for a counterexample.
"""
import json
from itertools import product
from pathlib import Path
import sympy as sp


def require(condition):
    if not condition:
        raise RuntimeError("Exact verification condition failed")


def rank2(a):
    rows = [[int(v) % 2 for v in row] for row in a.tolist()]
    r = 0
    for c in range(a.cols):
        pivot = next((i for i in range(r, a.rows) if rows[i][c]), None)
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        for i in range(a.rows):
            if i != r and rows[i][c]:
                rows[i] = [x ^ y for x, y in zip(rows[i], rows[r])]
        r += 1
    return r


def circles(n, bits):
    # At level k the two vertices are 2*k and 2*k+1. The final
    # level is joined to level zero, implementing braid closure.
    par = list(range(2 * (n + 1)))

    def root(x):
        while par[x] != x:
            x = par[x]
        return x

    def join(x, y):
        par[root(x)] = root(y)

    join(0, 2 * n)
    join(1, 2 * n + 1)
    for k, b in enumerate(bits):
        if b == 0:
            join(2 * k, 2 * k + 2)
            join(2 * k + 1, 2 * k + 3)
        else:
            join(2 * k, 2 * k + 1)
            join(2 * k + 2, 2 * k + 3)
    groups = {}
    for k in range(len(par)):
        groups.setdefault(root(k), set()).add(k)
    return sorted(groups.values(), key=min)


def cube(n, reduced):
    states = {s: circles(n, s) for s in product((0, 1), repeat=n)}
    basis, degree = {}, {}
    for s, cs in states.items():
        mark = next(i for i, c in enumerate(cs) if 0 in c)
        for labels in product((0, 1), repeat=len(cs)):
            # 0 labels 1; 1 labels X. Reduced subcomplex fixes X
            # at the marked circle, then shifts quantum degree by +1.
            if reduced and labels[mark] != 1:
                continue
            i = sum(s)
            q = n + i + len(cs) - 2 * sum(labels) + int(reduced)
            basis.setdefault((i, q), []).append((s, labels))
            degree[s, labels] = (i, q)
    indices = {g: {v: k for k, v in enumerate(bs)} for g, bs in basis.items()}
    mats = {}
    for g, bs in basis.items():
        i, q = g
        target = (i + 1, q)
        mat = sp.zeros(len(basis.get(target, [])), len(bs))
        for col, (s, labels) in enumerate(bs):
            old = states[s]
            for k, b in enumerate(s):
                if b:
                    continue
                t = s[:k] + (1,) + s[k + 1:]
                new = states[t]
                sign = (-1) ** sum(s[:k])
                overlaps = [[j for j, c in enumerate(old) if c & d] for d in new]
                options = []
                if len(new) == len(old) - 1:  # multiplication
                    out = []
                    for js in overlaps:
                        val = sum(labels[j] for j in js)
                        if val > 1:  # X*X = 0
                            break
                        out.append(val)
                    else:
                        options.append(tuple(out))
                else:  # comultiplication
                    require(len(new) == len(old) + 1)
                    oldsplit = next(j for j in range(len(old))
                                    if sum(j in js for js in overlaps) == 2)
                    split = [a for a, js in enumerate(overlaps) if oldsplit in js]
                    base = [labels[js[0]] for js in overlaps]
                    images = [(1, 1)] if labels[oldsplit] else [(0, 1), (1, 0)]
                    for aa, bb in images:
                        out = base[:]
                        out[split[0]], out[split[1]] = aa, bb
                        options.append(tuple(out))
                for out in options:
                    require(degree[t, out] == target)
                    mat[indices[target][t, out], col] += sign
        mats[g] = mat
    for (i, q), a in mats.items():
        b = mats.get((i + 1, q))
        if b is not None:
            require(b * a == sp.zeros(b.rows, a.cols))
    rq, r2 = {g: a.rank() for g, a in mats.items()}, {g: rank2(a) for g, a in mats.items()}
    hom = {}
    for (i, q), bs in sorted(basis.items()):
        hq = len(bs) - rq[i, q] - rq.get((i - 1, q), 0)
        h2 = len(bs) - r2[i, q] - r2.get((i - 1, q), 0)
        if hq or h2:
            hom[f"{i},{q}"] = {"Q": hq, "F2": h2}
    return {"Q": sum(x["Q"] for x in hom.values()),
            "F2": sum(x["F2"] for x in hom.values()),
            "bigraded": hom, "d_squared_zero": True}


def algebra_checks():
    # Two-term complex Z --2^e--> Z: beta_1 sees only e=1.
    bockstein = [{"exponent": e, "Q_total": 0, "F2_total": 2,
                  "first_bockstein_rank": int(e == 1), "tau2": 1}
                 for e in range(1, 5)]
    for v in bockstein:
        require((2 ** v["exponent"] // 2) % 2 == v["first_bockstein_rank"])
    # A = (Z --2--> Z) embeds in B = (Z^2 --[2,1]--> Z).
    skein = {"A_Q_total": 0, "A_F2_total": 2,
             "B_Q_total": 1, "B_F2_total": 1,
             "connecting_Z_to_Z2_surjective": True}
    require(sp.Matrix([[2, 1]]).rank() == rank2(sp.Matrix([[2, 1]])) == 1)
    # Staircase: a,c in homological degree 0, b,e in degree 1;
    # q(a,c,b,e)=(0,2,2,4), d(c)=b, T(a)=b, T(c)=e.
    d, t = sp.Matrix([[0, 1], [0, 0]]), sp.eye(2)
    a, c, b, e = (sp.Matrix(v) for v in ([1, 0], [0, 1], [1, 0], [0, 1]))
    require(d * c == t * a == b and t * c == e)
    require(d.rank() == rank2(d) == 1)
    require((d + t).det() == 1)
    staircase = {"integral_d_homology": "Z in degrees 0 and 1",
                 "d_homology_total": 2, "T_on_d_homology_rank": 0,
                 "second_page_differential_rank": 1,
                 "total_d_plus_T_homology_dimension_F2": 0}
    # Unsigned incidence of cycles: odd cycles create a Z/2 cokernel.
    incidence = []
    for n in range(3, 9):
        mat = sp.zeros(n)
        for j in range(n):
            mat[j, j] = 1
            mat[(j + 1) % n, j] = 1
        from sympy.matrices.normalforms import smith_normal_form
        smith = smith_normal_form(mat, domain=sp.ZZ)
        vals = [abs(int(smith[i, i])) for i in range(n)]
        require(vals == [1] * (n - 1) + [2 if n % 2 else 0])
        incidence.append({"cycle_length": n, "smith_diagonal": vals})
    # A sharp generalized module-lemma example: M=R/(H^2) + R/(H),
    # N=R/(H), f(e0)=z, g(z)=e1. Then gf=H_M, fg=H_N.
    hm = sp.Matrix([[0, 0, 0], [1, 0, 0], [0, 0, 0]])
    hn = sp.zeros(1)
    f, g = sp.Matrix([[1, 0, 0]]), sp.Matrix([[0], [1], [0]])
    require(g * f == hm and f * g == hn)
    require(f * hm == hn * f and g * hn == hm * g)
    module = {"M_bar_lengths": [2, 1], "N_bar_lengths": [1],
              "M_long_bar_count": 1, "N_bar_count": 1,
              "M_bar_count_minus_N_bar_count": 1, "M_unit_bar_count": 1,
              "composition_relations_verified": True}
    # Connecting maps tensor by the signed derivation rule. This sample
    # uses two rank-one maps on a three-dimensional graded space.
    delta = sp.Matrix([[0, 0, 0], [0, 0, 0], [0, 1, 0]])
    sign = sp.diag(1, 1, -1)  # homological degrees 0,2,3
    delta_sum = sp.kronecker_product(delta, sp.eye(3)) + sp.kronecker_product(sign, delta)
    require(delta_sum.rank() == 4)
    return {"bockstein": bockstein, "skein_obstruction": skein,
            "turner_staircase": staircase, "cycle_incidence": incidence,
            "module_lemma": module,
            "tensor_connecting_map": {"factor_rank": 1, "sum_rank": 4}}


def main():
    knots = {}
    # 1 crossing is the unknot, 3 is the trefoil, 5 the cinquefoil.
    for n, expected in [(1, (2, 2, 1, 1)), (3, (4, 6, 3, 3)), (5, (6, 10, 5, 5))]:
        unred, red = cube(n, False), cube(n, True)
        require((unred["Q"], unred["F2"], red["Q"], red["F2"]) == expected)
        tau = (unred["F2"] - unred["Q"]) // 2
        red_tau = (red["F2"] - red["Q"]) // 2
        rho = red["Q"] - unred["Q"] // 2
        require(tau == 2 * red_tau + rho)
        knots[f"T(2,{n})"] = {"unreduced": unred, "reduced": red,
                                "tau2": tau, "reduced_tau2": red_tau,
                                "connecting_rank_from_exact_sequence": rho}
    result = {"status": "all explicit checks passed", "sympy_version": sp.__version__,
              "knots": knots, "algebra": algebra_checks(),
              "scope": "Small exact examples and abstract obstruction checks; no universal proof."}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

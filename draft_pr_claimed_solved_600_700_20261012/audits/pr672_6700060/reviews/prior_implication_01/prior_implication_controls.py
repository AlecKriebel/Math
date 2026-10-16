"""Independent exact finite checks for the stated reduction; no PDE certificate."""
import json
import sympy as s


def run():
    results = []

    def check(name, predicate):
        if not bool(predicate):
            raise RuntimeError(name)
        results.append(name)

    # Four side facets meet at one nonsimple vertex of the square pyramid
    # |x| <= z, |y| <= z, 0 <= z <= 1. The inequality z>=0 is redundant.
    normals = [s.Matrix(v) for v in [(1, 0, -1), (-1, 0, -1),
                                    (0, 1, -1), (0, -1, -1), (0, 0, 1)]]
    check("nonsimple_apex_four_incident_facets_rank_three",
          s.Matrix.hstack(*normals[:4]).rank() == 3)
    import itertools
    for I in itertools.combinations(range(4), 3):
        check("apex_triple_rank_" + str(I),
              s.Matrix.hstack(*(normals[i] for i in I)).rank() == 3)
    # Positive and negative orientation; neither changes the outward side.
    L0 = s.Matrix([[1, s.Rational(1, 3), 0],
                   [0, 2, s.Rational(1, 4)], [0, 0, s.Rational(3, 2)]])
    for tag, L in [("positive", L0), ("negative", s.diag(-1, 1, 1) * L0)]:
        G = L.T * L
        Gi = G.inv()
        check(tag + "_invertible", L.det() != 0)
        for k in range(1, 4):
            check(tag + "_positive_definite_minor_" + str(k), G[:k, :k].det() > 0)
        ng, nt = [], []
        for i, a in enumerate(normals):
            q = s.sqrt((a.T * Gi * a)[0])
            ng.append(Gi * a / q)
            nt.append(L.inv().T * a / q)
            check(tag + "_outward_normal_pushforward_" + str(i),
                  (L * ng[-1] - nt[-1]).applyfunc(s.simplify) == s.zeros(3, 1))
            check(tag + "_unit_normal_" + str(i),
                  s.simplify((ng[-1].T * G * ng[-1])[0] - 1) == 0)
        # Includes opposite side facets meeting only at the apex: the
        # source conclusion, unlike its ridge hypotheses, includes them.
        for i, j in itertools.combinations(range(5), 2):
            check(tag + "_gram_preservation_" + str((i, j)),
                  s.simplify((ng[i].T * G * ng[j])[0]
                             - (nt[i].T * nt[j])[0]) == 0)
    check("interior_exterior_strict_direction",
          s.pi - s.pi / 3 > s.pi - s.pi / 2)
    check("normal_cosine_strict_direction",
          s.cos(2 * s.pi / 3) < s.cos(s.pi / 2))
    # Losing invertibility at a corner destroys the positive-definite
    # neighborhood metric; this is an excluded map, not a counterexample.
    x = s.symbols("x", real=True)
    bad = s.diag(3 * x**2, 1)
    check("degenerate_corner_pullback", (bad.T * bad).det().subs(x, 0) == 0)
    check("interior_map_nonsingular", (bad.T * bad).det().subs(x, 1) > 0)
    # Exact nonnegative planar defect patterns. The sum relation forbids
    # even a single strict deficit, without requiring all angles strict.
    patterns = list(itertools.product([s.Rational(0), s.Rational(1, 9)], repeat=4))
    for i, ds in enumerate(patterns):
        for K in [s.Rational(0), s.Rational(1, 7)]:
            check("planar_zero_defect_" + str((i, K)),
                  (sum(ds) + K == 0) == (all(d == 0 for d in ds) and K == 0))
    return {"schema": "pr672-independent-prior-reduction-controls-v1",
            "status": "PASS", "count": len(results), "checks": results,
            "limits": "Finite algebra/convention diagnostics only; not an analytic theorem, priority exhaustiveness, or corner regularization certificate."}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))

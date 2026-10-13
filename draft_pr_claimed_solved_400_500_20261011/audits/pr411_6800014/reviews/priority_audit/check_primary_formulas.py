"""Exact primary-formula consistency checks; Python standard library only.
Ring: Q[t,r]/(r^2-1-t^2), with r = sqrt(1+t^2).
Independent Koszul curvature is computed directly from structure constants.
No author checker or parent calculation is imported.
"""
from fractions import Fraction as F
import json
from pathlib import Path
from datetime import datetime, timezone

def poly(x=0):
    return {(0, 0): F(x)} if x else {}
def add(*args):
    d = {}
    for p in args:
        for k, v in p.items():
            d[k] = d.get(k, F(0)) + v
    return {k: v for k, v in d.items() if v}
def neg(p):
    return {k: -v for k, v in p.items()}
def mul(p, q):
    d = {}
    for (i, j), v in p.items():
        for (k, l), w in q.items():
            # Each factor has r-degree 0 or 1; reduce r^2 = 1+t^2.
            a, b = i+k, j+l
            terms = [(a, b)] if b < 2 else [(a, 0), (a+2, 0)]
            for z in terms:
                d[z] = d.get(z, F(0)) + v*w
    return {k: v for k, v in d.items() if v}
def scale(p, x):
    return mul(p, poly(x))
def transpose(a):
    return [list(x) for x in zip(*a)]
def mm(a, b):
    return [[add(*(mul(a[i][k], b[k][j]) for k in range(len(b))))
             for j in range(len(b[0]))] for i in range(len(a))]
def ma(a, b):
    return [[add(x, y) for x, y in zip(ar, br)] for ar, br in zip(a, b)]
def mn(a):
    return [[neg(x) for x in row] for row in a]
def norm2(a):
    return add(*(mul(x, x) for row in a for x in row))
def fmt(p):
    return {f"t^{i} r^{j}": str(v) for (i, j), v in sorted(p.items())}
def eval_rfree(p, t):
    assert all(j == 0 for i, j in p)
    return sum((v*F(t)**i for (i, j), v in p.items()), F(0))
T = {(1, 0): F(1)}
R = {(0, 1): F(1)}
Z = {}
E = [[T, neg(R), Z, Z], [R, neg(T), Z, Z],
     [Z, Z, Z, T], [Z, Z, Z, Z]]
D = [[Z, poly(-1), Z, Z], [poly(1), Z, Z, Z],
     [Z, Z, Z, T], [Z, Z, Z, Z]]

def koszul(a):
    n = len(a)+1
    c = [[[{} for k in range(n)] for j in range(n)] for i in range(n)]
    for i in range(1, n):
        for k in range(1, n):
            c[0][i][k] = a[k-1][i-1]
            c[i][0][k] = neg(c[0][i][k])
    g = [[[scale(add(c[i][j][k], neg(c[j][k][i]), c[k][i][j]), F(1, 2))
           for k in range(n)] for j in range(n)] for i in range(n)]
    ric = [[add(*(add(mul(g[i][j][k], g[a0][k][a0]),
                          neg(mul(g[a0][j][k], g[i][k][a0])),
                          neg(mul(c[a0][i][k], g[k][j][a0])))
                       for a0 in range(n) for k in range(n)))
            for j in range(n)] for i in range(n)]
    return ric

results = {}
for name, a in [("D_t", D), ("E_t", E)]:
    at = transpose(a)
    sym = [[scale(x, F(1, 2)) for x in row] for row in ma(a, at)]
    s = norm2(sym)
    comm = ma(mm(a, at), mn(mm(at, a)))
    q = norm2(comm)
    ric = koszul(a)
    scal = add(*(ric[i][i] for i in range(5)))
    ricnorm = norm2(ric)
    assert scal == neg(s)
    assert ricnorm == add(mul(s, s), scale(q, F(1, 4)))
    vals = {str(t): str(eval_rfree(mul(scal, scal), t)/eval_rfree(ricnorm, t))
            for t in [1, 2]}
    results[name] = {"s": fmt(s), "commutator_norm_squared": fmt(q),
                     "koszul_scalar": fmt(scal), "koszul_ricci_norm_squared": fmt(ricnorm),
                     "F_at_t": vals}
assert results["D_t"]["F_at_t"] == {"1": "1/3", "2": "1/3"}
assert results["E_t"]["F_at_t"] == {"1": "25/91", "2": "25/67"}
assert norm2(ma(mm(E, transpose(E)), mn(mm(transpose(E), E)))) == {
    (2, 0): F(32), (4, 0): F(34)}
D1 = [[Z, poly(-1), Z, Z], [poly(1), Z, Z, Z],
      [Z, Z, Z, poly(1)], [Z, Z, Z, Z]]
Ht = [[poly(1), T, Z, Z], [Z, R, Z, Z],
      [Z, Z, T, Z], [Z, Z, Z, poly(1)]]
assert mm(Ht, D1) == mm(E, Ht)
results['E_t_conjugacy'] = {
    'identity_checked': 'H_t D_1 = E_t H_t',
    'H_t': 'diag([[1,t],[0,sqrt(1+t^2)]],diag(t,1))',
    'det_H_t': 't sqrt(1+t^2)>0 for t>0',
    'D_u_to_D_1': 'diag(1,1,1/u,1) D_u diag(1,1,u,1) = D_1',
    'scope': 'Same-group comparison is independently checked; E_2=25/67>1/3'
}
results["E_t_printed_formula"] = {
    "source": "Lauret-Will I arXiv 1808.01380v2 section 6.4 printed p20",
    "printed": "4 t^4/(3 t^4+2 t^2)",
    "actual_from_displayed_matrix": "25 t^4/(59 t^4+32 t^2)",
    "printed_at_1": "4/5", "actual_at_1": "25/91",
    "consistent": False,
    "independent_crosscheck": "Koszul curvature and almost-abelian formula agree",
    "scope_effect": "Does not affect D_t=J direct-sum tE12; no E1=4/5 priority claim"
}
results["utc"] = datetime.now(timezone.utc).isoformat()
out = Path(__file__).resolve().parent / "PRIMARY_FORMULA_CONSISTENCY.json"
out.write_text(json.dumps(results, indent=2)+"\n")
print(json.dumps(results, indent=2))

"""Exact finite controls for the authored algebra; not topological certification."""
from fractions import Fraction as F
from itertools import product
import json

counts = {}
def check(name, condition):
    if not condition:
        raise RuntimeError('Failed control: ' + name)
    counts[name] = counts.get(name, 0) + 1

for r in range(1, 6):
    for nums in product(range(0, 5), repeat=r):
        gs = [F(x, 3) for x in nums]
        G = sum(gs)
        sq = sum(g*g for g in gs)
        B = max(gs)
        check('sum_square_refinement', sq <= B*G <= G*G)
        if G:
            ratios = [F(i+1, 2) for i in range(r)]
            ws = sum(g*z for g,z in zip(gs,ratios))/G
            check('weighted_average', ws <= max(ratios))
        else:
            check('zero_piece_norms', sq == 0 and B == 0)

for n in range(1, 4001):
    q = F(2, 3*n)
    delta = (1-q)**3 - F(n-1,n)**2
    check('long_slope_identity', delta == F(9*n-8,27*n**3))
    check('long_slope_positive', delta > 0)
    check('improved_cutoff_squared', F(3*n,2) < 2*n)
    for den in (2,3,7):
        qq = q/F(den)
        check('longer_slope_monotonicity', (1-qq)**3 >= (1-q)**3)

for k in range(1, 31):
    C = F(k*k)
    for t in range(1, 101):
        G=F(t,k)
        A=F(k+1,7)
        D=F(t+1,5)
        check('affine_absorption', A*G+D <= (A+D*k)*G)
        check('gap_squared', C*G*G >= 1)

for m in range(1, 4001):
    G=F(m); s=m*m; Q=F(m)
    check('quantum_nonimplication_model', Q<=s and Q<=G and G<=s<=G*G)
    check('ratio_model', F(s,m)==m)

out={'schema':1,'status':'pass','total_checks':sum(counts.values()),'checks':counts,
     'scope':'exact finite algebra only; no topological realization or full conjecture proof'}
print(json.dumps(out,sort_keys=True,indent=2))

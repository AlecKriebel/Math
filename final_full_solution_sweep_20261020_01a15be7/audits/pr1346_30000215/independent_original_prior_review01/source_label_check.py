"""Exact check of a D/D-prime labeling slip on printed Székely p.35.

This is our diagnostic, not a claim of an author-issued erratum.
Two disjoint edges admit a zero-crossing and a one-crossing normal drawing.
"""
import json
from fractions import Fraction as F


def require(x, msg):
    if not x:
        raise RuntimeError(msg)


rows = []
for c in [0,1]:
    # O_C=0, so c=(1+Q)/2. Ordered-pair weighted sum W=-Q.
    Q = 2*c-1
    W = -Q
    require(F(1,2)-F(1,2)*W == c,"published equation9")
    criterion = all((c^p)>=c for p in [0,1])
    require(criterion == (c==0),"exact criterion on two disjoint edges")
    rows.append({"crossing_bit":c,"Q":Q,"ordered_weighted_sum":W,
                 "criterion_holds":criterion})
D,Dprime = rows
require(Dprime["ordered_weighted_sum"] <= D["ordered_weighted_sum"],"printed10<=11")
require(D["criterion_holds"] and not Dprime["criterion_holds"],"which drawing is optimal")
print(json.dumps({"status":"PASS","rows":rows,
                  "interpretation":"Equation10<=11 compares D-prime to the optimal baseline D; it expresses optimality of D against D-prime, not optimality of D-prime. The theorem statement and direct c XOR p criterion are unaffected.",
                  "author_erratum_authenticated":False},indent=2))

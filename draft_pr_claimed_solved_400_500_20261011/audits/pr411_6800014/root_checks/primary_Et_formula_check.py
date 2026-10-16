#!/usr/bin/env python3
"""Direct exact Koszul check of the primary paper's displayed E_t matrix.

The printed F expression is not assumed. This reuses only the root's own
standard-library Fraction curvature implementation, not author or peer code.
"""
from pathlib import Path
from fractions import Fraction as F
import contextlib, io, json, runpy
with contextlib.redirect_stdout(io.StringIO()):
    own = runpy.run_path(str(Path(__file__).with_name("exact_boundary_koszul.py")))
mat, functional, require = (own[x] for x in ("mat", "functional", "require"))
rows = []
for t, k in [(F(3,4),F(5,4)),(F(4,3),F(5,3)),(F(15,8),F(17,8))]:
    require(k*k == 1+t*t, "positive Pythagorean relation")
    E = mat([[t,-k,0,0],[k,-t,0,0],[0,0,0,t],[0,0,0,0]])
    s = own["n2"](own["sym"](E))
    q = own["n2"](own["comm"](E,own["tr"](E)))
    value = functional(E)
    derived = 25*t**4/(59*t**4+32*t*t)
    printed = 4*t**4/(3*t**4+2*t*t)
    require(s == F(5,2)*t*t and q == 32*t*t+34*t**4, "displayed-matrix invariants")
    require(value == derived and value != printed, "direct curvature versus printed expression")
    u = F(1,4)
    H = mat([[1,t,0,0],[0,k,0,0],[0,0,t/u,0],[0,0,0,1]])
    Hi = mat([[1,-t/k,0,0],[0,1/k,0,0],[0,0,u/t,0],[0,0,0,1]])
    require(own["mul"](H,Hi) == own["eye"](4), "same-group conjugator inverse")
    require(own["mul"](own["mul"](H,own["au"](u)),Hi) == E, "same-group displayed E_t")
    rows.append({"t":str(t),"k":str(k),"tr_S_squared":str(s),"commutator_squared_norm":str(q),"direct_F":str(value),"printed_F":str(printed),"printed_expression_matches":False,"same_group_conjugacy_verified":True,"greater_than_one_third":value>F(1,3)})
print(json.dumps({"result":"PASS","source":"Lauret–Will1808.01380v2, section6.4 printedp20; matrix and printed expression visually checked against private PDF","derived_displayed_matrix_F":"25 t^4/(59 t^4+32 t^2)","printed_expression":"4 t^4/(3 t^4+2 t^2)","deduction":"The displayed matrix is a same-group comparison; F>1/3 when t^2>2. The paper's displayed F expression is inconsistent with that matrix. Its limit as t tends to0 remains0 under the corrected expression.","arithmetic":"stdlib exact Fraction, independent direct Koszul curvature","rows":rows,"priority_limit":"This checks a prior displayed family and its value; it does not establish a prior local-maximum proof or firstness."},indent=2))

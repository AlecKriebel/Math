#!/usr/bin/env python3
"""Finite floating spectral-gap regression, not a nonlinear stability proof."""

if not __debug__:
    raise SystemExit(
        "Exact verifier requires assertions; unset PYTHONOPTIMIZE and do not use python -O"
    )

import numpy as np
from core import Avec, selected
from pareto_core import A as PA, Deff, Hlist, L0, L1

for m in (3,4,5,6,8,10):
    A=np.array(Avec(m),float); d=selected(m)[1]; D=np.diag([float(x) for x in d])
    vals=np.linalg.eigvals(A-D)
    assert max(z.real for z in vals if abs(z)>1e-7)<0
    for k in (2,3,5): assert max(np.linalg.eigvals(A-k*k*D).real)<0
    for L in (L0(m),(L0(m)+L1(m))/2,L1(m)):
        H=np.diag([float(x) for x in Hlist(m,L)])
        M=H@(np.array(PA(m),float)-np.diag([float(x) for x in Deff(m)]))
        vals=np.linalg.eigvals(M)
        assert max(z.real for z in vals if abs(z)>1e-7)<0
print("BRANCH_STABILITY_REGRESSION_PASS")

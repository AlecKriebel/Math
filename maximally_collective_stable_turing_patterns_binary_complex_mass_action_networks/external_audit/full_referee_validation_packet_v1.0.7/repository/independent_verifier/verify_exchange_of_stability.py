#!/usr/bin/env python3
"""Exact sign checks plus finite spectral regressions for exchange of stability."""
import sympy as sp
import numpy as np
from core import Avec, selected, Hsum, ellr_formula, ellDr_formula, N_formula

for m in (3,4,5,6,8,10):
    A = Avec(m)
    r,d,ell = selected(m)
    D = sp.diag(*d)
    Hs = Hsum(m)
    assert ellr_formula(m,Hs) < 0
    assert ellDr_formula(m,Hs) < 0
    assert N_formula(m,Hs) > 0
    vals = np.linalg.eigvals(np.array(A-D,dtype=float))
    noncritical=[z for z in vals if abs(z)>1e-7]
    assert max(z.real for z in noncritical) < -1e-8
    for k in (2,3,5):
        assert max(np.linalg.eigvals(np.array(A-k*k*D,dtype=float)).real) < -1e-8
print("EXCHANGE_OF_STABILITY_PASS")

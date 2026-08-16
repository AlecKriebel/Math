#!/usr/bin/env python3
"""Independent exact check of the complete positive-realization parametrization."""
import sympy as sp
from stable_core import gamma_y, flux, A_matrix

for m in (3, 4, 5, 6, 8, 10):
    G, Y = gamma_y(m)
    assert G.rank() == m
    assert len(G.nullspace()) == 2
    a, b = sp.symbols("a b", positive=True)
    v = flux(m, a, b)
    assert G * v == sp.zeros(m + 1, 1)
    assert A_matrix(m, a, b) == G * sp.diag(*list(v)) * Y.T
print("REALIZATION_SPACE_PASS")

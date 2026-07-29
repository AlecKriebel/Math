#!/usr/bin/env python3
"""Exact cyclotomic audit of the tensor-product extension lemma."""

from __future__ import annotations

import sympy as sp


q = (1 + sp.I * sp.sqrt(3)) / 2
spectrum = (-sp.Integer(1), q)

# A multiplier stabilizing the two-element spectrum must send -1 to one
# of its two elements.  These are the only two candidates.
candidates = (sp.Integer(1), -q)
stabilizers = tuple(
    multiplier
    for multiplier in candidates
    if {
        sp.simplify(multiplier * eigenvalue)
        for eigenvalue in spectrum
    }
    == set(spectrum)
)

assert stabilizers == (sp.Integer(1),)
assert sp.simplify((-q) * q - sp.conjugate(q)) == 0
assert sp.conjugate(q) not in set(spectrum)

print("PASS the multiplicative stabilizer of {-1, exp(i*pi/3)} is {1}")
print("PASS tensor-product preservation forces a spectator identity")

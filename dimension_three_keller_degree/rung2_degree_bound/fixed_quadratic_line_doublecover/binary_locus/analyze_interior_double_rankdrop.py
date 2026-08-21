#!/usr/bin/env python3
"""Targeted elimination for residual interior doubled-fixed contact minors."""

from __future__ import annotations

import sympy as sp

A, w = sp.symbols("A w")

Q1 = (
    108 * A**3 * w**5
    - 266 * A**3 * w**3
    + 216 * A**2 * w**6
    - 855 * A**2 * w**4
    + 165 * A**2 * w**2
    + 108 * A * w**7
    - 972 * A * w**5
    + 450 * A * w**3
    - 60 * A * w
    - 378 * w**6
    + 270 * w**4
    - 45 * w**2
    - 5
)
Q2 = (
    127 * A**3 * w**4
    - 285 * A**3 * w**2
    + 294 * A**2 * w**5
    - 954 * A**2 * w**3
    + 186 * A**2 * w
    + 162 * A * w**6
    - 978 * A * w**4
    + 357 * A * w**2
    - 15 * A
    - 324 * w**5
    + 186 * w**3
    - 20 * w
)
Q3 = (
    20 * A**3 * w**5
    - 186 * A**3 * w**3
    + 324 * A**3 * w
    + 15 * A**2 * w**6
    - 357 * A**2 * w**4
    + 978 * A**2 * w**2
    - 162 * A**2
    - 186 * A * w**5
    + 954 * A * w**3
    - 294 * A * w
    + 285 * w**4
    - 127 * w**2
)
Q4 = (
    5 * A**3 * w**7
    + 45 * A**3 * w**5
    - 270 * A**3 * w**3
    + 378 * A**3 * w
    + 60 * A**2 * w**6
    - 450 * A**2 * w**4
    + 972 * A**2 * w**2
    - 108 * A**2
    - 165 * A * w**5
    + 855 * A * w**3
    - 216 * A * w
    + 266 * w**4
    - 108 * w**2
)

resultants = []
for label, left, right in (
    ("12", Q1, Q2),
    ("13", Q1, Q3),
    ("14", Q1, Q4),
    ("23", Q2, Q3),
):
    value = sp.factor(sp.resultant(left, right, A))
    resultants.append(value)
    print("resultant", label, value)

candidate = sp.factor(sp.gcd_list(resultants))
print("candidate gcd", candidate)

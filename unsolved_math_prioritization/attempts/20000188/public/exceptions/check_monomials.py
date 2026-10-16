#!/usr/bin/env python3
"""Finite exact check of monomial counts/witnesses; no external dependencies."""
from math import comb
from pathlib import Path
import json

count = 0
for n in range(1, 13):
    for m1 in range(n):
        for m2 in range(n):
            if m1 + m2 > n:
                continue
            monomials = {
                (i, j, n - i - j)
                for i in range(n + 1)
                for j in range(n - i + 1)
                if n - i >= m1 and n - j >= m2
            }
            expected = comb(n + 2, 2) - comb(m1 + 1, 2) - comb(m2 + 1, 2)
            assert len(monomials) == expected, (n, m1, m2)
            for witness in [(0, 0, n), (1, 0, n - 1), (0, 1, n - 1),
                            (n - m1, m1, 0), (m2, n - m2, 0)]:
                assert witness in monomials, (n, m1, m2, witness)
            count += 1
result = {
    "description": "Exact combinatorial verification of plane linear-system dimension and all witness monomials for degrees 1 through 12. This checks finite combinatorics, not the general Bertini theorem.",
    "count": count,
    "all_passed": True,
    "maximum_degree": 12,
}
out = Path(__file__).with_name("FINITE_MONOMIAL_CHECK.json")
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result))

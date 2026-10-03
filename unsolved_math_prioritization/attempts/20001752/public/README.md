# E8 and Leech midpoint Mellin values

Problem 20001752 / AIM-GEOMETRY-0090; queue rank 513.

## Result

A complete proof of the **8-dimensional subproblem** is given in `PROOF.md`:
\[
M_{f_8}(4)=M_{\widehat f_8}(4)=1/15.
\]
It uses an explicit quasimodular summation identity and the published exact
zero, derivative, and Taylor data of Viazovska's function. The summation
identity is proved for all radial Schwartz functions, rather than inferred
from numerical tests.

The **24-dimensional midpoint evaluation remains unresolved in this work**.
The automatic equality of the Fourier-paired moments holds, and a separate
weighted-tail functional is evaluated exactly as 20/91. That auxiliary
functional is not the requested midpoint moment. A real modular-integral
representation reproduces the primary-source numerical value
0.1778609647296502766..., without identifying a simpler exact constant.

The combined disposition is **partial progress**, not a complete solution.
The E8 argument is an independent derivation; priority or novelty is not
asserted. A bounded literature search did not locate this evaluation, which
is not proof that it has never appeared elsewhere.

## Files

- `PROOF.md`: full proofs, exact hypotheses, normalizations, and limitations
- `SOURCE_GATE.md`: original target recovery and primary-source checks
- `RESEARCH_LOG.md`: five substantive approaches and their outcomes
- `check_exact.py`, `exact_results.json`: exact symbolic checks and diagnostic Gaussian/Laguerre tests
- `check_periods.py`, `period_numerics.json`: non-interval diagnostic quadrature, not numerical certification
- `FROZEN_AUTHOR_MANIFEST.json`: hashes of this pre-audit author packet

To reproduce the checks, run `python check_exact.py` (SymPy and mpmath) and
`python check_periods.py` (mpmath). The latter reports approximate values
without rigorous error enclosures.

The author packet requires an independent audit before publication. Neither
source PDFs nor full source texts are part of the public deliverable.

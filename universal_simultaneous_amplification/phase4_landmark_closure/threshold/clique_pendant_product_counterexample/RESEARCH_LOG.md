# Research log

## 2026-08-08 — initial discovery exactified

- Started from the numerical endpoint candidate consisting of a 33-vertex
  clique and four leaves sharing one clique hub (`c=32,m=4,n=37`).
- Derived the six type-changing aggregate rates for each update rule directly
  from the replacement definitions and proved `S_32 x S_4` strong lumpability.
- Solved both 328-state transient systems over `QQ` at `r=3/2`.
- Verified all harmonic residuals with standard-library rational arithmetic.
- Rebuilt all transition rows independently from labelled replacement events
  and reproduced both fixation fractions through SymPy's exact matrix solver.
- Certified normalized ratios
  `x=1.119453111802425...` (Bd) and `y=0.894830996796498...` (dB), with
  `xy=1.001721343901106...>1` by a positive 1737-digit exact numerator.
- Also certified `(x+y)/2=1.007142054299462...>1`; the exact fixed-weight
  arithmetic crossing is `lambda_0=(1-y)/(x-y)=0.468204135646781...`.
- Logical status: **PROVED** counterexample to the endpoint product inequality
  and to the balanced arithmetic separator.  **NOT** a simultaneous amplifier;
  the universal disjunctive endpoint problem and the value of `R_sim` remain
  **OPEN**.

## 2026-08-08 — smaller hostile-audit witness adopted

- An independent family scan found `c=31,m=4,n=36`, one vertex smaller than
  the initial witness, and exactified it independently.
- Replaced the central certificate by this 32-clique-plus-four-leaves graph.
  Its exact normalized values are
  `x=1.121822899272823...`, `y=0.892002982408856...`,
  `xy=1.000669371885908...`, and `(x+y)/2=1.006912940840840...`.
- The arithmetic crossing is
  `lambda_0=0.469920183876267...`.  The original `n=37` graph remains in the
  transition regression suite as an independent nearby witness.
- The sibling hostile-audit package certifies that `n=36` is minimal **within
  this unweighted two-parameter clique--pendant family**.  No claim of
  minimality among all weighted graphs is made here.

# Research log: exact Eliahou ternary CP diagnostic

All times are PDT on 25 July 2026.

## Exact encoding audit

- Encoded long case 1 with 78 ternary coordinates, represented by 156
  mutually exclusive endpoint Booleans.
- Shared every distinct Boolean conjunction across all equations.  The
  resulting model has 5,928 conjunction variables, 6,085 total proto
  variables, and 17,949 proto constraints.
- Audited the source ternary polynomials, Boolean expansions, and direct
  physical correlations on 24 deterministic assignments.  All 4,080 scalar
  comparisons passed.
- Retained the exact shell, four root equations, 20 anti-fold equations,
  21 plus-fold equations, and 41 causal correlations.  Lag 83 is recorded
  but tautological in this case.

## Bounded solver diagnostic

- Profile 0 remained `UNKNOWN` after 300.03 seconds with four workers,
  51,133 branches, 2,891 conflicts, and 277.13 MB peak RSS.
- Profile 1 was deliberately interrupted after 62.68 seconds once the gate
  had failed.  It returned the normal `UNKNOWN` status after 1,788,048
  branches and 649,592 conflicts, with 321.83 MB peak RSS.
- No model, exclusion, Legendre pair, base sequence, or `H(668)` is claimed.
- A proof-capable pseudo-Boolean encoding is mechanically available, but
  the observed propagation gives no evidence that a raw certified proof
  search is tractable.  Further work needs a mathematical contraction.

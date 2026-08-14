# Research log

All times are America/Los_Angeles.

## 2026-08-13 18:05 PDT

- Began a proof-first audit of the exact multitype geometric
  Galton--Watson interpretation of the dB survival and Bd extinction
  endpoints.
- No graph or kernel search was used.

## 2026-08-13 18:18 PDT

- Derived the complete finite rooted plane-tree weights for both endpoint
  processes.
- Rewrote the diffuse support inequality as the difference between the two
  supercritical finite-tree masses and the critical `r=1` dB tree
  probability, whose total mass is exactly one.

## 2026-08-13 18:25 PDT

- Derived exact adjacent-reroot ratios.  Rerooting changes only a local root
  factor; the degree-dependent unrooted core survives.
- Identified a symbolic deterministic two-type family and a typed star
  sequence that tests the entire rerooting class without enumerating any
  kernels or trees.

## 2026-08-13 18:31 PDT

- Proved the decisive obstruction.  On `d`-leaf stars, both available target
  weights divided by the critical source weight decay exponentially for
  `k>1`.  The supplied normalization identity gives the strict contraction
  factor exactly.  Summing all `O(d)` rerootings cannot compensate.
- Reported the formulas and scope to the primary agent before preparing a
  commit.

## 2026-08-13 18:42 PDT

- Recorded the separate endpoint obstruction: the canonical positive
  expansion of `1/(1+rcRq)` contains Bd-survival configurations; replacing
  them by the finite extinction-tree series makes the expansion signed.
- Packaged the theorem, exact symbolic replay, and scope.  The result closes
  only pure rerooting/in-class mass transport, not nonlocal tree transforms
  or infinite-spine couplings.

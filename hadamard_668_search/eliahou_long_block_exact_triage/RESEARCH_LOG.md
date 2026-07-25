# Research log: Eliahou long-block exact triage

## 24 July 2026

- Opened a dedicated bounded audit for canonical long cases 2--20, later
  extending the accounting to still-open canonical case 1 (`L2`).
- Corrected an indexing ambiguity: the 79-variable boundary case is
  canonical case 0 (`L0`), already proof-certified UNSAT; open `L2` has 78
  variables.
- Derived every characteristic-two syndrome quotient.  Seventeen ordinary
  cases have 59 classes and dimension 38; case 6 has 58/dimension 37;
  cases 1 and 14 have 57/dimension 36.
- Proved that the nineteen nontrivial-class parities have full projection
  rank in every quotient.
- Classified the conditioned mod-3 interaction graphs as two cliques with
  zero, one, or two universal mixed-triple separator vertices.  Worst
  treewidth is 18 in every family.
- Exhausted all support-domain-preserving blockwise dihedral maps and found
  no nontrivial exact polynomial symmetry.  The short-case reflection gauge
  is unavailable.
- Computed every exact weight-39 mod-2 support count by a complete
  MacWilliams dual character sum.
- Derived rigorous component-row lower bounds and gross all-quotient work
  counts.  No case passes the two-hour gate.
- Audited the exact global long/short split.  All open long cases use 19
  distinct arithmetic block specifications and `19*2^39` raw block states.
  Minimal materialized table sizes are multi-terabyte.
- Found the new exact 2-adic structure: after fixing the mod-2 quotient,
  ordinary orientation variables do not interact in the mod-4 lift.
  Conditioned treewidth is 0, 1, or 2.
- Built an orientation-aware 57-coordinate parameterization and proved that
  the twenty next-digit equations are quadratic Boolean forms.  Their
  outer-only quadratic coefficient span has rank 20 and their outer graph
  is nearly complete.
- Implemented a bit-packed exact quadratic-Walsh engine.  Completed all
  `2^20` pencil combinations for each of the twenty open cases in 46.95 s
  wall time at 143 MB maximum RSS for the original full run.
- The exact odd-weight mod-4 common-zero counts range from
  `137,273,561,088` to `137,458,540,544`, essentially `2^37`.  Frozen full
  rank histograms show minimum nonzero polar rank 20--24 and no low-rank
  contraction.
- Verified the characteristic-seven Hasse ranks
  `3,6,9,12,15,18,20`, the three `F49` local factors, and the unrestricted
  count `336*117600*7^54`.  This is a repackaging, not a new Boolean
  contraction.
- Proved that mod 3+4+7 is exact because normalized residuals have absolute
  value at most 83.  A bounded 10,000-conflict comparison on cases
  1,2,6,14 found all modular and PB runs UNKNOWN; the naive CRT automata do
  not improve bounded solver time.
- Exhibited a nonzero CRT-42 residual pattern with everywhere nonnegative
  spectrum, ruling out a positivity-only closure of the mod-42 gap.
- Wrote detached replay tooling and frozen semantic certificates.
- No external communication, commit, push, or production support search was
  performed.

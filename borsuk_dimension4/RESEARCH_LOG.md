# Research Log

## 2026-08-01T15:24:03-07:00 — Program initialization

- Restated the finite counterexample target as an exact diameter graph in
  \(\mathbb R^4\) with chromatic number at least six.
- Established the discovery embargo on Borsuk-specific literature and
  catalogues. General-purpose mathematics and exact computational tools remain
  allowed.
- The original checkout was on an unrelated branch with uncommitted parallel
  work, and another dirty worktree held `main`. To preserve both, initialized a
  sparse standalone checkout at `/Users/alec/Documents/Math-borsuk4`, tracking
  `origin/main`, with all new work under `borsuk_dimension4/`.
- Hardware baseline: Apple M1 Pro, 10 CPU cores, 16 GB RAM, about 23 GB free
  disk. Initial system Python has no scientific packages; the existing project
  virtual environment supplies NumPy 2.0.2, SciPy 1.13.1, and SymPy 1.14.0.
- Began three parallel tracks: symmetric exact configurations, graph-first
  low-rank diameter realizations, and structural five-partition lemmas.

Best-guess completion toward a full resolution: **0.5%**. This is an honest
uncertainty estimate for a potentially open research problem, not a schedule.

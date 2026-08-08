# Research log: rank-weighted posterior reflection

## 2026-08-08 -- sharp rank envelope and active variance transport

- Recast the posterior collision at a state `B` by setting
  `x_v=1+e_v(B)`.  The constraints become `x_v>=1` and `sum x_v=n`.
- Proved the sharp arithmetic--harmonic inequality
  `J(B)<=n*c_(n,k)*G(B)`, including its exact two regimes and one-outlier
  extremizers.
- Isolated the single sufficient finite-baseline stationary inequality
  `E[cG]<=m_K-E|B|`.  It passed the exact deterministic corpus and broader
  floating screens, but remains open.
- Derived the Hilbert variational identity for `EJ` and exactly falsified
  target-centered Cayley contraction on `P3` and regular weighted `K4`.
- Derived `G/n` as the conditional law-of-total-variance gain from observing
  the target after observing the stationary output.
- Introduced the deleted source `D=A\{V}` and decomposed the weighted slack
  into a static Boolean term plus an active-channel Brier-risk loss.  The
  static term is exactly negative on `P3`, `K_(2,2)`, and the regular weighted
  `K4`; the active term compensates it.
- Converted the active Brier loss to an exact one-sample Cayley drift using
  `sigma-nu=(sigma+nu)(I-A)`.  Aggregate positivity survived the exact
  corpus, but componentwise positivity has an exact four-vertex
  counterexample.
- Expanded the entire weighted slack over original directed edges and paired
  the two orientations using `d_v P_vi=d_i P_iv`.  The resulting undirected
  edge contributions are exactly negative on the light edges of the
  `(1,1,5)` triangle and on four edges of the regular weighted `K4`; 24/54
  exact three-vertex graphs and 544/624 exact four-vertex graphs have a
  negative paired edge.  Reversible pairing therefore requires a global
  Laplacian/transport argument rather than termwise positivity.
- The unweighted four-path has an exactly negative middle-edge contribution,
  so cycle circulation cannot be the missing compensation either; a proof
  must be nonlocal even on trees.
- Exactly falsified both signs in the naive unweighted split with the
  `(1,1,5)` triangle and `K_(2,2)`.  The combined collision target survives
  both witnesses.
- No external search or communication was performed.

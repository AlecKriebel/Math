# Research log

All timestamps use America/Los_Angeles.

## 2026-07-27

- **20:55 PDT — Program opened (5% complete).**
  Created a dedicated worktree and research directory from current public
  `main`. The initial decisive fork is an exact audit of the minimal
  two-setting maximally-entangled-qudit self-test: compute all four ideal
  joint distributions and determine whether any target pair is uniformly
  distributed over \(d^2\) outcomes. In parallel, opened independent audits
  of the one-setting lower bound, the polar-linear permutation obstruction,
  and the proposed \(2\times3\) composition. No new external literature
  search has been performed in the core derivation phase.

- **21:15 PDT — Exact lower bound and binary optimum (18% complete).**
  Strengthened the elementary one-setting argument: if either party has only
  one available input, every complete behavior—not merely every Bell
  score—has a compatible purification in which Eve knows that party's
  output. This gives \(G(AB|E)\geq1/d\). Found and independently audited an
  exact binary \(2\times2\) score with quantum maximum \(3\sqrt3\) whose
  equality relations force all three nontrivial Eve-operator Fourier
  coefficients of the target pair to vanish. Hence \((2,2)\) is exactly
  setting-minimal for \(d=2\).

- **21:23 PDT — Standard two-input qudit fork closed (23% complete).**
  Derived all four ideal Fourier-phase/SATWAP probability tables exactly.
  None is uniform for any \(d\geq2\); the largest cell is
  \([2d^3\sin^2(\pi/(4d))]^{-1}\). Also proved that the naive
  separately-bounded third-setting term, perfectly correlated with either
  Alice basis, has a nonuniform maximizing cross pair for every \(d\geq3\).
  Thus the binary CHSH composition does not generalize through this direct
  SATWAP anchoring route.

- **21:28 PDT — Computational-MUB exposure obstruction (29% complete).**
  Proved an exact classification of all Hermitian operators in the real
  span of the two standard Alice PVM algebras that have a computational
  basis eigenvector.  After subtracting that eigenvalue, every such operator
  is an off-diagonal corner block with symmetric spectrum
  \(\{\pm\sigma_j\}\).  The computational eigenvalue is therefore never
  extremal unless the operator is scalar.  This rules out every
  coefficientwise separately bounded third-setting term that tries to
  expose the common computational MUB basis, not only the original perfect
  correlation term.

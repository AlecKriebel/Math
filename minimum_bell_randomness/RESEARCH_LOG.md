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

- **21:43 PDT — Second cyclic family also appears permutation-blind
  (38% complete).**
  Found an exact candidate extension of the cycle-permutation construction
  to the originating paper's second, SOS-certified family
  \(\mathcal F_d\).  The Fourier transform
  \(C_\ell=\sum_y\omega^{\ell y}B_y\) of every permuted weighted-shift tuple
  is a scalar times an order-\(d\) weighted shift.  Choosing the additional
  Alice observables as the conjugates of those normalized shifts annihilates
  every published SOS factor.  The first two Alice observables reduce
  exactly to the earlier \(A_0,A_1\), so the augmented target table remains
  biased.  Numerical source-convention checks pass for \(d=3,\ldots,12\);
  an independent analytic and exact-arithmetic audit is in progress before
  this claim is accepted.

- **22:03 PDT — Second-family extension accepted (52% complete).**
  An independent derivation identified and checked the phase omitted by a
  modulus-only argument:
  \(q_\ell=\eta^{-\ell(\ell-1+\delta_d)}\).  It gives
  \(C_\ell=d\lambda_\ell D_\ell\) and
  \(D_\ell^d=I\) for every root permutation.  Consequently the conjugate
  \(D_\ell\) observables annihilate every factor in the published SOS, while
  \(A_0\) and \(A_1\) are exactly the earlier weighted-shift target pair.
  The final-two swap therefore attains the second augmented maximum \(d+1\)
  with a nonuniform target distribution for every \(d\ge4\).  The analytic
  source-convention audit and independent matrix checks through \(d=12\)
  passed.  Work now turns to a portable exact \(d=4\) certificate and a
  publication package; this is a strong fallback theorem, not a solution of
  the still-open all-dimensional \(2\times2\) or \(2\times3\) problem.

- **22:14 PDT — One-input baseline strengthened.**
  Replaced the earlier \(G\geq1/d\) flagged-purification argument by the
  exact deterministic-local decomposition of any behavior with one input on
  one wing.  A pure three-party classical-flag realization reproduces the
  complete behavior and lets Eve guess the target pair with probability one.
  This is recorded as a standard locality fact, not as a novelty claim.

- **22:22 PDT — Constant-setting fork closed without a construction.**
  A final independent attack on the SATWAP-plus-third-setting route found no
  valid all-dimensional \(2\times3\) score.  It did produce an exact
  \(d=3\) Gram determinant \(1/81\), proving in a covariant Chu-basis gauge
  that no non-scalar operator from the two Alice PVM spans can even have the
  proposed third-basis vector as an eigenvector.  This corroborates the
  stronger all-dimensional computational-MUB corner-block obstruction in
  the main note.  The odd/even pattern observed through \(d=10\) is logged as
  numerical only.  A different target basis or genuinely coupled SOS remains
  open.

- **23:10 PDT — Structural checkpoint accepted and frozen.**
  Completed the proof manuscript, machine-readable family certificate,
  dependency-free tests for \(d=2,\ldots,6\), and an independently written
  exact \(d=4\) verifier over \(\mathbb Q(\zeta_{16})\).  The exact verifier
  checks the originating second-family coefficients, Fourier selection,
  all order-four relations, every SOS factor, the values \(4\) and \(5\),
  and the nonuniform target table \(1/32,3/32\).  Separate numerical
  regression through \(d=12\), the SATWAP ideal-table audit through \(d=10\),
  source compilation, JSON parsing, and repository whitespace checks all
  pass.  A targeted primary-source audit found no all-dimensional
  \(2\times2\) or \(2\times3\) solution and identified the binary benchmark
  as prior work.  The program therefore closes this phase with a rigorous
  architecture-specific obstruction paper, while explicitly leaving the
  minimum-setting problem open.

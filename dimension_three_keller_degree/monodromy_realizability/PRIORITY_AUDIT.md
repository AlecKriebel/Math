# Priority audit: regular obstruction and low-degree action ledger

**Audit timestamp (UTC):** 2026-07-25T21:02:56Z.

This is source-specific evidence, not a guarantee of worldwide priority.
No person was contacted.

## Classical inputs

- Campbell, *A condition for a polynomial map to be invertible*, Math. Ann.
  205 (1973), 243-248,
  [doi:10.1007/BF01349234](https://doi.org/10.1007/BF01349234), proves the
  complex Galois case.
- Razar, *Polynomial maps with constant Jacobian*, Israel J. Math. 32 (1979),
  97-106,
  [doi:10.1007/BF02764906](https://doi.org/10.1007/BF02764906), gives an
  algebraic treatment.
- Wright, *On the Jacobian conjecture*, Illinois J. Math. 25 (1981), 423-440,
  [doi:10.1215/ijm/1256047158](https://doi.org/10.1215/ijm/1256047158).
  The primary text was inspected at pages 438-439. Under the section-wide
  hypotheses \(k\) of characteristic zero, \(B=k[X_1,\ldots,X_n]\),
  \(A=k[f_1,\ldots,f_n]\), and constant nonzero Jacobian, Theorem 3.7 says
  that \(L/K\) Galois implies \(A=B\). Wright credits Campbell for
  \(k=\mathbb C\), and the following summary theorem states the
  characteristic-zero result.
- The equivalence between a connected cover being Galois and its natural
  monodromy action being regular is standard covering/Galois theory. It is
  stated in the [Stacks Project, Tag
  03SF](https://stacks.math.columbia.edu/tag/03SF) in the simply-transitive
  fibre formulation. Kuiken, *Coverings with singularities*, Canad. J. Math.
  33 (1981), 1141-1150,
  [doi:10.4153/CJM-1981-086-4](https://doi.org/10.4153/CJM-1981-086-4),
  states the monodromy-order/regular-representation criterion explicitly.
- The [official TransGrp
  manual](https://docs.gap-system.org/pkg/transgrp/doc/manual.pdf) documents
  that \(dTj\) labels transitive permutation actions up to conjugacy, and
  attributes the degree-at-most-11 classification to Butler and McKay.

Therefore the regular-action obstruction, the nonabelian corollary, and the
degree \(2\)-\(10\) extraction are classical/routine. No novelty is claimed.

## Monodromy-specific literature search

Searches combined “Keller map,” “constant Jacobian,” “Galois closure,”
“monodromy group,” “regular monodromy,” and “permutation monodromy.”

- Friedland, *Monodromy, differential equations and the Jacobian conjecture*,
  Ann. Polon. Math. 72 (1999), 219-249,
  [doi:10.4064/ap-72-3-219-249](https://doi.org/10.4064/ap-72-3-219-249),
  was inspected because of its title. Its monodromy is principally
  Gauss-Manin/homology monodromy of level curves of a polynomial, not the
  natural finite-sheet permutation monodromy used in this ledger.
- The July 2026
  [MathOverflow discussion](https://mathoverflow.net/questions/513387/)
  states nonnormality of the announced cubic extension and asks whether
  constraints beyond it were known. It already records the classical
  Galois-case attribution and the \(S_3\) computation.
- No older primary source was found that packages the exact sentence
  “Keller counterexample monodromy is nonregular” as a named theorem.
  This negative result is only about the searched and indexed sources; the
  statement is in any event an immediate reformulation of classical results.

## Realization inputs

- The symmetric \(S_d\) entries come from
  `weighted_lift_symmetric/NOTE.md`. Its own priority audit credits Gallagher
  for the weighted-lift family and Brink for the two-parameter symmetric
  Galois theorem.
- The \(9T31=S_3\wr S_3\) entry comes from
  `../../discovery_04_wreath_monodromy/NOTE.md`; its separate priority audit
  governs any claim about that exact iterate.

This synthesis makes no new priority claim for either realization.

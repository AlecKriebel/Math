# Conditional literal noisy consistency established

Problem 30003790 / OWR-16161-003; corrected release v2.

An independently accepted Euclidean safeguard gives expected integrated squared-error
consistency and sample-conditional integrated-risk convergence in probability in every
fixed finite dimension, for arbitrary Borel designs, bounded continuous F, and
conditionally centered noise with a common finite conditional second-moment bound.
All regression covariates are ranked, ties use sample index, and geometry assignment
uses independent training data and covariates only. The test point is independent of
all observed data jointly. See RESULT.md, Section 5A.

The exact accepted theorem/proof is preserved unchanged in AUXILIARY_THEOREM.md.
Its historical not-yet-audited notice is superseded by the fresh acceptance recorded
in ../history/auxiliary-independent-audit/AUDIT.md and ../CHANGE_LEDGER.md.

Original-model coverage is not established: the short source leaves relevant
integrability and noise-identification assumptions underspecified. Conservative
queue disposition remains unsolved, 5/5. Dimension-efficient geometric rates are
separately unproved and are not an added condition in the literal source question.
No novelty is claimed; generic nearest-neighbor consistency predates this work,
including Stone (1977).

The original packet and both audits are preserved byte-for-byte under ../history/.
The corrected author copy adds the required moment, interior/almost-everywhere,
joint-measurability and response-independent selection clarifications. Exact edits
are in ../AUTHOR_V1_TO_CORRECTED_V2.diff. This version is frozen for release-binding
review; no remote publication has occurred.

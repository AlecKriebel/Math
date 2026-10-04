# Ledrappier time-one measures: established-literature resolution

**ID 4400005, rank 653; `already_solved`, 1/5 substantive attempt turns.**

The answer is affirmative for every nonempty closed smooth Riemannian manifold
of constant strictly negative sectional curvature and dimension at least two.
The same deduction covers variable strictly negative curvature. For its
unit-speed geodesic flow on the unit tangent bundle, there exists a nonatomic,
time-one-ergodic, entropy-zero invariant probability which is not invariant
at time one-half. The metric and the specified time unit are unchanged.

This is a deduction from established literature, not a new theorem or a
first-resolution claim. Quas and Soo's published Corollary 4 directly covers
surfaces. The separate all-dimensional deduction uses fixed-gap specification
of geodesic time maps, documented by Thompson and Tian, and Burguet's
almost-Borel universality theorem, applied to the dyadic odometer without a
measure-preserving square root.

## Proof and review

- [Frozen authored deduction](packet/analysis.md)
- [Primary-source map and exact locators](packet/source_map.md)
- [Full independent adversarial audit](audit/AUDIT.md)
- [Audit source verification and retrieval limits](audit/source_verification.json)
- [Publication status and precise file manifest](PUBLICATION.json)

The independent AI audit passed at the literature-deduction level. It is not
peer review or a formal proof certificate. Original author files retain their
freeze-time references to an audit being pending; those historical statements
are preserved byte-for-byte, and the separate completed audit records the
subsequent result.

## Essential source cautions

The essential statement/application chain and relevant proof structure were
inspected. The complete original Bowen 1972 paper and Katok-Hasselblatt chapters
were not independently retrieved in full. Their specification/geometry role
was checked through Thompson, Tian, and Hasselblatt's primary exposition.
The conclusion remains explicitly dependent on established specification and
universality theorems.

The inspected full Burguet text is arXiv:1901.00666v1, not a fully retrieved
final publisher PDF. The audit records a reversed gap index, an
invertible/measurable wording slip, and a factor-three arithmetic slip whose
corrected bound remains summable. They do not obstruct the theorem application.
Hochman's 2013 erratum concerns the synchronized-subshift claims; the mixing-SFT
embedding result used in the dependency chain is unaffected. See the full
audit for the reasoning, exact locations, and limits.

Dimension one, noncompact geometry, zero curvature, and the neighboring
Thouvenot suspension question are not covered by this disposition. The direct
surface result is never used as an all-dimensional theorem.

## Reproduce

From any working directory, with Python 3.8 or later:

    python3 /path/to/4400005/verify_publication.py

This checks all listed file bytes, both original archives and their entries,
the frozen verifier, and the independent audit replay. It then checks rejection
of a same-length one-bit archive mutation and a truncated archive. No network,
source PDFs, or dataset corpus is needed. The finite controls pass 754 author
assertions and 1,533 independent assertions, with 46,233 and 409,113 permutation
enumerations respectively. These checks do not prove the infinite ergodic
theory inputs or numerically construct the measure.

The original author archive is 16,393 bytes, SHA-256
`66c2af685b3e86b88f78659db26aa60698415e7cab966bc3fa737d4794879bcf`.
The original audit archive is 20,919 bytes, SHA-256
`69a96bb68efb64178e3370cc851ed4f2267841bff7628740fcbb91220eb12887`.

Only authored mathematical commentary, original replay code, and public
verification metadata are published. No third-party source PDFs, source
transcriptions, dataset contents, or private coordination records are included.

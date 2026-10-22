# Monomial component signatures: audited partial results

Problem 20000817 (AIM-ARITHMETIC_GEOMETRY-0063), rank 760. **Unsolved, 5/5. No general resolution or novelty claim.**

The actual target is whether the entire set of monomial points distinguishes each irreducible component of an ordinary affine or projective Hilbert scheme. The catalog title describes a small-length partial result, not the full AIM question.

The [frozen author packet](author/README.md) gives the complete length-eight nonsmoothable-component signature, its higher-embedding-dimension boundary cases, the affine no-smooth-anchor obstruction, and an explicit projective separator. The [independent adversarial audit](independent_audit/AUDIT_REPORT.md) returned a scoped PASS with no mandatory corrections. It is an internal AI audit, not peer review or exhaustive literature/priority certification.

## Controlling scope and clarifications

These clarifications govern interpretation while preserving both historical freezes byte for byte, including the original proof formatting:

- The CEVV length-at-most-eight classification and the length-eight signature theorem are used only in characteristic different from 2 and 3. For dimensions 4 through 7 the nonsmoothable signature sizes are 120, 705, 2451 and 6553. The geometric converse is universal in ambient dimension; the finite enumeration is a control.
- The projective theorem assumes the actual number of Borel-fixed closed points is at most two, over an algebraically closed field. Its conclusion holds in every characteristic. Ramkumar case (ii) is excluded in characteristic two because it no longer has exactly two Borel-fixed points. The historical phrase about Staal omitting a case does not indicate an unproved gap.
- The full monomial signature is a set of all monomial closed points, not a double-generic initial ideal or a fixed subscheme with multiplicity. Equal double-generic initial ideals do not prove equal full signatures. The saturated ideal (x1*x3, x2*x3, x0^2*x1, x0^2*x2) separates the published conic-plus-line and twisted-cubic-plus-point components in the stated characteristic-zero setting.
- For Proposition 7.1, the smooth-plane-conic parameter space is an open subset of a projective bundle over the dual projective space and is irreducible. Its product with the line Grassmannian is irreducible; disjoint conic-line pairs form a nonempty open subset. Its image in the Hilbert scheme is therefore irreducible and lies in the stated conic-plus-line component. This supplies the implicit component-membership step in the frozen proof.
- The separating-anchor argument needs ambient Hilbert-scheme smoothness. Smoothness on one reduced component alone does not suffice. Every affine monomial ideal is smoothable, so all monomial points of a nonsmoothable component are ambient-singular. A genuine affine equal-signature pair would have to involve two nonsmoothable components.
- The invariant union-of-conics example is an abstract torus-scheme control, not an ordinary-Hilbert-scheme counterexample. The general signature question remains unresolved by this work. Liebling's full thesis and its suggested counterexample were not verified; there is no global open-status or novelty certificate.

The author and audit archives and their ten files each are unchanged. Historical statements that an audit is pending or that no remote writes were made describe those snapshots. This wrapper records the later scoped acceptance and publication.

## Reproduce

Run `python3 verify_publication.py` from this folder, or invoke the file by absolute path from any working directory. Python's standard library suffices. It checks a fixed file/directory allowlist, fingerprints, exact archive membership, scope, both original manifests, and author and independent replays. `python3 -O verify_publication.py` retains delivery checks; child scientific scripts run with assertions enabled. No replay modifies the frozen packet.

The independent controls enumerate lengths 0 through 8 in dimensions 1 through 7; verify 247 multiplication models, each with 512 associativity and 64 complete special-fiber checks; recompute all 120 rational tangent dimensions by border-basis commutators; and prove the separator Hilbert-series identity symbolically. Rational ranks do not certify positive-characteristic ranks. Finite checks do not replace imported classification or universal geometric arguments.

Published source/input fingerprints record acquisition-time verification only. Portable replay does not refetch source PDFs or raw datasets and does not independently repeat historical literature searches. Source-inspection limits, the unreproduced catalog review hash, and manuscript-status dates remain explicit in the preserved audit metadata.

Only this target row's Status and Turns change in QUEUE.md. Findings, Chat, DOI, every other row, and the embedded historical header remain byte-for-byte unchanged. Source PDFs, extracts, raw datasets and private coordination files are excluded. No merge or release is part of this draft.

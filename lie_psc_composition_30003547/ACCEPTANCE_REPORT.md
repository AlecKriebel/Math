# Packaging acceptance and mathematical scope

**PASS WITH EXPLICIT SCOPE LIMITS. Overall target: UNSOLVED. Five avenues completed.**

This acceptance record packages the existing independent audit; it is not a new external peer review. The frozen original reports are unedited. The mathematical acceptance basis is AUDIT_PSC_PARTIALS.md, together with COMPACT_CORE_AUDIT.md and the explicitly cited classical results.

## Claim-to-audit mapping

1. Controlled paths, local C² neighborhoods and collar gluing: independent audit Sections 3 and 6 verify the temporal curvature estimate and local argument. This does not identify concordance with isotopy or supply a binary endpoint operation.
2. Compact interior surgery: FIVE_AVENUE_REPORT.md Proposition 2.1 explicitly imports the classical local codimension-at-least-three PSC surgery theorem. The final independent-audit addendum verifies the standalone path and local-surgery arguments. The added bundle/bracket/metric gluing is confined to the ordinary interior, with unchanged Lie germ at infinity. This claim is not a general Lie surgery theorem; the independent audit Section 7 excludes that inference. No preservation of every analytic groupoid hypothesis is asserted.
3. Fixed-exterior law: independent audit Section 5 and COMPACT_CORE_AUDIT.md accept the actual Rosenberg–Stolz relative theorem for a fixed connected spin core of dimension at least five, actual fundamental-group data, and a fixed PSC collar germ. Both endpoints and concordances must keep the exterior fixed. No descent to arbitrary concordances or larger cores is claimed.
4. Cylindrical end: independent audit Sections 1–4 check the tensor norm convention, normalization path, exponent repair and section identity E j = id. The law is transported only to j(C(Y)); the end retract needs dim Y ≥ 2 and strict boundary positivity, while the imported spin law needs connected closed Y of dimension ≥ 5. The geometric realization uses the compact four-boundary closed surgery cobordism V times R, with bT(R-bar) ⊕ TV: only the spatial R factor is b-compactified, while temporal/bordism boundaries remain ordinary. Its generally noncompact product surgery loci are not an application of Avenue 2’s compact-support theorem. Surjectivity and j E = id are not established. The S⁷ existence example is imported, not an explicit metric construction.
5. Index/groupoid route: the displacement-bijection criterion is an elementary conditional transport of an abelian law. No such bijection is established in the general Lie setting. Neither index additivity nor disjoint union supplies the missing classification. The report and independent audit agree on these omissions.

The checked source-status claim is limited to an explicit open-question listing in the author's 2024 survey and no later full solution verified by the recorded search. It is not a claim that later work cannot exist.

## Computational acceptance

The original checker has four explicit RuntimeError guards, no Python assert statements. The packaging runner compares all output exactly with both saved normal and optimized references and launches each checker in both modes in a fresh temporary directory. The corruption-control program tests changed same-size content, added and missing files, changed reference JSON, and deliberately wrong symbolic identity coefficients under normal and optimized execution. These controls test fail-closed behavior, not mathematical completeness.

The reproducibility scope is symbolic consistency of the listed low-dimensional model and coefficient identities, not theorem-proving. Public PDF/dataset hashes are historical retrieval metadata, not inputs required by or reverified through the replay. Manifest hashes provide integrity against the supplied manifest, not authenticated provenance against a maliciously replaced whole package.
